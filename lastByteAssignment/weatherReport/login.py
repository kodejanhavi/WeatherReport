import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import constants
from .models import Admin
from .models import City
from .views import WeatherDetails

class dashboard(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather/dashboard.html'
    def post(self, request):
        if 'username' in request.POST:
            username = request.data.get('username')
            password = request.data.get('password')

            adminrecord = Admin.objects.filter(username=username).first()
            if adminrecord:
                if adminrecord.password == password:
                    city_list = City.objects.values('cityname', 'country')
                    return Response({'city_list': city_list}, status=status.HTTP_200_OK)

            return HttpResponse("User does not exist")
        if 'addcity' in request.POST:
            addcity = request.data.get('addcity')

            try:
                self.getlocationdeatils(self, addcity)
            except KeyError:
                return HttpResponse("invalid_access_key passed to location url")
            except IndexError:
                return HttpResponse("Please enter valid city name or try again")

            city_list = City.objects.values('cityname', 'country')
            return Response({'city_list': city_list}, status=status.HTTP_200_OK)

        if 'deletecity' in request.POST:
            deletecity = request.data.get('deletecity')
            city =  City.objects.filter(cityname=deletecity).first()
            if city:
                City.objects.filter(cityname=deletecity).delete()
                city_list = City.objects.values('cityname', 'country')
                return Response({'city_list': city_list}, status=status.HTTP_200_OK)
            else:
                return HttpResponse("Please enter valid city name")

    def getlocationdeatils(self, cityname):
        citymodel = City.objects.filter(cityname = cityname).first()
        if citymodel :
            return citymodel.country, citymodel.latitude, citymodel.longitude

        locationresponse = requests.get(constants.location_url.format(cityname)).json()
        if "invalid_access_key" in locationresponse:
            raise KeyError
        country = locationresponse["data"][0]["country"]
        lat = locationresponse["data"][0]["latitude"]
        lon = locationresponse["data"][0]["longitude"]
        City.objects.create(cityname=cityname, latitude=float(lat), longitude= float(lon), country=country)
        return country, lat, lon


class adminLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather/adminlogin.html'
    def get(self, request):
        return Response()