from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

class LoginView(TemplateView):
    template_name = 'login.html'
