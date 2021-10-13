import smtplib

from utils.config import get_system_config

from email.message import EmailMessage
# sender = 'from@fromdomain.com'
# receivers = ['to@todomain.com']
#
message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
MIME-Version: 1.0
Content-type: text/html
Subject: SMTP HTML e-mail test

This is an e-mail message to be sent in HTML format

<b>This is HTML message.</b>
<h1>This is headline.</h1>
"""

# try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message)
#    print "Successfully sent email"
# except SMTPException:
#    print "Error: unable to send email"

class MailerServer(object):
    query_string_form = "pre_access_token={}&user_id={}&server_domain={}"
    app_link = "clearkeep://resetpassword"
    user_name = "apikey"
    sender = get_system_config()["smtp_server"]['SMTP_SENDER']
    password = get_system_config()["smtp_server"]['SMTP_PASSWORD']
    host = get_system_config()["smtp_server"]['SMTP_HOST']
    port = get_system_config()["smtp_server"]['SMTP_PORT']
    message_form = """
    <b>This is HTML message.</b>
    <h1>This is headline.</h1>
    <p><a href="{}">deep_link testing</p>
    """

    @staticmethod
    def send_reset_password_mail(receiver_mail, user_id, pre_access_token, server_domain):
        # Email configuration
        deep_link = MailerServer.app_link + '?' + MailerServer.query_string_form.format(user_id, pre_access_token, server_domain)
        message = MailerServer.message_form.format(deep_link)
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Reset Password'
        msg['From'] = MailerServer.sender
        msg['To'] = receiver_mail

        print(str(msg))
        print(MailerServer.host, MailerServer.port)
        #host = smtp.sendgrid.net
        #port = 465
        # Start TLS and send email
        server = smtplib.SMTP(MailerServer.host, MailerServer.port)
        print(1)
        server.ehlo()
        print(2)
        server.starttls()
        print(3)
        server.login(MailerServer.user_name, MailerServer.password)
        print(message)
        server.sendmail(
            MailerServer.sender,
            receiver_mail,
            str(msg)
        )
        server.quit()
