from django.contrib import admin
from .models import Watchlist
from. models import Crypto
from. models import Review
from .models import Exchange

# Register your models here.
admin.site.register(Watchlist)
admin.site.register(Crypto)
admin.site.register(Review)
admin.site.register(Exchange)