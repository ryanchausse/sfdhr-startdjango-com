"""norm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HRHomePage.as_view(), name='hr_home_page'),
    path('index.html', views.HRHomePage.as_view(), name='index'),
    # Eligible Lists
    path('eligible_lists', views.EligibleLists.as_view(), name='eligible_lists'),
    path('eligible_lists/<int:pk>', views.EligibleLists.as_view(), name='eligible_lists'),
    path('create_eligible_list_form', views.CreateEligibleList.as_view(), name='create_eligible_list_form'),
    path('update_eligible_list_form/<int:pk>', views.UpdateEligibleList.as_view(), name='update_eligible_list_form'),
    # Candidates
    path('candidates', views.Candidates.as_view(), name='candidates'),
    path('candidates/<int:pk>', views.Candidates.as_view(), name='candidates'),
    path('create_candidate_form', views.CreateCandidate.as_view(), name='create_candidate_form'),
    path('update_candidate_form/<int:pk>', views.UpdateCandidate.as_view(), name='update_candidate_form'),
    # Positions
    path('positions', views.Positions.as_view(), name='positions'),
    path('positions/<int:pk>', views.Positions.as_view(), name='positions'),
    path('create_position_form', views.CreatePosition.as_view(), name='create_position_form'),
    path('update_position_form/<int:pk>', views.UpdatePosition.as_view(), name='update_position_form'),
    # Referrals
    path('referrals', views.Referrals.as_view(), name='referrals'),
    path('referrals/<int:pk>', views.Referrals.as_view(), name='referrals'),
    path('create_referral_form', views.CreateReferral.as_view(), name='create_referral_form'),
    path('update_referral_form/<int:pk>', views.UpdateReferral.as_view(), name='update_referral_form'),
    # ReferralCandidate (relational table)
    path('referralcandidates', views.ReferralCandidates.as_view(), name='referralcandidates'),
    path('referralcandidates/<int:pk>', views.ReferralCandidates.as_view(), name='referralcandidates'),
    path('create_referralcandidate_form', views.CreateReferralCandidate.as_view(), name='create_referralcandidate_form'),
    path('update_referralcandidate_form/<int:pk>', views.UpdateReferralCandidate.as_view(), name='update_referralcandidate_form'),
    # Department
    path('departments', views.Departments.as_view(), name='departments'),
    path('departments/<int:pk>', views.Departments.as_view(), name='departments'),
    path('create_department_form', views.CreateDepartment.as_view(), name='create_department_form'),
    path('update_department_form/<int:pk>', views.UpdateDepartment.as_view(), name='update_department_form'),
    # Job
    path('jobs', views.Jobs.as_view(), name='jobs'),
    path('jobs/<int:pk>', views.Jobs.as_view(), name='jobs'),
    path('create_job_form', views.CreateJob.as_view(), name='create_job_form'),
    path('update_job_form/<int:pk>', views.UpdateJob.as_view(), name='update_job_form'),

    # path('<int:pk>', views.HRHomePage.as_view(), name='index'),
    # path('get_pdf/<int:pk>', views.get_pdf_page, name='get_pdf_page'),
    # path('form/', views.HRHomePage.as_view(), name='form'),
    # path('submit_form', views.SubmitNormForm.as_view(), name='submit_form'),
    # path('view_psych_forms', views.ViewNormFormsPage.as_view(), name='view_psych_forms'),
    # path('email_bal/<int:pk>', views.email_bal, name='email_bal'),
    # path('api/v1/subjective_boilerplate_option', views.get_subjective_boilerplate_option_text, name='subjective_boilerplate_option'),
    # path('api/v1/subjective_option', views.get_subjective_option_text, name='subjective_option'),
    # path('api/v1/discussion_treatment_option', views.get_discussion_treatment_option_text, name='discussion_treatment_option'),
    # path('api/v1/icd_10_codes', views.get_icd_10_code_text, name='icd_10_code_text'),
    # path('api/v1/filtered_icd_10_codes', views.get_filtered_icd_10_code_text, name='filtered_icd_10_code_text'),
    # path('api/v1/previous_patient_forms', views.find_previous_patient_forms, name='previous_patient_forms'),
    # path('api/v1/add_patient', views.add_patient, name='add_patient'),
]
