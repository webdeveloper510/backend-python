from django.shortcuts import render
from django.http import HttpResponse

def test(request):
   html = "<html><body>It is now under testing 15 Final One</body></html>"
   return HttpResponse(html)