#include "deck.h"
#include <stdio.h>  // Ensure this is at the top
#include <stdlib.h>

/*
 * Variable: deck_instance
 * -----------------------
 *  
 * Go Fish uses a single deck
 */

// struct card
// {
//   char suit;
//   char rank[2];
// };


// struct deck {

//     struct card list[52];

//     int top_card;

// };

struct deck deck_instance;

/*
 * Function: shuffle
 * --------------------
 *  Initializes deck_instance and shuffles it.
 *  Resets the deck if a prior game has been played.
 * 
 *  returns: 0 if no error, and non-zero on error
 */ 
int shuffle()
{
    // Initialize the deck
    int i = 0;
    for (int suit = 0; suit < 4; suit++) {
        for (int rank = 1; rank < 14; rank++) {
            deck_instance.list[i].suit = suit;
            snprintf(deck_instance.list[i].rank, sizeof(deck_instance.list[i].rank), "%d", rank);
            i++;
        }
    }
    deck_instance.top_card = 51;

    // Shuffle the deck
    for (int i = 0; i < 52; i++) {
        int j = rand() % 52;
        struct card temp = deck_instance.list[i];
        deck_instance.list[i] = deck_instance.list[j];
        deck_instance.list[j] = temp;
    }
    return 0;
}

/*
 * Function: deal_player_cards
 * ---------------------------
 *  Deal 7 random cards to the player specified in the function.
 *  Remove the dealt cards from the deck. 
 *
 *  target: pointer to the player to be dealt cards
 *
 *  returns: 0 if no error, and non-zero on error
 */
int deal_player_cards(struct player* target)
{
    if (target == NULL) {
        return -1;
    }
    for (int i = 0; i < 7; i++) {
        struct card* new_card = next_card();
        if (new_card == NULL) {
            return -1;
        }
        add_card(target, new_card);
    }
    return 0;
}

/*
 * Function: next_card
 * -------------------
 *  Return a pointer to the top card on the deck.
 *  Removes that card from the deck. 
 *
 *  returns: pointer to the top card on the deck.
 */
struct card* next_card( )
{
    if (deck_instance.top_card < 0) {
        return NULL;
    }
    struct card* top_card = &deck_instance.list[deck_instance.top_card];
    deck_instance.top_card--;
    return top_card;
}

/*
 * Function: size
 * --------------
 *  Return the number of cards left in the current deck.
 *
 *  returns: number of cards left in the deck.
 */
size_t deck_size( )
{
    return deck_instance.top_card + 1;
}

struct card drawCard(struct player* user, struct player* computer){
    
    if(deckState(user, computer) == 0){
        int j = rand() % (deck_instance.top_card + 1);
        struct card dealCard = deck_instance.list[j];
        // Remove the drawn card from the deck
        for (int i = j; i < deck_instance.top_card; i++) {
            deck_instance.list[i] = deck_instance.list[i + 1];
        }
        deck_instance.top_card--;
        return dealCard;
    }
    exit(EXIT_FAILURE);
}

int deckState(struct player* user, struct player* computer) {
    // Check if the deck is empty by checking the top card index
    return deck_instance.top_card < 0 ? -1 : 0; // Return -1 if empty
}

char processRank(char rank) {
    char temp;
    
    switch (rank) {
        case 1: 
            temp = '0';
            break;
        case 2: 
            temp = '1';
            break;
        case 3: 
            temp = '2';
            break;
        case 4: 
            temp = '3';
            break;
        case 5: 
            temp = '4';
            break;
        case 6: 
            temp = '5';
            break;
        case 7: 
            temp = '6';
            break;
        case 8: 
            temp = '7';
            break;
        case 9: 
            temp = 'T';
            break;
        case 10: 
            temp = 'J';
            break;
        case 11: 
            temp = 'Q';
            break;
        case 12: 
            temp = 'K';
            break;
        case 13: 
            temp = 'A';
            break;
        default: return -1;  // Error case (shouldn't happen)
    }

    return rank;

}
