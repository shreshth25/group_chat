import falcon
from falcon_cors import CORS
from falcon_multipart.middleware import MultipartMiddleware
from database.mysql import Session
from middleware.AuthHandler import AuthHandler
from middleware.DatabaseManager import DatabaseManager
from middleware.JSONTranslator import JSONTranslator
from routes.v1_routes import V1Routes
from settings import V1_API_PREFIX

cors = CORS(allow_origins_list=['http://localhost:8080','http://localhost:8081','http://localhost:8000'],
    allow_all_headers=True, allow_all_methods=True)


# Initialize Middleware
middleware = [
    DatabaseManager(Session), AuthHandler(), JSONTranslator(), MultipartMiddleware(), cors.middleware
]

app = falcon.App(middleware=middleware)

# Call logging error Handler if exception occurrs

# Keep query parameters even when they have no corresponding values (aka flags)
app.req_options.keep_blank_qs_values = True

# Automatically parse a www-form-urlencoded POST body & insert into req.params
app.req_options.auto_parse_form_urlencoded = True

# Register API Route To APP
for endpoint, view in V1Routes.items():
    app.add_route(V1_API_PREFIX + endpoint, view)
