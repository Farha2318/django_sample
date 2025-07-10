from django.shortcuts import render

def crypto_view(request):
    return render(request, 'crypto/crypto.html')

