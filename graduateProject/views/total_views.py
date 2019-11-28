##default import
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
from django.forms.models import model_to_dict


##model import
from graduateProject.models import *

##form import
from graduateProject.forms import PostForm, LiveinterviewForm
from graduateProject.forms import *

# Create your views here.
def index(request):
    active = "index"
    return render(request, 'graduateProject/index/index.html', {'active':active})



##matching views
####question request views
def questionRequest(request):
    active = "matching"
    try:
        fields = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="001")
        tasktypes = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="002")
        lifestyles = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="003")
        questionRequests = QuestionRequest.objects.all().order_by('-pk').values('id', 'content', 'user_id')[:6]
        for index in questionRequests:
            index['questionRequestAnswers']=(QuestionRequestAnswerModel.objects.filter(request_no__exact=index['id']).select_related('answer_user').values('id', 'answer_user__last_name', 'amount', 'select_yn'))
        return render(request, 'graduateProject/matching/question_request.html', {'active':active, 'fields':fields, 'tasktypes':tasktypes, 'lifestyles':lifestyles, 'questionRequests':questionRequests})
    except Exception as ex:
        print('error occured :', ex)

def questionRequestCheckboxView(request):
    try:
        if request.method == "POST":
            fields = request.POST.getlist('fields[]')
            tasktypes = request.POST.getlist('tasktypes[]')
            lifestyles = request.POST.getlist('lifestyles[]')


            fieldQueryString = '['
            tasktypeQueryString = '['
            lifestyleQueryString = '['

            index = 0
            for field in fields:
                if index == len(fields)-1:
                    fieldQueryString += '"' + field[15:18] + '"'
                else:
                    fieldQueryString += '"' + field[15:18] + '",'
                index += 1

            index=0
            for tasktype in tasktypes:
                if index == len(tasktypes) - 1:
                    tasktypeQueryString += '"' + tasktype[19:22] + '"'
                else:
                    tasktypeQueryString += '"' + tasktype[19:22] + '",'
                index += 1

            index=0
            for lifestyle in lifestyles:
                if index == len(lifestyles) - 1:
                    lifestyleQueryString += '"' + lifestyle[20:23] + '"'
                else:
                    lifestyleQueryString += '"' + lifestyle[20:23] + '",'
                index += 1

            fieldQueryString += ']'
            tasktypeQueryString += ']'
            lifestyleQueryString += ']'

            fieldQueryString = json.loads(fieldQueryString)
            tasktypeQueryString = json.loads(tasktypeQueryString)
            lifestyleQueryString = json.loads(lifestyleQueryString)

            questionRequestCategories = QuestionRequestCategory.objects.filter(cat_m_category__exact='001').filter(cat_key__in=fieldQueryString) | \
                                        QuestionRequestCategory.objects.filter(cat_m_category__exact='002').filter(cat_key__in=tasktypeQueryString) | \
                                        QuestionRequestCategory.objects.filter(cat_m_category__exact='003').filter(cat_key__in=lifestyleQueryString)

            questionIdList = []
            for questionRequestCategory in questionRequestCategories:
                questionIdList.append(questionRequestCategory.request_no)

            index=0
            questionQueryString = '['
            for questionId in questionIdList:
                if index == len(questionIdList)-1:
                    questionQueryString += '"' + str(questionId.id) + '"'
                else:
                    questionQueryString += '"' + str(questionId.id) + '",'
                index += 1

            questionQueryString += ']'
            questionQueryString = json.loads(questionQueryString)

            questionRequestList = QuestionRequest.objects.filter(id__in = questionQueryString).order_by('-pk').values('id', 'content', 'user_id')

            for index in questionRequestList:
                answerQuerySet = QuestionRequestAnswerModel.objects.filter(request_no__exact=index['id']).select_related(
                        'answer_user').values('id', 'answer_user__last_name', 'amount', 'select_yn')
                index['questionRequestAnswers'] = answerQuerySet

            jsonReturnObject = list(questionRequestList)


            tmpList = []
            for questionRequest in questionRequestList:
                tmpDict = {}
                tmpDict['id'] = questionRequest['id']
                tmpDict['content'] = questionRequest['content']
                tmpDict['user_id'] = questionRequest['user_id']

                answerList = []
                for answer in questionRequest['questionRequestAnswers']:
                    answerDict = {}
                    answerDict['id'] = answer['id']
                    answerDict['last_name'] = answer['answer_user__last_name']
                    answerDict['amount'] = answer['amount']
                    answerDict['select_yn'] = answer['select_yn']
                    answerList.append(answerDict)
                tmpDict['questionRequestAnswers'] = answerList
                tmpList.append(tmpDict)




            return HttpResponse(json.dumps(tmpList), content_type="application/json")
        else:
            fields = ''
            tastypes = ''
            lifestyles = ''
            return httpResponse('fail')
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def questionRequestWriteView(request):
    active = "questionRequestWrite"

    try:
        if request.method == 'POST':

            form = QuestionRequestForm(request.POST)
            if form.is_valid():
                user_id = form.data['user_id']
                write_date_browser = form.data['write_date_browser']
                now = datetime.datetime.now()
                write_date_webserver = now.strftime('%Y%m%d')
                content = form.cleaned_data['content']
                fields = request.POST.getlist('fields')
                tasktypes = request.POST.getlist('tasktypes')
                lifestyles = request.POST.getlist('lifestyles')

                user = User.objects.get(id = user_id)
                questionRequest = QuestionRequest(user_id=user, write_date_browser=write_date_browser, write_date_webserver=write_date_webserver, content=content)
                questionRequest.save()

                request_no = QuestionRequest.objects.order_by('-pk')[0].id
                questionRequest = QuestionRequest.objects.get(id = request_no)
                seq = 1
                for field in fields:
                    questionRequestCategory = QuestionRequestCategory(request_no=questionRequest, seq=seq, cat_h_category='001', cat_m_category='001', cat_key=field)
                    questionRequestCategory.save()
                    seq=seq+1

                for tasktype in tasktypes:
                    questionRequestCategory = QuestionRequestCategory(request_no=questionRequest, seq=seq, cat_h_category='001', cat_m_category='002', cat_key=tasktype)
                    questionRequestCategory.save()
                    seq=seq+1

                for lifestyle in lifestyles:
                    questionRequestCategory = QuestionRequestCategory(request_no=questionRequest, seq=seq, cat_h_category='001', cat_m_category='003', cat_key=lifestyle)
                    questionRequestCategory.save()
                    seq=seq+1
                return redirect(reverse('questionRequest'))
            return("fail")
        elif request.method == 'GET':
            form = QuestionRequestForm()
            return render(request, 'graduateProject/matching/question_request_write.html', {'form':form, 'active':active})
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def questionRequestAnswerWriteView(request, id):
    active = 'questionRequestAnswerWrite'
    questionRequest = QuestionRequest.objects.filter(id__exact = id).values('id', 'content').first
    form = QuestionRequestAnswerForm()
    return render(request, 'graduateProject/matching/question_request_answer_write.html', {'form': form, 'active': active, 'questionRequest':questionRequest, 'request_no': id})

@login_required
@transaction.atomic
def questionRequestAnswerWriteResView(request):
    try :
        form = QuestionRequestAnswerForm(request.POST)
        if form.is_valid():
            request_no = form.data['request_no']
            seq = QuestionRequestAnswerModel.objects.filter(request_no__exact=request_no)
            if seq:
                seq = QuestionRequestAnswerModel.objects.filter(request_no__exact=request_no).order_by('-pk')[0].seq
                seq+1
            else:
                seq = 1
            answer_user = form.data['user_id']
            now = datetime.datetime.now()
            write_date = now.strftime('%Y%m%d')
            content = form.cleaned_data['content']
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']

            questionRequest = QuestionRequest.objects.get(id = request_no)
            user = User.objects.get(id = answer_user)

            questionRequestAnswer = QuestionRequestAnswerModel(request_no=questionRequest, seq=seq, answer_user=user, write_date = write_date, content=content, currency=currency, amount=amount)
            questionRequestAnswer.save()
            return redirect(reverse('questionRequest'))
        return("fail")
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def questionRequestAnswerSelectView(request, questionRequestAnswerId, timestamp, id):
    try:
        ##answer variables
        selectUser = User.objects.get(id=id)
        answerUser = QuestionRequestAnswerModel.objects.get(id=questionRequestAnswerId).answer_user
        answer = QuestionRequestAnswerModel.objects.get(id=questionRequestAnswerId)

        if selectUser.credit<answer.amount:
            return HttpResponse("not enough credit")

        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')

        answer.select_yn = 'Y'
        answer.select_date = date

        ##select list variables
        seq_selectList = QuestionRequestAnswerSelectListModel.objects.filter(user__exact=selectUser)
        if seq_selectList:
            seq_selectList = QuestionRequestAnswerSelectListModel.objects.filter(user__exact=selectUser).order_by('-seq')[0].seq
            seq_selectList = seq_selectList + 1
        else:
            seq_selectList = 1
        answerSelectList = QuestionRequestAnswerSelectListModel(user=selectUser, seq=seq_selectList, answer=answer)


        ##trade header variables
        receipt_no = TradeHeaderModel.objects.filter(date__exact=date)
        if receipt_no:
            receipt_no = TradeHeaderModel.objects.filter(date__exact=date).order_by('-receipt_no')[0].receipt_no
            receipt_no = receipt_no + 1
        else:
            receipt_no = 1

        trade_type = '001'

        trade_dttm_browser = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        if answer.currency == '002':
            take_price = answer.amount
            give_price = answer.amount
            take_currency = '002'
            give_currency = '002'
            answerUser.credit = answerUser.credit + answer.amount
            selectUser.credit = selectUser.credit - answer.amount
        elif answer.currency == '003':
            take_price = answer.amount
            give_price = 0
            take_currency = '003'
            give_currency = '000'
            answerUser.point = answerUser.point + answer.amount

            ##tradepointmodel variables
            seq_tradePointModel = TradePointModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no)
            if seq_tradePointModel:
                seq_tradePointModel = TradePointModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no).order_by('-seq')[0].seq
                seq_tradePointModel = seq_tradePointModel + 1
            else:
                seq_tradePointModel = 1

            QuestionRequest.objects.get(id=answer.request_no_id)
            questionRequestCatgories = QuestionRequestCategory.objects.filter(request_no_id__exact=answer.request_no_id)

            for questionRequestCategory in questionRequestCatgories:
                tradepointModel = TradePointModel(date=date, receipt_no=receipt_no, seq=seq_tradePointModel,
                                                  user=answerUser.id, trade_type=trade_type,
                                                  cat_h_category='001', cat_m_category='001', cat_key=questionRequestCategory.cat_key,
                                                  amount=answer.amount/len(questionRequestCatgories),
                                                  trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser)
                tradepointModel.save()






        ##trade per user variables
        seq_tradePerUserModel = TradePerUserModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no)
        if seq_tradePerUserModel:
            seq_tradePerUserModel = TradePerUserModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no).order_by('-seq')[0].seq
            seq_tradePerUserModel = seq_tradePerUserModel + 1
        else:
            seq_tradePerUserModel = 1

        ##tradeRequestAnswerModel variables
        request_no = QuestionRequest.objects.get(id=QuestionRequestAnswerModel.objects.get(id=questionRequestAnswerId).request_no_id)

        tradeHeaderModel = TradeHeaderModel(date=date, receipt_no=receipt_no, trade_type=trade_type,
                                            take_price=take_price, give_price=give_price,
                                            take_currency=take_currency, give_currency=give_currency,
                                            take_user=answerUser.id, give_user=selectUser.id,
                                            trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser
                                            )
        tradePerUserModel_takeUser = TradePerUserModel(date=date, receipt_no=receipt_no,
                                                       seq=seq_tradePerUserModel, user=answerUser.id,
                                                       trade_flag='001', currency=take_currency,
                                                       amount=take_price, trade_type=trade_type,
                                                       trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser
                                                       )
        seq_tradePerUserModel = seq_tradePerUserModel+1
        tradePerUserModel_giveUser = TradePerUserModel(date=date, receipt_no=receipt_no,
                                                       seq=seq_tradePerUserModel, user=selectUser.id,
                                                       trade_flag='002', currency=give_currency,
                                                       amount=give_price, trade_type=trade_type,
                                                       trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser
                                                       )
        tradeRequestAnswerModel = TradeRequestAnswerModel(date=date, receipt_no=receipt_no,
                                                          currency=take_currency, amount=take_price,
                                                          take_user=answerUser.id, give_user=selectUser.id,
                                                          request_no=request_no, answer_no=answer,
                                                          trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser
                                                          )



        ##save
        answer.save()
        answerSelectList.save()
        tradeHeaderModel.save()
        tradePerUserModel_takeUser.save()
        tradePerUserModel_giveUser.save()
        tradeRequestAnswerModel.save()
        selectUser.save()
        answerUser.save()

        # return redirect(reverse('answerView/'+str(answer.id)))
        return redirect(reverse('questionRequest'))

    except Exception as ex:
        print('error occured :', ex)

@login_required
def answerViewView(request, questionRequestAnswerId):
    try:
        active = "answerView"
        content = QuestionRequestAnswerModel.objects.get(id__exact=questionRequestAnswerId).content
    except Exception as ex:
        print('error occured :', ex)
    return render(request, 'graduateProject/matching/question_answer_view.html', {'active': active, 'content': content})




##user Views
def signup_page(request):
    return render(request, 'graduateProject/user/signup.html')

def signup_idcheck(request):
    if request.method == "POST":
        username = request.POST['username']
    else:
        username = ''

    idObject = User.objects.filter(username__exact=username)
    idCount = idObject.count()

    if idCount > 0:
        msg = "<font color='red'> the id is alerady exist.</font>"
        msg += "<input type='hidden' name='IDCheckResult' id='IDCheckResult' value=0 />"
    else:
        msg = "<font color='blue'> the id is avaiable.</font>"
        msg += "<input type='hidden' name='IDCheckResult' id='IDCheckResult' value=1 />"

    return HttpResponse(msg)


def signup_result(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        last_name = request.POST['last_name']
        # phone = request.POST['phone']
        phone = '01012431234'
        # email = request.POST['email']
        email = 'test1@test1.com'
        birth_year = request.POST['birth_year']
        birth_month = request.POST['birth_month']
        birth_day = request.POST['birth_day']

    try:
        if username and User.objects.filter(username__exact=username).count() == 0 :
            # date_of_birth = datetime(birth_year, birth_month, birth_day)
            user = User.objects.create_user(
                username,password,last_name, email, phone, '1990-01-01'
            )

            redirection_page = 'signup_completed'

        else:
            redirection_page = 'error'
    except Exception as ex:
        print('error occured :', ex)

    return redirect(redirection_page)


def signup_completed(request):
    return render(request, 'graduateProject/user/signup_completed.html')
