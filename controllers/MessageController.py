from builtins import Exception
import falcon
import json
from datetime import datetime

from psutil import users
from utils.helper import fetch, fetchOne

class CreateMessage:
    def on_post(self, req, resp):
        try:
            session = req.context['session']
            user_id = req.context['user_id']
            data = req.context['data']
            group_id = data['group_id']
            message = data['message']
            current_datetime = datetime.now()
            check_groups = """SELECT groups.id from groups where created_by = :user_id and groups.id= :group_id
                                UNION
                                SELECT g.id FROM group_users
                                join groups as g on g.id = group_users.group_id
                                join users as u on u.id = g.created_by
                                where group_users.user_id = :user_id and g.id= :group_id;"""
            is_valid_group = fetchOne(session, check_groups, params={'user_id': user_id, 'group_id': group_id}, to_dict= True)
            if is_valid_group:
                message_insert = """insert into messages 
                (group_id, created_by, message, created_at, updated_at)
                values (:group_id, :user_id, :message, :current_datetime, :current_datetime)"""
                params = {
                    'group_id': group_id,
                    'user_id': user_id,
                    'message': message,
                    'current_datetime': current_datetime
                }
                session.execute(message_insert, params)
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"message":"Message added to the group"})
            else:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({"message":"Not a valid group for this user"})
        except Exception as e:
            print("Unable to add the message to the group", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":"Opps! something went wrong"})
            


class MessageList:
    def on_post(self, req, resp):
        session = req.context['session']
        user_id = req.context['user_id']
        data = req.context['data']
        group_id = data['group_id']
        check_groups = """SELECT groups.id from groups where created_by = :user_id and groups.id= :group_id
                            UNION
                            SELECT g.id FROM group_users
                            join groups as g on g.id = group_users.group_id
                            join users as u on u.id = g.created_by
                            where group_users.user_id = :user_id and g.id= :group_id;"""
        is_valid_group = fetchOne(session, check_groups, params={'user_id': user_id, 'group_id': group_id}, to_dict= True)
        if is_valid_group:
            message_query = """select m.id, m.message, u.name from messages as m
            join users as u on u.id = m.created_by
            where group_id= :group_id"""
            finalData = []
            messages = fetch(session,message_query, params = {'group_id': group_id}, to_dict=True)
            for i in messages:
                query = '''select users.name from likes
                join users on users.id = likes.created_by
                where message_id= :message_id'''
                names = fetch(session, query, params={'message_id':i['id']}, to_dict=True)
                data = {
                    'id': i['id'],
                    'message': i['message'],
                    'created_by':i['name'],
                    'liked_by':names
                }
                finalData.append(data)
            
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({"messages":finalData})

        else:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":"Not a valid group for this user"})
