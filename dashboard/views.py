from django.shortcuts import render, redirect

def index(request):
    if 'id' not in request.session:
        return render(request, 'dashboard/index.html')
    else:
        username = request.session.get('username')
        return render(request, 'dashboard/index.html', {'username': username})
