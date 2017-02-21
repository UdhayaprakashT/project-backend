from django.conf.urls import include, url
from rest_framework import routers
from split_bills_app.api import views

router = routers.DefaultRouter()

router.register(r'groups', views.GroupViewSet, 'groups')
router.register(r'users', views.UserViewSet, 'users')
router.register(r'bills',views.BillViewSet, 'bills')

urlpatterns = [
    url(r'^', include(router.urls))
]