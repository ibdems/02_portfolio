from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# Create your models here.


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
    image_profile = models.ImageField(blank=True, null=True, upload_to="image/")
    image_home = models.ImageField(blank=True, null=True, upload_to="image/")
    contact = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    statut = models.BooleanField(default=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Profile"

    def __str__(self) -> str:
        return self.email
