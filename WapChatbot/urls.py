"""WapChatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from WapChatbot import views

urlpatterns = [
    path('admin/', admin.site.urls), # 관리자 페이지
    path('', views.index, name='index'), # 인덱스 페이지

    path('onsurvey/', views.onsurvey, name='onsurvey'),
    path('endsurvey/',views.endsurvey, name='endsurvey'),
    path('makesurvey/', views.makesurvey, name='makesurvey'),

    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/result/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
     # 투표 생성 URL
]
