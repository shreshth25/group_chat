from builtins import Exception
import falcon
from datetime import datetime
from utils.helper import fetchOne
import json
from utils.query import check_if_user_can_like_message_query, already_liked_query, insert_liked_query

class CreateLike:
    """
    Class to like the messages
    """
    def on_post(self, req, resp):
        try:
            session = req.context['session']
            user_id = req.context['user_id']
            data = req.context['data']
            message_id = data['message_id']
            current_datetime = datetime.now()
            if user_id:
                query = check_if_user_can_like_message_query
                params = {'user_id':user_id,'message_id':message_id}
                is_message_valid = fetchOne(session,query, params= params, to_dict=True)
                if is_message_valid:
                    params = {'message_id':message_id, 'user_id': user_id, 'current_datetime':current_datetime}
                    query = already_liked_query
                    already_added = fetchOne(session, query, params=params)
                    if already_added:
                        resp.status = falcon.HTTP_200
                        resp.body = json.dumps({'message':'Already Liked this message'})
                        return

                    query = insert_liked_query
                    params = {'message_id':message_id, 'user_id':user_id, 'current_datetime':current_datetime}
                    session.execute(query, params)
                    resp.status = falcon.HTTP_200
                    resp.body = json.dumps({'message':'Message Liked By you.'})
                else:
                    resp.status = falcon.HTTP_400
                    resp.body = json.dumps({'message':"Message does not belong to you "})
            else:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({'message':"Invalid request"})
        except Exception as e:
            print("Error occured while likeing the messages", str(e))
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'message':"Opps! Something went wrong."})

