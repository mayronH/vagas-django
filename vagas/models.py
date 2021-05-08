from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

# Create your models here.

class CustomUserManager(BaseUserManager):
    """User Manager customizado para validar email no lugar de username"""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Criar o SuperUser com email no lugar de username"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Model para User customizado com 2 campos booleans para diferenciar Empresa de Candidato"""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    is_company = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14)

    class Meta:
        verbose_name = ("Empresa")
        verbose_name_plural = ("Empresas")

    def __str__(self):
        return self.name

class Applicant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("Candidato")
        verbose_name_plural = ("Candidatos")

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.TextField()
    created_date = models.DateField(default=timezone.now)

    minimum_schooling = models.ForeignKey('vagas.Schooling', on_delete=models.CASCADE)
    salary = models.ForeignKey('vagas.Salary', on_delete=models.CASCADE)
    author = models.ForeignKey('vagas.CustomUser', on_delete=models.CASCADE, related_name='vagas')

    class Meta:
        verbose_name = ("Vaga")
        verbose_name_plural = ("Vagas")

    def __str__(self):
        return self.name

class Salary(models.Model):
    salary = models.CharField(max_length=200)

    class Meta:
        verbose_name = ("Faixa Salarial")
        verbose_name_plural = ("Faixas Salariais")

    def __str__(self):
        return self.salary

class Schooling(models.Model):
    schooling = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("Nível de Escolaridade")
        verbose_name_plural = ("Níveis de Escolaridade")

    def __str__(self):
        return self.schooling

class Candidacy(models.Model):
    experiences = models.TextField()
    created_date = models.DateField(default=timezone.now)
    salary_expectation = models.CharField(max_length=100)

    opportunity = models.ForeignKey('vagas.Opportunity', on_delete=models.PROTECT, related_name='vagas')
    applicant = models.ForeignKey('vagas.CustomUser', on_delete=models.PROTECT, related_name='candidatos')
    schooling = models.ForeignKey('vagas.Schooling', on_delete=models.PROTECT, related_name='escolaridades')

    def __str__(self):
        return self.applicant


