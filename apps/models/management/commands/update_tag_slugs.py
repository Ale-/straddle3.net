# django
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
# project
from apps.models.models import Tag

"""
A manage.py command to update Tag slugs
"""

class Command(BaseCommand):
    help = "Update tag slugs"

    """
    Imports JournalIssue objects from a given CSV file
    """
    def handle(self, *args, **options):
        tags = Tag.objects.all()
        for tag in tags:
            print(tag.name)
            tags.slug = slugify(tag.name)
            tag.save()
