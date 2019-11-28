##default import
from django.shortcuts import render, redirect

def index(request):
    active = "index"
    return render(request, 'graduateProject/index/index.html', {'active':active})

