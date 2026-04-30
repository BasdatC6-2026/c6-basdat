from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserAccount, AccountRole

def login_view(request):
    # login
    if request.method == 'POST':
        username_input = request.POST.get('email')
        password_input = request.POST.get('password')

        try:
            # validate
            user = UserAccount.objects.get(username=username_input, password=password_input)
            
            # retrieve role
            account_role = AccountRole.objects.filter(user=user).first()
            role_name = account_role.role.role_name if account_role else 'GUEST'

            # save session
            request.session['user_id'] = user.user_id
            request.session['username'] = user.username
            request.session['role'] = role_name
            
            return redirect('dashboard')
            
        except UserAccount.DoesNotExist:
            messages.error(request, "Email atau Password salah!")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
        
    context = {
        'role': request.session.get('role', 'GUEST'),
        'username': request.session.get('username')
    }
    return render(request, 'dashboard.html', context)