from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(Request):
    return render(Request, 'itreporting/home.html', {'title': 'Welcome'})

def about(Request):
    return HttpResponse('<h1>Student IT Services About</h1>')

def contact(Request):
    return HttpResponse('<h1>Student IT Services Contact</h1>')