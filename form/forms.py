from django import forms
from django.forms import SelectDateWidget
# from .models import NormForm
import datetime
from .models import EligibleList
from .models import Candidate
# from .models import Patient
# from .models import Facility
# from .models import SubjectiveBoilerplateOption
# from .models import SubjectiveOption
# from .models import DiscussionTreatmentOption
# from .models import Icd10Codes
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget


class EligibleListForm(forms.ModelForm):
    id = forms.HiddenInput()
    code = forms.TextInput(attrs={'required': True})
    job_class = forms.TextInput(attrs={'required': True})
    specialty = forms.TextInput()
    posted = forms.DateField(required=False,
                             initial=datetime.date.today(),
                             widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    inspection_start = forms.DateField(required=False,
                                       initial=datetime.date.today(),
                                       widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    inspection_end = forms.DateField(required=False,
                                     initial=datetime.date.today(),
                                     widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    adopted = forms.DateField(required=False,
                              initial=datetime.date.today(),
                              widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

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


# class NormFormForm(forms.ModelForm):
#     patient = forms.ModelChoiceField(queryset=Patient.objects.all())
#     facility = forms.ModelChoiceField(queryset=Facility.objects.all())
#     physician = forms.CharField(required=False)
#     date = forms.DateField(initial=datetime.date.today(),
#                            widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

#     # Subjective
#     subjective_boilerplate_options = forms.ModelMultipleChoiceField(queryset=SubjectiveBoilerplateOption.objects.all(), required=False)
#     subjective_options = forms.ModelMultipleChoiceField(queryset=SubjectiveOption.objects.all(), required=False)
#     chief_complaints_problems_history = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 7}))

#     # Objective - staff / other sources reported
#     agg_behavior_physical = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     agg_behavior_verbal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     agg_behavior_gestures = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     agg_behavior_threatening = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     agg_behavior_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     gen_appearance_well_groomed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     gen_appearance_fairly_groomed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     gen_appearance_poorly_groomed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     gen_appearance_disheveled = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     gen_appearance_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     treat_and_compliance_acceptable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_low_motivation = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_resistive = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_argumentative = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_exit_seeking = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_wandering = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     treat_and_compliance_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     inappropriate_behavior = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     inappropriate_behavior_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     attitude_cooperative = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attitude_uncooperative = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attitude_marginally_cooperative = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attitude_other = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attitude_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     speech_intact = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_pressured = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_hyperverbal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_loud = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_slow = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_unintelligible = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_yelling_out = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_perseverative = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     speech_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     verbal_abilities_receptive_language_sufficient = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     verbal_abilities_receptive_language_impaired = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     verbal_abilities_expressive_language_sufficient = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     verbal_abilities_expressive_language_impaired = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     verbal_abilities_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     communication_verbal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_non_verbal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_minimally_verbal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_withdrawn = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_avoidant = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_evasive = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     communication_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     perceptual_disturbances_none = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_hallucinations = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_visual = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_auditory = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_command = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_tactile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_olfactory = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     perceptual_disturbances_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     level_of_consciousness_alert = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     level_of_consciousness_confused = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     level_of_consciousness_drowsy = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     level_of_consciousness_somnolent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     level_of_consciousness_fluctuating = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     level_of_consciousness_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     thought_process_linear = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_disorganized = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_fragmented = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_racing = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_circumstantial = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_tangential = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_blocking = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_process_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     thought_content_normal = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_delusions = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_persecutory = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_grandiose = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_religious = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_self_referential = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_poverty_of_content = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     thought_content_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     mood_euthymic = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_depressed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_anxious = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_irritable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_angry = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_tearful = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_elated = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_labile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mood_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     affect_appropriate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     affect_flat = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     affect_blunted = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     affect_expansive = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     affect_agitated = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     affect_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     harmfulness_self = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     harmfulness_others = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     harmfulness_negative_statements = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     harmfulness_other = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     harmfulness_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     attention_concentration_good = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attention_concentration_fair = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attention_concentration_poor = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     attention_concentration_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     orientation_time = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     orientation_place = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     orientation_person = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     orientation_situation = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     orientation_disoriented = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     orientation_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     insight_judgement_good = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     insight_judgement_fair = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     insight_judgement_poor = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     insight_judgement_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     sleep_disturbance = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     sleep_disturbance_apnea = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     sleep_disturbance_narcolepsy = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     sleep_disturbance_nightmares = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     sleep_disturbance_hypnagogic_hypnopompic_hallucinations = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     sleep_disturbance_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     appetite_change_no = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     appetite_change_yes = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     appetite_change_notes = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

#     # Misc
#     tobacco_screen = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     tele_health = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     mental_capacity = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     placement_issues = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     other = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))

#     # Assessment
#     icd_10_codes = forms.ModelMultipleChoiceField(queryset=Icd10Codes.objects
#                                                   .filter(full_code__startswith="F")
#                                                   .order_by('abbreviated_description')
#                                                   .order_by('diagnosis_code'),
#                                                   required=False)
#     discussion_treatment_options = forms.ModelMultipleChoiceField(queryset=DiscussionTreatmentOption.objects.all(),
#                                                                   required=False)
#     diagnostic_impression = forms.CharField(required=False, max_length=50000,
#                                             widget=forms.Textarea(attrs={'cols': 30, 'rows': 7}))

#     # Plan
#     current_medication = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 7}))
#     discussion_treatment = forms.CharField(required=False, max_length=50000, widget=forms.Textarea(attrs={'cols': 30, 'rows': 7}))

#     signature = JSignatureField(widget=JSignatureWidget(jsignature_attrs={'color': '#0c00a0'}))
#     preview = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     emailed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': "width: 20px; height: 20px"}))
#     bal_accessed = forms.DateTimeField(required=False)

#     class Meta:
#         model = NormForm
#         exclude = ['created_by', 'filename']


# class PatientForm(forms.ModelForm):
#     first_name = forms.TextInput()
#     last_name = forms.TextInput()
#     dob = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

#     class Meta:
#         model = Patient
#         fields = ['first_name', 'last_name', 'dob']
