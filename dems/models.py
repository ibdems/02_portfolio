from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("L'adresse email doit etre fournie")
        
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Adresse Email", unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image_profile = models.ImageField(blank=True, null=True, upload_to='image/')
    image_home = models.ImageField(blank=True, null=True, upload_to="image/")
    contact = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    statut = models.BooleanField(default=True)
    adresse = models.CharField(max_length=100,null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = 'Profile'
    def __str__(self) -> str:
        return self.email


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name='Competance')
    level = models.IntegerField(verbose_name='Level', validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='La valeur doit etre comprise entre 0 et 100')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Competance'
        verbose_name_plural = 'Competances'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Categorie')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = ('Categorie')

class Project(models.Model):
    statusProject = [
        ('A venir', 'A venir'),
        ('Terminé' , 'Terminé'),
        ('En cours' , 'En cours'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    demo = models.FileField(upload_to="demo/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(blank= True, null=True)
    status = models.CharField(max_length=25, choices=statusProject, default='Terminé')

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.demo and not self.demo.name.endswith(('.mp4', '.mp3', '.mov', '.avi', '.mkv')):
            raise ValidationError('Seulement les fichiers vidéo sont autorisés.')

class Experience(models.Model):
    title = models.CharField(max_length=255, verbose_name='Titre')
    company = models.CharField(max_length=255, verbose_name='Companie')
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
    certificate = models.FileField(blank=True, null=True, upload_to='certificates/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.degree

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='tag')

    def __str__(self) -> list:
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to= 'blog/', blank=True, null=True)
    date_published = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    user_response = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True) 

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
    name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField()
    content = models.TextField(verbose_name='Témoignage')
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Poste")
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name="Entreprise")
    photo = models.ImageField(max_length=255, blank=True, null=True, verbose_name="Photo", upload_to="temoin/")
    date_published = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Témoignage de {self.name}"

class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name='Titre du Service')
    description = models.TextField(verbose_name='Description du Service')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Prix estimé')
    image = models.ImageField(upload_to='service/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


