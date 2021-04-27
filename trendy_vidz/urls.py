"""trendy_vidz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import path
from vid_lib import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('signup/', views.signup_view.as_view(),name='signup'),
    # group
    path('group/crt/', views.group_crt.as_view(),name='grp_crt'),
    path('group/<int:pk>/', views.group_dtl.as_view(), name='grp_dtl'),
    path('group/<int:pk>/updt/', views.group_updt.as_view(), name='grp_updt'),
    path('group/<int:pk>/dlt/', views.group_dlt.as_view(), name='grp_dlt'),
    # video
    path('group/<int:pk>/addvideo/', views.add_video, name='add_video'),
    path('video/search/', views.video_search, name='video_search'),
    path('vid/<int:pk>/dlt/', views.video_dlt.as_view(), name='vid_dlt'),
    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
