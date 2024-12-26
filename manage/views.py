import json

from django.shortcuts import render, get_object_or_404, redirect
from hands.models import Hand
from .forms import HandForm  # Create a HandForm for handling form data


def create_hand(request):
    if request.method == 'POST':
        form = HandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage:hand_list')  # Replace with the name of your success page or list view
    else:
        form = HandForm()
    return render(request, 'manage_hands/create_hand.html', {'form': form})


def update_hand(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        form = HandForm(request.POST, instance=hand)
        if form.is_valid():
            form.save()
            return redirect('manage:hand_list')  # Replace with the name of your success page or list view
    else:
        form = HandForm(instance=hand)
    return render(request, 'manage_hands/update_hand.html', {'form': form})


def delete_hand(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        hand.delete()
        return redirect('manage:hand_list')  # Replace with the name of your success page or list view
    return render(request, 'manage_hands/delete_hand.html', {'hand': hand})


def hand_list(request):
    hands = Hand.objects.all()
    return render(request, 'manage_hands/hand_list.html', {'hands': hands})
