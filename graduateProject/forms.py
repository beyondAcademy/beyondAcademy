##default import
from django.forms import ModelForm
from django import forms

##summernote import
from django_summernote.widgets import SummernoteWidget

##model import
from .models import Post, imageTest, BaseCode, LiveinterviewModel

##signup import
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm


##user models
# class signupForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
#     email = forms.EmailField(required=True) # 이메일 필드 추가
#
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#
#     def save(self, commit=True): # 저장하는 부분 오버라이딩
#         user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user


# class signinForm(forms.ModelForm):


##liveinterview forms
class LiveinterviewForm(forms.Form):
    try:
        fieldsQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="001").values()
        tasktypesQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="002").values()
        lifestyleQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="003").values()

        fieldsTuple = []
        for field in fieldsQueryset:
            fieldsTuple.append((field['key'], field['val']))

        tasktypesTuple = []
        for tasktype in tasktypesQueryset:
            tasktypesTuple.append((tasktype['key'], tasktype['val']))

        lifestylesTuple = []
        for lifestyle in lifestyleQueryset:
            lifestylesTuple.append((lifestyle['key'], lifestyle['val']))

        currencies = BaseCode.objects.filter(h_category__exact="002").filter(m_category__exact="001").values('key','val')[1:3]
        currenciesTuple = []
        for currency in currencies:
            currenciesTuple.append((currency['key'], currency['val']))


        fields = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=fieldsTuple),
        )
        tasktypes = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=tasktypesTuple),
        )
        lifestyles = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=lifestylesTuple),
        )
        title = forms.CharField(label="title", max_length=50)
        content = forms.CharField(label="content", widget=SummernoteWidget())

        currency = forms.CharField(widget=forms.Select(choices=currenciesTuple),)
        amount = forms.IntegerField()
    except Exception as ex:
        print('error occured :', ex)

##question forms
####question request forms
class QuestionRequestForm(forms.Form):
    try:
        fieldsQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="001").values()
        tasktypesQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="002").values()
        lifestyleQueryset = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="003").values()

        fieldsTuple = []
        for field in fieldsQueryset:
            fieldsTuple.append((field['key'], field['val']))

        tasktypesTuple = []
        for tasktype in tasktypesQueryset:
            tasktypesTuple.append((tasktype['key'], tasktype['val']))

        lifestylesTuple = []
        for lifestyle in lifestyleQueryset:
            lifestylesTuple.append((lifestyle['key'], lifestyle['val']))

        fields = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=fieldsTuple),
        )
        tasktypes = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=tasktypesTuple),
        )
        lifestyles = forms.CharField(
            widget=forms.CheckboxSelectMultiple(choices=lifestylesTuple),
        )
        content = forms.CharField(label="content", widget=SummernoteWidget())
    except Exception as ex:
        print('error occured :', ex)

class QuestionRequestAnswerForm(forms.Form):
    try :
        currencies = BaseCode.objects.filter(h_category__exact="002").filter(m_category__exact="001").values('key', 'val')[1:3]
        currenciesTuple = []
        for currency in currencies:
            currenciesTuple.append((currency['key'], currency['val']))
        content = forms.CharField(label="content", widget=SummernoteWidget())
        currency = forms.CharField(widget=forms.Select(choices=currenciesTuple),)
        amount = forms.IntegerField()

    except Exception as ex:
        print('error occured :', ex)


##Test Models




##test form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }

class imageTestForm(forms.ModelForm):
    class Meta:
        model = imageTest
        fields = ('image', 'content',)
