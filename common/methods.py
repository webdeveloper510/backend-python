from django.utils import timezone
from django.utils.dateparse import parse_date

def calculate_age(dob):
    if dob == None:
        return None
    if( isinstance(dob, str)):
        dob = parse_date(dob)

    today = timezone.now()
    # dob = parse_date(self.dob)
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)