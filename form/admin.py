from django.contrib import admin
from .models import NormForm
from .models import Patient
from .models import Facility
from .models import SubjectiveBoilerplateOption
from .models import SubjectiveOption
from .models import DiscussionTreatmentOption
from .models import Icd10Codes

admin.site.register(NormForm)
admin.site.register(Patient)
admin.site.register(Facility)
admin.site.register(SubjectiveBoilerplateOption)
admin.site.register(SubjectiveOption)
admin.site.register(DiscussionTreatmentOption)
admin.site.register(Icd10Codes)
