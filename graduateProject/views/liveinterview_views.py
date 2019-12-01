##default import
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction

##model import
from graduateProject.models import LiveinterviewModel, LiveinterviewSelectListModel, LiveinterviewReplyModel, User, LiveinterviewCategoryModel
from graduateProject.models import TradeHeaderModel, TradePointModel, TradePerUserModel, TradeLiveinterviewSelectModel

##form import
from graduateProject.forms import LiveinterviewForm


##liveinterview views
def liveinterviewListView(request, userId):
    try:
        active="liveinterview_list"
        interviewList = LiveinterviewModel.objects.all().order_by('-pk').select_related('write_user').values('id', 'write_user', 'write_user__last_name', 'write_dttm', 'title','content','currency','amount','read_count')
        selectInterviewList = LiveinterviewSelectListModel.objects.filter(user_id__exact=userId).values("interview_id")



        interviewTuple = []
        for interview in interviewList:
            replyCount = len(LiveinterviewReplyModel.objects.filter(interview_id__exact = interview['id']))
            interview['replyCount'] = replyCount
            interviewTuple.append(interview)

        selectInterviewListTuple = []
        for selectInterview in selectInterviewList:
            selectInterviewListTuple.append(selectInterview['interview_id'])
        return render(request, 'graduateProject/liveinterview/liveinterview_list.html', {'active': active, 'interviewList':interviewTuple, 'selectInterviewList':selectInterviewListTuple})
    except Exception as ex:
        print('error occured :', ex)


@login_required
@transaction.atomic
def liveinterviewWriteView(request):
    active="liveinterview_write"
    try:
        if request.method == 'POST':

            form = LiveinterviewForm(request.POST)
            if form.is_valid():
                userId = form.data['user_id']
                write_user = User.objects.get(id__exact=userId)
                write_dttm = datetime.datetime.now()
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                currency = form.cleaned_data['currency']
                amount = form.cleaned_data['amount']
                fields = request.POST.getlist('fields')
                tasktypes = request.POST.getlist('tasktypes')
                lifestyles = request.POST.getlist('lifestyles')

                liveinterview = LiveinterviewModel(write_user=write_user, write_dttm=write_dttm,
                                                   title=title, content=content,
                                                   currency=currency, amount=amount
                                                   )
                liveinterview.save()

                interviewId = liveinterview
                seq = 1
                for field in fields:
                    liveinterviewCategory = LiveinterviewCategoryModel(interview_id=interviewId, seq=seq,
                                                                      cat_h_category='001', cat_m_category='001',
                                                                      cat_key=field)
                    liveinterviewCategory.save()
                    seq = seq + 1

                for tasktype in tasktypes:
                    liveinterviewCategory = LiveinterviewCategoryModel(interview_id=interviewId, seq=seq,
                                                                      cat_h_category='001', cat_m_category='002',
                                                                      cat_key=tasktype)
                    liveinterviewCategory.save()
                    seq = seq + 1

                for lifestyle in lifestyles:
                    liveinterviewCategory = LiveinterviewCategoryModel(interview_id=interviewId, seq=seq,
                                                                      cat_h_category='001', cat_m_category='003',
                                                                      cat_key=lifestyle)
                    liveinterviewCategory.save()
                    seq = seq + 1

                return redirect('liveinterviewList/'+userId)
            return ("fail")
        elif request.method == 'GET':
            form = LiveinterviewForm()
            return render(request, 'graduateProject/liveinterview/liveinterview_write.html', {'active':active, 'form':form})
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def liveinterviewViewView(request, interviewId):
    try:
        active = 'liveinterviewView'
        interview = LiveinterviewModel.objects.get(id__exact=interviewId)
        replies = LiveinterviewReplyModel.objects.filter(interview_id__exact=interview)
        return render(request, 'graduateProject/liveinterview/liveinterview_view.html', {'active': active, 'interview':interview, 'replies':replies})
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def liveinterviewSelectView(request, interviewId, userId, timestamp):
    try:
        ##liveinterview select list model variables
        interview = LiveinterviewModel.objects.get(id__exact=interviewId)


        giveUser = User.objects.get(id__exact=userId)
        takeUser = User.objects.get(id__exact=interview.write_user.id)
        if giveUser.credit < interview.amount:
            return HttpResponse("not enough credit")
        seq = LiveinterviewSelectListModel.objects.filter(user_id__exact=giveUser)
        if seq:
            seq = LiveinterviewSelectListModel.objects.filter(user_id__exact=giveUser).order_by('-seq')[0].seq+1
        else:
            seq = 1

        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')

        liveinterviewSelectList = LiveinterviewSelectListModel(user_id=giveUser, seq=seq, interview_id=interview, select_date=date)

        ##tradeheadermodel variables
        receipt_no = TradeHeaderModel.objects.filter(date__exact=date).first()
        if receipt_no:
            receipt_no = TradeHeaderModel.objects.filter(date__exact=date).order_by('-receipt_no')[0].receipt_no+1
        else:
            receipt_no = 1

        trade_type = '051'
        trade_dttm_browser = datetime.datetime.fromtimestamp(int(timestamp) / 1000)

        if interview.currency == '002':
            take_price = interview.amount
            give_price = interview.amount
            take_currency = '002'
            give_currency = '002'
            takeUser.credit = takeUser.credit+take_price
            giveUser.credit = giveUser.credit-take_price
        elif interview.currency == '003':
            take_price = interview.amount
            give_price = 0
            take_currency = '003'
            give_currency = '000'

            ##trade point model variables
            seq_tradePointModel = TradePointModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no)
            if seq_tradePointModel:
                seq_tradePointModel = TradePointModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no).order_by('-seq')[0].seq+1
            else:
                seq_tradePointModel = 1

            interviewCategories = LiveinterviewCategoryModel.obejcts.filter(answer_id__exact=interviewId)

            for interviewCategory in interviewCategories:
                tradepointModel = TradePointModel(date=date, receipt_no=receipt_no, seq=seq_tradePointModel,
                                                  user=takeUser, trade_type=trade_type,
                                                  cat_h_category='001', cat_m_category='001',
                                                  cat_key=interviewCategory.cat_key,
                                                  amount=interview.amount / len(interviewCategories),
                                                  trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser)
                tradepointModel.save()


        tradeHeader = TradeHeaderModel(date=date, receipt_no=receipt_no, trade_type=trade_type,
                                       take_price=take_price, give_price=give_price,
                                       take_currency=take_currency, give_currency=give_currency,
                                        take_user=takeUser.id, give_user=giveUser.id,
                                        trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser)

        tradePerUserModel_takeUser = TradePerUserModel(date=date, receipt_no=receipt_no, seq=1,
                                                       user=takeUser.id, trade_flag='001',
                                                       currency=take_currency, amount=take_price,
                                                       trade_type=trade_type,
                                                       trade_dttm_webserver=now,
                                                       trade_dttm_browser=trade_dttm_browser)

        tradePerUserModel_giveUser = TradePerUserModel(date=date, receipt_no=receipt_no, seq=2,
                                                       user=giveUser.id, trade_flag='002',
                                                       currency=give_currency, amount=give_price,
                                                       trade_type=trade_type,
                                                       trade_dttm_webserver=now,
                                                       trade_dttm_browser=trade_dttm_browser)

        tradeLiveinterviewSelect = TradeLiveinterviewSelectModel(date=date, receipt_no=receipt_no, currency=interview.currency,
                                                                 amount=interview.amount, take_user=takeUser.id, give_user=giveUser.id,
                                                                 trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser)

        liveinterviewSelectList.save()
        tradeHeader.save()
        tradePerUserModel_takeUser.save()
        tradePerUserModel_giveUser.save()
        tradeLiveinterviewSelect.save()
        takeUser.save()
        giveUser.save()

        return HttpResponse("success")


    except Exception as ex:
        print('error occured :', ex)
