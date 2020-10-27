from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .forms import LoginForm, SearchForm, AddForm, EditVisitorForm
from .models import Visitors, Register
from django.utils import timezone
import datetime

def index(request):
    form = LoginForm()
    context = {
        "form": form
    }
    return render(request,'checkin/index.html',context)

def login(request):
    visitors_list = Register.objects.all()
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
    visitors_list = Register.objects.all()
    search_form = SearchForm()
    add_form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            company = form.cleaned_data.get('company')
            temperature = form.cleaned_data.get('temperature')
            identification_number = form.cleaned_data.get('identification_number')
            telephone_number = form.cleaned_data.get('telephone_number')
            try:
                visitor_check = Visitors.objects.get(name=name)
                return HttpResponse("Visitor already exists")
            except Visitors.DoesNotExist:

                visitor = Visitors(name=name, company=company, identification_number=identification_number,telephone_number=telephone_number)
                visitor.save()
                registered_visitor = Register(visitor=visitor, temperature=temperature)
                registered_visitor.save()
                return render(request,'checkin/mainpage.html',{'form': search_form, 'addform':add_form, 'visitors_list':visitors_list})      
        else:
            
            return HttpResponse("error")

def check_in_returning_visitor(request, visitor_id):
    visitors_list = Register.objects.all()
    search_form = SearchForm()
    add_form = AddForm()
    if request.method == 'POST':
        form = EditVisitorForm(request.POST)
        
        if form.is_valid():
            visitor = Visitors.objects.get(pk=visitor_id)
            if visitor is not None:
                temperature = form.cleaned_data.get('temperature')
                registered_visitor = Register.objects.get(visitor=visitor)
                registered_visitor.temperature = temperature
                registered_visitor.save()
                return render(request,'checkin/mainpage.html',{'form': search_form, 'addform':add_form, 'visitors_list':visitors_list})
        else:
            form = EditVisitorForm()
            return HttpResponse( 'invalid inputs')
