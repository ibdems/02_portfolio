from django.urls import path

from .views import (
    AboutView,
    BlogDetailView,
    BlogListView,
    ContactView,
    IndexView,
    ProjectDetailView,
    ProjectListView,
    ResumeView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("project/", ProjectListView.as_view(), name="project"),
    path("<int:pk>/detail/", ProjectDetailView.as_view(), name="detail_project"),
    path("resume/", ResumeView.as_view(), name="resume"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("blog/", BlogListView.as_view(), name="blog"),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
]
