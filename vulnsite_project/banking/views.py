from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import connection
from .models import Account
import sys
import sqlite3

@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})

@login_required
def confirmView(request):
    # Note no CSRF
	amount = request.session['amount']
	to = User.objects.get(username=request.session['to'])

	request.user.account.balance -= amount
	to.account.balance += amount

	request.user.account.save()
	to.account.save()
	
	return redirect('/')

@login_required
def transferView(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = int(request.GET.get('amount'))
	return render(request, 'pages/confirm.html')

@login_required
def depositView(request):
    amount = int(request.GET.get('amount'))
    request.user.account.balance += amount
    request.user.account.save()
    return redirect('/')

@login_required	
def withdrawView(request):
    amount = int(request.GET.get('amount'))
    request.user.account.balance -= amount
    request.user.account.save()
    return redirect('/')

@login_required
def postmessageView(request):
    message = request.GET.get('message')
    request.user.account.messagetext = message
    request.user.account.save()
    return redirect('/')

@login_required
def retrievemessageView(request):
    """
    conn = sqlite3.connect(db.sqlite3)
    """
    person = request.GET.get('retrieveuser')
    with connection.cursor() as cursor:
        cursor.execute("SELECT messagetext FROM banking_account WHERE user_id in(SELECT id from auth_user WHERE username = '%s')"%(person))
        messages = cursor.fetchall()
        context = {'messages' : messages, 'person' : person}
    return render(request, 'pages/messageboard.html', context)