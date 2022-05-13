import pytest
from django.urls import reverse


url = reverse("superadmin:revenue:SubscriptionRevenue")

def test_withoutLogin(api_client, vendor_subscription, country, receipts, city):
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.delete(url)
    assert resp.status_code == 405
    # initial queryparams
    url1 = url + '?type=TIME_BASED&country='+country.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # # with city filter
    url1 = url + '?type=TIME_BASED&country='+country.name + '&city='+ city.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # try with past date random
    url1 = url + '?type=TIME_BASED&country='+country.name + '&city='+ city.name+ '&first_date=2021-07-01&last_date=2021-07-20'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # get 30 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name+ '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # get 60 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name+ '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200


    # initial queryparams
    url1 = url + '?type=ACCOUNTING&country='+country.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # # with city filter
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # try with past date random
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name+ '&first_date=2021-07-01&last_date=2021-07-20'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    
    # get 30 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name+ '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # get 60 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name + '&city='+ city.name+ '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    

