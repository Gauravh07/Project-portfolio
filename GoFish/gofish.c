#include "deck.h"
#include "player.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    reset_player(&user);
    reset_player(&computer);
    srand(time(NULL));
    create_deck();
    shuffle();
    deal_player_cards(&user, &computer);

    struct player *current_player = &user;

    while (!game_over(&user) && !game_over(&computer)) {
        char rank;

        // Show Player 1's cards and books only at the start of Player 1's turn
        if (current_player == &user) {
            show_user_cards(&user); // Show Player 1's hand
            show_player_books(&user, &computer); // Show Player 1 and Player 2 books
            rank = user_play(current_player); // Get Player 1's input
        } else {
            rank = computer_play(current_player); // Player 2 (CPU) plays
        }

        // Determine the other player
        struct player *other_player = current_player == &user ? &computer : &user;

        // Check if the other player has the requested rank
        if (search(other_player, rank)) {
            // Correct guess: current player gets another turn
            printf("\t- Player %d guessed correctly and gets another turn\n", current_player == &user ? 1 : 2);
            Check_book(current_player, rank, 0);
        } else {
            // Handle "Go Fish"
            printf("\t- Player %d has no %c's\n", current_player == &user ? 2 : 1, rank);

            struct card *card = next_card();

            if (current_player == &user) {
                // Show the card drawn for Player 1
                printf("\t- Go Fish! Player 1 draws %c%c\n", card->rank, card->suit);
            } else {
                // Hide the card drawn for Player 2
                printf("\t- Go Fish! Player 2 draws a card\n");
            }

            // Add the drawn card to the current player's hand
            add_card(current_player, card);

            // Switch turns: the current player guessed wrong
            printf("\t- Player %d's turn\n\n", current_player == &user ? 2 : 1);
            current_player = other_player;
        }
    }

    // Check for game over and print the result
    if (game_over(&user)) {
        printf("Player 1 wins with 7 decks!\n");
    } else {
        printf("Player 2 wins with 7 decks!\n");
    }

    // Reset the players
    reset_player(&user);
    reset_player(&computer);

    return 0;
}
