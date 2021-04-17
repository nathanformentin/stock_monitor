from django.shortcuts import render
#import importlib
#importlib.import_module('functions')
from django.views.decorators.csrf import csrf_exempt

from currency_checker.functions import *


@csrf_exempt

def index(request):
    stock_name = request.POST.get('stock')
    desired_currency = request.POST.get('desired_currency')
    try:
        stock_name = stock_name.upper()
        desired_currency = desired_currency.upper()
    except:
        pass
    response = obtain_values(stock_name,desired_currency)
    return render(request, 'index.html',
                    response)
        
        
