from .forms import PracticeForm, DoneForm
from hands.models import Hand
from django.shortcuts import render, get_object_or_404, redirect
import random


def bridge_hand(request):
    return render(request, 'hands/bids_practice.html', locals())


def bridge_hand_labels(request):
    return render(request, 'hands/bids_practice_labels.html', locals())


def hands_by_user(request, user_name):
    hands = list(Hand.objects.all())
    hands = [hand for hand in hands if hand.correct_answer not in '?']
    filtered_hands = []
    for hand in hands:
        if "users_done_practice" in hand.metadata and user_name in hand.metadata["users_done_practice"]:
            continue
        filtered_hands.append(hand)
    random.shuffle(filtered_hands)
    return render(request, 'hands/hand_list_by_user.html', {'hands': filtered_hands[:20]})


def hands_that_need_validation(request):
    hands = list(Hand.objects.all())
    filtered_hands = []
    for hand in hands:
        if "needs_validation" in hand.metadata:
            filtered_hands.append(hand)
    return render(request, 'hands/hand_list_by_user.html', {'hands': filtered_hands[:20]})


def update_practice(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        # Create a form with only the fields we want to update
        form = PracticeForm(request.POST, instance=hand)

        # Only update the 'correct_answer' and 'explanation' fields
        if form.is_valid():
            if "users_need_practice" not in hand.metadata:
                hand.metadata["users_need_practice"] = [form.cleaned_data.get('user_name', "moshe")]
            else:
                hand.metadata["users_need_practice"].append(form.cleaned_data.get('user_name', "moshe"))
            # Save the updated hand
            hand.save()
            # Redirect back to the referring page
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('manage:hand_list')  # Fallback if no referer is provided

    else:
        form = HandForm(instance=hand)

    return render(request, 'manage_hands/update_hand.html', {'form': form})


def update_done(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        # Create a form with only the fields we want to update
        form = DoneForm(request.POST, instance=hand)

        # Only update the 'correct_answer' and 'explanation' fields
        if form.is_valid():
            if "users_done_practice" not in hand.metadata:
                hand.metadata["users_done_practice"] = [form.cleaned_data.get('user_name', "moshe")]
            else:
                hand.metadata["users_done_practice"].append(form.cleaned_data.get('user_name', "moshe"))
            # Save the updated hand
            hand.save()
            # Redirect back to the referring page
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('manage:hand_list')  # Fallback if no referer is provided

    else:
        form = HandForm(instance=hand)

    return render(request, 'manage_hands/update_hand.html', {'form': form})


def needs_validation(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        # Create a form with only the fields we want to update
        form = DoneForm(request.POST, instance=hand)

        # Only update the 'correct_answer' and 'explanation' fields
        if form.is_valid():
            if "needs_validation" not in hand.metadata:
                hand.metadata["needs_validation"] = [form.cleaned_data.get('user_name', "moshe")]
            else:
                hand.metadata["needs_validation"].append(form.cleaned_data.get('user_name', "moshe"))
            # Save the updated hand
            hand.save()
            # Redirect back to the referring page
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('manage:hand_list')  # Fallback if no referer is provided

    else:
        form = HandForm(instance=hand)

    return render(request, 'manage_hands/update_hand.html', {'form': form})
