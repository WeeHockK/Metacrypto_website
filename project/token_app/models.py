from django.db import models
# Create your models here.
from time import sleep
import requests
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Watchlist(models.Model):
    username = models.CharField(max_length=100)
    cryptoName = models.CharField(max_length=100)
    Targetprice = models.IntegerField()


def gnews_generate_news(search_term):
    auth_token = "1c4c9811a9b3a32a4f67218f9f28b93d"
    url = f"https://gnews.io/api/v4/search?q={search_term}&apikey={auth_token}"
    print(url)
    response = requests.get(url)
    response_json = response.json()
    # print(response_json)
    return response_json
    


if __name__ == '__main__':
    search_term = "bitcoin"
    j = gnews_generate_news(search_term)
    print(len(j['articles']))
    for i in j['articles']:
        print(i)    

class Crypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    exchange = models.CharField(max_length=50)
    coin = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    alerts = models.DecimalField(max_digits=10, decimal_places=2)\

class Exchange(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.exchange.name} ({self.rating})'



  