from django.urls import path, include
from knox import views as knox_views
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('companies', views.CompanyViewSet)

urlpatterns = [
    path('user/', views.get_user),
    path('login/', views.login),
    path('register/', views.register),
    path('verify/', views.verify),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),



    #company URLS
    # path('', include(router.urls)),



    #clients URLS
    path('clients/', views.get_clients),

    # path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall')
]