from builtins import print
import falcon
import json
from datetime import datetime
from utils.auth import create_token
from utils.helper import email_validation, fetch, fetchOne
from utils.crypt import check_pass
from utils.query import logged_out_query

class Login:
    """
    API to check and login the user
    Email and password are required
    """
    def on_get(self, req, resp):
        """
        Get Request For login
        Method not allowed
        """
        data = {"message": "Method not allowed", "status": False}
        resp.status = falcon.HTTP_400
        resp.body = json.dumps(data)
        return

    def on_post(self, req, resp):
        """
        Post Request For login
        Email and password are required
        """
        req_data = req.context["data"]
        session = req.context["session"]
        email = req_data.get('email', None)
        password = req_data.get('password', None)
        
        data = {}
        if email and password:
            if not email_validation(email):
                raise falcon.HTTPBadRequest("Enter a valid email address")
            query = "select * from users where email=:email"
            user = fetchOne(session, query, params={'email':email}, to_dict=True)
            if user:
                try:
                    result = check_pass(password, user['password'])
                except Exception as e:
                    print(str(e))
                    result = False
                if result:
                    jwt = create_token(user['id'])
                    data["access_token"] = jwt
                    resp.body = json.dumps(data)
                    resp.status = falcon.HTTP_200
                else:
                    raise falcon.HTTPBadRequest("Invalid Credentials")
            else:
                raise falcon.HTTPBadRequest("Invalid Credentials")
        else:
            resp.status = falcon.HTTP_422
            resp.body = json.dumps({'message':"Email id and password are required"})


class Logout:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.is_deactivated = 1
        self.errorMessage = 'Opps! Something went wrong.'

    def on_get(self, req, resp):
        try:
            session = req.context["session"]
            user_id = req.context['user_id']
            token = req.auth
            query = logged_out_query
            current_datetime = datetime.now()
            params = {
                'token': token,
                'user_id': user_id,
                'is_deactivated': 1,
                'created_at': current_datetime
            }
            session.execute(query, params = params)
            data = {"message": "Logged out successfully"}
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(data)
            return
        except Exception as e:
            print("Error occured while logging out the user", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'message':self.errorMessage})

    