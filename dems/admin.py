from django.contrib import admin

from dems.forms import BlogForm
from myauth.models import User

from .models import (
    Blog,
    Category,
    Comment,
    Contact,
    Education,
    Experience,
    ImageProject,
    Project,
    Reseaux,
    Service,
    Skill,
    Tache,
    Tag,
    Tecnologies,
    Testimonial,
)

# Register your models here.
admin.site.site_header = "Dems Portfolio"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "contact"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "level",
    ]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageProject)
class ImageProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Tecnologies)
class TechnologieAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "image_first", "category", "link"]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "description", "start_date", "end_date"]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_date", "end_date", "obtention"]
    exclude = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "date_published"]
    filter_horizontal = ("tags",)
    form = BlogForm

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        blog = form.save(commit=False)
        tags = form.cleaned_data.get("new_tags")
        blog.save()
        if tags:
            self.handle_tag(tags, blog)
        return super().save_form(request, form, change)

    def handle_tag(self, tags, blog):
        tag_names = []
        for tag in tags.split(","):
            tag = tag.strip()
            if tag:
                tag_names.append(tag)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            blog.tags.add(tag)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "experience"]


@admin.register(Reseaux)
class ResauxAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
