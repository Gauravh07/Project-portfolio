#ifndef CARD_H
#define CARD_H

/*
  Valid suits: C, D, H, and S
  Valid ranks: 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A
*/

//char processRank(char *rank);

struct card {
    char rank[3];  // Use a character array to store ranks like "5", "J", etc.
    char suit;     // Use a character for suit (e.g., 'S' for Spades, 'H' for Hearts)
    struct card* next; // Pointer to the next card (if you're using a linked list)
};
/*
  Linked list of cards in hand.
    top: first card in hand
    next: pointer to next card in hand
*/
struct hand {
    struct card top; // The card data
    struct hand* next; // Pointer to the next card
};

#endif
