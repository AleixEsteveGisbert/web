"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from Web_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),
    path('login', views.login_form, name='login'),
    path('register', views.register_form, name='register'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    # Control Panel URLs
    path('dashboard', views.dashboard, name='dashboard'),
    path('server/new', views.new_server, name='server-new'),
    path('server/<int:server_id>/stop', views.stop_server, name='server-stop'),
    path('server/<int:server_id>/details', views.details_server, name='server-edit'),
    path('server/<int:server_id>/show', views.show_server, name='server-show'),
]

