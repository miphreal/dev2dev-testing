from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from .api import views as api_views

api_router = routers.DefaultRouter()
api_router.register('login', api_views.LoginView, 'api.auth.login')
api_router.register('questions', api_views.QuestionViewSet, 'api.questions')
api_router.register('questions/(?P<question_id>\d+)/votes', api_views.VoteViewSet, 'api.questions.votes')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_router.urls)),
]
