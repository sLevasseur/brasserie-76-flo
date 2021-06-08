from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader

from .forms import contactForm, emailsForNewsletter
from .models import NewsletterDB, CoordinatesMapDB
from django.core.mail import send_mail
from datetime import datetime
from json import dumps, load
from django.core.paginator import Paginator
from .serializer import get_gps_coordinates_and_more
from .facebook import query_facebook_api, token_refresher
from pathlib import Path

class General_data:
    path_post_data_json = Path(__file__).parent / "./facebook/posts_data.json"
    marker_data = get_gps_coordinates_and_more(CoordinatesMapDB.objects.values_list("name_of_locations",
                                                                                    "adresse",
                                                                                    "code_postal",
                                                                                    "localite",
                                                                                    "categories",
                                                                                    "informations_supplementaires",
                                                                                    "url_coordinates"))
    with open(path_post_data_json, "r") as f:
        facebook_posts = load(f)


class Homepage(View):
    template_html = loader.get_template("bakpak_website/index.html")
    # loading forms
    contact_form = contactForm()
    newsletter_form = emailsForNewsletter()
    # loading models
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)

    def get(self, request):
        token_refresher.get_permanent_token()
        query_facebook_api.main()
        context = {"contact_form": self.contact_form,
                   "newsletter_form": self.newsletter_form,
                   "map_positions": self.data_as_JSON,
                   "facebook_post": General_data.facebook_posts["data"][0],
                   "check_picture": General_data.facebook_posts["data"][0]["all_picture_s"][0]["type_of_media"]}
        return HttpResponse(self.template_html.render(request=request, context=context))

    def post(self, request):
        contact_form_post = contactForm(request.POST)
        newsletter_form_post = emailsForNewsletter(request.POST)
        context = {"contact_form": contact_form_post,
                   "newsletter_form": newsletter_form_post,
                   "map_positions": self.data_as_JSON
                   }
        if contact_form_post.is_valid() or newsletter_form_post.is_valid():
            if "contact_form" in request.POST:  # handling data from the contact form
                sujet = contact_form_post.cleaned_data.get("sujet")
                email = contact_form_post.cleaned_data.get("email")
                text = contact_form_post.cleaned_data.get("message")
                if sujet and email and text:
                    send_mail(subject=sujet,
                              message=f"{text},"
                                      f"\n From: {email} \n"
                                      f" At: {datetime.now()}",
                              from_email=email,
                              recipient_list=["BakPak@outlook.fr"],
                              fail_silently=False)
                    context["state"] = True
                    context["message_contact"] = "Bien envoyé !"
                    return HttpResponse(self.template_html.render(request=request, context=context))

                context["message"] = "Mauvaise adresse mail ou un champs est vide"

                return HttpResponse(self.template_html.render(request=request, context=context))
            elif "newsletter_form" in request.POST:  # handling data from the newsletter subscription form
                email = newsletter_form_post.cleaned_data.get("email")
                double_email_check = NewsletterDB.objects.filter(email__icontains=email)

                if double_email_check.exists():
                    context[
                        "message_newsletter"] = "\n Nous avons reperé un doublons de mails, vous êtes déjà inscrit !\n"

                    return HttpResponse(self.template_html.render(request=request, context=context))

                context["message_newsletter"] = "\n Vous êtes bien inscrit ! \n"
                context["state"] = True
                NewsletterDB.objects.create(email=email)
                return HttpResponse(self.template_html.render(request=request, context=context))


class Blogs(View):
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)
    all_blogs = General_data.facebook_posts["data"]

    def get(self, request):
        paginator = Paginator(self.all_blogs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {"all_blog": self.all_blogs,
                   "map_positions": self.data_as_JSON,
                   "page_obj": page_obj}
        return render(request, "bakpak_website/blog.html", context=context)

class Unsubscribe(View):
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)

    def get(self, request):
        newsletter_form = emailsForNewsletter()
        context = {"newsletter_form": newsletter_form,
                   "map_positions": self.data_as_JSON}
        return render(request, "bakpak_website/unsubscribe.html", context=context)

    def post(self, request):
        newsletter_form = emailsForNewsletter(request.POST)
        context = {"newsletter_form": newsletter_form,
                   "map_positions": self.data_as_JSON}
        newsletter_for_post = emailsForNewsletter(request.POST)
        if newsletter_for_post.is_valid():
            email = newsletter_for_post.cleaned_data.get("email")
            email_to_delete = NewsletterDB.objects.filter(email__icontains=email)
            if email_to_delete.exists():
                email_to_delete.delete()
                context["state"] = True
                context["message_contact"] = "Vous ne recevrez plus de mails de notre part !"
                return render(request, "bakpak_website/unsubscribe.html", context=context)

        context["message_contact"] = "Vous n'êtes pas inscrit ou votre syntaxe ne nous " \
                                     "permet pas de trouver votre adresse mail. " \
                                     "<a href='/bakpak/#ancre_newsletter_message'> S'inscrire !</a>"
        return render(request, "bakpak_website/unsubscribe.html", context=context)


class Legal_Stuff(View):

    def get(self, request):
        return render(request, "bakpak_website/legal_stuff.html")

