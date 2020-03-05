from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		url = "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_332a32e0ec8e40e78b2927fbb55992fd"
		api_request = requests.get(url)

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error"
		return render(request, 'home.html', {'api': api})
	
	else:
		return render(request, 'home.html', {'ticker': "Enter a ticker symbol above to view its quote."})

	
def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		# TBD - to catch empty post, otherwise it will crash

		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added"))
			return redirect('add_stock')
	else:
		tickers = Stock.objects.all()
		output = []
		for ticker in tickers:
			url = "https://cloud.iexapis.com/stable/stock/" + str(ticker) + "/quote?token=pk_332a32e0ec8e40e78b2927fbb55992fd"
			api_request = requests.get(url)

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error"

		return render(request, 'add_stock.html', {'tickers': tickers, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted"))
	return redirect(delete_stock)

def delete_ticker(request, ticker):
	item = Stock.objects.get(ticker=ticker)
	item.delete()
	messages.success(request, ("Stock " + ticker + " has been deleted!"))
	return redirect(add_stock)


def delete_stock(request):
	tickers = Stock.objects.all()
	return render(request, 'delete_stock.html', {'tickers': tickers})

