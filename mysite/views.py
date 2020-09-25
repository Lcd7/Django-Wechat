from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from mysite.forms import AddForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(a + b)
    else:
        form = AddForm()
    return render(request, 'mysite/index.html', {'form': form})
    
def add(request):               # add?a=1&b=2
    a = request.GET.get('a', 0) # request.GET 是一个字典
    b = request.GET.get('b', 0)
    c = int(a) + int(b)
    return HttpResponse(str(c))
    
def add2(request, num1, num2):  # add2/1/2/
    c = int(num1) + int(num2)
    return HttpResponse(c)
    
def old_add2_redirect(request, num1, num2):
    return HttpResponseRedirect(
        reverse('add2', args = (num1, num2))
    )
    