import random
import string
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPaginator(LimitOffsetPagination):
    limit_query_param = "perpage"
    default_limit = 25

    def get_paginated_response(self, data,**args):
        res = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'results': data
        }
        if args:
            for key,value in args.items():
                res[key]=value
        return Response(res)


def genarate_rand_sting(length):
    res = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=length))
    return res


def genarate_rand_int(length):
    res = ''.join(random.choices(string.digits, k=length))
    return res


