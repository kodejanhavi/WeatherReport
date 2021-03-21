from django.urls import path
from .login import dashboard, adminLogin
from .views import WeatherDetails , landingView

urlpatterns = [
    path('', landingView.as_view(), name='landing_view'),
    path('weather/', WeatherDetails.as_view(), name='weather_view'),
    path('custom_admin/dashboard/', dashboard.as_view(), name='admin_dashboard_view'),
    path('custom_admin/login/', adminLogin.as_view(), name='admin_login_view'),
]
