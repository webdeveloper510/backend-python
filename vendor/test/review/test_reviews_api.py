# import pytest
# from django.urls import reverse
# import datetime

# url = reverse('vendor:activity_management:reviews')


# def test_getRequest(api_client, review, vendor, city):
#     resp = api_client.get(url)
#     assert resp.status_code == 200
#     assert len(resp.data['data']) == 1
#     data = resp.data['data'][0]
#     assert data['review'] == 'some random reviews'
#     assert data['ratings'] == 5

#     assert resp.data['stars']['5'] == 1
#     assert resp.data['stars']['4'] == 0
#     assert resp.data['stars']['3'] == 0
#     assert resp.data['stars']['2'] == 0
#     assert resp.data['stars']['1'] == 0
#     assert resp.data['stars']['over_all'] == 5

#     query_url = url + '?perpage=1'
#     resp = api_client.get(query_url)
#     assert resp.status_code == 200
#     data = resp.data['results']
#     result = data['stars']
#     data = data['data'][0]
#     assert data['review'] == 'some random reviews'
#     assert data['ratings'] == 5

#     assert result['5'] == 1
#     assert result['4'] == 0
#     assert result['3'] == 0
#     assert result['2'] == 0
#     assert result['1'] == 0
#     assert result['over_all'] == 5
#     today = datetime.datetime.now()
#     tomorrow = today + datetime.timedelta(days=1)
#     tomorrow = tomorrow.strftime("%Y-%m-%d")
#     yesterday = today - datetime.timedelta(days=1)
#     yesterday = yesterday.strftime("%Y-%m-%d")
#     query_url = url + '?vendor_code={0}&city={1}&first_date={2}&last_date={3}&perpage=1&vendor_name={4}'.format(
#         vendor.vendor_code, city.name, yesterday, tomorrow, vendor.name)
#     resp = api_client.get(query_url)
#     assert resp.status_code == 200
#     data = resp.data['results']
#     result = data['stars']
#     data = data['data'][0]
#     assert data['review'] == 'some random reviews'
#     assert data['ratings'] == 5

#     assert result['5'] == 1
#     assert result['4'] == 0
#     assert result['3'] == 0
#     assert result['2'] == 0
#     assert result['1'] == 0
#     assert result['over_all'] == 5


# def test_postRequest(api_client, user, vendor, city, activity, userDetails):
#     data = {
#         'review': 'Test review', 'ratings': 5,
#         'activity': activity.id,

#     }
#     resp = api_client.post(url, data=data, format='json')
#     assert resp.status_code == 201
#     resp_data = resp.data
#     assert resp_data['review'] == data['review']
#     assert resp_data['ratings'] == data['ratings']
#     assert resp_data['response'] == ''
#     assert resp_data['activity'] == activity.id
#     assert resp_data['status'] == 'ACTIVE'
#     assert resp_data['vendor_name'] == vendor.name
#     assert resp_data['vendor_code'] == vendor.vendor_code
#     assert resp_data['country'] == city.country.name
#     assert resp_data['activity_title'] == activity.title
#     assert resp_data['activity_code'] == activity.code
#     assert resp_data['user_name'] == None
#     assert resp_data['user_id'] == None

#     api_client.force_authenticate(user)
#     resp = api_client.post(url, data=data, format='json')
#     assert resp.status_code == 201
#     resp_data = resp.data
#     print(resp_data)
#     assert resp_data['review'] == data['review']
#     assert resp_data['ratings'] == data['ratings']
#     assert resp_data['response'] == ''
#     assert resp_data['activity'] == activity.id
#     assert resp_data['status'] == 'ACTIVE'
#     assert resp_data['vendor_name'] == vendor.name
#     assert resp_data['vendor_code'] == vendor.vendor_code
#     assert resp_data['country'] == city.country.name
#     assert resp_data['activity_title'] == activity.title
#     assert resp_data['activity_code'] == activity.code
#     assert resp_data['user_name'] == ''
#     assert resp_data['user_id'] == userDetails.userdetails.code

# # pytest test_reviews_api.py -s
