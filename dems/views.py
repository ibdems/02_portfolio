from datetime import date
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, TemplateView

from dems.forms import CommentForm, ContactForm, TemoignageForm
from dems.models import (
    Blog,
    Category,
    Comment,
    Contact,
    Education,
    Experience,
    Project,
    Reseaux,
    Skill,
    Testimonial,
)
from myauth.models import User


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "index"
        context["reseaux"] = Reseaux.objects.all()
        return context


class AboutView(ListView):
    model = Skill
    template_name = "about.html"
    context_object_name = "skills"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = "about"
        context["profile"] = User.objects.get(email="ibrahima882001@gmail.com")
        today = date.today()
        context["age"] = (
            today.year
            - context["profile"].birthday.year
            - (
                (today.month, today.day)
                < (context["profile"].birthday.month, context["profile"].birthday.day)
            )
        )
        context["experiences"] = Experience.objects.all()
        context["educations"] = Education.objects.all()
        context["temoignages"] = Testimonial.objects.all()
        context["total_projects"] = Project.objects.count()
        context["total_comments"] = Comment.objects.count()
        context["total_blogs"] = Blog.objects.count()
        context["total_messages"] = Contact.objects.count()
        return context

    def post(self, request, *args, **kwargs):
        form = TemoignageForm(request.POST)
        if form.is_valid():
            temoignage = form.save(commit=False)
            temoignage.user = request.user
            temoignage.save()
            messages.success(request, "Temoignage ajouter avec success")
            return redirect("about")
        else:
            messages.error(request, "Echec lors de l'envoie du message")
            return redirect("about")


class ProjectListView(ListView):
    model = Project
    template_name = "project.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = "project"
        context["categories"] = Category.objects.all()
        return context


class ProjectDetailView(DetailView):
    template_name = "project_detail.html"
    context_object_name = "project"
    model = Project

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("image_project", "technologies")
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        form = CommentForm()
        context["form"] = form
        context["comments"] = project.comment_project.all().select_related("user")
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = self.get_object()
            comment.user = request.user
            comment.save()
            messages.success(request, "Commentaire envoyer avec success")
            return redirect("detail_project", pk=self.get_object().pk)
        else:
            messages.error(request, "Echec lors de l'envoie du message")
            return redirect("detail_project", pk=self.get_object.pk)


class ResumeView(TemplateView):
    template_name = "resume.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = "resume"
        context["profile"] = User.objects.get(email="ibrahima882001@gmail.com")
        context["educations"] = Education.objects.all()
        context["experiences"] = Experience.objects.all()
        context["competances"] = Skill.objects.all()
        return context


class ContactView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = "contact"
        context["profile"] = User.objects.get(email="ibrahima882001@gmail.com")
        context["reseaux"] = Reseaux.objects.all()
        context["form"] = ContactForm()
        return context

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            subject = f"Depuis le portfolio: {form.cleaned_data['subject']}"  # Sujet de l'email
            message = (
                f"Nom: {form.cleaned_data['name']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Message:\n{form.cleaned_data['message']}"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ["ibrahima882001@gmail.com"]

            # Envoyer l'email
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Votre message a ete envoyer avec success")
            return redirect("contact")
        else:
            messages.error(request, "Veuillez remplir tous les champs")

        context = self.get_context_data()
        context["form"] = form
        return render(request, "contact.html", context)


class BlogListView(ListView):
    model = Blog
    template_name = "blog.html"
    context_object_name = "blogs"


class BlogDetailView(DetailView):
    template_name = "blog_detail.html"
    context_object_name = "blog"
    model = Blog

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.save()
            messages.success(request, "Votre commentaire a ete enregistre avec success")
            return redirect("blog_detail", pk=self.object.pk)
        else:
            messages.error(request, "Veuillez remplir tous les champs")
            context = self.get_context_data()
            context["form"] = form
            return render(request, "blog_detail.html", context)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context["form"] = form
        return context


def custom_404_view(request):
    return render(request, "404.html")


def custom_500_view(request):
    return render(request, "500.html")
