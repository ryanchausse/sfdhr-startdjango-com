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
from .models import Patient
from .models import NormForm
from .forms import NormFormForm
from .forms import PatientForm
from django.contrib.auth import get_user_model
from django.contrib import messages
import reportlab
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from django.http.response import FileResponse
from django.http.response import JsonResponse
from . import flowable_form_builder
from .models import SubjectiveBoilerplateOption
from .models import SubjectiveOption
from .models import DiscussionTreatmentOption
from .models import Icd10Codes
from jsignature.utils import draw_signature


class SubmitNormForm(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Admins').exists():
            return redirect('/')
        context = self.get_context_data(**kwargs)
        # create a form instance and populate it with data from the request:
        form = NormFormForm(request.POST)

        # Create Preview if indicated
        if 'preview' in request.POST and request.POST.get('preview'):
            if form.is_valid():
                form_to_save = form.save(commit=False)
                form_to_save.created_by = request.user
                form_to_save.filename = f'preview - {form_to_save.date} - {form_to_save.patient} - ' \
                                        f'{form_to_save.facility} ' + str(uuid.uuid4()) + '.pdf'

                # Save to PDF
                print('Processing NormForm to PDF now... '
                      f'preview - {form_to_save.date} - {form_to_save.patient} - {form_to_save.facility}')
                filename = os.path.abspath(
                    os.path.dirname(__file__)) + '/patient_files/preview/' + form_to_save.filename
                signature = form.cleaned_data.get('signature')
                if signature:
                    signature_file_path = draw_signature(signature, as_file=True)
                else:
                    raise FileExistsError("No signature file found")
                flowable_form_builder.build_form(form_to_save=form_to_save, filename=filename,
                                                 signature_file_path=signature_file_path)
                return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
                                         '/patient_files/preview/' +
                                         form_to_save.filename, 'rb'), content_type='application/pdf')
        else:
            if form.is_valid():
                # Save to DB
                form_to_save = form.save(commit=False)
                form_to_save.created_by = request.user
                form_to_save.filename = f'{form_to_save.date} - {form_to_save.patient} - ' \
                                        f'{form_to_save.facility} ' + str(uuid.uuid4()) + '.pdf'
                form_to_save.save()
                messages.add_message(request, messages.SUCCESS, "Successfully saved form.")
                print('saved successfully')

                # Save to PDF
                print('Processing NormForm to PDF now... '
                      f'{form_to_save.patient} - {form_to_save.facility} - {form_to_save.date}')
                filename = os.path.abspath(os.path.dirname(__file__)) + '/patient_files/' + form_to_save.filename
                # pdf = canvas.Canvas(filename=os.path.abspath(os.path.dirname(__file__)) + '/patient_files/' + filename,
                #                     pagesize=letter)
                signature = form.cleaned_data.get('signature')
                if signature:
                    # as an image
                    # signature_picture = draw_signature(signature)
                    # or as a file
                    signature_file_path = draw_signature(signature, as_file=True)
                    # Might be a corner case here when nothing is entered into field on second
                    # entry after a long time when tmp files have been purged
                else:
                    raise FileExistsError("No signature file found")
                flowable_form_builder.build_form(form_to_save=form_to_save, filename=filename,
                                                 signature_file_path=signature_file_path)

        return redirect('/view_psych_forms')


class NormFormPage(TemplateView):
    """
    First / Login page at root
    """
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='NonBal').exists():
            return redirect('/view_psych_forms')
        return super(NormFormPage, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='NonBal').exists():
            context['user_is_in_non_bal_group'] = True
        else:
            context['user_is_in_non_bal_group'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
            if pk:
                norm_form = NormForm.objects.get(id=pk)
                form = NormFormForm(initial=model_to_dict(norm_form))
            else:
                form = NormFormForm()
            patient_form = PatientForm()
            context['form'] = form
            context['patient_form'] = patient_form
        else:
            context['user_is_in_admins'] = False
            context['form'] = None
        return context


class ViewNormFormsPage(TemplateView):
    """
    View previously submitted Norm Forms
    """
    template_name = 'view_psych_forms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='NonBal').exists():
            context['user_is_in_non_bal_group'] = True
        else:
            context['user_is_in_non_bal_group'] = False
        if self.request.user.groups.filter(name='Admins').exists():
            context['user_is_in_admins'] = True
            context['norm_forms'] = NormForm.objects.all().order_by('-created_at')
        else:
            context['user_is_in_admins'] = False
            context['norm_forms'] = None
        return context


def get_pdf_page(request, pk=None):
    """
    Get PDF of a given NormForm via pk id
    """
    if request.user.groups.filter(name='Admins').exists() and pk:
        norm_form = NormForm.objects.get(id=pk)
        if norm_form.filename:
            if request.user.email == settings.EMAIL_TO:
                if not norm_form.bal_accessed:
                    norm_form.bal_accessed = datetime.datetime.now()
                    norm_form.save()
            # return file from patient_files as pdf response
            return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
                                     '/patient_files/' +
                                     norm_form.filename, 'rb'), content_type='application/pdf')
    return redirect('/')


def get_preview_pdf_page(request, pk=None):
    """
    Create and return Sample PDF based on current form
    """
    if request.user.groups.filter(name='Admins').exists() and pk:
        norm_form = NormForm.objects.get(id=pk)
        if norm_form.filename:
            # return file from patient_files as pdf response
            return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
                                     '/patient_files/' +
                                     norm_form.filename, 'rb'), content_type='application/pdf')
    return redirect('/')


def get_subjective_boilerplate_option_text(request):
    """
    Get value of a given SubjectiveBoilerplateOption via $.AJAX in main_card
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'ids' in request.GET and request.GET.get('ids'):
        ids = request.GET.get('ids').split(',')
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        subjective_boilerplate_options = SubjectiveBoilerplateOption.objects.filter(id__in=ids)
        response_text = ''
        for subjective_boilerplate_option in subjective_boilerplate_options:
            if subjective_boilerplate_option.full_text:
                response_text += subjective_boilerplate_option.full_text + ' '
        return JsonResponse(response_text, safe=False)
    return redirect('/')


def get_subjective_option_text(request):
    """
    Get value of a given SubjectiveOption via $.AJAX in main_card
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'ids' in request.GET and request.GET.get('ids'):
        ids = request.GET.get('ids').split(',')
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        subjective_options = SubjectiveOption.objects.filter(id__in=ids)
        response_text = ''
        for subjective_option in subjective_options:
            if subjective_option.full_text:
                response_text += subjective_option.full_text + ' '
        return JsonResponse(response_text, safe=False)
    return redirect('/')


def get_discussion_treatment_option_text(request):
    """
    Get value of a given DiscussionTreatmentOption via $.AJAX() in main_card
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'ids' not in request.GET or request.GET.get('ids'):
        ids = request.GET.get('ids').split(',')
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        discussion_treatment_options = DiscussionTreatmentOption.objects.filter(id__in=ids)
        response_text = ''
        for discussion_treatment_option in discussion_treatment_options:
            if discussion_treatment_option.full_text:
                response_text += discussion_treatment_option.full_text + ' '
        return JsonResponse(response_text, safe=False)
    return redirect('/')


def get_icd_10_code_text(request):
    """
    Get value of a given ICD-10 Code via $.AJAX in main_card
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'ids' in request.GET and request.GET.get('ids'):
        ids = request.GET.get('ids').split(',')
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        icd_10_codes = Icd10Codes.objects\
                                 .filter(full_code__startswith="F")\
                                 .filter(id__in=ids)
        response_text = ''
        for icd_10_code in icd_10_codes:
            if icd_10_code.abbreviated_description:
                response_text += icd_10_code.diagnosis_code + ': ' + icd_10_code.abbreviated_description + ' '
        return JsonResponse(response_text, safe=False)
    return redirect('/')


def get_filtered_icd_10_code_text(request):
    """
    Given text, filter ICO-10 code choices (return array) via $.AJAX in main_card
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'data' in request.GET:
        filter_text = request.GET.get('data')
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        if request.GET.get('data') is not None:
            icd_10_codes = Icd10Codes.objects\
                                     .filter(full_code__startswith="F")\
                                     .filter(Q(full_description__icontains=filter_text) |
                                             Q(diagnosis_code__icontains=filter_text))\
                                     .values('id', 'diagnosis_code',
                                             'full_code', 'abbreviated_description',
                                             'full_description')\
                                     .order_by('abbreviated_description')\
                                     .order_by('diagnosis_code')
        else:
            icd_10_codes = Icd10Codes.objects\
                                     .filter(full_code__startswith="F")\
                                     .values('id', 'diagnosis_code',
                                             'full_code', 'abbreviated_description',
                                             'full_description')\
                                     .order_by('abbreviated_description')\
                                     .order_by('diagnosis_code')
        # print(icd_10_codes)
        return JsonResponse(list(icd_10_codes), safe=False)
    return redirect('/')


def find_previous_patient_forms(request):
    """
    Get list of ids and dates of forms submitted given a patient id
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    if 'patient_id' in request.GET and request.GET.get('patient_id'):
        patient = Patient.objects.get(pk=request.GET.get('patient_id'))
    else:
        return JsonResponse('', safe=False)
    if request.is_ajax():
        previous_norm_forms = NormForm.objects.filter(patient=patient)\
                                      .order_by('-date')[:5]
        response_text = ''
        for norm_form in previous_norm_forms:
            if norm_form.id and norm_form.date:
                response_text += "<a href='./" + str(norm_form.id) + "'>" + str(norm_form.date) + "</a><br />"
        return JsonResponse(response_text, safe=False)
    return redirect('/')


def email_bal(request, pk=None):
    """
    Send Email to Bal with current NormForm
    """
    if request.user.groups.filter(name='Admins').exists() and pk:
        norm_form = NormForm.objects.get(id=pk)
        if norm_form.filename:
            # Email Bal
            send_mail(
                'New Form for Norm Hendricksen',
                f'Hello Bal!\n\n'
                f'There is a new form to process on the SFDHR MB Replacement website\n\n'
                f'Please log in at https://form.hendricksenphd.com\n\n'
                f'Then, click the link below to see the PDF\n\n'
                f'https://form.hendricksenphd.com/get_pdf/{pk}\n\n'
                f'Thanks!',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_TO],
                fail_silently=False,
            )
        messages.add_message(request, messages.SUCCESS, "Successfully emailed Bal.")
        norm_form.emailed = True
        norm_form.save()
    return redirect('/view_psych_forms')


def add_patient(request):
    """
    Adds patient through form in hidden div on Norm Form root
    """
    if not request.user.groups.filter(name='Admins').exists():
        return redirect('/')
    form = PatientForm(request.POST)
    if 'first_name' in request.POST and request.POST.get('first_name'):
        form.first_name = request.POST.get('first_name')
    if 'last_name' in request.POST and request.POST.get('last_name'):
        form.last_name = request.POST.get('last_name')
    if 'dob' in request.POST and request.POST.get('dob'):
        form.dob = request.POST.get('dob')
    # Save to DB
    form_to_save = form.save(commit=False)
    form_to_save.created_by = request.user
    form_to_save.save()
    messages.add_message(request, messages.SUCCESS, "Successfully saved patient.")
    return redirect('/')


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
