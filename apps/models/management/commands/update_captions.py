import json
# django
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
# project
from apps.models.models import Image

"""
A manage.py command to update Tag slugs
"""

class Command(BaseCommand):
    help = "Update tag slugs"

    """
    Imports JournalIssue objects from a given CSV file
    """
    def handle(self, *args, **options):
        with open('../fixtures/s3__1-ago-2018.json', encoding='utf-8') as fixture:
            data = json.loads(fixture.read())
            for obj in data:
                if obj['model'] == 'models.image':
                    try:
                        Image.objects.filter(pk=obj['pk']).update(caption=obj['fields']['alt_text'])
                    except Exception as e:
                        print(str(e))
