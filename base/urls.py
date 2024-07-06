from django.urls import path
from .views import DashboardView, SelectDirectionView, SelectDateTimeView, UserDetailsView, MainDashboardView

urlpatterns = [
    path('',DashboardView.as_view(), name='dashboard'),
    path('booking/',SelectDirectionView.as_view(), name='selecting-direction'),
    path('booking/process/<int:token>',SelectDateTimeView.as_view(), name='selecting-datetime'),
    path('booking/process/user-details/<int:token>',UserDetailsView.as_view(), name='user-details'),
    path('booking/<int:token>/success/',MainDashboardView.as_view(), name='main-dashboard'),
]