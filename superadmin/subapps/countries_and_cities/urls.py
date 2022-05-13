
from django.urls import path
from . import views 

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'countries_and_cities'

# Countries & Cities URLs
urlpatterns = [
    # Unsecured endpoints [used in user registration]
    path('countries/list', views.countries_unsecured.as_view(), name='unsecured_countries'), # Open (Unsecured) Endpoint
    
    # Endpoints to get list to Filter other module objects
    path('filters/countries', views.countries_list_filters_unsecured.as_view(), name='countrieslist'), # Open (Unsecured) Endpoint
    path('filters/cities', views.city_list_filters_unsecured.as_view(), name='citieslist'), # Open (Unsecured) Endpoint

    # Secured endpoints
    path('countries', views.Countries.as_view(), name='countries'),
    path('countries/<int:id>', views.Country.as_view(), name='Country'),
    path('countries/csv', views.CountriesCSV.as_view(), name='CountriesCSV'),

    path('countries/<int:cid>/cities/<str:action>', views.Cities.as_view(), name='cities'),
    path('countries/<int:country>/cities/<int:city>/regions/<str:action>', views.Regions.as_view(), name='Regions'),
    path('countries/<int:country>/cities/<int:city>/regions/<int:region>/areas/<str:action>', views.Areas.as_view(), name='Area'),
]
