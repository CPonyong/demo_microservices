from datetime import datetime
from http.client import HTTPConnection
from uuid import UUID
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify, json
from jwt import decode
from pymongo import MongoClient
from celery import shared_task
import omise

from app.lib.cryption import jwt_decode

@shared_task(bind=True)
def add_sum():
    return 0

vpayment_payment = Blueprint('vpayment_payment', __name__)

OMISE_SECRET_KEY = "skey_test_5mngbtegkd02nxejrw8"
OMISE_PUBLIC_KEY = "pkey_test_5mngbteg8osqcdqrr1d"

omise.api_secret = OMISE_SECRET_KEY
omise.api_public = OMISE_PUBLIC_KEY

myclient = MongoClient("mongodb+srv://cake:0810004833@vezdev.ghalb.mongodb.net/?ssl=true&authSource=admin&uuidRepresentation=standard")
mydb = myclient["vpayment"]

@vpayment_payment.route('/api/v1/vpayment/add_address', methods=['POST'])
def add_address_app():
    address_collection = mydb['address']
    address_data = request.get_json()
    user_token = request.headers.get('Authorization').split(' ')[1]

    uuid = jwt_decode(user_token)['uuid']

    query = {
        "fname": address_data['fname'],
        "mname": address_data['mname'],
        "lname": address_data['lname'],
        "addr_full": address_data['addr_full'],
        "building": address_data['building'],
        "floor":address_data['floor'],
        "house_no":address_data['house_no'],
        "village":address_data['village'],
        "alley": address_data['alley'],
        "road": address_data['road'],
        "sub_district":address_data['sub_district'],
        "district":address_data['district'],
        "province":address_data['province'],
        "postalcode":address_data['postalcode'],
        "landmark":address_data['landmark'],
        "google_map":address_data['google_map'],
        "mobile_phone":address_data['mobile_phone'],
        "uuid":UUID(uuid)
    }

    address_collection.insert(query)

    return jsonify({"status":"success"})

@vpayment_payment.route('/api/v1/vpayment/add_tax_address', methods=['POST'])
def add_tax_address_app():
    tax_address_collection = mydb['tax_address']
    address_data = request.get_json()
    user_token = request.headers.get('Authorization').split(' ')[1]

    uuid = jwt_decode(user_token)['uuid']

    query = {
        "building": address_data['building'],
        "floor":address_data['floor'],
        "house_no":address_data['house_no'],
        "village":address_data['village'],
        "alley": address_data['alley'],
        "road": address_data['road'],
        "sub_district":address_data['sub_district'],
        "district":address_data['district'],
        "province":address_data['province'],
        "postalcode":address_data['postalcode'],
        "landmark":address_data['landmark'],
        "google_map":address_data['google_map'],
        "company_name":address_data['company_name'],
        "tax_identification_number":address_data['tax_identification_number'],
        "branch":address_data['branch'],
        "type_of_tax_invoice_address":address_data['type_of_tax_invoice_address'],
        "identifications_number":address_data['identifications_number'],
        "passport_number":address_data['passport_number'],
        "lname": address_data['lname'],
        "uuid":UUID(uuid),
    }

    tax_address_collection.insert(query)

    return jsonify({"status":"success"})

    # in case of uuid already exist.

@vpayment_payment.route('/api/v1/vpayment/list_address', methods=['GET'])
def retrieve_address_app():
    address_collection = mydb['address']
    tax_address_collection = mydb['tax_address']

    user_address = []
    tax_adress = []
    address = []

    user_token = request.headers.get('Authorization').split(' ')[1]
    uuid = jwt_decode(user_token)['uuid']

    query = {"uuid":UUID(uuid)}
    address_result = address_collection.find(query)
    tax_address_result = tax_address_collection.find(query)

    for item in address_result:
        item['id'] = str(item['_id'])
        del item['_id']
        user_address.insert(len(user_address), item)

    for item in tax_address_result:
        item['id'] = str(item['_id'])
        del item['_id']
        print(item)
        tax_adress.insert(len(tax_adress), item)

    address = {"data":{
        "address": user_address,
        "tax_address": tax_adress
    }}

    return jsonify(address)

@vpayment_payment.route('/api/v1/vpayment/card/<card_id>', methods=['GET', 'DELETE'])
def card_all_and_delete(card_id):
    if request.method == 'GET':
        collection = mydb['card']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']

        query = {"uuid": UUID(uuid),
                 "_id": ObjectId(card_id)}
        result = collection.find_one(query, {"_id": 0})

        data = {"card": {
            "brand": result['brand'],
            "isdefault_card": result['isdefault_card'],
            "last_digits": result['last_digits'],
            "name": result['name'],
            "card_id": result['id']
        }}
        return data
    elif request.method == 'DELETE':
        card_collection = mydb['card']
        cus_collection = mydb['omise_data']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']

        cus_query = {"uuid": UUID(uuid)}
        cus_result = cus_collection.find_one(cus_query, {'_id': 0})

        card_query = {"_id": ObjectId(card_id)}
        card = card_collection.find_one(cus_query)['id']
        card_collection.delete_one(card_query)

        customer = omise.Customer.retrieve(cus_result['cus_id'])
        card = customer.cards.retrieve(card)
        card.destroy()

        return jsonify({"status": "success"})

@vpayment_payment.route('/api/v1/vpayment/card', methods=['GET', 'POST'])
def card_add_and_retrieve():
    if request.method=='GET':
        card_list = []
        collection = mydb['card']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']

        query = {"uuid":UUID(uuid)}

        result = collection.find(query,{"brand": 1, "last_digits": 1, "name": 1, "isdefault": 1 })

        for item in result:
            item['id'] = str(item['_id'])
            del item['_id']
            card_list.insert(len(card_list), item)

        output_data = {"cards":
                           card_list
                       }
        return output_data
    elif request.method == 'POST':
        collection = mydb['omise_data']
        card_collection = mydb['card']
        customer_data = request.get_json()
        customer_id = request.headers.get('Authorization').split(' ')[1]

        uuid = jwt_decode(customer_id)['uuid']

        # add_card.delay(customer_data,uuid)

        query = {"uuid": UUID(uuid)}
        data = collection.find_one(query, {"_id": 0})
        # create token
        token = omise.Token.create(
            name=customer_data['name'],
            number=customer_data['card_number'],
            expiration_month=customer_data['expiration_month'],
            expiration_year=customer_data['expiration_year'],
            city=customer_data['city'],
            postal_code=customer_data['postal_code'],
            security_code=customer_data['security_code']
        )

        token_id = token._attributes['id']
        # return jsonify(token_id)

        if data is not None:
            cus_id = data['cus_id']
            # update customer
            customer = omise.Customer.retrieve(cus_id)
            customer.update(card=token_id)
            update_cus_response = customer._attributes

            update_cus = update_cus_response['cards']['data'][-1]

            new_card_data = {
                "uuid": UUID(uuid),
                "id": update_cus['id'],
                "brand": update_cus['brand'],
                "last_digits": update_cus['last_digits'],
                "name": update_cus['name'],
                "isdefault_card": False
            }

            card_collection.insert(new_card_data)

            return jsonify({"status": "success"})
        else:
            # create customer
            customer = omise.Customer.create(
                email=customer_data['email'],
                description=customer_data['description'],
                card=token_id,
            )
            customer_response = customer._attributes

            customer_query = {"uuid": UUID(uuid),
                              "cus_id": customer_response['id'],
                              "create_at": customer_response['created_at'],
                              "email": customer_response['email']
                              }

            collection.insert(customer_query)
            # retrieve default card
            customer = omise.Customer.retrieve(customer_response['id'])
            card = customer.cards.retrieve(customer_response['cards']['data'][0]['id'])
            card_response = card._attributes

            card_data = {
                "uuid": UUID(uuid),
                "id": card_response['id'],
                "brand": card_response['brand'],
                "last_digits": card_response['last_digits'],
                "name": card_response['name'],
                "isdefault_card": True
            }

            card_collection.insert(card_data)

            return jsonify({"status": "success"})

@vpayment_payment.route('/api/v1/vpayment/create_charge', methods=['POST'])
def create_charge_app():
    ip = request.remote_addr
    #transaction -> mock up order data
    collection = mydb['transaction']
    card_collection = mydb['card']
    cus_collection = mydb['omise_data']
    charge_data = request.get_json()
    user_token = request.headers.get('Authorization').split(' ')[1]
    uuid = jwt_decode(user_token)['uuid']

    data_query = {"_id":ObjectId(charge_data['transaction_id'])}
    transaction = collection.find_one(data_query)

    card_query = {"_id":ObjectId(transaction['card_id'])}
    card = card_collection.find_one(card_query,{"_id":0})['id']

    cus_query = {"_id":ObjectId(transaction['customer_id'])}
    customer = cus_collection.find_one(cus_query,{"_id":0})['cus_id']

    connection = HTTPConnection('www.weprovideall-int.appspot.com')
    headers = {
        'accept-language': 'th',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmYjU0OTI2MTY1Yjg0NTFmMWY1ZGU2MyIsImlhdCI6MTYwNTcxNzI1MCwiZXhwIjozMTcxNTAxNTk2NTB9.DLSWBw9whJebDyKzuKnQ1bezOB3loa_G1PVcZuxlau4'
    }
    payload = {}

    connection.request('GET', '/api/tenant/default/service/'+transaction['service_id'], payload, headers)

    service_response = connection.getresponse()
    service_response = service_response.read()

    service_price = json.loads(service_response)['price']*100

    charge = omise.Charge.create(
        amount=service_price,
        currency="thb",
        customer=customer,
        card=card,
    )
    response = charge._attributes

    query = {"_id":ObjectId(charge_data['transaction_id'])}

    data_update = {"$set":{
        "charge_id":response['id'],
        "amount":response['amount'],
        "net":response['net'],
        "fee":response['fee'],
        "fee_vat":response['fee_vat'],
        "interest":response['interest'],
        "interest_vat":response['interest_vat'],
        "funding_amount":response['funding_amount'],
        "refunded_amount":response['refunded_amount'],
        "capturable":response['capturable'],
        "disputable":response['disputable'],
        "refundable":response['refundable'],
        "voided":response['voided'],
        "paid":response['paid'],
        "expired":response['expired'],
        "currency":response['currency'],
        "funding_currency":response['funding_currency'],
        "ip":response['ip'],
        "status":response['status'],
        "created_at":response['created_at'],
        "paid_at":response['paid_at'],
        "expires_at":response['expires_at']
    }
    }

    collection.update(query, data_update)
    output = {"status":response['status']}

    return jsonify(output)

@vpayment_payment.route('/api/v1/vpayment/address/<address_id>', methods=['GET' ,'PATCH'])
def address_app(address_id):
    if request.method == 'PATCH':
        collection = mydb['address']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']
        data = request.get_json()

        query = {"uuid":UUID(uuid),
                 "_id":ObjectId(address_id)
                 }

        data_update = {"$set":data}

        collection.update_one(query,data_update)


        return jsonify({"status":"success"})
    else:
        collection = mydb['address']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']

        query = {"uuid": UUID(uuid),
                 "_id": ObjectId(address_id)
                 }
        result = collection.find_one(query,{"_id":0})
        result = {"data":result}

        return result

@vpayment_payment.route('/api/v1/vpayment/tax_address/<tax_address_id>', methods=['GET' ,'PATCH'])
def edit_tax_address_app(tax_address_id):
    if request.method == 'PATCH':
        collection = mydb['tax_address']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']
        data = request.get_json()

        query = {"uuid": UUID(uuid),
                 "_id": ObjectId(tax_address_id)
                 }

        data_update = {"$set": data}

        collection.update_one(query, data_update)

        return jsonify({"status":'Success'})
    else:
        collection = mydb['tax_address']
        user_token = request.headers.get('Authorization').split(' ')[1]
        uuid = jwt_decode(user_token)['uuid']

        query = {"uuid": UUID(uuid),
                 "_id": ObjectId(tax_address_id)
                 }
        result = collection.find_one(query,{"_id":0})
        result = {"data":result}

        return result


@vpayment_payment.route('/api/v1/vpayment/create_transaction', methods=['POST'])
def create_transaction():
    collection = mydb['transaction']
    user_token = request.headers.get('Authorization').split(' ')[1]
    uuid = jwt_decode(user_token)['uuid']
    transaction = request.get_json()


    d = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    data_update = {"timestamp":d,
                   "uuid":UUID(uuid)}
    #service id, transaction detail, timestamp

    transaction.update(data_update)

    collection.insert(transaction)

    query = {"uuid":transaction['uuid']}

    result = collection.find(query).sort([('_id', -1)]).limit(1)

    for item in result:
        item['id'] = str(item['_id'])
        del item['_id']
        t_id = item['id']

    return jsonify({"transaction_id":t_id})