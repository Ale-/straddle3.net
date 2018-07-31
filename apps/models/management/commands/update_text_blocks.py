# django
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
# project
from apps.models.models import Block

"""
A manage.py command to update Tag slugs
"""

class Command(BaseCommand):
    help = "Update tag slugs"

    """
    Imports JournalIssue objects from a given CSV file
    """
    def handle(self, *args, **options):
        blocks = Block.objects.all()
        for block in blocks:
            tmp_name = block.name
            block.name  = block.label
            block.label = tmp_name
            block.save()
