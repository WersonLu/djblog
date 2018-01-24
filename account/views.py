from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoainForm


def user_login(request):
    if request.method == 'POST':
        form = LoainForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse('错误的帐号')
            else:
                return HttpResponse('已经登录')
    else:
        form = LoainForm()
    return render(request, 'account/login.html', {'form': form})
# def contact(request):
#     return render(request, 'blog/contact.html', context={
#         'welcome': '足下的到访使小站蓬荜生辉'
#     })