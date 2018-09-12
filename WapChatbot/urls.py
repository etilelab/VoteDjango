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
    path('onsurvey/', views.onsurvey, name='onsurvey'), # 진행중인 투표
    path('endsurvey/',views.endsurvey, name='endsurvey'), # 투표 종료
    path('makesurvey/', views.makesurvey, name='makesurvey'), # 투표 만들기
    path('votes/<int:question_id>/', views.votes, name='votes'), # 투표하기 URL
]
