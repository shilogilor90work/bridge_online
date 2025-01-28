from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from games.forms import GameForm
from games.models import Game
from django.http import HttpResponseRedirect
from django.views.generic import FormView, UpdateView, DeleteView, ListView

player_cards_options = [
    "n_cards_s", "n_cards_h", "n_cards_d", "n_cards_c",
    "e_cards_s", "e_cards_h", "e_cards_d", "e_cards_c",
    "s_cards_s", "s_cards_h", "s_cards_d", "s_cards_c",
    "w_cards_s", "w_cards_h", "w_cards_d", "w_cards_c"
]


class GameListView(ListView):
    model = Game
    template_name = 'manage_games/game_list.html'
    context_object_name = 'games'


def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('games:game-list'))
    else:
        initial_data = {f"round_{i}": {"start": "n", "n": "5C", "e": "6C", "s": "7C", "w": "8C"} for i in range(1, 14)}
        initial_data.update({player_cards_option: "A K Q T" for player_cards_option in player_cards_options})
        initial_data["subject"] = "test"
        initial_data["dealer"] = "n"
        initial_data["bids"] = ["Pass", "1C", "Pass", "Pass", "Pass"]
        form = GameForm(initial=initial_data)  # Pre-fill the form with default data
    return render(request, 'manage_games/game_form.html', {'form': form})


class GameUpdateView(UpdateView):
    model = Game
    fields = '__all__'
    template_name = 'manage_games/game_form.html'
    success_url = reverse_lazy('manage:game-list')


class GameDeleteView(DeleteView):
    model = Game
    template_name = 'manage_games/game_confirm_delete.html'
    success_url = reverse_lazy('manage:game-list')

