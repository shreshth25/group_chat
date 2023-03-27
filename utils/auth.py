import jwt
import settings
import falcon
from datetime import datetime, timedelta

def decodeJwt(encoded, verify=True):
    options = {'verify_aud': False, 'require_sub': True}
    try:
        try:
            return jwt.decode(encoded, settings.SECRET_KEY, verify=verify, algorithms=['HS256'], options=options)
        except:
            raise falcon.HTTPUnauthorized("Your session has expired.Kindly logout and login")
    except jwt.ExpiredSignatureError as e:
        raise falcon.HTTPUnauthorized("Token Expired")

def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "iat": datetime.now(),
        "exp": datetime.now() + timedelta(int(settings.JWT_EXPIRY_DAY))}
        
    # decode jwt to convert into string
    decodedJwt = encodeJwt(payload)
    encodedJwt = decodedJwt.decode("utf-8")
    return encodedJwt

def encodeJwt(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def is_admin(req, resp, resource, *args):
    if not req.context['is_admin']:
        raise falcon.HTTPUnauthorized("You need admin access for this activity")