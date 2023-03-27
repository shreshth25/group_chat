import json
import falcon


class JSONTranslator:
    """
    Json Translater
    """
    def process_request(self, req, res):

        if req.content_type and ';' in req.content_type:
            req.content_type = req.content_type.split(';')[0]

        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                raise falcon.HTTPBadRequest('Read Error')
            try:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
                req.context['raw_json'] = raw_json
            except (ValueError, UnicodeDecodeError):
                # No JSON object could be decoded or Malformed JSON
                # Cannot be decoded by utf-8
                raise falcon.HTTPBadRequest("Invalid request")
        else:
            req.context['data'] = None
