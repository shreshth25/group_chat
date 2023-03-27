from builtins import Exception
import falcon
import json
from datetime import datetime
from utils.helper import fetch, fetchOne
from utils.query import user_list_query, create_group_query, user_group_query, user_group_search_query

class CreateGroup:
    def on_post(self, req, resp):
        try:
            session = req.context['session']
            user_id = req.context['user_id']
            data = req.context['data']
            group_name = data['name']
            current_datetime = datetime.now()
            query = create_group_query
            params = {
                'name': group_name,
                'created_by': user_id,
                'current_datetime':current_datetime
            }
            session.execute(query, params = params)
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({"message":f"Group {group_name} created successfully"})
        except Exception as e:
            print("Something went wrong while creating user", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":"Opps! Something went wrong"})


class GroupList:
    def on_get(self, req, resp):
        session = req.context['session']
        user_id = req.context['user_id']
        group_query = user_group_query
        chat_groups = fetch(session, group_query, params={'user_id':user_id}, to_dict=True)
        finalData = []
        for group in chat_groups:
            user_query = """
            select u.name, u.id from group_users as gu 
            join users as u on u.id = gu.user_id where group_id= :group_id"""
            users = fetch(session, user_query, params = {'group_id': group['id']}, to_dict=True)
            data = {
                'group_name': group['name'],
                'group_id':group['id'],
                'created_by':group['creator'],
                'created_at': str(group['created_at']),
                'users': users
            }
            finalData.append(data)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"message":finalData})

    
class UsersList:
    """
    Get users list
    """
    def on_post(self, req, resp):
        try:
            session = req.context['session']
            user_id = req.context['user_id']
            if user_id:
                query = user_list_query
                users = fetch(session, query, params={'id':user_id}, to_dict=True)
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"Users":users})
        except Exception as e:
            print("Error Occured while fetching the list", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({"message":'Opps! Something went wrong'})


class AddUser:
    def on_post(self, req, resp):
        session = req.context['session']
        user_id = req.context['user_id']
        data = req.context['data']
        add_user = data['add_user']
        group_id = data['group_id']
        current_datetime = datetime.now()
        if user_id:
            query = "select id from chat_groups where id= :group_id and created_by= :user_id"
            is_group = fetchOne(session,query, params={'group_id':group_id,'user_id':user_id}, to_dict=True)
            if is_group:
                params = {'group_id':group_id, 'user_id': add_user, 'current_datetime':current_datetime}
                already_added_query = "select id from group_users where group_id= :group_id and user_id= :user_id"
                already_added = fetchOne(session, already_added_query, params=params)
                if already_added:
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps({'message':'Already Added in group'})
                    return

                query = "Insert into group_users (group_id, user_id, created_at, updated_at) values (:group_id, :user_id, :current_datetime,:current_datetime)"
                params = {'group_id':group_id, 'user_id':add_user, 'current_datetime':current_datetime}
                session.execute(query, params)
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({'message':'User successfully Added'})
            else:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({'message':"No group is there"})
        else:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'message':"No user id"})


class SearchGroup:
    def on_get(self, req, resp):
        session = req.context['session']
        user_id = req.context['user_id']
        data = req.context['data']
        search = req.params['search']
        group_query = user_group_search_query
        query = group_query.format(user_id, search, user_id, search)
        chat_groups = fetch(session, query, to_dict=True)
        finalData = []
        for group in chat_groups:
            user_query = """
            select u.name, u.id from group_users as gu 
            join users as u on u.id = gu.user_id where group_id= :group_id"""
            users = fetch(session, user_query, params = {'group_id': group['id']}, to_dict=True)
            data = {
                'group_name': group['name'],
                'group_id':group['id'],
                'created_by':group['creator'],
                'created_at': str(group['created_at']),
                'users': users
            }
            finalData.append(data)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"message":finalData})

class DeleteGroup:
    def on_get(self, req, resp):
        session = req.context['session']
        user_id = req.context['user_id']
        data = req.context['data']
        search = req.params['search']
        group_query = user_group_search_query
        query = group_query.format(user_id, search, user_id, search)
        chat_groups = fetch(session, query, to_dict=True)
        finalData = []
        for group in chat_groups:
            user_query = """
            select u.name, u.id from group_users as gu 
            join users as u on u.id = gu.user_id where group_id= :group_id"""
            users = fetch(session, user_query, params = {'group_id': group['id']}, to_dict=True)
            data = {
                'group_name': group['name'],
                'group_id':group['id'],
                'created_by':group['creator'],
                'created_at': str(group['created_at']),
                'users': users
            }
            finalData.append(data)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"message":finalData})
