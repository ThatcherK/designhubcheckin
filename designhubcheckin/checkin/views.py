from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .forms import LoginForm, SearchForm, AddForm, EditVisitorForm
from .models import Visitors
# Create your views here.



def index(request):
    form = LoginForm()
    context = {
        "form": form
    }
    return render(request,'checkin/index.html',context)

def login(request):
    visitors_list = Visitors.objects.all()
    search_form = SearchForm()
    add_form = AddForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                search_form = SearchForm()
                add_form = AddForm()
                visitors_list = Visitors.objects.all()
                return render(request,'checkin/mainpage.html',{'form': search_form, 'addform':add_form, 'visitors_list':visitors_list})
            else:
                pass

        else:
            form = LoginForm()
            context = {
                        "form": form
                        }
            return render(request,'checkin/index.html',context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('visitor_name')
            visitor = get_object_or_404(Visitors, name=name)
            if visitor is not None:                
                visitor_id = visitor.id
                editing_form = EditVisitorForm()
                return render(request, 'checkin/visitors.html',{'visitor':visitor, 'editform': editing_form})

def add_new_visitor(request):
    visitors_list = Visitors.objects.all()
    search_form = SearchForm()
    add_form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST)
        print(form)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            company = form.cleaned_data.get('company')
            temperature = form.cleaned_data.get('temperature')
            identification_number = form.cleaned_data.get('identification_number')
            telephone_number = form.cleaned_data.get('telephone_number')
            # date = form.cleaned_data.get('date')
            visitor = Visitors(name=name, company=company,temperature=temperature, identification_number=identification_number,telephone_number=telephone_number)
            visitor.save()
            return render(request,'checkin/mainpage.html',{'form': search_form, 'addform':add_form, 'visitors_list':visitors_list})

        else:
            print(form.errors)
            
            return HttpResponse("error")

def check_in_returning_visitor(request, visitor_id):
    if request.method == 'POST':
        form = EditVisitorForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data.get('date'))
            visitor = Visitors.objects.get(pk=visitor_id)
            if visitor is not None:
                date = form.cleaned_data.get('date')
                temperature = form.cleaned_data.get('temperature')
                visitor.date = date
                visitor.temperature = temperature
                visitor.save()
                return render(request,'checkin/mainpage.html',{'form': search_form, 'addform':add_form, 'visitors_list':visitors_list})
        else:
            form = EditVisitorForm()
            return HttpResponse( 'invalid inputs')
