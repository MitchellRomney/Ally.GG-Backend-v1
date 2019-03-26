from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.champions import *
from dashboard.functions.summoners import *
from django.http import JsonResponse

def checkErrors(raw_json):
    if 'status' in raw_json:
        if raw_json['status']['status_code'] == 429: # Limit Exceeded
            return json.dumps({'message': raw_json['status']['message'], 'isError': True})
        if raw_json['status']['status_code'] == 404: # Summoner Not Found
            return json.dumps({'message': 'This summoner doesn\'t exist!', 'isError': True})

    return json.dumps({'message': 'No errors found.', 'isError': False,})
