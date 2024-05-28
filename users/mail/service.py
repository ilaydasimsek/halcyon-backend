from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings


class MailService:
    _client = SendGridAPIClient(settings.SENDGRID['API_KEY'])
    @staticmethod
    def send_reset_password_mail(email, code):
        message = Mail(
            from_email='info@halcyon.yoga',
            to_emails=email
        )
        message.template_id = settings.SENDGRID['TEMPLATE_ID']
        message.dynamic_template_data = dict(code=code)
        return MailService._client.send(message)

