from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from app.authentication import vmember_authentication
from app.token import vmember_token_get, vtrack_token_get, vfund_token_validate, vtrack_token_validate
from app.register import vmember_register
from app.security import vfund_authentication_check
from app.profile import vmember_profile_view, vmember_password_change, vmember_profile, vmember_pin, vmember_privacy, vfund_profile_view, vfund_profile, vpartner_service_images
from app.testimonial import vmember_question, vmember_answer, vmember_testimonial
from app.upload import vmember_document_upload, vpartner_document_upload, vfund_project_upload
from app.test import vmember_post_test
from app.api import vtrack_main, vexpert_business_type, vexpert_company, vexpert_service, vexpert_order
from app.post import vmember_post
from app.feature import vmember_module, vmember_facility, vmember_feature
from app.favorite import vmember_favorite, vpartner_favorite, vfund_favorite
from app.call_expert import vmember_call_expert_service, vfund_call_expert
from app.advertise import vmember_advertise
from app.help import vpartner_order_edit
from app.review import vfund_review
from app.otp import vmember_otp, vmember_otp_validate
from app.notification import vmember_notification
from app.data import vmember_web_config_post_image, vmember_web_config_post_video, vmember_web_config_module_image, vmember_web_config_module_video, vmember_web_config_partner_image, vmember_web_config_partner_video, vmember_web_config_service_image, vmember_web_config_service_video, vmember_web_config_profile_image, vmember_profile_image, vmember_document_view, vpartner_document_view, vpartner_order_edit_attachment, vfund_document_view, vmember_web_config_advertise_image, vmember_web_config_advertise_video, vmember_web_config_question_image, vpartner_service_images_image
from app.send_email import send_email
from app.payment import vpayment_payment
app = Flask(__name__)
CORS(app)
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'test.vezmailverify@gmail.com'
app.config['MAIL_PASSWORD'] = 'w4dHNxM78^PA<u"?'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['file_upload'] = "./file_upload"


mail = Mail(app)
app.config['mail'] = mail

app.register_blueprint(vmember_module)
app.register_blueprint(vmember_facility)
app.register_blueprint(vmember_post)
app.register_blueprint(vmember_authentication)
app.register_blueprint(vmember_token_get)
app.register_blueprint(vtrack_token_get)
app.register_blueprint(vfund_token_validate)
app.register_blueprint(vtrack_token_validate)
app.register_blueprint(vmember_register)
app.register_blueprint(vmember_profile_view)
app.register_blueprint(vfund_profile)
app.register_blueprint(vmember_password_change)
app.register_blueprint(vmember_profile)
app.register_blueprint(vfund_profile_view)
app.register_blueprint(vmember_question)
app.register_blueprint(vmember_answer)
app.register_blueprint(vmember_testimonial)
app.register_blueprint(vmember_post_test)
app.register_blueprint(vmember_document_upload)
app.register_blueprint(vpartner_document_upload)
app.register_blueprint(vfund_project_upload)
app.register_blueprint(vmember_web_config_post_image)
app.register_blueprint(vmember_web_config_post_video)
app.register_blueprint(vmember_web_config_module_image)
app.register_blueprint(vmember_web_config_module_video)
app.register_blueprint(vmember_web_config_partner_image)
app.register_blueprint(vmember_web_config_partner_video)
app.register_blueprint(vmember_web_config_service_image)
app.register_blueprint(vmember_web_config_service_video)
app.register_blueprint(vmember_web_config_profile_image)
app.register_blueprint(vmember_profile_image)
app.register_blueprint(vmember_document_view)
app.register_blueprint(vpartner_document_view)
app.register_blueprint(vpartner_order_edit)
app.register_blueprint(vfund_document_view)
app.register_blueprint(vtrack_main)
app.register_blueprint(vexpert_business_type)
app.register_blueprint(vexpert_company)
app.register_blueprint(vexpert_service)
app.register_blueprint(vexpert_order)
app.register_blueprint(vmember_favorite)
app.register_blueprint(vpartner_favorite)
app.register_blueprint(vfund_favorite)
app.register_blueprint(vmember_advertise)
app.register_blueprint(vmember_web_config_advertise_image)
app.register_blueprint(vmember_web_config_advertise_video)
app.register_blueprint(vpartner_order_edit_attachment)
app.register_blueprint(vfund_review)
app.register_blueprint(vmember_web_config_question_image)
app.register_blueprint(vmember_pin)
app.register_blueprint(vmember_privacy)
app.register_blueprint(vpartner_service_images)
app.register_blueprint(vfund_authentication_check)
app.register_blueprint(vpartner_service_images_image)
app.register_blueprint(vmember_call_expert_service)
app.register_blueprint(vfund_call_expert)
app.register_blueprint(vmember_otp)
app.register_blueprint(vmember_otp_validate)
app.register_blueprint(vpayment_payment)
app.register_blueprint(vmember_notification)
app.register_blueprint(send_email)
app.register_blueprint(vmember_feature)

if __name__ == '__main__':
   app.run(host = "0.0.0.0", port = 5000, debug = True)