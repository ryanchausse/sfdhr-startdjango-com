from django import forms
from django.forms import SelectDateWidget
from django.forms import DateInput
from django.forms import DateTimeInput
import datetime
from .models import EligibleList
from .models import Candidate
from .models import Position
from .models import Referral
from .models import Department
from .models import Job
from .models import Application
from .models import EligibleListCandidate
from .models import EligibleListCandidateReferral
from .models import ReferralStatus
from .models import CandidateReferralStatus
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget


class EligibleListForm(forms.ModelForm):
    id = forms.HiddenInput()
    code = forms.TextInput(attrs={'required': True})
    job_class = forms.TextInput(attrs={'required': True})
    specialty = forms.TextInput()
    # posted = forms.DateField(required=False,
    #                          widget=DateInput(attrs={'type': 'date'}))
    inspection_start = forms.DateField(required=False,
                                       widget=DateInput(attrs={'type': 'date'}))
    inspection_end = forms.DateField(required=False,
                                     widget=DateInput(attrs={'type': 'date'}))
    # adopted = forms.DateField(required=False,
    #                           widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EligibleList
        fields = ['id', 'code', 'job_class', 'specialty', 'posted', 'inspection_start', 'inspection_end', 'adopted']


class CandidateForm(forms.ModelForm):
    id = forms.HiddenInput()
    first_name = forms.TextInput(attrs={'required': True})
    last_name = forms.TextInput(attrs={'required': True})
    email = forms.TextInput(attrs={'required': True})

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'email']


class PositionForm(forms.ModelForm):
    id = forms.HiddenInput()
    number = forms.TextInput(attrs={'required': True})

    class Meta:
        model = Position
        fields = ['id', 'number']


class ReferralForm(forms.ModelForm):
    id = forms.HiddenInput()
    eligible_list = forms.ModelChoiceField(queryset=EligibleList.objects.all())
    position = forms.ModelChoiceField(queryset=Position.objects.all())
    status = forms.ModelChoiceField(queryset=ReferralStatus.objects.all())

    class Meta:
        model = Referral
        fields = ['id', 'eligible_list', 'position', 'status']


class DepartmentForm(forms.ModelForm):
    id = forms.HiddenInput()
    title = forms.TextInput(attrs={'required': True})
    code = forms.TextInput(attrs={'required': True})
    description = forms.TextInput()

    class Meta:
        model = Department
        fields = ['id', 'title', 'code', 'description']


class JobForm(forms.ModelForm):
    id = forms.HiddenInput()
    title = forms.TextInput()
    description = forms.TextInput()
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'department']


class ApplicationForm(forms.ModelForm):
    id = forms.HiddenInput()
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all())
    position = forms.ModelChoiceField(queryset=Position.objects.all())
    job = forms.ModelChoiceField(queryset=Job.objects.all())

    class Meta:
        model = Application
        fields = ['id', 'candidate', 'position', 'job']


# Relational Entities
class EligibleListCandidateForm(forms.ModelForm):
    id = forms.HiddenInput()
    eligible_list = forms.ModelChoiceField(queryset=EligibleList.objects.all())
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all())
    score = forms.DecimalField()
    rank = forms.IntegerField()
    notes = forms.TextInput()

    class Meta:
        model = EligibleListCandidate
        fields = ['id', 'eligible_list', 'candidate', 'score', 'rank', 'notes']


class EligibleListCandidateReferralForm(forms.ModelForm):
    id = forms.HiddenInput()
    eligible_list_candidate = forms.ModelChoiceField(queryset=EligibleListCandidate.objects.all())
    referral = forms.ModelChoiceField(queryset=Referral.objects.all())
    status = forms.ModelChoiceField(queryset=CandidateReferralStatus.objects.all(), required=False)
    active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
    notes = forms.TextInput()

    class Meta:
        model = EligibleListCandidateReferral
        fields = ['id', 'eligible_list_candidate', 'referral', 'status', 'active', 'notes']


# Reference tables
class ReferralStatusForm(forms.ModelForm):
    id = forms.HiddenInput()
    status = forms.TextInput()
    description = forms.TextInput()

    class Meta:
        model = ReferralStatus
        fields = ['id', 'status', 'description']


class CandidateReferralStatusForm(forms.ModelForm):
    id = forms.HiddenInput()
    status = forms.TextInput()
    description = forms.TextInput()

    class Meta:
        model = CandidateReferralStatus
        fields = ['id', 'status', 'description']

