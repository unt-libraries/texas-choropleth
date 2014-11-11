import csv
from django.http import HttpResponse
from .models import Cartogram


def cartogram_csv_template(request, pk):
    cartogram = Cartogram.objects.get(id=pk)

    content_disposition = 'attachment; filename="{}.csv"'.format(
        cartogram.name.lower())

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    writer.writerow(['fips', 'name', 'value'])
    for entity in cartogram.entities.all().order_by('entity_id'):
        writer.writerow([entity.entity_id, entity.name, ''])

    return response
