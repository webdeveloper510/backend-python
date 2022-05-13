# import pytest
# from django.urls import reverse

# url = reverse('vendor:activity_management:review', kwargs={'id': 1})


# def test_getRequest(api_client,  review, vendor, city, activity):
#     resp = api_client.get(url)
#     assert resp.status_code == 200
#     resp_data = resp.data
#     assert resp_data['review'] == review.review
#     assert resp_data['ratings'] == review.ratings
#     assert resp_data['activity'] == 1
#     assert resp_data['status'] == 'ACTIVE'
#     assert resp_data['vendor_name'] == vendor.name
#     assert resp_data['vendor_code'] == vendor.vendor_code
#     assert resp_data['country'] == city.country.name
#     assert resp_data['activity_title'] == activity.title
#     assert resp_data['activity_code'] == activity.code


# def test_postRequest(api_client, db):
#     resp = api_client.post(url)
#     assert resp.status_code == 405


# def test_putRequest(api_client, db):
#     resp = api_client.put(url)
#     assert resp.status_code == 405


# def test_patchRequest(api_client, review, vendor, city, activity):
#     data = {
#         'response': 'Response of vendor'
#     }
#     resp = api_client.patch(url, data=data, format='json')
#     assert resp.status_code == 200
#     assert resp.data['response'] == data['response']


# def test_deleteRequest(api_client, review, vendor, city, activity):
#     resp = api_client.delete(url)
#     assert resp.status_code == 200


# # pytest test_review_api.py -s
