from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


from . import views
from graduateProject.views import *


urlpatterns = [
    path('', views.index, name='defaultIndex'),
    path('index', views.index, name='index'),
    # path('findSenior', views.findSenior, name='findSenior'),
    # path('chatting', views.chattingView, name='chatting'),
    # path('profile', views.profileView, name='profile'),

    #
    ##user urls
    path('signup', signup_page, name='register'),
    path('signup_idcheck', signup_idcheck, name='signup_idcheck'),
    path('signup_result', signup_result, name='signup_result'),
    path('signup_completed', signup_completed, name='signup_completed'),
    path('signin/', auth_views.LoginView.as_view(template_name='graduateProject/user/signin.html'), name='signin'),
    path('signout', auth_views.LogoutView.as_view(), name='logout'),
    #
    ##matching urls
    ####questionRequest urls
    path('questionRequest', views.questionRequest, name='questionRequest'),
    path('questionRequestWrite', views.questionRequestWriteView, name='questionRequestWrite'),
    path('questionRequestAnswerWrite/<int:id>', views.questionRequestAnswerWriteView, name='questionRequestAnswerWrite'),
    path('questionRequestAnswerWriteRes', views.questionRequestAnswerWriteResView, name='questionRequestAnswerWriteRes'),
    path('questionRequestAnswerSelect/<int:questionRequestAnswerId>/<str:timestamp>/<int:id>', views.questionRequestAnswerSelectView, name='questionRequestAnswerSelect'),
    path('answerView/<int:questionRequestAnswerId>', views.answerViewView, name='answerView'),
    path('questionRequestCheckbox', views.questionRequestCheckboxView, name='questionRequestCheckbox'),
    #
    # ##liveinterview urls
    # path(r'liveinterviewList/<int:userId>', views.liveinterviewListView, name='liveinterviewList'),
    # path('liveinterviewWrite', views.liveinterviewWriteView, name='liveinterviewWrite'),
    # path('liveinterviewView/<int:interviewId>', views.liveinterviewViewView, name='liveinterviewView'),
    # path('liveinterviewSelect/<int:interviewId>/<int:userId>/<str:timestamp>', views.liveinterviewSelectView, name='liveinterviewSelect'),
    #
    #
    # ##test urls
    # path('chattingList', views.chattingListView, name='chattingList'),
    # path('test', views.test, name='test'),
    # path('listTest', views.listTest, name='listTest'),
    # path('mapTest', views.mapTest, name='mapTest'),
    # path(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # path('imageTest', views.imageTestView, name='imageTest'),
    # # path('signin', views.signin, name='signin'),
]

urlpatterns += static('upload_files', document_root=settings.MEDIA_ROOT)
