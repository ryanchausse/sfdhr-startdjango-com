from django.contrib import admin
# from .models import NormForm
# from .models import Patient
# from .models import Facility
# from .models import SubjectiveBoilerplateOption
# from .models import SubjectiveOption
# from .models import DiscussionTreatmentOption
# from .models import Icd10Codes
from .models import Candidate
from .models import Position
from .models import EligibleList
from .models import Referral
from .models import Job
from .models import Application
from .models import Department
from .models import EligibleListCandidate
from .models import EligibleListCandidateReferral


# admin.site.register(NormForm)
# admin.site.register(Patient)
# admin.site.register(Facility)
# admin.site.register(SubjectiveBoilerplateOption)
# admin.site.register(SubjectiveOption)
# admin.site.register(DiscussionTreatmentOption)
# admin.site.register(Icd10Codes)

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