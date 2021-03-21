from django.http import HttpResponse
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import City
import datetime
from weatherReport import constants

class landingView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather/landingPage.html'
    def get(self, request):
        # logic of view will be implemented here
        city_list = City.objects.values('cityname')
        return Response({'city_list': city_list}, status=status.HTTP_200_OK)

class WeatherDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'weather/weatherBootstrap.html'

    def get(self, request):
        city = request.query_params.get('name')

        try:
            country, lat, lon = self.getlocationdeatils(city)
        except KeyError:
            return HttpResponse("invalid_access_key passed to location url")
        except NameError:
            return HttpResponse("Please contact admin to add this city")

        weatherresponse = requests.get(constants.weather_url.format(lat,lon)).json()

        if "cod" in weatherresponse:
            return HttpResponse("invalid_access_key passed to weather url")
        city_weather = self.createweatherresponse(city, country, weatherresponse)
        city_list = City.objects.values('cityname')

        context = {'city_weather' : city_weather, 'city_list': city_list}

        return Response (context, status=status.HTTP_200_OK)

    def createweatherresponse(self, city, country, weatherresponse):
        daily = weatherresponse["daily"]
        dailylist = []

        for dailyweather in range(1, len(daily)):
            day = {}
            day["daytemp"] = daily[dailyweather]["temp"]["day"]
            day["description"] = daily[dailyweather]["weather"][0]["description"]
            day["icon"] = daily[dailyweather]["weather"][0]["icon"]
            day["weekday"] = datetime.datetime.fromtimestamp(daily[dailyweather]["dt"]).strftime('%a')
            day["daymonth"] = datetime.datetime.fromtimestamp(daily[dailyweather]["dt"]).strftime('%d %b')
            dailylist.append(day)

        city_weather = {
            'city': city,
            'country': country,
            'weekday': datetime.datetime.fromtimestamp(weatherresponse["current"]["dt"]).strftime('%A'),
            'daydate': datetime.datetime.fromtimestamp(weatherresponse["current"]["dt"]).strftime('%d %b, %Y'),
            'temperature': weatherresponse["current"]["temp"],
            'description': weatherresponse["current"]["weather"][0]["description"],
            'icon': weatherresponse["current"]["weather"][0]["icon"],
            'daily': dailylist
        }
        return city_weather

    def getlocationdeatils(self, cityname):
        citymodel = City.objects.filter(cityname = cityname).first()
        if citymodel :
            return citymodel.country, citymodel.latitude, citymodel.longitude

        else:
            raise NameError
