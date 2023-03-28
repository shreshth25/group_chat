import unittest
import requests
import settings
import json
from utils.test_helper import email_generator
import random


class TestAPI(unittest.TestCase):
    """
    Test cases
    """
    admin_email = email_generator()
    user_email = email_generator()

    def _init_(self):
        self.token = ''
        self.admin_email = ''

    def get_admin_token(self):
        data = {
            'email': self.admin_email,
            'password': '1234'
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response_login_check = requests.post(settings.APP_URL+'login', data = json.dumps(data), headers=headers)
        data = response_login_check.json()
        if data:
            self.token = data.get('access_token','')
            return self.token

    def get_user_token(self):
        data = {
            'email': self.user_email,
            'password': '1234'
        }
        headers = {
            'Content-Type': 'application/json',
        }
        response_login_check = requests.post(settings.APP_URL+'login', data = json.dumps(data), headers=headers)
        data = response_login_check.json()
        if data:
            self.token = data.get('access_token','')
            return self.token

    def test_a_health_check(self):
        print("test a: Check health of application")
        response_health_check = requests.get(settings.APP_URL+'health')
        self.assertEqual(response_health_check.status_code, 200)

    def test_b_create_admin(self):
        print("test b: check create admin")
        data = {
            'email':self.admin_email,
            'password':'1234',
            'name':'Admin',
            'api_key': settings.API_KEY
        }
        headers = {
        'Content-Type': 'application/json',
        }
        response_login_check = requests.post(settings.APP_URL+'admin/create-admin', data = json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)
    
    def test_c_login(self):
        print("test c: check admin login")
        data = {
            'email':self.admin_email,
            'password':'1234'
        }
        headers = {
        'Content-Type': 'application/json',
        }
        response_login_check = requests.post(settings.APP_URL+'login', data = json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)
    
    def test_d_users_list(self):
        print("test d: check users list")
        token = self.get_admin_token()
        headers = {
            'Authorization': token
        }
        users_list = requests.get(settings.APP_URL+'admin/get-users', headers=headers)
        self.assertEqual(users_list.status_code, 200)

    def test_e_get_chat_groups(self):
        print("test e: check chat groups")
        token = self.get_admin_token()
        headers = {
            'Authorization': token
        }
        users_list = requests.get(settings.APP_URL+'admin/get-chat-groups', headers=headers)
        self.assertEqual(users_list.status_code, 200)

    def test_f_create_user(self):
        print("test f: Check create user")
        token = self.get_admin_token()
        data = {
            'email': self.user_email,
            'password':'1234',
            'name':'User'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        response_login_check = requests.post(settings.APP_URL+'admin/create-user', data = json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)

    def test_g_user_login(self):
        print("test g: Check user login")
        data = {
            'email':self.user_email,
            'password':'1234'
        }
        headers = {
        'Content-Type': 'application/json',
        }
        response_login_check = requests.post(settings.APP_URL+'login', data = json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)

    def test_h_create_group(self):
        print("test h: Check create group")
        token = self.get_user_token()
        data = {
            'name':"Test"+str(random.randint(10,10000)),
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        response_login_check = requests.post(settings.APP_URL+'create-group', data = json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)

    def test_i_get_user_chat_groups(self):
        print("test i: check user chat groups")
        token = self.get_user_token()
        headers = {
            'Authorization': token
        }
        response_login_check = requests.get(settings.APP_URL+'chat-groups-list', headers=headers)
        self.assertEqual(response_login_check.status_code, 200)

    def test_j_search_chat_groups(self):
        print("test j: Check search chat group")
        token = self.get_user_token()
        params = {
            'search':'Te'
        }
        headers = {
            'Authorization': token
        }
        response_login_check = requests.get(settings.APP_URL+'search-group',params=params, headers=headers)
        self.assertEqual(response_login_check.status_code, 200)

    def test_k_get_users(self):        
        print("test k: Check get users")
        token = self.get_user_token()
        headers = {
            'Authorization': token
        }
        users_list = requests.post(settings.APP_URL+'users-list', headers=headers)
        self.assertEqual(users_list.status_code, 200)

    def test_l_add_chat_groups(self):
        print("test l: Check add chat group")
        token = self.get_user_token()
        headers = {
            'Authorization': token
        }
        users_list = requests.post(settings.APP_URL+'users-list', headers=headers)
        users = users_list.json()
        user_id = users['Users'][0]['id']
        response_login_check = requests.get(settings.APP_URL+'chat-groups-list', headers=headers)
        chat_groups = (response_login_check.json())
        group_id = chat_groups['message'][0]['group_id']
        data = {
            'group_id':group_id,
            'add_user': user_id,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        response_login_check = requests.post(settings.APP_URL+'add-user', data=json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)
    
    def test_m_add_message(self):
        print("test m: Check add message to group")
        token = self.get_user_token()
        headers = {
            'Authorization': token
        }
        response_login_check = requests.get(settings.APP_URL+'chat-groups-list', headers=headers)
        chat_groups = (response_login_check.json())
        group_id = chat_groups['message'][0]['group_id']
        data = {
            'group_id':group_id,
            'message': 'Text Message',
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }
        response_login_check = requests.post(settings.APP_URL+'create-message', data=json.dumps(data), headers=headers)
        self.assertEqual(response_login_check.status_code, 200)
    

    

if __name__ == '__main__':
    unittest.main()