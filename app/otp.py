from flask import Blueprint, request, jsonify
from http.client import HTTPConnection
from json import dumps, loads
from secrets import token_urlsafe
from uuid import UUID
from datetime import datetime, timedelta
from app.lib.database import vez_connection, vmember_database, vmember_token_refresh, vmember_otp_query, \
    vmember_otp_insert, vmember_otp_update, member_update, vmember_log_query
from app.lib.cryption import jwt_decode

vmember_otp = Blueprint('vmember_otp', __name__)


@vmember_otp.route('/api/v1/vmember/otp', methods=['POST'])
def vmember_otp_app():
    if request.method == 'POST':
        vez_connect = vez_connection()
        vmember_connect = vmember_database(vez_connect)
        data = {}
        data['reference_id'] = token_urlsafe(4)

        connection = HTTPConnection('www.molinkapi.com')

        headers = {
            'Content-Type': 'application/json'
        }

        data['username'] = "wpa_vez"
        data['password'] = "wpa1234"
        data['txtSMS'] = "ขอบคุณที่สมัครใช้บริการ VEZ รหัสยืนยันตัวตนของคุณคือ ${code}"
        data['sender'] = "VEZ"
        json = request.get_json()
        data['txtMobile'] = json.get('mobile_num')
        payload = dumps(data)
        connection.request('POST', '/molink_otp_service/sms.asmx/OTPSend', payload, headers)
        response = connection.getresponse()
        data2 = response.read()
        data2 = loads(data2)
        data['otp_id'] = data2['d']['Result']['otp_id']

        del data['username']
        del data['password']
        del data['txtSMS']
        del data['sender']
        del data['txtMobile']
        data['status'] = 0
        vmember_otp_insert(vmember_connect, data)

        result = {
            "status": True,
            "result": {
                "reference_id": data['reference_id']
            }
        }

        return jsonify(result)


vmember_otp_validate = Blueprint('vmember_otp_validate', __name__)


@vmember_otp_validate.route('/api/v1/vmember/otp_verify', methods=['POST'])
def vmember_otp_validate_app():
    if request.method == 'POST':
        vez_connect = vez_connection()
        vmember_connect = vmember_database(vez_connect)
        bearer = request.headers.get('Authorization')
        token = bearer.split()[1]

        if token == None or token == '':
            value = {
                "status": False,
                "message": "token is require"
            }

            return jsonify(value)

        result, exprie_dtm = vmember_log_query(vmember_connect, "token_validate", None, bytes(token, 'utf-8'))
        dtm = datetime.now()

        if result == True and exprie_dtm >= dtm:
            exprie_dtm = datetime.now() + timedelta(minutes=20)
            vmember_token_refresh(vmember_connect, "vmember", bytes(token, 'utf-8'), exprie_dtm)
            payload = jwt_decode(token)
            uuid = payload.get('uuid')
            data = {}
            json = request.get_json()
            data['reference_id'] = json.get('reference_id')
            data = vmember_otp_query(vmember_connect, data)

            data['code'] = json.get('code')
            payload = dumps(data)
            connection = HTTPConnection('www.molinkapi.com')

            headers = {
                'Content-Type': 'application/json'
            }

            connection.request('POST', '/molink_otp_service/sms.asmx/OTPValidate', payload, headers)
            response = connection.getresponse()
            data = response.read()
            data = loads(data)
            data2 = data['d']['Result']['code']

            if data2 == None:
                data = {}
                value = {}
                data['reference_id'] = json.get('reference_id')
                value['status'] = 1

                vmember_otp_update(vmember_connect, data, value)

                data2 = {}
                value2 = {}

                data2['uuid'] = UUID(uuid)
                value2['mobile_verify'] = True

                member_update(vmember_connect, data2, value2)

                result = {
                    "status": True
                }

                return jsonify(result)
            else:
                error = data['d']['Result']['message']

                result = {
                    "status": False,
                    "message": error
                }

                return jsonify(result)
        elif result == False:
            value = {
                "status": False,
                "message": "token not existing"
            }

            return jsonify(value)
        elif exprie_dtm < dtm:
            value = {
                "status": False,
                "message": "token expired"
            }

            return jsonify(value)