from . import methods

def log_db_create_operation(function):
    def wrap(request, *args, **kwargs):
        methods.log_db_operation(request, "CREATE")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap

def log_db_read_operation(function):
    def wrap(request, *args, **kwargs):
        methods.log_db_operation(request, "READ")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap

def log_db_update_operation(function):
    def wrap(request, *args, **kwargs):
        methods.log_db_operation(request, "UPDATE")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap

def log_db_delete_operation(function):
    def wrap(request, *args, **kwargs):
        methods.log_db_operation(request, "DELETE")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap