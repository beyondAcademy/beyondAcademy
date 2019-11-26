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
from .models import *

##form import
# from graduateProject.forms import PostForm, LiveinterviewForm
# from .forms import *

# Create your views here.



def index(request):
    active = "index"
    return render(request, 'graduateProject/index/index.html', {'active':active})