import base64
import json
import requests
import logging

from background_task import background
from mtn import settings
logger = logging.getLogger(__name__)
def gettoken(type="COLLECT"):
    if(type=='DISBURSE'):
        url = settings.MOMO_URL+"/disbursement/token/"
        key=settings.DISBURSE_KEY
    else:
        url = settings.MOMO_URL + "/collection/token/"
        key=settings.COLLECT_KEY
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic " + base64.b64encode(settings.API_USERID + ":" +settings.API_KEY),
        'Ocp-Apim-Subscription-Key': key,
    }
    print(url)
    response = requests.request("POST", url, data='', headers=headers,verify=False)
    print(response)
    token = json.loads(response.text)
    return token['access_token']

def collect(momorequest):
    url = settings.MOMO_URL+'/collection/v1_0/requesttopay'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+gettoken("COLLECT"),
        'X-Reference-Id': str(momorequest.id),
        'X-Target-Environment': "sandbox",
        'Ocp-Apim-Subscription-Key': settings.COLLECT_KEY,
    }

    payload = {
        'amount': str(momorequest.amount),
        'currency': settings.CURRENCY,
        'externalId': str(momorequest.id),
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": momorequest.msisdn
        },
        "payerMessage": momorequest.narration,
        "payeeNote": momorequest.narration
    }
    print(url)
    print(headers)
    print(payload)
    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

        momorequest.status_code=response.status_code
        momorequest.save()
        print(response)
        return response
    except Exception as e:
        momorequest.error = str(e)
        momorequest.save()
        print(str(e))
        return e

def disburse(momorequest):
    url = settings.MOMO_URL + '/disbursement/v1_0/transfer'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + gettoken("DISBURSE"),
        'X-Reference-Id': str(momorequest.id),
        'X-Target-Environment': "sandbox",
        'Ocp-Apim-Subscription-Key': settings.DISBURSE_KEY,
    }

    payload = {
        'amount': str(momorequest.amount),
        'currency': settings.CURRENCY,
        'externalId': str(momorequest.id),
        "payee": {
            "partyIdType": "MSISDN",
            "partyId": momorequest.msisdn
        },
        "payerMessage": momorequest.narration,
        "payeeNote": momorequest.narration
    }
    print(url)
    print(headers)
    print(payload)
    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        print(response)
        momorequest.status_code=response.status_code
        momorequest.save()
        return response
    except Exception as e:
        momorequest.error = str(e)
        momorequest.save()
        print(str(e))
        return str(e)

@background(schedule=1,queue='mtn-momo')
def worker():
    from models import MomoRequest
    transactions = MomoRequest.objects.filter(momo_status="PENDING")
    for transaction in transactions:
        transaction_status(str(transaction.id))

def transaction_status(momorequest):
    from models import MomoRequest
    momorequest=MomoRequest.objects.get(pk=momorequest)
    url = settings.MOMO_URL + '/collection/v1_0/requesttopay/'+str(momorequest.id)
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + gettoken("COLLECT"),
        'X-Target-Environment': "sandbox",
        'Ocp-Apim-Subscription-Key': settings.COLLECT_KEY,
    }
    print(url)
    print(headers)
    try:
        response = requests.request("GET", url, headers=headers)
        if(response.status_code==200):
            transaction=json.loads(response.text)
            momorequest.momo_status=transaction['status']
            momorequest.momo_reference=transaction['financialTransactionId']
            momorequest.status_code=response.status_code
            momorequest.save()
        else:
            momorequest.status_code=response.status_code
            momorequest.error=response.text
            momorequest.momo_status="FAILED"
            momorequest.save()
        print(response)
        return response
    except Exception as e:
        momorequest.momo_status = "FAILED"
        momorequest.error = str(e)
        momorequest.save()
        print(str(e))
        return e
