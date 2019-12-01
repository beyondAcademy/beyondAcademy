##default import
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.db import transaction
from django.contrib.auth.decorators import login_required
##model import
from graduateProject.models import *


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
        # birth_year = request.POST['birth_year']
        # birth_month = request.POST['birth_month']
        # birth_day = request.POST['birth_day']
        birth_year = '1990'
        birth_month = '01'
        birth_day = '01'

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


def signup_completed(request, id):
    return render(request, 'graduateProject/user/signup_complete.html')

def profileView(request, id):
    active = "profile"
    tradePerUserList = TradePerUserModel.objects.filter(user__exact=id).values('date','trade_flag','currency','amount','trade_type')
    for tradePerUser in tradePerUserList:
        if(tradePerUser['trade_type'] == '001'):
            tradePerUser['trade_type'] = '응답채택'
        elif(tradePerUser['trade_type'] == '011'):
            tradePerUser['trade_type'] = '크레딧충전'

        if(tradePerUser['currency'] == '001'):
            tradePerUser['currency'] = '원'
        elif(tradePerUser['currency'] == '002'):
            tradePerUser['currency'] = '크레딧'
        elif(tradePerUser['currency'] == '003'):
            tradePerUser['currency'] = '포인트'
    return render(request, 'graduateProject/profile/profile.html', {'active':active, 'tradePerUserList':tradePerUserList})

@login_required
@transaction.atomic
def rechargeCreditView(request):
    try:
        active = "rechargeCredit"

        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        id = request.POST['id']

        ##trade header variables
        receipt_no = TradeHeaderModel.objects.filter(date__exact=date)
        if receipt_no:
            receipt_no = TradeHeaderModel.objects.filter(date__exact=date).order_by('-receipt_no')[0].receipt_no
            receipt_no = receipt_no + 1
        else:
            receipt_no = 1

        trade_type = '011'
        take_price = request.POST['credit']
        give_price = request.POST['credit']
        take_currency = '002'
        give_currency = '001'
        user = User.objects.get(id=id)
        take_user = user.id
        give_user = 0
        trade_dttm_webserver = now
        trade_dttm_browser = datetime.datetime.fromtimestamp(int(request.POST['timestamp']) / 1000)

        ##trade per user variables
        seq_tradePerUserModel = TradePerUserModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no)
        if seq_tradePerUserModel:
            seq_tradePerUserModel = \
            TradePerUserModel.objects.filter(date__exact=date).filter(receipt_no__exact=receipt_no).order_by('-seq')[0].seq
            seq_tradePerUserModel = seq_tradePerUserModel + 1
        else:
            seq_tradePerUserModel = 1

        user.credit = user.credit + int(take_price)

        tradeHeaderModel = TradeHeaderModel(date=date, receipt_no=receipt_no, trade_type=trade_type,
                                            take_price=take_price, give_price=give_price,
                                            take_currency=take_currency, give_currency=give_currency,
                                            take_user=take_user, give_user=give_user,
                                            trade_dttm_webserver=trade_dttm_webserver, trade_dttm_browser=trade_dttm_browser
                                            )
        tradePerUserModel = TradePerUserModel(date=date, receipt_no=receipt_no,
                                              seq=seq_tradePerUserModel, user=take_user,
                                              trade_flag='001', currency=take_currency,
                                              amount=take_price, trade_type=trade_type,
                                              trade_dttm_webserver=now, trade_dttm_browser=trade_dttm_browser
                                              )
        tradeRechargeModel = TradeRechargeModel(date=date, receipt_no=receipt_no, amount=take_price, user=user,
                                                trade_dttm_webserver=trade_dttm_webserver, trade_dttm_browser=trade_dttm_browser)

        tradeHeaderModel.save()
        tradePerUserModel.save()
        tradeRechargeModel.save()
        user.save()

        msg = take_price + '원이 충전되었습니다.'
        return HttpResponse(msg)
    except Exception as ex:
        print('error occured :', ex)