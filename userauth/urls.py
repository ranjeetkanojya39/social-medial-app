from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from userauth import views

urlpatterns = [
    path('admin/',          admin.site.urls),

    # Auth
    path('',                views.home,           name='home'),
    path('loginn/',         views.loginn,          name='loginn'),
    path('signup/',         views.signup,          name='signup'),
    path('logoutt/',        views.logoutt,         name='logoutt'),

    # Posts
    path('upload/',         views.upload,          name='upload'),
    path('delete/<str:id>/',views.delete,          name='delete'),
    path('like-post/<str:id>/', views.likes,       name='like-post'),

    # Social
    path('explore/',        views.explore,         name='explore'),
    path('profile/<str:id_user>/', views.profile,  name='profile'),
    path('follow/',         views.follow,          name='follow'),

    # Search
    path('search-results/', views.search_results,  name='search_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
