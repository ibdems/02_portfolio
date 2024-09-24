from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib import messages
from datetime import date
from dems.forms import CommentForm, ContactForm
from dems.models import Blog, Category, Comment, Contact, Education, Experience, Project, Reseaux, Skill, Testimonial, User

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = 'index'
        context["reseaux"] = Reseaux.objects.all()
        

        return context

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = 'about'
        context['profile'] = User.objects.get(email='ibrahima882001@gmail.com')
        today = date.today()
        context['age'] = today.year - context['profile'].birthday.year - ((today.month, today.day) < (context['profile'].birthday.month, context['profile'].birthday.day))
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.all()
        context['educations'] = Education.objects.all()
        context['temoignages'] = Testimonial.objects.all()
        context['total_projects'] = Project.objects.count()
        context['total_comments'] = Comment.objects.count()
        context['total_blogs'] = Blog.objects.count()
        context['total_messages'] = Contact.objects.count()
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'project.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = 'project'
        context["categories"] = Category.objects.all()
        return context

class ProjectDetailView(DetailView):
    template_name = 'project_detail.html'
    context_object_name = 'project'
    model = Project

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = self.get_object()
            comment.save()
            messages.success(request, "Commentaire envoyer avec success")
            return redirect('detail_project', pk=self.get_object().pk)
        else:
            messages.error(request, "Echec lors de l'envoie du message")
            return redirect('detail_project', pk=self.get_object.pk)

class ResumeView(TemplateView):
    template_name ='resume.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = 'resume'
        context['profile'] = User.objects.get(email = "ibrahima882001@gmail.com")
        context['educations'] = Education.objects.all()
        context['experiences'] = Experience.objects.all()
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_page"] = 'contact'
        context["profile"] = User.objects.get(email='ibrahima882001@gmail.com')
        context['reseaux'] = Reseaux.objects.all()
        context['form'] = ContactForm()
        return context
    
    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a ete envoyer avec success")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez remplir tous les champs")

        context = self.get_context_data()
        context['form'] = form
        return render(request, 'contact.html', context)

class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'

class BlogDetailView(DetailView):
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    model = Blog

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.save()
            messages.success(request, "Votre commentaire a ete enregistre avec success")
            return redirect('blog_detail', pk=self.object.pk)
        else:
            messages.error(request, "Veuillez remplir tous les champs")
            context = self.get_context_data()
            context['form'] = form
            return render(request, 'blog_detail.html', context)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context['form'] = form
        return context
        



        
