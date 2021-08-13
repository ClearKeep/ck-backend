import os
import random
import string
import datetime
from hashlib import md5
from hmac import compare_digest as compare_hash
from twilio.rest import Client
from utils.config import get_otp_server
from utils.logger import *

account_sid = get_otp_server()["twilio_account_sid"]
auth_token =  get_otp_server()["twilio_auth_token"]
client = Client(account_sid, auth_token)
life_time = datetime.timedelta(seconds=get_otp_server()["life_time"])
message_form = 'Your OTP code is {}'
# set up a phone number for sending
code_length = get_otp_server()["otp_code_length"]
from_phone = get_otp_server()["server_phone_number"]
secret_key = get_otp_server()["otp_secret_key"]

class OTPServer(object):

    @staticmethod
    def get_otp(phone_number):
        otp = OTPServer._create_otp()
        logger.info('{} sent to {}'.format(message_form.format(otp), phone_number))
        OTPServer._otp_message_sending(otp, phone_number)
        return otp

    @staticmethod
    def _create_otp():
        otp = ''.join(random.choices(string.digits, k=code_length))
        return otp

    @staticmethod
    def get_valid_time():
        return datetime.datetime.now() + life_time

    @staticmethod
    def hash_uid(user_id):
        secret_string = user_id + secret_key
        hash_string = md5(secret_string.encode("utf-8")).hexdigest()
        return hash_string

    @staticmethod
    def verify_hash_code(user_id, hash_string):
        verify_secret_string = user_id + secret_key
        verify_hash_string = md5(verify_secret_string.encode("utf-8")).hexdigest()
        return compare_hash(verify_hash_string, hash_string)

    @staticmethod
    def _otp_message_sending(otp, phone_number):
        try:
            message = client.messages.create(
                                      body=message_form.format(otp),
                                      from_=from_phone,
                                      to=phone_number
                                  )
            return True
        except Exception as e:
            # log e
            return False
