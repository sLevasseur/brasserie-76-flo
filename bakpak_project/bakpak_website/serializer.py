
def get_gps_coordinates_and_more(coordinates):
    coordinates_info = list()
    for location in coordinates:
        one_location = dict()
        one_location.__setitem__("name_of_location", location[0])

        one_location.__setitem__("adresse", location[1])
        one_location.__setitem__("code_postal", location[2])
        one_location.__setitem__("localite", location[3])
        one_location.__setitem__("categorie", location[4])

        one_location.__setitem__("informations_supplementaires", location[5])

        str_location = "".join(location[6])
        url_for_lat = str_location[str_location.index("!3d") + 3:] + "!"
        url_for_long = str_location[str_location.index("!4d") + 3:] + "!"
        lat = url_for_lat[:url_for_lat.index("!4d")]
        long = url_for_long[:url_for_long.index("!")]
        one_location.__setitem__("lat", lat)
        one_location.__setitem__("long", long)

        coordinates_info.append(one_location)

    return coordinates_info
