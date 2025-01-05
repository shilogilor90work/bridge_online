import random
import json
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from hands.models import Hand
from .forms import HandForm, JSONUploadForm, ExplanationForm  # Create a HandForm for handling form data


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
        if hand.cards:
            hand.cards = hand.cards.replace('\n', '\\n')
        if hand.bids:
            hand.bids = hand.bids.replace('\n', '\\n')
        if hand.explanation:
            hand.explanation = hand.explanation.replace('\n', '\\n')
        if hand.correct_answer:
            hand.correct_answer = to_symbol(hand.correct_answer.replace('\n', '\\n'))
        form = HandForm(instance=hand)
    return render(request, 'manage_hands/update_hand.html', {'form': form})


def update_explanation(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    print(request.method)
    if request.method == 'POST':
        # Create a form with only the fields we want to update
        form = ExplanationForm(request.POST, instance=hand)

        # Only update the 'correct_answer' and 'explanation' fields
        print(form.is_valid())
        print(form)
        if form.is_valid():
            hand.correct_answer = to_symbol(form.cleaned_data.get('correct_answer', hand.correct_answer))
            hand.explanation = form.cleaned_data.get('explanation', hand.explanation)

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


def update_answer(request, hand_id, answer, explaination):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        hand.correct_answer = to_symbol(answer)
        hand.explanation = explaination
        form = HandForm(request.POST, instance=hand)
        if form.is_valid():
            form.save()
            return redirect('manage:hand_list')  # Replace with the name of your success page or list view


def delete_hand(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        hand.delete()
        return redirect('manage:hand_list')  # Replace with the name of your success page or list view
    return render(request, 'manage_hands/delete_hand.html', {'hand': hand})


def hand_list(request):
    hands = list(Hand.objects.all())
    hands = [hand for hand in hands if '?' not in hand.correct_answer]
    random.shuffle(hands)
    return render(request, 'manage_hands/hand_list.html', {'hands': hands})


def hand_list_limit(request, limit):
    hands = list(Hand.objects.all())
    hands = [hand for hand in hands if '?' not in hand.correct_answer]
    random.shuffle(hands)
    return render(request, 'manage_hands/hand_list.html', {'hands': hands[:limit]})


def hand_list_no_shuffle(request):
    hands = list(Hand.objects.all())
    return render(request, 'manage_hands/hand_list.html', {'hands': hands})



def hand_list_no_answer_only(request):
    hands = list(Hand.objects.all())
    hands = [hand for hand in hands if '?' in hand.correct_answer]
    return render(request, 'manage_hands/hand_list.html', {'hands': hands})


def hand_list_no_shuffle_limit_and_start(request, start_point, end_point):
    hands = list(Hand.objects.all())
    return render(request, 'manage_hands/hand_list.html', {'hands': hands[start_point:end_point]})


def hand_list_no_shuffle_limit(request, limit):
    hands = list(Hand.objects.all())
    return render(request, 'manage_hands/hand_list.html', {'hands': hands[:limit]})


def upload_json_view(request):
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']

            try:
                # Load JSON data from the uploaded file
                data = json.load(json_file)

                # Process each entry in the JSON data
                for entry in data:
                    correct_answer_parts = entry["correctAnswer"].split(maxsplit=1)
                    correct_answer = correct_answer_parts[0]
                    explanation = correct_answer_parts[1] if len(correct_answer_parts) > 1 else ""

                    # Create and save a Hand instance
                    Hand.objects.create(
                        subject="Bridge Hand",
                        cards=entry["cards"],
                        bids=entry["bids"],
                        correct_answer=to_symbol(correct_answer),
                        explanation=explanation,
                        metadata={},  # Add metadata if required
                    )
                return HttpResponse("JSON data successfully uploaded and processed!")

            except json.JSONDecodeError:
                return HttpResponse("Invalid JSON file format.", status=400)
            except KeyError as e:
                return HttpResponse(f"Missing key in JSON: {e}", status=400)

    else:
        form = JSONUploadForm()

    return render(request, 'manage_hands/upload_json.html', {'form': form})


def display_hand(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    return render(request, 'manage_hands/hand_list.html', {'hands': [hand]})


def to_symbol(answer):
    bid = answer.strip().lower()

    if len(bid) != 2:
        return answer

    # Extract the level (number) and suit (letter) from the bid
    level = bid[0]  # All characters except the last
    suit = bid[1]    # Last character

    # Define a mapping of suit letters to symbols
    suit_symbols = {
        'c': '♣',  # Clubs
        'd': '♦',  # Diamonds
        'h': '♥',  # Hearts
        's': '♠',  # Spades
        'n': 'NT'  # No Trump
    }

    # Check if the level is a valid number
    if not level.isdigit():
        return answer

    # Check if the suit is valid
    if suit not in suit_symbols:
        return answer

    # Combine the level with the suit symbol
    return f"{level}{suit_symbols[suit]}"

