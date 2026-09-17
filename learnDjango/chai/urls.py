
from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_chai, name='all_chai'),
    path('<int:chai_id>/', views.chai_detail, name='chai_detail'),
    path('store_detail/', views.store_detail, name='store_detail'),
    path('store_reviews/<int:store_id>/', views.store_reviews, name='store_reviews'),
]
