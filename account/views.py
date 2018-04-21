from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from home.models import Coins, Tweets, UserTransactions, UserBalance

def account(request):
    if not request.user.is_authenticated:    
        return render(request,"home/login.html",{"message": "Enter username and password"})
    else:
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')
        else:
            context = {
                "user": request.user
            }
            return render(request,'account/user.html',context)

def signedinhome(request):
    return render(request, 'account/signedinhome.html')

def about(request):
    return render(request, 'account/about.html')

def contact(request):
    return render(request, 'account/contact.html')

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        status = Coins.objects.filter(coin_name=search_query)
        coins = {"coins": status} #true or false
        return render(request, 'account/signedinhome.html', coins)

def logout_view(request):
        logout(request)
        return render(request,"home/login.html",{"message": "Logged out"})

def buy(request):
    curr_amount = 0
    if request.method == 'POST':
        print("hit")
        username = request.user.username
        buy_amount = request.POST.get('buy_box', "")
        ticker = request.POST.get('ticker_box', "")
        transaction, created = UserTransactions.objects.get_or_create(username=username, ticker=ticker, defaults={"amount": buy_amount})
        curr_amount = created
        if created:
            pass # means new transaction, so amount set
        else:
            curr_amount = UserTransactions.objects.get(username=username, ticker=ticker)
            print(curr_amount)
            UserTransactions.objects.filter(username=username, ticker=ticker).update(amount=float(buy_amount)+float(curr_amount.amount))

    return render(request, 'account/signedinhome.html', {"curr_amounts": {"amount": float(buy_amount)+float(curr_amount.amount), "ticker": ticker}})