from django.contrib.sites import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import constants
from .models import Admin, City


class AddCityView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather/landingPage.html'
    def post(self, request):
        city = request.data.get('city')
        locationresponse = requests.get(constants.location_url.format(city)).json()
        if "invalid_access_key" in locationresponse:
            return HttpResponse("invalid_access_key passed to location url")
        country = locationresponse["data"][0]["country"]
        lat = locationresponse["data"][0]["latitude"]
        lon = locationresponse["data"][0]["longitude"]
        City.objects.create(cityname=city, latitude=float(lat), longitude=float(lon), country=country)
        return HttpResponse("city added")

