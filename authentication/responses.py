# HTTP Responses
def create_response_dict(success, message, code=None):
    resp = {}
    if(success):
        resp['success'] = success
    if(message):
        resp['message'] = message
    if(code):
        resp['code'] = code
    return resp


RESP_NOT_FOUND = create_response_dict(False, "object not found")
RESP_INTERNAL_SERVER_ERROR = create_response_dict(False, "unexpected error occured at server")
RESP_BAD_REQUEST =create_response_dict(False, "bad request")

# Operational Responses
def create_success_response(message):
    resp = {}
    resp['success'] = True
    resp['message'] = message
    return resp

def create_failure_response(message):
    resp = {}
    resp['success'] = False
    resp['message'] = message
    return resp

