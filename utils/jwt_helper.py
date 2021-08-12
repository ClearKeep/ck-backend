import time
import json
from jose import jwk
from jose.jws import verify
from jose.utils import base64url_encode, base64url_decode
#from utils.config import get_otp_server

class JWTFactory(object):
    def __init__(self):
        # currently do not take any config from outside. This may be change in future
        with open('configs/private_key.pem', 'rb') as key_file:
            self.otp_server_private_key = key_file.read()
        with open('configs/public_key.pem', 'rb') as key_file:
            self.otp_server_public_key = key_file.read()

    def re_signed(self, access_token):
        header_segment, claims_segment, _, crypto_segment = self._get_new_segment_data(access_token)
        header = self._load_public_segment(header_segment)
        alg = header.get('alg')
        access_token = self._custom_sign(header_segment, claims_segment, alg)
        signature = crypto_segment.decode("utf-8")
        return access_token, signature

    def verify_and_reclaim(self, action_token, original_crypto_segment):
        # simple verify and reclaim access_token
        header_segment, claims_segment, signing_input, crypto_segment = self._get_new_segment_data(action_token)
        header = self._load_public_segment(header_segment)
        alg = header.get('alg')
        signature = base64url_decode(crypto_segment)
        is_valid_token = self._sig_matches_keys(signing_input, signature, alg)
        if not is_valid_token:
            return False, ""
        original_crypto_segment = original_crypto_segment.encode("utf-8")
        access_token = b".".join([header_segment, claims_segment, original_crypto_segment])
        return is_valid_token, access_token.decode("utf-8")

    def _get_new_segment_data(self, access_token):
        access_token = access_token.encode("utf-8")
        signing_input, crypto_segment = access_token.rsplit(b".", 1)
        header_segment, claims_segment = signing_input.split(b".", 1)
        return header_segment, claims_segment, signing_input, crypto_segment

    def _load_public_segment(self, input_segment):
        input_data = base64url_decode(input_segment)
        input_json = json.loads(input_data.decode("utf-8"))
        return input_json

    def _custom_sign(self, encoded_header, encoded_claims, algorithm):
        signing_input = b".".join([encoded_header, encoded_claims])
        key = jwk.construct(self.otp_server_private_key, algorithm)
        signature = key.sign(signing_input)
        encoded_signature = base64url_encode(signature)
        encoded_string = b".".join([encoded_header, encoded_claims, encoded_signature])
        return encoded_string.decode("utf-8")

    def _sig_matches_keys(self, signing_input, signature, alg):
        key = jwk.construct(self.otp_server_public_key, alg)
        try:
            if key.verify(signing_input, signature):
                return True
        except Exception:
            # we got exception when cannot verified access_token by any mean. this also mean that access_token is wrong
            pass
        return False
