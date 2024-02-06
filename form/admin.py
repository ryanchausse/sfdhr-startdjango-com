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
from .models import CandidateReferralStatus

admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(EligibleList)
admin.site.register(Referral)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Department)

# Relational Entities
admin.site.register(EligibleListCandidate)
admin.site.register(EligibleListCandidateReferral)

# Reference Tables
admin.site.register(CandidateReferralStatus)
