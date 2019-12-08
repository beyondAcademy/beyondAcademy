##default import
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

##model import
from graduateProject.models import LiveinterviewModel, LiveinterviewSelectListModel, LiveinterviewReplyModel, User, LiveinterviewCategoryModel
from graduateProject.models import TradeHeaderModel, TradePointModel, TradePerUserModel, TradeLiveinterviewSelectModel
from graduateProject.models import BaseCode

##form import
from graduateProject.forms import LiveinterviewForm


##liveinterview views
def liveinterviewListView(request, userId):
    try:
        active="liveinterview_list"
        interviewList = LiveinterviewModel.objects.all().order_by('-pk').select_related('write_user').values('id', 'write_user', 'write_user__last_name', 'write_dttm', 'title','content','currency','amount','read_count')
        selectInterviewList = LiveinterviewSelectListModel.objects.filter(user_id__exact=userId).values("interview_id")

        fields = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="001")
        tasktypes = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="002")
        lifestyles = BaseCode.objects.filter(h_category__exact="001").filter(m_category__exact="003")

        interviewTuple = []
        for interview in interviewList:
            replyCount = len(LiveinterviewReplyModel.objects.filter(interview_id__exact = interview['id']))
            interview['replyCount'] = replyCount
            interviewTuple.append(interview)

        selectInterviewListTuple = []
        for selectInterview in selectInterviewList:
            selectInterviewListTuple.append(selectInterview['interview_id'])
        return render(request, 'graduateProject/liveinterview/liveinterview_list.html', {'active': active, 'interviewList':interviewTuple, 'selectInterviewList':selectInterviewListTuple, 'fields': fields, 'tasktypes': tasktypes, 'lifestyles': lifestyles})
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
        interview.read_count += 1
        interview.save()
        return render(request, 'graduateProject/liveinterview/liveinterview_view.html', {'active': active, 'interview':interview, 'replies':replies})
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def liveinterviewSelectView(request):
    try:
        ##liveinterview select list model variables
        userId = request.POST['id']
        timestamp = request.POST['timestamp']
        interviewId = request.POST['interviewId']
        interview = LiveinterviewModel.objects.get(id__exact=interviewId)

        giveUser = User.objects.get(id__exact=userId)
        takeUser = User.objects.get(id__exact=interview.write_user.id)
        if giveUser.credit < interview.amount:
            return HttpResponse("크레딧이 부족합니다. 크레딧을 충전해주세요.")
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

            interviewCategories = LiveinterviewCategoryModel.objects.filter(interview_id__exact=interviewId)

            for interviewCategory in interviewCategories:
                tradepointModel = TradePointModel(date=date, receipt_no=receipt_no, seq=seq_tradePointModel,
                                                  user=takeUser.id, trade_type=trade_type,
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

        msg = '게시글을 열람하셨습니다. 이 무료로 게시글을 조회하실 수 있습니다.'
        return HttpResponse(msg)

    except Exception as ex:
        print('error occured :', ex)

def liveinterviewCheckboxView(request):
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

            liveinterviewCategories = LiveinterviewCategoryModel.objects.filter(cat_m_category__exact='001').filter(cat_key__in=fieldQueryString) | \
                                        LiveinterviewCategoryModel.objects.filter(cat_m_category__exact='002').filter(cat_key__in=tasktypeQueryString) | \
                                        LiveinterviewCategoryModel.objects.filter(cat_m_category__exact='003').filter(cat_key__in=lifestyleQueryString)

            liveinterviewList = []
            for liveinterviewCategory in liveinterviewCategories:
                liveinterviewList.append(liveinterviewCategory.interview_id)

            tmpList = []
            for liveinterview in liveinterviewList:
                tmpDict = {}
                tmpDict['id'] = liveinterview.id
                tmpDict['write_user'] = liveinterview.write_user.id
                tmpDict['write_user__last_name'] = liveinterview.write_user.last_name
                tmpDict['write_dttm'] = str(liveinterview.write_dttm)
                tmpDict['title'] = liveinterview.title
                tmpDict['amount'] = liveinterview.amount
                tmpDict['read_count'] = liveinterview.read_count
                tmpDict['reply_count'] = liveinterview.reply_count
                tmpList.append(tmpDict)


        return HttpResponse(json.dumps(tmpList), content_type="application/json")
    except Exception as ex:
        print('error occured :', ex)

@login_required
@transaction.atomic
def liveinterviewReplyWriteView(request):
    try:
        interviewId = request.POST['interviewId']
        userId = request.POST['userId']
        replyContent = request.POST['replyContent']
        liveinterview = LiveinterviewModel.objects.get(id__exact=interviewId)
        replyWriteUser = User.objects.get(id__exact=userId)
        is_seq = LiveinterviewReplyModel.objects.filter(interview_id__exact=liveinterview).order_by('-seq')
        if is_seq:
            seq=LiveinterviewReplyModel.objects.filter(interview_id__exact=liveinterview).order_by('-seq')[0].seq+1
        else:
            seq=1
        reply_dttm = datetime.datetime.now()


        reply = LiveinterviewReplyModel(interview_id=liveinterview, seq=seq, reply_user=replyWriteUser, reply_content=replyContent, reply_dttm=reply_dttm)
        liveinterview.read_count += 1
        liveinterview.save()
        reply.save()
        replyList = LiveinterviewReplyModel.objects.filter(interview_id__exact=interviewId)

        tmpList = []
        for reply in replyList:
            tmpDict = {'replyId':reply.id, 'userId':reply.reply_user_id, 'content':reply.reply_content}
            tmpList.append(tmpDict)

        jlist = json.dumps(tmpList)
        return HttpResponse(jlist,content_type="application/json")
    except Exception as ex:
        print('error occured :', ex)