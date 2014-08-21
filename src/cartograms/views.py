import csv
from django.http import HttpResponse
from .models import Cartogram

def cartogram_csv_template(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefile.csv"'

    cartogram = Cartogram.objects.get(id=pk)

    writer = csv.writer(response)
    writer.writerow(['entity_id', 'value'])
    for entity in cartogram.entities.all():
        writer.writerow([entity.entity_id, 'null'])

    return response
