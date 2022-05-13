import time
from superadmin import models

class LogRequest:
    def __init__(self, get_response):
        self.get_response = get_response

        # List of url's that should be logged, everything else ignored.
        self.prefixs = [
            '',
            # '/example/'
        ]
        
        self.exclude = [
            '/admin/',
            # '/example/'
        ]

    def __call__(self, request):
        _t = time.time() # Calculated execution time.
        response = self.get_response(request) # Get response from view function.
        _t = int((time.time() - _t)*1000)    

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        # (Remove these two lines below to log everything)
        if not list(filter(request.get_full_path().startswith, self.prefixs)): 
            return response 
        
        if list(filter(request.get_full_path().startswith, self.exclude)): 
            return response 

        # print(LogRequest)
        # Create instance of our model and assign values
        request_log = models.LogRequest(endpoint=request.get_full_path(), response_code=response.status_code,method=request.method,
            remote_address=self.get_client_ip(request),
            exec_time=_t,
            body_response=str(response.content),
            body_request=str(request.body)
        )

        # Assign user to log if it's not an anonymous user
        if not request.user.is_anonymous:
            request_log.user = request.user

        # Save log in db
        request_log.save() 
        return response

    # get clients ip address
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            _ip = x_forwarded_for.split(',')[0]
        else:
            _ip = request.META.get('REMOTE_ADDR')
        return _ip