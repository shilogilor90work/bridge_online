from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Hand
from django.http import HttpResponseRedirect


def bridge_hand(request):
    return render(request, 'hands/bids_practice.html', locals())
