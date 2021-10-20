import smtplib

from utils.config import get_system_config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailerServer(object):
    host = get_system_config()["smtp_server"]['SMTP_HOST']
    port = get_system_config()["smtp_server"]['SMTP_PORT']
    sender = get_system_config()["smtp_server"]['SMTP_SENDER']
    user_name = get_system_config()["smtp_server"]['SMTP_USERNAME']
    password = get_system_config()["smtp_server"]['SMTP_PASSWORD']
    query_string_form = "pre_access_token={}&user_name={}&server_domain={}"
    app_link = "http://www.clearkeep.com/resetpassword"
    text_form = """Your administrator has just requested that you update your Keycloak account by performing the following action(s): Reset Password. Click on the link below to start this process.\n
    {}\n
    This link will expire within 30 days.
    If you are unaware that your administrator has requested this, just ignore this message and nothing will be changed.
    """
    html_form = """
    <p>Your administrator has just requested that you update your Keycloak account by performing the following action(s): Reset Password. Click on the link below to start this process.\n</p>
    <p><a clicktracking=off href="{}">Link to account update</a></p>
    <p>This link will expire within 30 days.</p>
    <p>If you are unaware that your administrator has requested this, just ignore this message and nothing will be changed.</p>
    """

    @staticmethod
    def send_reset_password_mail(receiver_mail, user_name, pre_access_token, server_domain):
        # Email configuration
        deep_link = MailerServer.app_link + '?' + MailerServer.query_string_form.format(user_name, pre_access_token, server_domain)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset Password'
        msg['From'] = MailerServer.sender
        msg['To'] = receiver_mail
        text = MailerServer.text_form.format(deep_link)
        html = MailerServer.html_form.format(deep_link)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(MailerServer.host, MailerServer.port)
        server.ehlo()
        server.starttls()
        server.login(MailerServer.user_name, MailerServer.password)
        server.sendmail(
            MailerServer.sender,
            receiver_mail,
            msg.as_string()
        )
        server.quit()

if __name__ == "__main__":
    MailerServer.send_reset_password_mail("trungdq1@vmodev.com", "trungdq1@vmodev.com", "pre_access_token", "server_domain")
