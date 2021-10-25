import smtplib

from utils.config import get_system_config

import email.header
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def format_addresses(addresses, header_name=None, charset='iso-8859-1'):
    """This is an extension of email.utils.formataddr.
       Function expect a list of addresses [ ('name', 'name@domain'), ...].
       The len(header_name) is used to limit first line length.
       The function mix the use Header(), formataddr() and check for 'us-ascii'
       string to have valid and friendly 'address' header.
       If one 'name' is not unicode string, then it must encoded using 'charset',
       Header will use 'charset' to decode it.
       Unicode string will be encoded following the "Header" rules : (
       try first using ascii, then 'charset', then 'uft8')
       'name@address' is supposed to be pure us-ascii, it can be unicode
       string or not (but cannot contains non us-ascii)

       In short Header() ignore syntax rules about 'address' field,
       and formataddr() ignore encoding of non us-ascci chars.
    """
    header=email.header.Header(charset=charset, header_name=header_name)
    for i, (name, addr) in enumerate(addresses):
        if i!=0:
            # add separator between addresses
            header.append(',', charset='us-ascii')
        # check if address name is a unicode or byte string in "pure" us-ascii
        try:
            if isinstance(name, str):
                # convert name in byte string
                name.encode('us-ascii')
            else:
                # check id byte string contains only us-ascii chars
                name=name.decode('us-ascii')
        except UnicodeError:
            # Header will use "RFC2047" to encode the address name
            # if name is byte string, charset will be used to decode it first
            header.append(name)
            # here us-ascii must be used and not default 'charset'
            header.append('<%s>' % (addr,), charset='us-ascii')
        else:
            # name is a us-ascii byte string, i can use formataddr
            formated_addr=email.utils.formataddr((name, addr))
            # us-ascii must be used and not default 'charset'
            header.append(formated_addr, charset='us-ascii')

    return header

class MailerServer(object):
    host = get_system_config()["smtp_server"]['SMTP_HOST']
    port = get_system_config()["smtp_server"]['SMTP_PORT']
    sender_display_name = "ClearKeep"
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
        deep_link = MailerServer.app_link + '?' + MailerServer.query_string_form.format(pre_access_token, user_name, server_domain)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset Password'
        msg['From'] = format_addresses([(MailerServer.sender_display_name, MailerServer.sender)], header_name='from')
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
