import datetime
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from django.db.models import Q
from jsignature.fields import JSignatureField
from django.core.exceptions import ValidationError as ExceptionValidationError

# Mixins
class SingleInstanceMixin(object):
    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ExceptionValidationError(f'Can only create 1 {model.__name__} instance')
        super(SingleInstanceMixin, self).clean()


# Reference tables
class ScoringModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='scoring_model_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='scoring_model_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'ScoringModel'
        verbose_name_plural = 'ScoringModels'


class ScoreBandingModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='score_banding_model_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='score_banding_model_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'ScoreBandingModel'
        verbose_name_plural = 'ScoreBandingModels'


class ScoreBand(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    rank = models.IntegerField()
    upper_score_limit = models.FloatField()
    lower_score_limit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='score_band_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='score_band_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title} - {self.rank} - {self.upper_score_limit} - {self.lower_score_limit}'

    class Meta:
        verbose_name = 'ScoreBand'
        verbose_name_plural = 'ScoreBand'


class EligibleListRule(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    number_of_reachable_ranks = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='eligible_list_rule_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='eligible_list_rule_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'EligibleListRule'
        verbose_name_plural = 'EligibleListRules'


class JobClass(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='job_class_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='job_class_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.code} - {self.title}'

    class Meta:
        verbose_name = 'JobClass'
        verbose_name_plural = 'JobClasses'


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


class LongRunningTaskType(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='long_running_task_type_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='long_running_task_type_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'LongRunningTaskType'
        verbose_name_plural = 'LongRunningTaskTypes'


class LongRunningTaskStatus(models.Model):
    status = models.CharField(max_length=255)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='long_running_task_status_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='long_running_task_status_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'LongRunningTaskStatus'
        verbose_name_plural = 'LongRunningTaskStatuses'


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
    code = models.CharField(max_length=255, unique=True)
    job_class = models.ForeignKey(JobClass, blank=True, null=True, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255, blank=True, null=True, default='')
    eligible_list_rule = models.ForeignKey(EligibleListRule, blank=True, null=True, on_delete=models.CASCADE)
    scoring_model = models.ForeignKey(ScoringModel, blank=True, null=True, on_delete=models.CASCADE)
    score_banding_model = models.ForeignKey(ScoreBandingModel, blank=True, null=True, default=None, on_delete=models.CASCADE)
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
    status = models.ForeignKey(ReferralStatus, on_delete=models.CASCADE)
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
        unique_together = ('position', 'eligible_list', 'status')


class Department(models.Model):
    title = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
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
    # "job_" necessary because class is a reserved word
    job_class = models.ForeignKey(JobClass, blank=True, null=True, on_delete=models.CASCADE)
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
        unique_together = ('sr_uuid', 'candidate')


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
        unique_together = ('eligible_list', 'candidate')


class EligibleListCandidateReferral(models.Model):
    eligible_list_candidate = models.ForeignKey(EligibleListCandidate, on_delete=models.CASCADE)
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
    status = models.ForeignKey(CandidateReferralStatus, null=True, blank=True, on_delete=models.CASCADE)
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
        unique_together = ('eligible_list_candidate', 'referral')


class ScoreBandingModelScoreBand(models.Model):
    score_banding_model = models.ForeignKey(ScoreBandingModel, on_delete=models.CASCADE)
    score_band = models.ForeignKey(ScoreBand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='score_banding_score_band_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='score_banding_score_band_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.score_banding_model} - {self.score_band}'

    class Meta:
        verbose_name = 'ScoreBandingModelScoreBand'
        verbose_name_plural = 'ScoreBandingModelScoreBands'
        unique_together = ('score_banding_model', 'score_band')


# Abstract entities
class LongRunningTask(models.Model):
    # For delegating tasks in a pseudo-async fashion, using the
    # DB as a message queue, and a worker to poll for items in the queue
    # to processing them in sequential, stack, FIFO order
    type = models.ForeignKey(LongRunningTaskType, on_delete=models.CASCADE)
    status = models.ForeignKey(LongRunningTaskStatus, on_delete=models.CASCADE)
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    # Entities by FK relation, for use if necessary. This is a God model,
    # which is also a serious antipattern
    referral_statuses = models.ManyToManyField(ReferralStatus, blank=True)
    candidate_referral_statuses = models.ManyToManyField(CandidateReferralStatus, blank=True)
    candidates = models.ManyToManyField(Candidate, blank=True)
    positions = models.ManyToManyField(Position, blank=True)
    eligible_lists = models.ManyToManyField(EligibleList, blank=True)
    referrals = models.ManyToManyField(Referral, blank=True)
    departments = models.ManyToManyField(Department, blank=True)
    jobs = models.ManyToManyField(Job, blank=True)
    applications = models.ManyToManyField(Application, blank=True)
    eligible_list_candidates = models.ManyToManyField(EligibleListCandidate, blank=True)
    eligible_list_candidate_referrals = models.ManyToManyField(EligibleListCandidateReferral, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='long_running_task_created_by',
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey(get_user_model(),
                                        related_name='long_running_task_last_updated_by',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)

    def __str__(self):
        return f'Task: {self.type} - {self.description}'

    class Meta:
        verbose_name = 'LongRunningTask'
        verbose_name_plural = 'LongRunningTasks'


class APIRateLimiter(SingleInstanceMixin, models.Model):
    sr_current_concurrent_tokens = models.IntegerField(default=8, blank=True, null=True)
    sr_current_concurrent_candidate_tokens = models.IntegerField(default=1, blank=True, null=True)
    sr_current_requests_per_second_tokens = models.IntegerField(default=10, blank=True, null=True)
    aws_current_concurrent_tokens = models.IntegerField(default=10, blank=True, null=True)
    aws_current_requests_per_second_tokens = models.IntegerField(default=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    notes = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f'SR tokens: {self.sr_current_concurrent_tokens} AWS tokens: {self.aws_current_concurrent_tokens}'

    class Meta:
        verbose_name = 'APIRateLimiter'
        verbose_name_plural = 'APIRateLimiters'
