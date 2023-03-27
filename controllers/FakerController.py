import falcon
from datetime import datetime
import json
from utils.crypt import encrypt_pass

class Faker():
    def on_get(self, req, resp):
        session = req.context['session']
        current_datetime = datetime.now()
        users = [{
            "name": "Inge",
            "email": "iruddin0@etsy.com",
            "password": "pqNzdqB8Up4"
            }, {
            "name": "Angela",
            "email": "adibiagio1@mozilla.com",
            "password": "6Vgq6e4"
            }, {
            "name": "Heidi",
            "email": "hsalery2@epa.gov",
            "password": "lfCP4Du"
            }, {
            "name": "Nissy",
            "email": "npiegrome3@china.com.cn",
            "password": "5BxrIZBrX"
            }, {
            "name": "Valry",
            "email": "vbromont4@hc360.com",
            "password": "tULbeM"
            }, {
            "name": "Frans",
            "email": "fjakov5@digg.com",
            "password": "3GmNEjZ8"
            }, {
            "name": "Carter",
            "email": "chabert6@technorati.com",
            "password": "myziIbg"
            }, {
            "name": "Margie",
            "email": "mbrandt7@oaic.gov.au",
            "password": "O8KsKokKVmy"
            }, {
            "name": "Raynell",
            "email": "rzelley8@spiegel.de",
            "password": "bNqucQ"
            }, {
            "name": "Odelle",
            "email": "obutterick9@pinterest.com",
            "password": "7HhkjX5rDjJ9"
        }]

        for i in users:
            query = 'insert into users (email,password,name,created_at,updated_at) values (:email,:password,:name,:current_datetime,:current_datetime)'
            password = encrypt_pass(i['password']).decode('ascii')
            params = {
                'email':i['email'],
                'password': password,
                'name':i['name'],
                'current_datetime':current_datetime
            }
            session.execute(query,params)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message':'Done'})

