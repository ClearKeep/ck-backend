import time
import json
from jose import jwk
from jose.jws import verify
from jose.utils import base64url_encode, base64url_decode
#from utils.config import get_otp_server
with open('configs/private_key.pem', 'rb') as key_file:
    otp_server_private_key = key_file.read()
with open('configs/public_key.pem', 'rb') as key_file:
    otp_server_public_key = key_file.read()

class JWTFactory(object):

    @staticmethod
    def re_signed(access_token):
        header_segment, claims_segment, _, crypto_segment = JWTFactory._get_new_segment_data(access_token)
        header = JWTFactory._load_public_segment(header_segment)
        alg = header.get('alg')
        access_token = JWTFactory._custom_sign(header_segment, claims_segment, alg)
        signature = crypto_segment.decode("utf-8")
        return access_token, signature

    @staticmethod
    def verify_and_reclaim(action_token, original_crypto_segment):
        # simple verify and reclaim access_token
        header_segment, claims_segment, signing_input, crypto_segment = JWTFactory._get_new_segment_data(action_token)
        header = JWTFactory._load_public_segment(header_segment)
        alg = header.get('alg')
        signature = base64url_decode(crypto_segment)
        is_valid_token = JWTFactory._sig_matches_keys(signing_input, signature, alg)
        if not is_valid_token:
            return False, ""
        original_crypto_segment = original_crypto_segment.encode("utf-8")
        access_token = b".".join([header_segment, claims_segment, original_crypto_segment])
        return is_valid_token, access_token.decode("utf-8")

    @staticmethod
    def get_unverified_payload(action_token):
        header_segment, claims_segment, signing_input, crypto_segment = JWTFactory._get_new_segment_data(action_token)
        payload = JWTFactory._load_public_segment(claims_segment)
        return payload

    @staticmethod
    def _get_new_segment_data(access_token):
        access_token = access_token.encode("utf-8")
        signing_input, crypto_segment = access_token.rsplit(b".", 1)
        header_segment, claims_segment = signing_input.split(b".", 1)
        return header_segment, claims_segment, signing_input, crypto_segment

    @staticmethod
    def _load_public_segment(input_segment):
        input_data = base64url_decode(input_segment)
        input_json = json.loads(input_data.decode("utf-8"))
        return input_json

    @staticmethod
    def _custom_sign(encoded_header, encoded_claims, algorithm):
        signing_input = b".".join([encoded_header, encoded_claims])
        key = jwk.construct(otp_server_private_key, algorithm)
        signature = key.sign(signing_input)
        encoded_signature = base64url_encode(signature)
        encoded_string = b".".join([encoded_header, encoded_claims, encoded_signature])
        return encoded_string.decode("utf-8")

    @staticmethod
    def _sig_matches_keys(signing_input, signature, alg):
        # miragate code from jws to here with some simplifying
        key = jwk.construct(otp_server_public_key, alg)
        try:
            if key.verify(signing_input, signature):
                return True
        except Exception:
            # we got exception when cannot verified access_token by any mean. this also mean that access_token is wrong
            pass
        return False
