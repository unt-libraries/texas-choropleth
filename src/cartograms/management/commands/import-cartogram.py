from django.core.management.base import BaseCommand, CommandError
from cartograms.models import Cartogram, CartogramEntity

import json
from pprint import pprint

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs="+", type=string)

    def handle(self, *args, **options):
        print "Starting import\n------------------\n"
        json_data = open(args[0])
        data = json.load(json_data)
        cartogram = Cartogram(name='Texas', cartogram_id="48", json_filename="/texas.json")
        cartogram.save()

        for entity in data['objects']['counties']['geometries']:
            cartogram_entity = CartogramEntity()
            cartogram_entity.name = entity['properties']['name']
            cartogram_entity.entity_id = entity['properties']['fips']
            cartogram.entities.add(cartogram_entity)

        cartogram.save()
        print 'Import finished successfully'

