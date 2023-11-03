import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from django.db.models import Q
from jsignature.fields import JSignatureField


class Candidate(models.Model):
    sr_uuid = models.UUIDField(editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'


class Position(models.Model):
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'


class EligibleList(models.Model):
    code = models.IntegerField()
    job_class = models.CharField(max_length=255, blank=True, null=True, default='')
    specialty = models.CharField(max_length=255, blank=True, null=True, default='')
    posted = models.DateTimeField(blank=True, null=True)
    inspection_start = models.DateTimeField(blank=True, null=True)
    inspection_end = models.DateTimeField(blank=True, null=True)
    adopted = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'Eligible List'
        verbose_name_plural = 'Eligible Lists'


class Referral(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    eligible_list = models.ForeignKey(EligibleList, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'Pos: {self.position} - EL: {self.eligible_list}'

    class Meta:
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'


class ReferralCandidate(models.Model):
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'Referral: {self.referral} - Candidate: {self.candidate}'

    class Meta:
        verbose_name = 'ReferralCandidate'
        verbose_name_plural = 'ReferralCandidates'


class Job(models.Model):
    sr_uuid = models.UUIDField()
    title = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class Application(models.Model):
    sr_uuid = models.UUIDField(editable=False)
    position = models.ForeignKey(Position, blank=True, null=True, default=None, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, blank=True, null=True, default=None, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, blank=True, null=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.sr_uuid}'

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


# class Facility(models.Model):
#     name = models.CharField(max_length=1000, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Facility'
#         verbose_name_plural = 'Facilities'


# class Patient(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255, null=True)
#     dob = models.DateField(max_length=8, blank=True, null=True)
#     mrn = models.CharField(max_length=255, blank=True, null=True, default='')
#     ssn = models.CharField(max_length=255, blank=True, null=True, default='')
#     facility = models.ForeignKey(Facility, blank=True, null=True, default=None, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         if self.ssn and self.dob:
#             return f'{self.last_name}, {self.first_name} - {self.ssn} - {self.dob}'
#         elif self.ssn:
#             return f'{self.last_name}, {self.first_name} - {self.ssn}'
#         elif self.dob:
#             return f'{self.last_name}, {self.first_name} - {self.dob}'
#         else:
#             return f'{self.last_name}, {self.first_name}'

#     class Meta:
#         verbose_name = 'Patient'
#         verbose_name_plural = 'Patients'


# class SubjectiveBoilerplateOption(models.Model):
#     name = models.CharField(max_length=1000, null=True)
#     full_text = models.CharField(max_length=1000, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Subjective Boilerplate Option'
#         verbose_name_plural = 'Subjective Boilerplate Options'


# class SubjectiveOption(models.Model):
#     name = models.CharField(max_length=1000, null=True)
#     full_text = models.CharField(max_length=1000, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Subjective Option'
#         verbose_name_plural = 'Subjective Options'


# class DiscussionTreatmentOption(models.Model):
#     name = models.CharField(max_length=1000, null=True)
#     full_text = models.CharField(max_length=1000, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.name}'

#     class Meta:
#         verbose_name = 'Discussion and Treatment Option'
#         verbose_name_plural = 'Discussion and Treatment Options'


# class Icd10Codes(models.Model):
#     category_code = models.CharField(max_length=1000, null=True)
#     diagnosis_code = models.CharField(max_length=1000, null=True)
#     full_code = models.CharField(max_length=1000, null=True)
#     abbreviated_description = models.CharField(max_length=1000, null=True)
#     full_description = models.CharField(max_length=10000, null=True)
#     category_title = models.CharField(max_length=1000, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    blank=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.diagnosis_code} - {self.abbreviated_description}'

#     class Meta:
#         verbose_name = 'ICD-10 Code'
#         verbose_name_plural = 'ICD-10 Codes'


# class NormForm(models.Model):
#     patient = models.ForeignKey(Patient, default=None, on_delete=models.CASCADE, blank=True, null=True)
#     facility = models.ForeignKey(Facility, default=None, on_delete=models.CASCADE, blank=True, null=True)
#     physician = models.CharField(max_length=255, null=True, blank=True)
#     date = models.DateField(blank=True, default=datetime.date.today)

#     # Subjective
#     subjective_options = models.ManyToManyField(SubjectiveOption, blank=True)
#     chief_complaints_problems_history = models.CharField(max_length=50000, blank=True, null=True, default='')

#     # Objective - staff / other sources reported
#     agg_behavior_physical = models.BooleanField(default=False)
#     agg_behavior_verbal = models.BooleanField(default=False)
#     agg_behavior_gestures = models.BooleanField(default=False)
#     agg_behavior_threatening = models.BooleanField(default=False)
#     agg_behavior_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     gen_appearance_well_groomed = models.BooleanField(default=False)
#     gen_appearance_fairly_groomed = models.BooleanField(default=False)
#     gen_appearance_poorly_groomed = models.BooleanField(default=False)
#     gen_appearance_disheveled = models.BooleanField(default=False)
#     gen_appearance_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     treat_and_compliance_acceptable = models.BooleanField(default=False)
#     treat_and_compliance_low_motivation = models.BooleanField(default=False)
#     treat_and_compliance_resistive = models.BooleanField(default=False)
#     treat_and_compliance_argumentative = models.BooleanField(default=False)
#     treat_and_compliance_exit_seeking = models.BooleanField(default=False)
#     treat_and_compliance_wandering = models.BooleanField(default=False)
#     treat_and_compliance_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     inappropriate_behavior = models.BooleanField(default=False)
#     inappropriate_behavior_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     attitude_cooperative = models.BooleanField(default=False)
#     attitude_uncooperative = models.BooleanField(default=False)
#     attitude_marginally_cooperative = models.BooleanField(default=False)
#     attitude_other = models.BooleanField(default=False)
#     attitude_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     speech_intact = models.BooleanField(default=False)
#     speech_pressured = models.BooleanField(default=False)
#     speech_hyperverbal = models.BooleanField(default=False)
#     speech_loud = models.BooleanField(default=False)
#     speech_slow = models.BooleanField(default=False)
#     speech_unintelligible = models.BooleanField(default=False)
#     speech_yelling_out = models.BooleanField(default=False)
#     speech_perseverative = models.BooleanField(default=False)
#     speech_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     verbal_abilities_receptive_language_sufficient = models.BooleanField(default=False)
#     verbal_abilities_receptive_language_impaired = models.BooleanField(default=False)
#     verbal_abilities_expressive_language_sufficient = models.BooleanField(default=False)
#     verbal_abilities_expressive_language_impaired = models.BooleanField(default=False)
#     verbal_abilities_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     communication_verbal = models.BooleanField(default=False)
#     communication_non_verbal = models.BooleanField(default=False)
#     communication_minimally_verbal = models.BooleanField(default=False)
#     communication_withdrawn = models.BooleanField(default=False)
#     communication_avoidant = models.BooleanField(default=False)
#     communication_evasive = models.BooleanField(default=False)
#     communication_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     perceptual_disturbances_none = models.BooleanField(default=False)
#     perceptual_disturbances_hallucinations = models.BooleanField(default=False)
#     perceptual_disturbances_visual = models.BooleanField(default=False)
#     perceptual_disturbances_auditory = models.BooleanField(default=False)
#     perceptual_disturbances_command = models.BooleanField(default=False)
#     perceptual_disturbances_tactile = models.BooleanField(default=False)
#     perceptual_disturbances_olfactory = models.BooleanField(default=False)
#     perceptual_disturbances_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     level_of_consciousness_alert = models.BooleanField(default=False)
#     level_of_consciousness_confused = models.BooleanField(default=False)
#     level_of_consciousness_drowsy = models.BooleanField(default=False)
#     level_of_consciousness_somnolent = models.BooleanField(default=False)
#     level_of_consciousness_fluctuating = models.BooleanField(default=False)
#     level_of_consciousness_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     thought_process_linear = models.BooleanField(default=False)
#     thought_process_disorganized = models.BooleanField(default=False)
#     thought_process_fragmented = models.BooleanField(default=False)
#     thought_process_racing = models.BooleanField(default=False)
#     thought_process_circumstantial = models.BooleanField(default=False)
#     thought_process_tangential = models.BooleanField(default=False)
#     thought_process_blocking = models.BooleanField(default=False)
#     thought_process_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     thought_content_normal = models.BooleanField(default=False)
#     thought_content_delusions = models.BooleanField(default=False)
#     thought_content_persecutory = models.BooleanField(default=False)
#     thought_content_grandiose = models.BooleanField(default=False)
#     thought_content_religious = models.BooleanField(default=False)
#     thought_content_self_referential = models.BooleanField(default=False)
#     thought_content_poverty_of_content = models.BooleanField(default=False)
#     thought_content_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     mood_euthymic = models.BooleanField(default=False)
#     mood_depressed = models.BooleanField(default=False)
#     mood_anxious = models.BooleanField(default=False)
#     mood_irritable = models.BooleanField(default=False)
#     mood_angry = models.BooleanField(default=False)
#     mood_tearful = models.BooleanField(default=False)
#     mood_elated = models.BooleanField(default=False)
#     mood_labile = models.BooleanField(default=False)
#     mood_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     affect_appropriate = models.BooleanField(default=False)
#     affect_flat = models.BooleanField(default=False)
#     affect_blunted = models.BooleanField(default=False)
#     affect_expansive = models.BooleanField(default=False)
#     affect_agitated = models.BooleanField(default=False)
#     affect_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     harmfulness_self = models.BooleanField(default=False)
#     harmfulness_others = models.BooleanField(default=False)
#     harmfulness_negative_statements = models.BooleanField(default=False)
#     harmfulness_other = models.BooleanField(default=False)
#     harmfulness_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     attention_concentration_good = models.BooleanField(default=False)
#     attention_concentration_fair = models.BooleanField(default=False)
#     attention_concentration_poor = models.BooleanField(default=False)
#     attention_concentration_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     orientation_time = models.BooleanField(default=False)
#     orientation_place = models.BooleanField(default=False)
#     orientation_person = models.BooleanField(default=False)
#     orientation_situation = models.BooleanField(default=False)
#     orientation_disoriented = models.BooleanField(default=False)
#     orientation_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     insight_judgement_good = models.BooleanField(default=False)
#     insight_judgement_fair = models.BooleanField(default=False)
#     insight_judgement_poor = models.BooleanField(default=False)
#     insight_judgement_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     sleep_disturbance = models.BooleanField(default=False)
#     sleep_disturbance_apnea = models.BooleanField(default=False)
#     sleep_disturbance_narcolepsy = models.BooleanField(default=False)
#     sleep_disturbance_nightmares = models.BooleanField(default=False)
#     sleep_disturbance_hypnagogic_hypnopompic_hallucinations = models.BooleanField(default=False)
#     sleep_disturbance_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     appetite_change_no = models.BooleanField(default=False)
#     appetite_change_yes = models.BooleanField(default=False)
#     appetite_change_notes = models.CharField(max_length=50000, blank=True, null=True, default='')

#     # Misc
#     tobacco_screen = models.BooleanField(default=False)
#     tele_health = models.BooleanField(default=False)
#     mental_capacity = models.BooleanField(default=False)
#     placement_issues = models.BooleanField(default=False)
#     other = models.BooleanField(default=False)

#     # Assessment
#     diagnostic_impression = models.CharField(max_length=50000, blank=True, null=True, default='')

#     # Plan
#     current_medication = models.CharField(max_length=50000, blank=True, null=True, default='')
#     discussion_treatment_options = models.ManyToManyField(DiscussionTreatmentOption, blank=True)
#     discussion_treatment = models.CharField(max_length=50000, blank=True, null=True, default='')

#     signature = JSignatureField()
#     preview = models.BooleanField(default=False)

#     filename = models.CharField(max_length=1000, blank=True, null=True, default='')
#     emailed = models.BooleanField(default=False)
#     bal_accessed = models.DateTimeField(blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(get_user_model(),
#                                    null=True,
#                                    on_delete=models.SET_NULL)

#     def __str__(self):
#         return f'{self.date} - {self.patient} - {self.facility}'

#     class Meta:
#         verbose_name = 'Norm Form'
#         verbose_name_plural = 'Norm Forms'
