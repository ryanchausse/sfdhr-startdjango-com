from django.contrib import admin
from .models import Candidate
from .models import Position
from .models import EligibleList
from .models import Referral
from .models import Job
from .models import Application
from .models import Department
from .models import EligibleListCandidate
from .models import EligibleListCandidateReferral
from .models import ReferralStatus
from .models import CandidateReferralStatus
from .models import LongRunningTask
from .models import LongRunningTaskType
from .models import LongRunningTaskStatus
from .models import APIRateLimiter
from .models import ScoringModel
from .models import JobClass
from .models import EligibleListRule

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(EligibleList)
admin.site.register(Referral)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Department)
admin.site.register(LongRunningTask)

# Relational Entities
admin.site.register(EligibleListCandidate)
admin.site.register(EligibleListCandidateReferral)

# Reference Tables
admin.site.register(ReferralStatus)
admin.site.register(CandidateReferralStatus)
admin.site.register(ScoringModel)
admin.site.register(JobClass)
admin.site.register(EligibleListRule)
admin.site.register(LongRunningTaskType)
admin.site.register(LongRunningTaskStatus)

# Rate Limiting
admin.site.register(APIRateLimiter)
