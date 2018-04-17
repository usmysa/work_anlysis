
from django.urls import path
from plot_maps import views

app_name = 'plot_maps'
urlpatterns = [
	path('/', views.maps), 
]