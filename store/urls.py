from django.urls import path
from .views import *

app_name = 'store'
urlpatterns = [
    path('', Index.as_view(), name='index')
]
