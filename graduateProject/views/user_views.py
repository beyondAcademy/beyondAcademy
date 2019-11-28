##default import
from django.shortcuts import render, redirect
from django.http import HttpResponse
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
