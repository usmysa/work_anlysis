from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def maps(request):
    """書籍の一覧"""
    return HttpResponse('Hoge')
