from django.urls import path
from api.views import PhoneBook, PhoneBookDetail

urlpatterns = [
    path('', PhoneBook.as_view()),
    path('<str:pk>', PhoneBookDetail.as_view())
]