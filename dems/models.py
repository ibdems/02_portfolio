from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from myauth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Competance")
    level = models.IntegerField(
        verbose_name="Level",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="La valeur doit etre comprise entre 0 et 100",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Competance"
        verbose_name_plural = "Competances"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Categorie")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Categorie"


class Project(models.Model):
    statusProject = [
        ("A venir", "A venir"),
        ("Terminé", "Terminé"),
        ("En cours", "En cours"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image_first = models.ImageField(upload_to="image/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=statusProject, default="Terminé")

    def __str__(self) -> str:
        return self.title


class ImageProject(models.Model):
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="image_project"
    )


class Tecnologies(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="technologies"
    )


class Experience(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre")
    company = models.CharField(max_length=255, verbose_name="Companie")
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Tache(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Education(models.Model):
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    obtention = models.CharField(max_length=200)
    option = models.CharField(max_length=200, null=True, blank=True)
    certificate = models.FileField(blank=True, null=True, upload_to="certificates/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.degree


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="tag")

    def __str__(self) -> list:
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    date_published = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment"
    )
    content = models.TextField()
    user_response = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project, blank=True, null=True, on_delete=models.CASCADE, related_name="comment_project"
    )

    def __str__(self) -> str:
        return self.content


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject


class Reseaux(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self) -> str:
        return self.name


class Testimonial(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_testimonial"
    )
    content = models.TextField(verbose_name="Témoignage")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Poste")
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name="Entreprise")
    photo = models.ImageField(
        max_length=255, blank=True, null=True, verbose_name="Photo", upload_to="temoin/"
    )
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Témoignage de {self.user}"


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre du Service")
    description = models.TextField(verbose_name="Description du Service")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix estimé"
    )
    image = models.ImageField(upload_to="service/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
