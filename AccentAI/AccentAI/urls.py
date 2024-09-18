"""
URL configuration for AccentAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ANN import views
from ANN.views import *
from ANN.views import receive_data
#from . import views

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('',index),
    path('data/',views.receive_data, name='receive_data'),
  #  path('process_transcript/', process_transcript,name='process_transcript'),
 #   path('submit-transcript/', views.submit_transcript, name='submit-transcript'),
#    path('receive-data/', receive_data, name='receive_data'),
#    path('send-transcript/', views.send_transcript_to_server, name='send_transcript')
]
