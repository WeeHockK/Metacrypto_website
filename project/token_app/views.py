from django.shortcuts import render, redirect, get_object_or_404
from token_app.models import *
from typing import Dict, List, Tuple
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Crypto
from .forms import CryptoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Review, Exchange
from .forms import ReviewForm
import ccxt

def index_view(request):
    
    context = {}
    context['s1'] = 'string 1'
    
    list_of_values = [1,2,3,4]
    context['list_of_values'] = list_of_values
    
    
    return render(request, 'token_app/homepage.html', context)

def chart_view(request):
    context = {}
    
    return render(request, 'token_app/chart.html', context)

def news_view(request):    
    # GNewsAPI = GNewsAPI()
    
    # json_news = GNewsAPI.generate_news('crypto')
    # print(json_news)
    context = {}
    list_of_news = []
    
    search_term_1 = 'Coinbase'
    search_term_2 = 'Binance'
    json_news = gnews_generate_news(search_term_1)
    json_news_2 = gnews_generate_news(search_term_2)
    
    count = 0 
    
    for i in json_news['articles']:
        
        title_2 = json_news_2['articles'][count]['title']
        source_2 = json_news_2['articles'][count]['source']['name']
        source_2 = search_term_2
        
        publishedAt_2 = json_news_2['articles'][count]['publishedAt']
        description_2 = json_news_2['articles'][count]['description']
        url_2 = json_news_2['articles'][count]['url']
        image_2 = json_news_2['articles'][count]['image']
        
        i['source']['name'] = search_term_1
        i['title_2'] = title_2
        i['source_2'] = source_2
        i['publishedAt_2'] = publishedAt_2
        i['description_2'] = description_2
        i['url_2'] = url_2
        i['image_2'] = image_2
        
        list_of_news.append(i)
        if count <10:
            count = count + 1
    
    context['list_of_news'] = list_of_news
    
    return render(request, 'token_app/news.html', context)


def home_view(request):
    
    context = {}
    
    return render(request, 'token_app/homepage.html', context)

def exchangeDetail_view(request):
    context = {}
    return render(request, 'token_app/exchangeDetail.html', context)

def login_view(request):
    context={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome! {user.username}")
            return redirect('home_view')
        else:
            messages.error(request, "Login failed, please check...")
    return render(request, 'token_app/login.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            messages.success(request, f"Registration success! Welcome {user.username}")
            return redirect('home_view')
        else:
            messages.error(request, 'There was an error with your registration. Please try again. Your password must contain at least 8 characters and uses uppercase and lowercase letters, numbers and special symbols. ')
    else:
        form = UserCreationForm()
    return render(request, 'token_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    #messages.success("Log out success!")
    return redirect('home_view')

def cryptodata(request):
    apidata = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    return render(request, 'token_app/homepage.html',{'apidata':apidata})

def autocomplete(request):
    query = request.GET.get('term', '')
    max_suggestions = 5 # Set maximum number of suggestions to 10
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    symbols = [market['symbol'] for market in markets.values()]
    matches = [symbol for symbol in symbols if query.lower() in symbol.lower()]
    suggestions = []
    suggestions = matches[:max_suggestions]
    return JsonResponse(suggestions, safe=False)

def search_view(request):
    query = request.GET.get('query', '')
    # List of exchanges to check prices from
    exchanges = ['binance', 'blockchaincom', 'currencycom', 'bitcoincom', 'bitpanda', 'lykke', 'hollaex', 'bitopro', 'coinbasepro', 'kraken']
    print(query)
    # List to store the coins and their prices
    coins = []

    # Loop through each exchange and get the price of the coin
    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        ticker = exchange.fetch_ticker(query)
        price = ticker['last']
        coins.append({'symbol': exchange, 'price': price, 'name': exchange_id})

    # Sort the list of coins by price in ascending order
    coins = sorted(coins, key=lambda x: x['price'])

    # Render the search.html template with the list of coins
    return render(request, 'token_app/search.html', {'coins': coins[:5]})

@login_required(login_url='login_view', redirect_field_name='next')
def portfolio_view(request):
    cryptos = Crypto.objects.filter(user=request.user)
    return render(request, 'token_app/portfolio.html', {'cryptos': cryptos})

@login_required(login_url='login_view', redirect_field_name='next')
def crypto_create(request):
    if request.method == "POST":
        form = CryptoForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.user = request.user
            alert.save()
            return redirect('portfolio_view')

    form = CryptoForm()
    return render(request, 'token_app/add.html', {'form': form})

@login_required(login_url='login_view', redirect_field_name='next')
def crypto_update(request, pk):
    alert = get_object_or_404(Crypto, pk=pk, user=request.user)
    form = CryptoForm(request.POST or None, instance=alert)
    if form.is_valid():
        form.save()
        return redirect('portfolio_view')

    return render(request, 'token_app/update.html', {'form': form})

@login_required(login_url='login_view', redirect_field_name='next')
def crypto_delete(request, pk):
    alert = get_object_or_404(Crypto, pk=pk, user=request.user)
    if request.method == 'POST':
        alert.delete()
        return redirect('portfolio_view')

    return render(request, 'token_app/delete.html', {'alert': alert})

@login_required(login_url='login_view', redirect_field_name='next')
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            exchange_name = request.POST['exchange']
            print("exchange name is " + exchange_name)
            review.exchange = Exchange.objects.get(id=exchange_name)
            review.save()
            return redirect('reviews')
    else:
        return redirect('reviews')

def reviews(request):
    exchange = request.GET.get('exchange', 'binance')  # Default to 'Binance' if no exchange is selected
    selected_exchange = Exchange.objects.get(name=exchange)
    reviews = Review.objects.filter(exchange=selected_exchange)
    all_exchanges = Exchange.objects.all()
    form = ReviewForm()
    return render(request, 'token_app/view_review.html', {'exchange': exchange, 'Reviews': reviews, 'form': form, 'all_exchanges': all_exchanges})


