const suits = ["♠", "♥", "♦", "♣"];
const ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
const hands = document.querySelectorAll(".hand");
const cardsContainer = document.querySelector(".cards");
let selectedHand = null;

// Define suit colors for both cards and player suit sections
const suitColors = {
  "♠": "black",
  "♥": "red",
  "♦": "orange",
  "♣": "green",
};

// Generate 52 cards
suits.forEach((suit) => {
  ranks.forEach((rank) => {
    const card = document.createElement("div");
    const suitColor = suitColors[suit]; // Get the color for the suit
    card.className = `card ${suitColor}`;
    card.textContent = `${rank}${suit}`;
    card.dataset.card = `${rank}${suit}`;
    card.dataset.suit = suit;
    cardsContainer.appendChild(card);
  });
});

// Assign colors to suit sections for each player
hands.forEach((hand) => {
  suits.forEach((suit) => {
    const suitSection = hand.querySelector(`.suit[data-suit="${suit}"]`);
    if (suitSection) {
      const suitColor = suitColors[suit]; // Get the color for the suit
      suitSection.classList.add(suitColor);
    }
  });
});

// Select a hand
hands.forEach((hand) => {
  hand.addEventListener("click", () => {
    console.log("hands")

    // Deselect all hands
    hands.forEach((h) => h.classList.remove("selected"));
    // Select the clicked hand
    hand.classList.add("selected");
    selectedHand = hand;
  });
});

// Assign card to the correct suit section in the selected hand
cardsContainer.addEventListener("click", (e) => {
  console.log("cards container")
  if (e.target.classList.contains("card") && !e.target.classList.contains("disabled")) {
    if (selectedHand) {
      const card = e.target.dataset.card;
      const rank = card.slice(0, -1); // Remove the last character (suit symbol)
      const suit = e.target.dataset.suit;
      const suitSection = selectedHand.querySelector(`.suit[data-suit="${suit}"]`);

      if (suitSection) {
        const cardElement = document.createElement("span");
        cardElement.textContent = rank; // Add only the rank
        cardElement.dataset.suit = suit; // Store the suit in a data attribute
//        console.log(selectedHand.id);
        cardElement.dataset.player = selectedHand.id;
        cardElement.addEventListener("click", handleCardClick);
        suitSection.appendChild(cardElement);

        // Disable the card
        e.target.classList.add("disabled");
      }
    } else {
      alert("Please select a player first!");
    }
  }
});

const playedCardsContainer = document.querySelector(".played-cards-container");

function handleCardClick(e) {
  const cardElement = e.target; // The span element clicked
  const rank = cardElement.textContent; // The rank of the clicked card
  const suit = cardElement.dataset.suit; // The suit of the clicked card
  const playerNumber = cardElement.dataset.player; // The player associated with the card

  // Remove the card from the suit section
  cardElement.remove();

  // Determine which player's box the card should go to (Example: using currentPlayer variable)
  const currentPlayerBox = document.querySelector(`#${playerNumber}-box`);

  // Create the card element to be placed inside the player's box
  const playedCardElement = document.createElement("div");
  playedCardElement.classList.add("card", suitColors[suit]);
  playedCardElement.textContent = `${rank}${suit}`; // Show full card (rank + suit)

  // Add the card to the correct player's box
  currentPlayerBox.appendChild(playedCardElement);

  playedCardElement.addEventListener("click", function () {
  console.log("playedCardElement")
      const cardElement = document.querySelector(`.card[data-card="${playedCardElement.textContent}"]`);
      if (cardElement && cardElement.classList.contains('disabled')) {
        // Remove the 'disabled' class
        cardElement.classList.remove('disabled');
      }
      playedCardElement.remove();

  });
}

function addBiddingRow() {
  // Get the bidding rows container
  const biddingRowsContainer = document.querySelector('.bidding-rows');
     console.log(biddingRowsContainer);
  // Create a new row
  const newRow = document.createElement('div');
  newRow.classList.add('bidding-row');

  // Create 4 input elements for the row
  for (let i = 0; i < 4; i++) {
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Pass';
    newRow.appendChild(input);
  }

  // Append the new row to the container
  biddingRowsContainer.appendChild(newRow);
}