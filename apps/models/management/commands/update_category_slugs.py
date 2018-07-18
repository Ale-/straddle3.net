# django
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
# project
from apps.models.models import ProjectCategory, ConnectionCategory, ResourceCategory

"""
A manage.py command to update Category slugs
"""

class Command(BaseCommand):
    help = "Update category slugs"

    """
    Imports JournalIssue objects from a given CSV file
    """
    def handle(self, *args, **options):
        categories = [ ProjectCategory, ConnectionCategory, ResourceCategory]
        for category in categories:
            cats = category.objects.all()
            for cat in cats:
                cat.slug = slugify(cat.name)
                cat.save()
