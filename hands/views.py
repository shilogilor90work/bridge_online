from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Hand
from django.http import HttpResponseRedirect

class HandsView(generic.ListView):
    template_name = 'hands/bids_practice.html'
