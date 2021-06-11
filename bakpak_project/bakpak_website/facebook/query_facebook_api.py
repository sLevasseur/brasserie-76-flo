import facebook
import json
import datetime
import re
from pathlib import Path
# BEGIN : DECLARATION OF VARIABLES
path_facebook_json = Path(__file__).parent / "facebook.json"
path_post_data_json = Path(__file__).parent / "posts_data.json"
posts_data = dict()
posts_data.__setitem__("data", list())

with open(path_facebook_json, "r") as f:
    data = json.load(f)
    user_long_token = data["page"]["token"]
    page_id = data["page"]["id"]

with open(path_post_data_json, "r") as f:
    facebook_API_data = json.load(f)

graph = facebook.GraphAPI(access_token=user_long_token, version="3.0")
# END : DECLARATION OF VARIABLES


# BEGIN : USE OF FUNCTIONS

def main():

    length_of_json_data = len(facebook_API_data["data"])

    pages_data = graph.get_object(id=page_id, fields="posts")

    every_posts = pages_data["posts"]["data"]
    number_of_posts = len(pages_data["posts"]["data"])
    dummy_dict_for_medias = {"src": "no_media", "type_of_media": "None"}

    test_number_of_post = compare_length_internal_data_to_facebook(length_of_json_data, number_of_posts, every_posts)   
    if len(test_number_of_post) == 0:  # only run if there is a new useful post
        print("no new post")
        return 1
    else:
        print("new post")
        for id_of_one_post in test_number_of_post:
            post_attachment = graph.get_connections(id=id_of_one_post, connection_name="attachments")
            post_main_info = graph.get_object(id=id_of_one_post)

            created_time = get_created_time_from_facebook(post_main_info)
            text_post = get_text_post_from_facebook(post_main_info)
            attachment_s_video = get_all_video_s_from_facebook(post_attachment)
            if len(attachment_s_video) == 0:
                attachment_s_video.append(dummy_dict_for_medias)
            attachment_s_picture = get_all_photo_s_from_facebook(post_attachment)
            if len(attachment_s_picture) == 0:
                attachment_s_picture.append(dummy_dict_for_medias)

            link_to_post = get_link_to_post_from_facebook(post_attachment, id_of_one_post)

            make_data_as_json(make_dict_from_facebook(id_of_one_post, created_time, text_post, attachment_s_picture,
                                                      attachment_s_video, link_to_post))

        with open(path_post_data_json, "w") as d:
            json.dump(posts_data, d, indent=4)
        return 0

# END : USE OF FUNCTIONS


# BEGIN : DECLARATION OF FUNCTIONS

def compare_length_internal_data_to_facebook(length_of_internal_data, length_from_facebook, every_post_from_facebook):
    number_of_useless_post = 0
    list_of_id_post = list()
    empty_list = []
    for post in every_post_from_facebook:
        try:
            post["message"]
        except KeyError:
            number_of_useless_post += 1
        else:
            list_of_id_post.append(post["id"])
    if length_of_internal_data == length_from_facebook - number_of_useless_post:
        return empty_list  # False if no new post
    else:
        return list_of_id_post  # True if there is a difference


def formatting_date_from_facebook(date_as_string):
    format_date = "%Y-%m-%d"
    T_position = date_as_string.find("T")

    return datetime.datetime.strptime(date_as_string[0:T_position], format_date).strftime("%d-%m-%Y")


def get_created_time_from_facebook(main_info_about_post):
    return formatting_date_from_facebook(main_info_about_post["created_time"])


def get_text_post_from_facebook(main_info_about_posts):
    try:
        main_info_about_posts["message"]
    except KeyError:
        text = main_info_about_posts["story"]
    else:
        text = main_info_about_posts["message"]

    if text == "Brasserie Bakpaker a actualisé son statut." or text == "Brasserie Bakpaker a mis à jour ses horaires d’ouverture.":
        return False
    elif "http" in text:
        return get_hypertext_from_text(text)
    else:
        return text

def get_hypertext_from_text(text):
    url_to_match = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    url_to_format = text[re.search(url_to_match, text).span()[0]:re.search(url_to_match, text).span()[1]]

    return text.replace(url_to_format, f'<a href="{url_to_format}" target="blank">{url_to_format}</a>')

def get_all_video_s_from_facebook(media_of_post):
    all_video = list()
    try:
        number_of_picture = len(media_of_post["data"][0]["subattachments"]["data"])
    except KeyError:  # if only 1 attachment
        if "video" in media_of_post["data"][0]["type"]:
            info_about_video = dict()
            all_video.append(get_info_on_single_video(media_of_post, info_about_video))
    except IndexError:  # if no media
        info_about_media = dict()
        info_about_media.__setitem__("src", "no_media")
        info_about_media.__setitem__("type_of_media", "None")
        all_video.append(info_about_media)
    else:
        info_about_videos = dict()
        for i in range(0, number_of_picture):
            if "video" in media_of_post["data"][0]["subattachments"]["data"][i]["type"]:
                all_video.append(get_info_on_attachments_video(media_of_post, info_about_videos, i).copy())
    return all_video


def get_all_photo_s_from_facebook(media_of_post):
    all_pictures = list()
    try:
        number_of_picture = len(media_of_post["data"][0]["subattachments"]["data"])
    except KeyError:  # if only 1 attachment
        if media_of_post["data"][0]["type"] == "photo":
            info_about_photo = dict()
            all_pictures.append(get_info_on_single_photo(media_of_post, info_about_photo))
    except IndexError:  # if no media
        info_about_media = dict()
        info_about_media.__setitem__("src", "no_media")
        info_about_media.__setitem__("type_of_media", "None")
        all_pictures.append(info_about_media)
    else:
        info_about_photos = dict()
        for i in range(0, number_of_picture):
            if media_of_post["data"][0]["subattachments"]["data"][i]["type"] == "photo":
                all_pictures.append(get_info_on_attachments_photo(media_of_post, info_about_photos, i).copy())
    return all_pictures


def get_info_on_single_video(media_of_post, dict_to_use):
    dict_to_use.__setitem__("src", media_of_post["data"][0]["target"]["id"])
    dict_to_use.__setitem__("type_of_media", media_of_post["data"][0]["type"])
    return dict_to_use


def get_info_on_single_photo(media_of_post, dict_to_use):
    dict_to_use.__setitem__("src", media_of_post["data"][0]["media"]["image"]["src"])
    dict_to_use.__setitem__("type_of_media", media_of_post["data"][0]["type"])
    dict_to_use.__setitem__("description", " ")

    return dict_to_use


def get_info_on_attachments_photo(media_of_post, dict_to_use, i):  # bug : always the same picture
    dict_to_use["src"] = media_of_post["data"][0]["subattachments"]["data"][i]["media"]["image"]["src"]
    dict_to_use["type_of_media"] = media_of_post["data"][0]["subattachments"]["data"][i]["type"]
    try:
        media_of_post["data"][0]["subattachments"]["data"][i]["description"]
    except KeyError:
        dict_to_use.__setitem__("description", " ")
    else:
        dict_to_use.__setitem__("description", media_of_post["data"][0]["subattachments"]["data"][i]["description"])
    return dict_to_use


def get_info_on_attachments_video(media_of_post, dict_to_use, i):
    dict_to_use.__setitem__("src", media_of_post["data"][0]["subattachments"]["data"][i]["target"]["id"])
    dict_to_use.__setitem__("type_of_media", media_of_post["data"][0]["subattachments"]["data"][i]["type"])
    try:
        media_of_post["data"][0]["subattachments"]["data"][i]["description"]
    except KeyError:
        dict_to_use.__setitem__("description", " ")
    else:
        dict_to_use.__setitem__("description", media_of_post["data"][0]["subattachments"]["data"][i]["description"])
    return dict_to_use


def get_link_to_post_from_facebook(media_of_post, id_of_post):
    try:
        media_of_post["data"][0]["url"]
    except IndexError:
        url_to_get = graph.get_object(id=id_of_post, fields="permalink_url")
        url_post = url_to_get["permalink_url"]
    else:
        url_post = media_of_post["data"][0]["url"]

    return url_post


def make_dict_from_facebook(id_of_post, date_of_creation, text_of_post, all_picture_s, all_video_s, url_of_post):
    data_for_one_post = dict()
    data_for_one_post.__setitem__("id", id_of_post)
    data_for_one_post.__setitem__("creation_time", date_of_creation)
    data_for_one_post.__setitem__("text", text_of_post)
    data_for_one_post.__setitem__("all_picture_s", all_picture_s)
    data_for_one_post.__setitem__("all_video_s", all_video_s)
    data_for_one_post.__setitem__("link_to_post", url_of_post)

    return data_for_one_post


def make_data_as_json(data_needed_from_one_post):
    posts_data["data"].append(data_needed_from_one_post)

def dump_json():
    with open("bakpak_website/facebook/posts_data.json", "r") as f:
        facebook_posts = json.load(f)

    return facebook_posts
# END : DECLARATION OF FUNCTIONS
