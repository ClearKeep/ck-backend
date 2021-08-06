import os
import random
import string
import datetime
from twilio.rest import Client
from utils.logger import *

# for testing only

# account_sid = 'AC282f3cc1b6a21094bf363790734daff1'
# auth_token = '9cccf653a58c593f0de2ff39c3440628'
# client = Client(account_sid, auth_token)
# need an option to generate access token and return to user

class OTPServer(object):
    def __init__(self):
        account_sid = 'AC282f3cc1b6a21094bf363790734daff1'
        auth_token = '722879b6fe16ed3c12c0fef65423e421'
        self.client = Client(account_sid, auth_token)
        self.existing_time = 60 # 1 minutes
        self.message_form = 'Your OTP code is {}'
        # set up a phone number for sending
        self.n_number = 6
        self.from_phone = '+15394242840'

    def __call__(self, phone_number):
        otp = self._create_otp()
        logger.info('{} sent to {}'.format(self.message_form.format(otp), phone_number))
        self._otp_message_sending(otp, phone_number)
        return otp

    def _create_otp(self):
        otp = ''.join(random.choices(string.digits, k=self.n_number))
        return otp


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
