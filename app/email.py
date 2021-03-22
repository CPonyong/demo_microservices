from flask import jsonify, request, render_template, Blueprint, current_app
from flask_mail import Message

send_email = Blueprint('send_email', __name__)

@send_email.route('/api/v1/vmember/send_email', methods=['POST'])
def email():
    data = request.get_json()
    recipients = []
    for item in data['recipients']:
        recipients.append(data['recipients'][item])

    if data['template'] and data['recipients']:
        get_template = data['template']
        # template = "/email_template.html"
        # template = db_connect.select_template(get_template).split('/')[2]
        email_template = render_template(get_template, confirm_url=data['message'])

        msg = Message(
            data['subject'],
            recipients=recipients,
            cc=[data['cc']],
            html=email_template,
            sender=(data['sender'])
        )
        current_app.config['mail'].send(msg)
        status = {"file": None,
                  "status": "success"}
        data.update(status)
        return jsonify(status)





