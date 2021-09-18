from django.shortcuts import render
from accounts.models import User


def about_us(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'about_us.html', context=context)
