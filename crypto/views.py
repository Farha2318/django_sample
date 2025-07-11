from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Portfolio
from .serializers import PortfolioSerializer
import requests

# ✅ HTML View (for your frontend WebSocket crypto page)
def crypto_view(request):
    return render(request, 'crypto/crypto.html')

# ✅ CRUD API for Portfolio
class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ✅ Summary API: Total investment, profit/loss, per coin breakdown
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_summary(request):
    user = request.user
    portfolio = Portfolio.objects.filter(user=user)
    summary = {}
    total_investment = 0
    total_current_value = 0

    prices = get_live_prices()

    for item in portfolio:
        symbol = item.coin_name.upper() + 'USDT'
        live_price = float(prices.get(symbol, 0))
        current_value = item.quantity * live_price
        investment = item.quantity * item.buy_price

        total_investment += investment
        total_current_value += current_value

        if item.coin_name not in summary:
            summary[item.coin_name] = {
                'quantity': 0,
                'investment': 0,
            }
        summary[item.coin_name]['quantity'] += item.quantity
        summary[item.coin_name]['investment'] += investment

    for coin, data in summary.items():
        symbol = coin.upper() + 'USDT'
        live_price = float(prices.get(symbol, 0))
        data['average_buy'] = round(data['investment'] / data['quantity'], 2)
        data['live_rate'] = live_price
        data['current_value'] = round(data['quantity'] * live_price, 2)
        data['profit_loss'] = round(data['current_value'] - data['investment'], 2)

    return Response({
        'total_investment': round(total_investment, 2),
        'total_current_value': round(total_current_value, 2),
        'total_profit_loss': round(total_current_value - total_investment, 2),
        'summary': summary,
    })

# ✅ Helper function to fetch live prices
def get_live_prices():
    url = "https://api.coindcx.com/exchange/ticker"
    result = {}
    try:
        response = requests.get(url)
        data = response.json()
        for coin in ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT']:
            for entry in data:
                if entry['market'] == coin:
                    result[coin] = entry['last_price']
    except:
        result = {}
    return result
