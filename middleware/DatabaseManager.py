class DatabaseManager(object):
    def __init__(self, session):
        self.session = session

    def process_request(self, req, res, resource=None):
        req.context["session"] = self.session

    def process_response(self, req, resp, resource, req_succeeded):
        pass