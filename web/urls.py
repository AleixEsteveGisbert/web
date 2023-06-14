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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from Web_App import views
from Web_App.consumers import MinecraftConsoleConsumer

websocket_urlpatterns = [
    re_path(r'ws/minecraft_console/$', MinecraftConsoleConsumer.as_asgi()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='home'),
    path('login', views.login_form, name='login'),
    path('register', views.register_form, name='register'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    # Control Panel URLs
    path('dashboard', views.dashboard, name='dashboard'),
    path('server/new', views.new_server, name='server-new'),
    path('updateservers', views.update_servers, name='update-servers'),
    path('server/<int:server_id>/stop', views.stop_server, name='server-stop'),
    path('server/<int:server_id>/start', views.start_server, name='server-start'),
    path('server/<int:server_id>/restart', views.restart_server, name='server-restart'),
    path('server/<int:server_id>/delete', views.delete_server, name='server-delete'),
    path('server/<int:server_id>/details', views.details_server, name='server-edit'),

    # Wallet URLs
    path('wallet', views.wallet, name='wallet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
