from django.core.management import BaseCommand

from dev.test_data.populate import populate


class Command(BaseCommand):
    help = "Populates data for dev environment"

    def add_arguments(self, parser):
        parser.add_argument("--r", action="store_true", help="Clean existing data and recreate")

    def handle(self, *args, **options):
        populate(clean_existing_data=options.get("r"))
