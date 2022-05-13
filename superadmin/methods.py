from . import models

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
 
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_db_operation(request, type):
    route = request.path
    ip = visitor_ip_address(request)
    models.DBOperation.objects.create(user=request.user, route=route, ip_address=ip, op_type=type)
