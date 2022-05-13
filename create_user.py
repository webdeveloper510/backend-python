#!/usr/bin/env python
"""Creating user for administrative purpose"""
from django.contrib.auth import get_user_model

# see ref. below
UserModel = get_user_model()

if not UserModel.objects.filter(username='admin').exists():
    user = UserModel.objects.create_user(
        username='admin', password='MoppeTt0-222', email='info@moppetto.com')
    user.is_superuser = True
    user.is_staff = True
    user.save()
