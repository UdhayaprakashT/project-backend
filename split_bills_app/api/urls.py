from django.conf.urls import include, url
from rest_framework import routers
from split_bills_app.api import views

router = routers.DefaultRouter()

router.register(r'groups', views.GroupViewSet, 'groups')
router.register(r'bills',views.BillViewSet, 'bills')
router.register(r'users', views.CustomUserViewSet, 'users')

urlpatterns = [
    url(r'^', include(router.urls))
]