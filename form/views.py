import datetime
import uuid
import json
import requests
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
import reportlab
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from django.http.response import FileResponse
from django.http.response import JsonResponse
from .models import EligibleList
from .forms import EligibleListForm
from .models import Candidate
from .forms import CandidateForm
from .models import Position
from .forms import PositionForm
from .models import Referral
from .forms import ReferralForm
from .models import Department
from .forms import DepartmentForm
from .models import Job
from .forms import JobForm
from .models import Application
from .forms import ApplicationForm
from .models import EligibleListCandidate
from .forms import EligibleListCandidateForm
from .models import EligibleListCandidateReferral
from .forms import EligibleListCandidateReferralForm
from jsignature.utils import draw_signature


class HRHomePage(TemplateView):
    """
    View HR Home Page
    """
    template_name = 'hr_home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        else:
            context['user_is_in_admins'] = False
        context['eligible_lists'] = EligibleList.objects.all().order_by('-created_at')
        context['positions'] = Position.objects.all().order_by('-created_at')
        context['eligible_list_candidate_referrals'] = EligibleListCandidateReferral.objects.all().order_by('-created_at')
        return context


class Roadmap(TemplateView):
    """
    View Project Roadmap
    """
    template_name = 'roadmap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        else:
            context['user_is_in_admins'] = False
        return context


class EligibleLists(TemplateView):
    """
    Eligible List CRUD page
    """
    template_name = 'eligible_lists.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            eligible_list_form = EligibleList.objects.get(id=pk)
            form = EligibleListForm(initial=model_to_dict(eligible_list_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = EligibleListForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['eligible_lists'] = EligibleList.objects.all().order_by('-created_at')
        return context


class CreateEligibleList(TemplateView):
    template_name = 'eligible_lists.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligible_lists')
        form = EligibleListForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Eligible List: {form.errors}")
            return redirect('/eligible_lists')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Eligible List")
        return redirect('/eligible_lists')


class UpdateEligibleList(TemplateView):
    template_name = 'eligible_lists.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligible_lists')
        el_object = EligibleList.objects.get(pk=pk)
        el_object.code = request.POST['code']
        el_object.job_class = request.POST['job_class']
        el_object.specialty = request.POST['specialty']
        el_object.inspection_start = request.POST['inspection_start']
        el_object.inspection_end = request.POST['inspection_end']
        el_object.last_updated_by = request.user
        el_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Eligible List")
        return redirect('/eligible_lists')


class PostEligibleList(TemplateView):
    template_name = 'eligible_lists.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligible_lists')
        el_id = request.POST['el_id']
        el_object = EligibleList.objects.get(pk=el_id)
        el_object.posted = datetime.datetime.now()
        # TODO: Create EL PDF, then send email to EIS (or post on SFDHR website directly)
        el_object.last_updated_by = request.user
        el_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully posted Eligible List")
        return redirect(f'/eligible_lists')


class AdoptEligibleList(TemplateView):
    template_name = 'eligible_lists.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligible_lists')
        el_id = request.POST['el_id']
        el_object = EligibleList.objects.get(pk=el_id)
        el_object.adopted = datetime.datetime.now()
        # TODO: Create EL PDF, then send email to EIS (or post on SFDHR website directly)
        el_object.last_updated_by = request.user
        el_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully adopted Eligible List")
        return redirect(f'/eligible_lists')


class Candidates(TemplateView):
    """
    Candidate CRUD page
    """
    template_name = 'candidates.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            candidate_form = Candidate.objects.get(id=pk)
            form = CandidateForm(initial=model_to_dict(candidate_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = CandidateForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['candidates'] = Candidate.objects.all().order_by('-created_at')
        return context


class CreateCandidate(TemplateView):
    template_name = 'candidates.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/candidates')
        form = CandidateForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Candidate: {form.errors}")
            return redirect('/candidates')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Candidate")
        return redirect('/candidates')


class UpdateCandidate(TemplateView):
    template_name = 'candidates.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/candidates')
        candidate_object = Candidate.objects.get(pk=pk)
        candidate_object.first_name = request.POST['first_name']
        candidate_object.last_name = request.POST['last_name']
        candidate_object.email = request.POST['email']
        candidate_object.last_updated_by = request.user
        candidate_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Candidate")
        return redirect('/candidates')


class Positions(TemplateView):
    """
    Position CRUD page
    """
    template_name = 'positions.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            position_form = Position.objects.get(id=pk)
            form = PositionForm(initial=model_to_dict(position_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = PositionForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['positions'] = Position.objects.all().order_by('-created_at')
        return context


class CreatePosition(TemplateView):
    template_name = 'positions.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/positions')
        form = PositionForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Position: {form.errors}")
            return redirect('/positions')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Position")
        return redirect('/positions')


class UpdatePosition(TemplateView):
    template_name = 'positions.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/positions')
        position_object = Position.objects.get(pk=pk)
        position_object.number = request.POST['number']
        position_object.last_updated_by = request.user
        position_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Position")
        return redirect('/positions')


class Referrals(TemplateView):
    """
    Referral CRUD page
    """
    template_name = 'referrals.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            referral_form = Referral.objects.get(id=pk)
            form = ReferralForm(initial=model_to_dict(referral_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = ReferralForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['referrals'] = Referral.objects.all().order_by('-created_at')
        return context


class CreateReferral(TemplateView):
    template_name = 'referrals.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/referrals')
        form = ReferralForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Referral: {form.errors}")
            return redirect('/referrals')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Referral")
        return redirect('/referrals')


class UpdateReferral(TemplateView):
    template_name = 'referrals.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/referrals')
        referral_object = Referral.objects.get(pk=pk)
        referral_object.eligible_list = EligibleList.objects.get(pk=request.POST['eligible_list'])
        referral_object.position = Position.objects.get(pk=request.POST['position'])
        referral_object.last_updated_by = request.user
        referral_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Referral")
        return redirect('/referrals')


class Departments(TemplateView):
    """
    Department CRUD page
    """
    template_name = 'departments.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            department_form = Department.objects.get(id=pk)
            form = DepartmentForm(initial=model_to_dict(department_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = DepartmentForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['departments'] = Department.objects.all().order_by('-created_at')
        return context


class CreateDepartment(TemplateView):
    template_name = 'departments.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/departments')
        form = DepartmentForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Department: {form.errors}")
            return redirect('/departments')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Department")
        return redirect('/departments')


class UpdateDepartment(TemplateView):
    template_name = 'departments.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/departments')
        department_object = Department.objects.get(pk=pk)
        department_object.title = request.POST['title']
        department_object.code = request.POST['code']
        department_object.description = request.POST['description']
        department_object.last_updated_by = request.user
        department_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Department")
        return redirect('/departments')


class Jobs(TemplateView):
    """
    Job CRUD page
    """
    template_name = 'jobs.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            job_form = Job.objects.get(id=pk)
            form = JobForm(initial=model_to_dict(job_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = JobForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['jobs'] = Job.objects.all().order_by('-created_at')
        return context


class CreateJob(TemplateView):
    template_name = 'jobs.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/jobs')
        form = JobForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Job: {form.errors}")
            return redirect('/jobs')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Job")
        return redirect('/jobs')


class UpdateJob(TemplateView):
    template_name = 'jobs.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/jobs')
        job_object = Job.objects.get(pk=pk)
        job_object.title = request.POST['title']
        job_object.description = request.POST['description']
        job_object.department = Department.objects.get(pk=request.POST['department'])
        job_object.last_updated_by = request.user
        job_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Job")
        return redirect('/jobs')


class Applications(TemplateView):
    """
    Application CRUD page
    """
    template_name = 'applications.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            application_form = Application.objects.get(id=pk)
            form = ApplicationForm(initial=model_to_dict(application_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = ApplicationForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['applications'] = Application.objects.all().order_by('-created_at')
        return context


class CreateApplication(TemplateView):
    template_name = 'applications.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/applications')
        form = ApplicationForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save Application: {form.errors}")
            return redirect('/applications')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved Application")
        return redirect('/applications')


class UpdateApplication(TemplateView):
    template_name = 'applications.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/applications')
        application_object = Application.objects.get(pk=pk)
        application_object.candidate = Candidate.objects.get(pk=request.POST['candidate'])
        application_object.position = Position.objects.get(pk=request.POST['position'])
        application_object.job = Job.objects.get(pk=request.POST['job'])
        application_object.last_updated_by = request.user
        application_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated Application")
        return redirect('/applications')


# Relational Entities
class EligibleListCandidates(TemplateView):
    """
    EligibleListCandidate (relational table) CRUD page
    """
    template_name = 'eligiblelistcandidates.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            eligiblelistcandidate_form = EligibleListCandidate.objects.get(id=pk)
            form = EligibleListCandidateForm(initial=model_to_dict(eligiblelistcandidate_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = EligibleListCandidateForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['eligiblelistcandidates'] = EligibleListCandidate.objects.all().order_by('-created_at')
        return context


class CreateEligibleListCandidate(TemplateView):
    template_name = 'eligiblelistcandidates.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidates')
        form = EligibleListCandidateForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save EligibleListCandidate: {form.errors}")
            return redirect('/eligiblelistcandidates')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved EligibleListCandidate")
        return redirect('/eligiblelistcandidates')


class UpdateEligibleListCandidate(TemplateView):
    template_name = 'eligiblelistcandidates.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidates')
        eligiblelistcandidate_object = EligibleListCandidate.objects.get(pk=pk)
        eligiblelistcandidate_object.eligible_list = EligibleList.objects.get(pk=request.POST['eligible_list'])
        eligiblelistcandidate_object.candidate = Candidate.objects.get(pk=request.POST['candidate'])
        eligiblelistcandidate_object.score = request.POST['score']
        eligiblelistcandidate_object.rank = request.POST['rank']
        eligiblelistcandidate_object.notes = request.POST['notes']
        eligiblelistcandidate_object.last_updated_by = request.user
        eligiblelistcandidate_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated EligibleListCandidate")
        return redirect('/eligiblelistcandidates')


class ToggleActiveStatusEligibleListCandidate(TemplateView):
    template_name = 'eligiblelistcandidates.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidates')
        elcandidate_id = request.POST['elcandidate_id']
        eligiblelistcandidate_object = EligibleListCandidate.objects.get(pk=elcandidate_id)
        if eligiblelistcandidate_object.active == True:
            eligiblelistcandidate_object.active = False
        else:
            eligiblelistcandidate_object.active = True
        eligiblelistcandidate_object.last_updated_by = request.user
        eligiblelistcandidate_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully toggled Active status of Eligible List Candidate")
        return redirect(f'/eligiblelistcandidates')


class EligibleListCandidateReferrals(TemplateView):
    """
    EligibleListCandidateReferral (relational table) CRUD page
    """
    template_name = 'eligiblelistcandidatereferrals.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_in_admins'] = False
        context['form_data_present'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
        if pk:
            eligiblelistcandidatereferral_form = EligibleListCandidateReferral.objects.get(id=pk)
            form = EligibleListCandidateReferralForm(initial=model_to_dict(eligiblelistcandidatereferral_form))
            context['form_data_present'] = True
            context['pk'] = pk
        else:
            form = EligibleListCandidateReferralForm()
        context['form'] = form
        # Note that jQuery datatable has its own sort by function
        context['eligiblelistcandidatereferrals'] = EligibleListCandidateReferral.objects.all().order_by('-created_at')
        return context


class CreateEligibleListCandidateReferral(TemplateView):
    template_name = 'eligiblelistcandidatereferrals.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidatereferrals')
        form = EligibleListCandidateReferralForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, f"Could not save EligibleListCandidateReferral: {form.errors}")
            return redirect('/eligiblelistcandidatereferrals')
        form_to_save = form.save(commit=False)
        form_to_save.created_by = request.user
        form_to_save.save()
        messages.add_message(request, messages.SUCCESS, "Successfully saved EligibleListCandidateReferral")
        return redirect('/eligiblelistcandidatereferrals')


class UpdateEligibleListCandidateReferral(TemplateView):
    template_name = 'eligiblelistcandidatereferrals.html'

    def post(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidatereferrals')
        eligiblelistcandidatereferral_object = EligibleListCandidateReferral.objects.get(pk=pk)
        eligiblelistcandidatereferral_object.eligible_list_candidate = EligibleListCandidate.objects.get(pk=request.POST['eligible_list_candidate'])
        eligiblelistcandidatereferral_object.referral = Referral.objects.get(pk=request.POST['referral'])
        eligiblelistcandidatereferral_object.notes = request.POST['notes']
        eligiblelistcandidatereferral_object.last_updated_by = request.user
        eligiblelistcandidatereferral_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully updated EligibleListCandidateReferral")
        return redirect('/eligiblelistcandidatereferrals')


class ToggleActiveStatusEligibleListCandidateReferral(TemplateView):
    template_name = 'eligiblelistcandidatereferrals.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='Admins').exists():
            messages.add_message(request, messages.WARNING, f"You are not permitted to edit data")
            return redirect('/eligiblelistcandidatereferrals')
        elcandidatereferral_id = request.POST['elcandidatereferral_id']
        eligiblelistcandidatereferral_object = EligibleListCandidateReferral.objects.get(pk=elcandidatereferral_id)
        if eligiblelistcandidatereferral_object.active == True:
            eligiblelistcandidatereferral_object.active = False
        else:
            eligiblelistcandidatereferral_object.active = True
        eligiblelistcandidatereferral_object.last_updated_by = request.user
        eligiblelistcandidatereferral_object.save()
        messages.add_message(request, messages.SUCCESS, "Successfully toggled Active status of Eligible List Candidate Referral")
        return redirect(f'/eligiblelistcandidatereferrals')


def handler404(request, exception, template_name="404.html"):
    """
    Custom 404 page
    """
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="500.html"):
    """
    Custom 500 page
    """
    response = render(template_name)
    response.status_code = 500
    return response
