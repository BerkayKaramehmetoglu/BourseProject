from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, f'Hoş Geldin *{username}* Başarıyla Giriş Yaptın')
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Kullanıcı Adı veya Şifre Yanlış')
            return redirect('giris')
    else:
        return render(request, 'user/giris.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.WARNING, 'Kullanıcı Adı Daha Önceden Alınmış')
                return redirect('kayit')
            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(request, messages.WARNING, 'E-Mail Daha Önceden Alınmış')
                    return redirect('kayit')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    messages.add_message(request, messages.SUCCESS, f'Aramıza Hoş Geldin *{username}* Giriş Sayfasına '
                                                                    f'Yönlendiriliyorsun')
                    user.save()
                    return redirect('giris')
        else:
            return redirect('kayit')
    else:
        return render(request, 'user/kayit.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.WARNING, 'Görüşmek Üzere Çıkış Yaptın')
        return redirect('index')
    return render(request, 'user/cikis.html')


