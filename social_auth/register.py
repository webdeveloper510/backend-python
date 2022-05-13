from django.contrib.auth import authenticate
from authentication.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import UserProfile
from superadmin.subapps.countries_and_cities.models import Country, City


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            if provider== 'google' :
                registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))
                print("hello",email)
            else :
                registered_user = authenticate(
                    email=email, password=os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY'))
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        if provider == 'google':
            user = {
            'username': generate_username(name), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        else:
            user = {
                'username': generate_username(name), 'email': email,
                'password': os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')}

        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        country = Country.objects.order_by('name')[0]
        city = City.objects.order_by('name')[0]
        userdetails = UserProfile.objects.create(user=user, firstname=name,
                                                 role='CUSTOMER',
                                                   lastname='', country=country , city=city)
        userdetails.save()
        print("******************************************** coming here")
        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }