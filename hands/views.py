from .forms import PracticeForm, DoneForm, AllCorrectForm
from hands.models import Hand, Competition
from django.shortcuts import render, get_object_or_404, redirect
import random
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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
    return render(request, 'hands/hand_list_needs_validation.html', {'hands': filtered_hands[:20]})


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


def remove_needs_validation(request, hand_id):
    hand = get_object_or_404(Hand, id=hand_id)
    if request.method == 'POST':
        # Create a form with only the fields we want to update
        form = AllCorrectForm(request.POST, instance=hand)

        # Only update the 'correct_answer' and 'explanation' fields
        if form.is_valid():
            if "needs_validation" in hand.metadata:
                del hand.metadata["needs_validation"]
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


def compete(request, competition_id):
    # Fetch the competition object or return a 404 if not found
    competition = get_object_or_404(Competition, id=competition_id)

    # Fetch the hands associated with the competition
    hands = competition.hands.all()
    hands_without_answers = hands.values('id', 'cards', 'bids', 'optional_bids', 'ns_vul', 'ew_vul')

    # Pass the competition and hands to the template
    context = {
        'competition': competition,
        'hands': hands_without_answers,
    }
    return render(request, 'hands/compete.html', context)


@csrf_exempt
def compete_submit(request, competition_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            answers = data.get('answers')

            if not username or not answers:
                return JsonResponse({'error': 'Username and answers are required.'}, status=400)

            # Get the competition instance
            competition = Competition.objects.get(id=competition_id)

            # If user_input exists, update it; if not, initialize as an empty dictionary
            user_input = competition.users_input or {}

            # Add the user's answers to the user_input dictionary
            user_input[username] = answers

            # Save the updated user_input back to the competition model
            competition.users_input = user_input
            competition.save()
            #None, None #
            password, hands = generate_password(request, competition_id)
            if password:  
                # Create a mutable copy of GET parameters
                query_params = request.GET.copy()

                # Add or update the 'username' parameter
                query_params['password'] = password

                # Pass the competition and hands to the template
                context = {
                    'competition': competition,
                    'hands': hands,
                    'users_input': competition.users_input,  # Added the users_input to context
                    'query_params': query_params,
                }
                return render(request, 'manage_competitions/competition_results.html', context)
            # Return a success response
            return JsonResponse({'message': 'Answers submitted successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
        except Competition.DoesNotExist:
            return JsonResponse({'error': 'Competition not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def generate_password(request, competition_id):
    
    # Fetch the competition object or return a 404 if not found
    competition = get_object_or_404(Competition, id=competition_id)
    password = request.GET.get('password')
    hands = competition.hands.all()
    password_hand = None
    lowest_id = 99999
    for hand in hands:
        if hand.metadata.get("password") and hand.id < lowest_id:
            lowest_id = hand.id
            password_hand = hand.metadata.get("password")
    if password_hand:
        return password_hand, hands
    else:
        new_password = str(random.randint(0, 999))
        hand = get_object_or_404(Hand, id=lowest_id)
    
        hand.metadata["password"] = new_password
        # Save the updated hand
        hand.save()
        return new_password, hands
    return None, hands
