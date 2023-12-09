"""project URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from token_app.views import (
    index_view,
    news_view,
    chart_view,
    home_view,
    exchangeDetail_view,
    login_view,
    logout_view,
    register_view,
    cryptodata,
    search_view,
    autocomplete,
    portfolio_view,
    crypto_create,
    crypto_update,
    crypto_delete,
    add_review,
    reviews
)

# URL configuration
urlpatterns = [

    path('admin/', admin.site.urls),
    path('', index_view, name='index_view'),
    path('chart', chart_view, name='chart_view'),
    path('news', news_view, name='news_view'),
    path('home', home_view, name='home_view'),
    path('exchangeDetail', exchangeDetail_view, name='exchangeDetail_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register/', register_view, name='register_view'),
    path('cryptodata/', cryptodata, name='cryptodata'),
    path('portfolio', portfolio_view, name='portfolio_view'),
    path('search', search_view, name='search_view'),
    path('autocomplete', autocomplete, name='autocomplete'),
    path('add', crypto_create, name='crypto_create'),
    path('update/<int:pk>', crypto_update, name='crypto_update'),
    path('delete/<int:pk>', crypto_delete, name='crypto_delete'),
    path('add_review', add_review, name='add_review'),
    path('view_review', reviews, name='reviews'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)