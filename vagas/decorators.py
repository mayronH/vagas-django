from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def applicant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """Decorator para exigir candidato logado"""
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_applicant,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def company_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """Decorator para exigir empresa logada"""
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_company,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator