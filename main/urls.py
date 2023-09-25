from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    # path('history/search/', views.history, name='search'),
    path('settings/', views.settings, name='settings'),
    path('faq/', views.faq, name='faq'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('history/<int:id>/', views.detailsPage, name='details'),
    path('settings/get-auth-url/',views.AuthURL.as_view(), name='' ),
    path('settings/is-authenticated/',views.IsAuthenticated.as_view(), name=''),
    path('redirect/',views.spotify_callback, name=''),
]
