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
    # run_once()
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

#
# def run_once():
#     with open('/home/rhizome/Desktop/shilo_bridge/bridge_online/data.json', 'r') as file:
#         json_data = json.load(file)
#
#     # Insert data into the database
#     for entry in json_data:
#         # Split the correctAnswer into correct_answer and explanation
#         correct_answer_parts = entry["correctAnswer"].split(maxsplit=1)
#         correct_answer = correct_answer_parts[0]  # The first word
#         explanation = correct_answer_parts[1] if len(correct_answer_parts) > 1 else ""  # The rest of the sentence
#
#         # Create and save the Hand instance
#         hand = Hand(
#             subject="Bridge Hand",  # Use a default subject or customize if needed
#             cards=entry["cards"],
#             bids=entry["bids"],
#             correct_answer=correct_answer,
#             explanation=explanation,
#             metadata={},  # Optional: Populate with any additional data if necessary
#         )
#         hand.save()
#
#     print("Data inserted successfully!")
