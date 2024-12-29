#ifndef PLAYER_H
#define PLAYER_H
#include "card.h"
#include <stdio.h>
struct card;  // Forward declaration

struct player {
    struct hand* card_list; // Ensure this is initialized properly
    char book[7];
    int hand_size; // Hand size is updated when cards are added/removed
};


// Function prototypes
int add_card(struct player* target, struct card* new_card);
void remove_card(struct player* target, struct card* old_card);
char check_add_book(struct player* target);
int search(struct player *target, char rank);
int transfer_cards(struct player *src, struct player *dest, char rank);
int game_over(struct player *target);
int reset_player(struct player *target);
char computer_play(struct player *target);
char processRank(char rank);
int check_victory(struct player* user, struct player* computer);

#endif
