# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(req):
    return render(req, 'users/index.html')

def create(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/')
    User.objects.create(first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password= bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt()))
    return redirect('/')

def login(req):
    tempUser = User.objects.get(email = req.POST['email'])
    if bcrypt.checkpw(req.POST['password'].encode(), tempUser.password.encode()) == True:
        context = {
            'user': User.objects.get(id = tempUser.id)
        }
        return render(req, 'users/sucess.html', context)
    return redirect('/')