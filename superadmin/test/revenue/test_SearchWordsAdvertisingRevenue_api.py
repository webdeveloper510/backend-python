import pytest
from django.urls import reverse
from decimal import Decimal

from authentication import responses
url = reverse("superadmin:revenue:SearchWordsAdvertisingRevenue")



# pytest test_SearchWordsAdvertisingRevenue_api.py -s
def test_requesting(api_client, country, searchWords, city):
    resp = api_client.post(url)
    assert resp.status_code == 405

    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405

    url1 = url + '?type=TIME_BASED&country='+country.name
    resp = api_client.get(url1)
    assert resp.status_code == 200
    responses = [{'word_count': 5, 'gross_revenue': Decimal('3650.00'), 'tax': Decimal('71.568627450980392156862745'), 'net_revenue': Decimal('3578.431372549019607843137255'), 'number_of_unique_vendors': 1, 'average_revenue_per_day': 3650}, {
        'word_count': 9, 'gross_revenue': Decimal('7300.00'), 'tax': Decimal('143.137254901960784313725490'), 'net_revenue': Decimal('7156.862745098039215686274510'), 'number_of_unique_vendors': 2, 'average_revenue_per_day': 3650}]
    assert responses == resp.data

    # filter with city
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city='+city.name
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting last 30 days
    url1 = url + '?type=TIME_BASED&country='+country.name + \
        '&city='+city.name + '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting last 60 days
    url1 = url + '?type=TIME_BASED&country='+country.name + \
        '&city='+city.name + '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting data by custome date range
    url1 = url + '?type=TIME_BASED&country='+country.name+'&city=' + \
        city.name + '&first_date=2021-01-01&last_date=2022-02-01'
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
    url1 = url + '?type=ACCOUNTING&country='+country.name + \
        '&city='+city.name + '&day=last_thirty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting last 60 days
    url1 = url + '?type=ACCOUNTING&country='+country.name + \
        '&city='+city.name + '&day=last_sixty_day'
    resp = api_client.get(url1)
    assert resp.status_code == 200

    # getting data by custome date range
    url1 = url + '?type=ACCOUNTING&country='+country.name+'&city=' + \
        city.name + '&first_date=2021-01-01&last_date=2022-02-01'
    resp = api_client.get(url1)
    assert resp.status_code == 200
