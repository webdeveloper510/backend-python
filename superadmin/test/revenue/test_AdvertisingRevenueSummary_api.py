import pytest
from django.urls import reverse

url = reverse("superadmin:revenue:AdvertisingRevenueSummary")

def test_getRequest(api_client, country, marketing, city):
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.delete(url)
    assert resp.status_code == 405

    # TIME BASED
    url1 = url + '?type=TIME_BASED&country='+country.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # filter with city
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city='+city.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting last 30 days 
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city='+city.name+ '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    

    # getting last 60 days 
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city='+city.name+ '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    

    # getting data by custome date range
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city='+city.name+ '&first_date=2021-01-01&last_date=2022-02-01'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    # ACCOUNTING BASED
    url1 = url + '?type=ACCOUNTING&country='+country.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # filter with city
    url1 = url + '?type=ACCOUNTING&country='+country.name+'&city='+city.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting last 30 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name+'&city='+city.name+ '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200
    

    # getting last 60 days 
    url1 = url + '?type=ACCOUNTING&country='+country.name+'&city='+city.name+ '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    

    # getting data by custome date range
    url1 = url + '?type=ACCOUNTING&country='+country.name+'&city='+city.name+ '&first_date=2021-01-01&last_date=2022-02-01'
    resp = api_client.get(url1)
    assert resp.status_code == 200




