#ifndef GOFISH_H
#define GOFISH_H

struct card; // Forward declaration
struct player;
// Function prototypes
void shuffle_deck();
void player_turn(struct player* current_player, struct player* opponent);
void computer_turn(struct player* current_player, struct player* opponent);
int check_for_books(struct player* current_player);
struct card* find_cards(struct player* opponent, int rank);
void display_winner(struct player* user, struct player* computer);

#endif
