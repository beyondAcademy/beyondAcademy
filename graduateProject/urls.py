from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views
from graduateProject.views import *


urlpatterns = [
    path('', views.index, name='defaultIndex'),
    path('index', views.index, name='index'),
    # path('findSenior', views.findSenior, name='findSenior'),
    # path('chatting', views.chattingView, name='chatting'),



    ##user urls
    path('signup', signup_page, name='signup'),
    path('signup_idcheck', signup_idcheck, name='signup_idcheck'),
    path('signup_result', signup_result, name='signup_result'),
    path('signup_completed', signup_completed, name='signup_completed'),
    path('signin/', auth_views.LoginView.as_view(template_name='graduateProject/user/signin.html'), name='signin'),
    path('signout', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:id>/', views.profileView, name='profile'),
    # url(r'^profile/(?P<id>\d+)', views.profileView, name='profile'),
    path('rechargeCredit', views.rechargeCreditView, name='rechargeCredit'),

    ##matching urls
    ####questionRequest urls
    path('questionRequest', views.questionRequest, name='questionRequest'),
    path('questionRequestWrite', views.questionRequestWriteView, name='questionRequestWrite'),
    path('questionRequestAnswerWrite/<int:id>', views.questionRequestAnswerWriteView, name='questionRequestAnswerWrite'),
    path('questionRequestAnswerWriteRes', views.questionRequestAnswerWriteResView, name='questionRequestAnswerWriteRes'),
    path('questionRequestAnswerSelect', views.questionRequestAnswerSelectView, name='questionRequestAnswerSelect'),
    path('answerView/<int:questionRequestAnswerId>', views.answerViewView, name='answerView'),
    path('questionRequestCheckbox', views.questionRequestCheckboxView, name='questionRequestCheckbox'),
    path('questionRequestMyQuestion', views.questionRequestMyQuestionView, name='questionRequestMyQuestion'),

    ##liveinterview urls
    path(r'liveinterviewList/<int:userId>', views.liveinterviewListView, name='liveinterviewList'),
    path('liveinterviewWrite', views.liveinterviewWriteView, name='liveinterviewWrite'),
    path('liveinterviewView/<int:interviewId>', views.liveinterviewViewView, name='liveinterviewView'),
    path('liveinterviewSelect', views.liveinterviewSelectView, name='liveinterviewSelect'),
    path('liveinterviewCheckbox', views.liveinterviewCheckboxView, name='liveinterviewCheckbox'),
    path('liveinterviewReplyWrite', views.liveinterviewReplyWriteView, name='liveinterviewReplyWrite'),

    ##algorithm urls
    path('algorithm', views.algorithmView, name='algorithm'),
    path('algorithmSelect', views.algorithmSelectView, name='algorithmSelect'),
    path('algorithmReset', views.algorithmResetView, name='algorithmReset'),
    path('algorithmRecommend', views.algorithmRecommend, name='algorithmRecommend')

    # ##test urls
    # path('test', views.test, name='test'),
    # path('listTest', views.listTest, name='listTest'),
    # path('mapTest', views.mapTest, name='mapTest'),
    # path(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # path('imageTest', views.imageTestView, name='imageTest'),
    # # path('signin', views.signin, name='signin'),
]

urlpatterns += static('upload_files', document_root=settings.MEDIA_ROOT)
