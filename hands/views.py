from django.shortcuts import render


def bridge_hand(request):
    return render(request, 'hands/bids_practice.html', locals())


def bridge_hand_labels(request):
    return render(request, 'hands/bids_practice_labels.html', locals())
