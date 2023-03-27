import falcon
import json
from datetime import datetime 
from utils.crypt import encrypt_pass
from utils.helper import fetch, fetchOne
from utils.auth import is_admin
from utils.query import all_users_with_roles_query, all_groups_query
from settings import API_KEY

@falcon.before(is_admin)
class CreateUser:

    def __init__(self):
        self.email = None
        self.password = None
        self.name = None
        self.data = []
        self.error = False
        self.errorMssg = ''
        self.session = None

    def on_post(self, req, resp):
        try:
            self.data = req.context['data']
            self.session = req.context['session']

            #getting the data
            status, message = self.parse_data()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return
            
            status , message = self.check_email_alredy_exists()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return

            status, message = self.create_user()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return

            resp.status = falcon.HTTP_200
            resp.body = json.dumps({"message":message})

        except Exception as e:
            print("Error Occured While creating the user", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":"Unable to create the user"})

    
    def parse_data(self):
        """
        Paring and checking the data
        """
        self.name = self.data.get('name')
        self.email = self.data.get('email')
        self.password = self.data.get('password')

        if not self.name or not self.email or not self.password:
            return False, "Email, Password and Name are mandatory"
        return True, ""

    def check_email_alredy_exists(self):
        query = """select * from users where email= :email"""
        params = {'email': self.email}
        is_user = fetchOne(self.session, query, params=params, to_dict=True)
        if is_user:
            return False, f"User {self.email} already exists"
        return True, ""

    def create_user(self):
        try:
            current_datetime = datetime.now()
        
            #encrypting the password
            self.password = encrypt_pass(self.password).decode('ascii')

            query = 'insert into users (email,password,name,created_at,updated_at) values (:email,:password,:name,:current_datetime,:current_datetime)'
            params = {
                'email':self.email,
                'password':self.password,
                'name':self.name,
                'current_datetime':current_datetime
            }
            self.session.execute(query,params)
            return True, f"User {self.email} account created successfully"

        except Exception as e:
            print('Error Occured while saving the user info', str(e))
            return False, "Opps! something went wrong."

@falcon.before(is_admin)
class UpdateUser:
    def on_post(self, req, resp):
        req_data = req.context['data']
        session = req.context['session']
        name = req_data.get('name')
        email = req_data.get('email')
        password = req_data.get('password')
        user_id = req_data.get('user_id')
        current_datetime = datetime.now()
        password = encrypt_pass(password).decode('ascii')
        query = 'insert into users (email,password,name,created_at,updated_at) values (:email,:password,:name,:current_datetime,:current_datetime)'
        params = {
            'email':email,
            'password':password,
            'name':name,
            'current_datetime':current_datetime
        }
        session.execute(query,params)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"message":"Created"})

@falcon.before(is_admin)
class Users:
    """
    Get all users with roles
    """
    def on_get(self, req, resp):
        session = req.context['session']
        query = all_users_with_roles_query
        session = req.context['session']
        users = fetch(session, query, to_dict=True)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'users':users})


@falcon.before(is_admin)
class Groups:
    """
    Get all groups
    """
    def on_get(self, req, resp):
        session = req.context['session']
        query = all_groups_query
        session = req.context['session']
        groups = fetch(session, query, to_dict=True)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'groups':groups})

class CreateAdmin:

    def __init__(self):
        self.email = None
        self.password = None
        self.name = None
        self.data = []
        self.error = False
        self.errorMssg = ''
        self.session = None

    def on_post(self, req, resp):
        try:
            self.data = req.context['data']
            self.session = req.context['session']

            #getting the data
            status, message = self.parse_data()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return
            
            status , message = self.check_email_alredy_exists()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return

            status, message = self.create_user()

            if not status:
                self.error = True
                self.errorMssg = message
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":self.errorMssg})
                return

            resp.status = falcon.HTTP_200
            resp.body = json.dumps({"message":message})

        except Exception as e:
            print("Error Occured While creating the user", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":"Unable to create the user"})

    
    def parse_data(self):
        """
        Paring and checking the data
        """
        self.name = self.data.get('name')
        self.email = self.data.get('email')
        self.password = self.data.get('password')
        self.api_key = self.data.get('api_key')

        if not self.name or not self.email or not self.password or not self.api_key:
            return False, "Email, Password and Name, API key are mandatory"

        if self.api_key!= API_KEY:
            return False, "Invalid API KEY"
        return True, ""

    def check_email_alredy_exists(self):
        query = """select * from users where email= :email"""
        params = {'email': self.email}
        is_user = fetchOne(self.session, query, params=params, to_dict=True)
        if is_user:
            return False, f"User {self.email} already exists"
        return True, ""

    def create_user(self):
        try:
            current_datetime = datetime.now()
        
            #encrypting the password
            self.password = encrypt_pass(self.password).decode('ascii')

            query = 'insert into users (email,password,name,is_admin,created_at,updated_at) values (:email,:password,:name,:is_admin,:current_datetime,:current_datetime)'
            params = {
                'email':self.email,
                'password':self.password,
                'name':self.name,
                'current_datetime':current_datetime,
                'is_admin':1
            }
            self.session.execute(query,params)
            return True, f"Admin {self.email} account created successfully"

        except Exception as e:
            print('Error Occured while saving the user info', str(e))
            return False, "Opps! something went wrong."