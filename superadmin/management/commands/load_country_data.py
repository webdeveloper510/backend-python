from django.conf import settings
from django.core.management.base import BaseCommand
from superadmin.subapps.countries_and_cities import models as models_country
import csv

class Command(BaseCommand):
    help = 'Load ISO Country data from CSV file country_data.csv'

    def handle(self, *args, **kwargs):
        # print("Loading Country data")
        
        with open('country_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    models_country.Country.objects.create(name=row[0], abbr=row[1])
                    print(f'\t{row[0]} - {row[1]}')
                    line_count += 1
            # print(f'Processed {line_count} lines.')
            print(f'Saved {line_count} entries.')