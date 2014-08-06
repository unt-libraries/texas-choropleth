import csv

from django.core.exceptions import ValidationError
from cartograms.models import CartogramEntity

INCORRECT_DELIMITER = u'Incorrect delimiter'
INCORRECT_FILETYPE = u'Not a valid CSV file' 
INCORRECT_ENTITY_ID = u'entity_id %s does not exist in row %s'
MISSING_HEADERS = u'Missing headers: %s' 
MISSING_REQUIRED_VALUE = u'Missing required value %s for row %s'

MESSAGES = (
    INCORRECT_DELIMITER,
    INCORRECT_FILETYPE,
    INCORRECT_ENTITY_ID,
    MISSING_HEADERS,
    MISSING_REQUIRED_VALUE,
)

DELIMITER = ','
HEADERS = {
        'entity_id': {'field': 'entity_id', 'required': True},
        'value' : {'field': 'value', 'required': False},
        }

def import_validator(document):
    try:
        # might need to be document.file.file
        dialect = csv.Sniffer().sniff(document.read(1024))
        document.seek(0, 0)
        if dialect.delimiter != DELIMITER:
            raise ValidationError(INCORRECT_DELIMITER)
    except csv.Error:
        raise ValidationError(INCORRECT_FILETYPE)

    reader = csv.reader(document.read().splitlines(), dialect)
    csv_headers = []

    required_headers = [header_name for header_name, values in HEADERS.items()]
    required_fields = [header_name for header_name, values in HEADERS.items() if values['required']]

    for row_num, row in enumerate(reader):
        # Check the headers
        if row_num == 0:
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_msg = ', '.join(missing_headers)
                raise ValidationError(MISSING_HEADERS % (missing_headers_msg))
            continue

        # Check for empty rows
        if not ''.join(str(x) for x in row) and 0 == len(row):
            continue

        # Check the individual cells for required values
        for index, cell_value in enumerate(row):
            try:
                csv_headers[index]
            except IndexError:
                continue

            if csv_headers[index] in required_fields:
                if not cell_value:
                    raise ValidationError(MISSING_REQUIRED_VALUE % (csv_headers[index], row_num + 1))

        # Check that the corresponding entity exists
        if not CartogramEntity.objects.filter(entity_id=row[0]).exists():
            msg = INCORRECT_ENTITY_ID % (row[0], row_num + 1)
            raise ValidationError(msg)

    return True



    
