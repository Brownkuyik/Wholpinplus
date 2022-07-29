from .views import Home_page,About_page, ClothsViews
from django.urls import path
app_name = 'k_store'

urlpatterns = [
    path('',Home_page.as_view(), name='homePage'),
    path('about_us/', About_page, name="about"),
    path('cloths//<slug>/', ClothsViews.as_view(), name='cloths')
]