import os
import random
import string
import datetime
from twilio.rest import Client
from utils.config import get_otp_server
from utils.logger import *

# for testing only

class OTPServer(object):
    def __init__(self):
        account_sid = get_otp_server()["twilio_account_sid"]
        auth_token =  get_otp_server()["twilio_auth_token"]
        self.client = Client(account_sid, auth_token)
        self.life_time = datetime.timedelta(seconds=get_otp_server()["life_time"])
        self.message_form = 'Your OTP code is {}'
        # set up a phone number for sending
        self.n_number =get_otp_server()["otp_code_length"]
        self.from_phone = get_otp_server()["server_phone_number"]

    def get_otp(self, phone_number):
        otp = self._create_otp()
        logger.info('{} sent to {}'.format(self.message_form.format(otp), phone_number))
        self._otp_message_sending(otp, phone_number)
        return otp

    def _create_otp(self):
        otp = ''.join(random.choices(string.digits, k=self.n_number))
        return otp

    def get_valid_time(self):
        return datetime.datetime.now() + self.life_time

    def _otp_message_sending(self, otp, phone_number):
        try:
            message = self.client.messages.create(
                                      body=self.message_form.format(otp),
                                      from_=self.from_phone,
                                      to=phone_number
                                  )
            return True
        except Exception as e:
            # log e
            return False

    @classmethod
    def create_instance(cls):
        return cls()
