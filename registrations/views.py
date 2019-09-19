from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout


def index(request):
    context = {}
    return render(request, 'registrations/login.html', context)

def logout(request, next_page):
    auth_logout(request)
    return redirect(next_page)
