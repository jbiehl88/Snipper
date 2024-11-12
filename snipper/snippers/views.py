from django.shortcuts import render
from django.http import HttpResponse

def snippers(request):
    return HttpResponse("Hello world!")