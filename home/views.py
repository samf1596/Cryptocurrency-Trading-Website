from django.shortcuts import render
from django.http import HttpResponse
from home.models import Coins, Tweets

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def signin(request):
    return render(request, 'home/signin.html')

def register(request):
    return render(request, 'home/register.html')

def contact(request):
    return render(request, 'home/contact.html')

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        status = Coins.objects.filter(coin_name=search_query)
        coins = {"coins": status} #true or false
        return render(request, 'home/index.html', coins)

