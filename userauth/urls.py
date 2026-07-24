from django.contrib import admin
from django.urls import path , include
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home),
    path('signup/',views.signup),
    path('loginn/', views.loginn, name='loginn'),
    path('upload/' , views.upload , name='upload'),
   path('logout/', views.logoutt, name='logout'),
   path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),



]