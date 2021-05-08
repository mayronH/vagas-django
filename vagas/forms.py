from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Candidacy, Applicant, CustomUser, Company, Opportunity

class CompanySingupForm(UserCreationForm):
    name = forms.CharField(required=True, label="Nome da Empresa")
    cnpj = forms.CharField(required=True, label="CNPJ")

    field_order = ['name', 'cnpj', 'email', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email']
        exclude = ['username']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user)
        company.name = self.cleaned_data.get('name')
        company.cnpj = self.cleaned_data.get('cnpj')
        company.save()
        return user

class  ApplicantSignUpForm(UserCreationForm):
    name = forms.CharField(required=True, label="Nome")

    field_order = ['name', 'email', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email']
        exclude = ['username']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_applicant = True
        user.save()
        applicant = Applicant.objects.create(user=user)
        applicant.name = self.cleaned_data.get('name')
        applicant.save()
        return user

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ('name', 'description', 'requirements', 'minimum_schooling', 'salary')
        labels = {
            'name': "Nome da Vaga",
            'description': "Descrição",
            'requirements': "Requisitos",
            'minimum_schooling': "Escolaridade Mínima",
            'salary': 'Faixa Salarial'
        }


class CandidacyForm(forms.ModelForm):
    class Meta:
        model = Candidacy
        fields = ('experiences', 'salary_expectation', 'schooling', )
        labels = {
            'experiences': "Experiência",
            'salary_expectation': "Pretensão salarial",
            'schooling': "Escolaridade"
        }