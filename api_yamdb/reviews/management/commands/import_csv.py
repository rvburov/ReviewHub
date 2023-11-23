from typing import Any
import pandas
from django.core.management.base import BaseCommand, CommandParser
from reviews.models import Title, TitleGenre


class Command(BaseCommand):
    help = 'Import from CSV'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('csv_file', type=str)
    
    def handle(self, *args: Any, **options: Any):
        csv_file = options['csv_file']
        df = pandas.read_csv(csv_file)

        for index, row in df.iterrows():
            TitleGenre.objects.create(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id']
            )
        
        
