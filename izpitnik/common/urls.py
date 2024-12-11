from django.urls import path, include

from izpitnik.common.views import HomePage, CalendarView

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('calendar/', include([
        path('', CalendarView.as_view(), name='calendar-page'),
        path('<slug:date>/', CalendarView.as_view(), name='calendar-dates'),
    ])),
]
