import facebook


class Facebook:
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            print("ass is", auth_token)
            graph = facebook.GraphAPI(access_token=auth_token)
            print("graphs os", graph)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            return "The token is invalid or expired."