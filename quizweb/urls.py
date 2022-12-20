from django.urls import path
from quizweb import views

urlpatterns = [
    path('register/',views.RegistrationForm.as_view(),name="signup"),
    path('signin/',views.UserLoginForm.as_view(),name="sign--in"),
    path('index/',views.IndexView.as_view(),name="house"),
    path('logout/',views.sign_out_view,name="sign-out"),
]
