import datetime
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from django.db.models import Q
from jsignature.fields import JSignatureField


# Reference tables
class ReferralStatus(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='referral_status_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='referral_status_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'ReferralStatus'
        verbose_name_plural = 'ReferralStatuses'


class CandidateReferralStatus(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='candidate_referral_status_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='candidate_referral_status_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'CandidateReferralStatus'
        verbose_name_plural = 'CandidateReferralStatuses'


# Entity tables
class Candidate(models.Model):
    sr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='candidate_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='candidate_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        unique_together = ('first_name', 'last_name', 'email')


class Position(models.Model):
    number = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='position_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='position_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'


class EligibleList(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True, default='', unique=True)
    job_class = models.CharField(max_length=255, blank=True, null=True, default='')
    specialty = models.CharField(max_length=255, blank=True, null=True, default='')
    posted = models.DateTimeField(blank=True, null=True)
    inspection_start = models.DateTimeField(blank=True, null=True)
    inspection_end = models.DateTimeField(blank=True, null=True)
    adopted = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='eligible_list_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='eligible_list_last_updated_by',
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
    status = models.ForeignKey(ReferralStatus, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='referral_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='referral_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'Pos: {self.position} - EL: {self.eligible_list}'

    class Meta:
        verbose_name = 'Referral'
        verbose_name_plural = 'Referrals'


class Department(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='department_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='department_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Job(models.Model):
    sr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.CharField(max_length=255, blank=True, null=True, default='')
    department = models.ForeignKey(Department, blank=True, null=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='job_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='job_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class Application(models.Model):
    sr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    position = models.ForeignKey(Position, blank=True, null=True, default=None, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, blank=True, null=True, default=None, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, blank=True, null=True, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='application_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='application_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.position} - {self.candidate}'

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


# Relational Entities
class EligibleListCandidate(models.Model):
    eligible_list = models.ForeignKey(EligibleList, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=28, max_digits=100, blank=True, null=True, default='')
    rank = models.IntegerField(blank=True, null=True, default='')
    notes = models.CharField(max_length=10000, blank=True, null=True, default='')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='eligible_list_candidate_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='eligible_list_candidate_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'EL: {self.eligible_list} - Candidate: {self.candidate}'

    class Meta:
        verbose_name = 'EligibleListCandidate'
        verbose_name_plural = 'EligibleListCandidate'


class EligibleListCandidateReferral(models.Model):
    eligible_list_candidate = models.ForeignKey(EligibleListCandidate, on_delete=models.CASCADE)
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
    status = models.ForeignKey(CandidateReferralStatus, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)
    notes = models.CharField(max_length=255, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='eligible_list_candidate_referral_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='eligible_list_candidate_referral_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'ELCandidate: {self.eligible_list_candidate} - Referral: {self.referral}'

    class Meta:
        verbose_name = 'EligibleListCandidateReferral'
        verbose_name_plural = 'EligibleListCandidateReferrals'
