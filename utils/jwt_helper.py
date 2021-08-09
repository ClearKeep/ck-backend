import time
import json
from jose import jwk
from jose.jws import verify
from jose.utils import base64url_encode, base64url_decode

class JWTFactory(object):
    def __init__(self):
        # currently do not take any config from outside. This may be change in future
        with open('utils/private_key.pem', 'rb') as key_file:
            self.otp_server_private_key = key_file.read()
        with open('utils/public_key.pem', 'rb') as key_file:
            self.otp_server_public_key = key_file.read()

    def re_signed(self, access_token, modifying_payload={}):
        header_segment, claims_segment, crypto_segment, origin_modified_payload = self._get_new_segment_data(access_token, modifying_payload)
        header = self._load_public_segment(header_segment)
        alg = header.get('alg')
        access_token = self._custom_sign(header_segment, claims_segment, alg)
        return access_token, crypto_segment, origin_modified_payload

    def verify_and_reclaim_access_token(self, access_token, crypto_segment, modifying_payload):
        # simple verify and reclaim access_token
        payload = verify(access_token, self.otp_server_public_key, alg)
        header_segment, claims_segment, crypto_segment, _ = self._get_new_segment_data(access_token, modifying_payload)
        header = self._load_public_segment(header_segment)
        alg = header.get('alg')
        crypto_segment = crypto_segment.encode("utf-8")
        encoded_string = b".".join([encoded_header, encoded_claims, encoded_signature])
        return payload, encoded_string.decode("utf-8")

    def _get_new_segment_data(self, access_token, modifying_payload={}):
        header_segment, claims_segment, signing_input, crypto_segment = self._split_access_token(access_token)

        payload = self._load_public_segment(claims_segment)
        origin_modified_payload = {
            key: payload[key] for key in modifying_payload
        }
        payload.update(modifying_payload)
        claims_segment =  base64url_encode(json.dumps(
                                                payload,
                                                separators=(",", ":"),
                                            ).encode("utf-8")
                                        )
        return header_segment, claims_segment, crypto_segment, origin_modified_payload

    def _split_access_token(self, access_token):
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
