from django.urls import path, include

from izpitnik.orth_calendar.views import SingleSaintView, SaintsListView, FeastListView, SingleFeastView

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
]
