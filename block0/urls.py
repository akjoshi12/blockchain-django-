from django.urls import path ,include
from block0 import views
urlpatterns = [
    path('',views.login,name="login"),
    path("home",views.home,name="index"),
    path("steps",views.steps,name="steps"),
    path('about',views.about,name="about"),
    path('transactions',views.transactions,name="transactions"),
    path('quotes',views.quotes,name="quotes"),
    path("history",views.history, name="history")
]