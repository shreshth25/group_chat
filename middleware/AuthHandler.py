import falcon
from database.mysql import Session
from utils.helper import fetchOne
from utils.auth import decodeJwt
from utils.query import check_if_logged_out

class AuthHandler:
    def process_request(self, req, resp):
        bypass_list = ['login','faker','health','create_admin']
        url = req.uri.split("/")[-1]
        if url in bypass_list:
            return   
        if req.auth and req.auth != 'null':
            query = check_if_logged_out
            is_blocked = fetchOne(Session, query, params={'token':req.auth})
            if is_blocked:
                raise falcon.HTTPUnauthorized("Your Account is logged out, Please login again")
            token_data = decodeJwt(req.auth)
            if token_data:
                user_id = int(token_data['sub'])
                user_q ='SELECT * FROM users WHERE id={}'.format(user_id)
                udata = fetchOne(Session, user_q, to_dict=True)
                if not udata:
                    raise falcon.HTTPUnauthorized("Your Account does not exist, Please contact admin")
                # setting user in the context
                req.context['user_id'] = udata['id']
                req.context['is_admin'] = udata['is_admin']
            else:
                raise falcon.HTTPUnauthorized("Your session has expired. Kindly logout and login")
        else:
            raise falcon.HTTPUnauthorized("Your session has expired. Kindly logout and login")