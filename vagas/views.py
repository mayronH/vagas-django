from vagas.decorators import applicant_required, company_required
from django.contrib.auth.decorators import login_required

from calendar import month_name

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.core import paginator
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Applicant, Candidacy, Opportunity, Company, CustomUser
from .forms import CandidacyForm, CompanySingupForm, ApplicantSignUpForm, OpportunityForm

# Create your views here.
def index(request):
    """Index"""
    user = request.user

    return render(request, 'index.html', {
        "user": user,
    })

def opportunity_list(request):
    """Página de vagas"""
    op_list = Opportunity.objects.filter().order_by('created_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(op_list, 9)

    try:
        opportunities = paginator.page(page)
    except PageNotAnInteger:
        opportunities = paginator.page(1)
    except EmptyPage:
        opportunities = paginator.page(paginator.num_pages)

    return render(request, 'opportunity/op_list.html', {'opportunities' : opportunities})

def opportunity(request,pk):
    """Página de detalhes da vaga"""
    opportunity = get_object_or_404(Opportunity, pk=pk)

    return render(request, 'opportunity/op_detail.html', {'opportunity' : opportunity})

@login_required
@company_required
def my_opportunities(request):
    """Página de vagas da empresa"""
    user = request.user
    op_list = Opportunity.objects.filter(author=user).order_by('created_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(op_list, 9)

    try:
        opportunities = paginator.page(page)
    except PageNotAnInteger:
        opportunities = paginator.page(1)
    except EmptyPage:
        opportunities = paginator.page(paginator.num_pages)

    return render(request, 'opportunity/op_list_company.html', {'opportunities' : opportunities})

@login_required
@company_required
def add_opportunity(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            op = form.save(commit=False)
            op.author = request.user
            op.save()
            form.save_m2m()
            return redirect('my_opportunities')
    else:
        form = OpportunityForm()
    return render(request, 'opportunity/opportunity_form.html', {'form': form})

@login_required
@company_required
def opportunity_edit(request,pk):
    op = get_object_or_404(Opportunity, pk=pk)
    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=op)
        if form.is_valid():
            op = form.save(commit=False)
            op.author = request.user
            op.save()
            form.save_m2m()
            return redirect('my_opportunities')
    else:
        form = OpportunityForm(instance=op)
    return render(request, 'opportunity/opportunity_form.html', {'form': form})

@login_required
@company_required
def opportunity_remove(request,pk):
    op = get_object_or_404(Opportunity, pk=pk)
    op.delete()
    return redirect('my_opportunities')

def dashboard(request):
    candidacy_list = Candidacy.objects.filter().order_by('created_date')
    data_dict = {(int(data.created_date.month)): 0 for data in candidacy_list}

    for data in candidacy_list:
        data_dict[(int(data.created_date.month))] = + data_dict[(int(data.created_date.month))] + 1

    labels_candidacy = []
    data_candidacy = []
    for key, data in data_dict.items():
        labels_candidacy.append(month_name[key])
        data_candidacy.append(data)

    op_list = Opportunity.objects.all()
    data_dict = {(int(data.created_date.month)): 0 for data in op_list}

    for data in op_list:
        data_dict[(int(data.created_date.month))] = + data_dict[(int(data.created_date.month))] + 1

    labels_opportunity = []
    data_opportunity = []
    for key, data in data_dict.items():
        labels_opportunity.append(month_name[key])
        data_opportunity.append(data)
    

    return render(request, 'dashboard.html', {
        'dataTable': candidacy_list,
        'labelOpportunity': labels_opportunity,
        'labelCandidacy': labels_candidacy,
        'dataOpportunity': data_opportunity,
        'dataCandidacy': data_candidacy,
    })

@login_required
@applicant_required
def add_candidacy(request,pk):
    """Página de candidatura, é necessário estar logado como candidato"""
    op = get_object_or_404(Opportunity, pk=pk)

    if request.method == "POST" :
        form = CandidacyForm(request.POST)
        if form.is_valid():
            candidacy = form.save(commit=False)
            candidacy.opportunity = op
            candidacy.applicant = request.user
            candidacy.save()
            return redirect('opportunity', pk=op.pk)
    else:
        form = CandidacyForm()
    return render(request, 'candidacy/add_candidacy.html', {'form': form})

@login_required
@applicant_required
def my_candidacies(request):
    """Página das candidaturas do candidato"""
    user = request.user
    candidacy_list = Candidacy.objects.filter(applicant=user).order_by('created_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(candidacy_list, 9)

    try:
        candidacies = paginator.page(page)
    except PageNotAnInteger:
        candidacies = paginator.page(1)
    except EmptyPage:
        candidacies = paginator.page(paginator.num_pages)

    return render(request, 'candidacy/candidacy_list.html', {'candidacies' : candidacies})

def signup(request):
    """Página de cadastro"""
    return render(request, 'registration/home.html')


class CompanySignUpView(CreateView):
    """Página de cadastro para empresas"""
    model = CustomUser
    form_class = CompanySingupForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class ApplicantSignUpView(CreateView):
    """Página de cadastro para candidatos"""
    model = CustomUser
    form_class = ApplicantSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'applicant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('opportunity_list')