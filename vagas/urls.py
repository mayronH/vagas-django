from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name="dashboard"),

    path('vagas/', views.opportunity_list, name="opportunity_list"),
    path('vagas/minhas-vagas/', views.my_opportunities, name="my_opportunities"),
    path('vaga/criar-vaga/', views.add_opportunity, name="add_opportunity"),
    path('vaga/<int:pk>/', views.opportunity, name="opportunity"),
    path('vaga/<int:pk>/editar-vaga', views.opportunity_edit, name="opportunity_edit"),
    path('vaga/<int:pk>/remover', views.opportunity_remove, name="opportunity_remove"),

    path('vaga/<int:pk>/candidatar',views.add_candidacy, name="add_candidacy"),
    path('vaga/minhas-candidaturas/', views.my_candidacies, name="my_candidacies"),
    
    path('conta/cadastro/', views.signup, name='signup'),
    path('conta/cadastro/empresa', views.CompanySignUpView.as_view(), name="company_signup"),
    path('conta/cadastro/candidato', views.ApplicantSignUpView.as_view(), name="applicant_signup"),
]