#include "deck.h"
#include "player.h"
#include <stdio.h>
#include <stdlib.h>

/*
 * Variable: deck_instance
 * -----------------------
 *
 * Go Fish uses a single deck
 */

struct deck deck_instance;

/*
 * Function: print_deck
 * --------------------
 *
 * This function prints the deck of cards
 */
void print_deck() {
  int i;
  for (i = 0; i < 52; i++) {
    printf("%d %d\n", deck_instance.cards[i].suit, deck_instance.cards[i].rank);
  }
}

/*
 * Function: create_deck
 * ---------------------
 *
 * This function creates a deck of cards
 */
void create_deck() {
  char suits[4] = {'C', 'D', 'H', 'S'};
  char ranks[13] = {'A', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'T', 'J', 'Q', 'K'};
  int i, j, k = 0;
  for (i = 0; i < 4; i++) {
    for (j = 1; j <= 13; j++) {
      deck_instance.cards[k].suit = suits[i];
      deck_instance.cards[k].rank = ranks[j - 1];
      k++;
    }
  }
  deck_instance.top_card = 51;
}

/*
 * Function: shuffle_deck
 * ----------------------
 *
 * This function shuffles the deck of cards
 */
int shuffle() {
  int i, j;
  struct card temp;
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  for (i = 51; i > 0; i--) {
    j = rand() % (i + 1);
    temp = deck_instance.cards[i];
    deck_instance.cards[i] = deck_instance.cards[j];
    deck_instance.cards[j] = temp;
  }
  printf("Shuffling deck...\n");
  return 0;
}

/*
 * Function: distribute_cards
 * --------------------------
 *
 * This function distributes the cards to the players
 */
int deal_player_cards(struct player *player1, struct player *player2) {
  player1->card_list = NULL;
  player2->card_list = NULL;
  int i;
  for (i = 0; i < 7; i++) {
    add_card(player1, next_card());
    add_card(player2, next_card());
  }
  return 0;
}

/*
 * Function: next_card
 * -------------------
 *
 * This function returns the next card from the deck
 */
struct card *next_card() {
  deck_instance.top_card--;
  return &deck_instance.cards[deck_instance.top_card + 1];
}

/*
 * Function: deck_size()
 * --------------------
 *
 * This function prints the hand of cards
 */
size_t deck_size() { return deck_instance.top_card + 1; }
