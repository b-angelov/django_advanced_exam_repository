from django.urls import path, include

from izpitnik.orth_calendar.views import SingleSaintView, SaintsListView, FeastListView, SingleFeastView, \
    SingleHolidayView, HolidayListView, SingleHolidayByDateView

urlpatterns = [
    path('saints/',
         include([
             path('', SaintsListView.as_view(), name='saints-view'),
             path('<int:pk>/', SingleSaintView.as_view(), name='single-saint-view'),


         ])
    ),
    path('feasts/',
         include([
             path('', FeastListView.as_view(), name='seasts-view'),
             path('<int:pk>/', SingleFeastView.as_view(), name='single-seast-view'),


         ])
    ),
    path('holidays/',
         include([
             path('', HolidayListView.as_view(), name='holidays-view'),
             path('<int:pk>/', SingleHolidayView.as_view(), name='single-holiday-view'),
             path('<slug:date_slug>/', SingleHolidayByDateView.as_view(), name='single-holiday-view'),

         ])
    ),
]