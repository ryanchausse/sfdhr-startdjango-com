import csv
from .models import Icd10Codes
# Put this script in views.py's ViewNormFormsPage
filename = os.path.abspath(os.path.dirname(__file__)) + '/icd_10_2020_diagnosis_codes.csv'
with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        _, created = Icd10Codes.objects.get_or_create(
            diagnosis_code=row[2],
            full_code=row[1],
            abbreviated_description=row[3],
            full_description=row[4]
        )
