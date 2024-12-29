#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "gofish.h"
#include "deck.h"
#include "player.h"
#include "card.h"

struct deck deck_instance;

struct player user = {NULL, {0}, 0};    // Initialize user player
struct player computer = {NULL, {0}, 0}; // Initialize computer player

void initialize_game() {
    printf("Shuffling deck...\n");
    shuffle(); // Make sure this function initializes and shuffles the deck
    deal_player_cards(&user); // Deal cards to players

}

void display_hand(struct player* target) {
    if (!target || !target->card_list) {
        printf("Player's Hand - (empty)\n");
        return;
    }

    struct hand* current = target->card_list;
    printf("Player's Hand - ");
    
    while (current) {
        // Print the card details
        printf("%s %d ", processRank(current->top.rank), current->top.suit); 
        current = current->next; // Move to the next card
    }
    printf("\n");
}

void display_books(struct player* target) {
    printf("Player %s's Book - ", (target == &user) ? "1" : "2");
    
    for (int i = 0; i < 7; i++) {  // Assuming max of 7 unique ranks
        if (target->book[i] != 0) {
            printf("%d ", target->book[i]);
        }
    }
    printf("\n");
}

// Function to check if a player has won (for example, if they have 7 books)
int check_victory(struct player* user, struct player* computer) {
    int user_books = 0; // Assume you will track the number of books
    int computer_books = 0; // Same for the computer

    // Count books for the user
    user_books = check_for_books(user);
    computer_books = check_for_books(computer);

    // Check victory conditions
    if (user_books >= 7) {
        return 1; // User wins
    } else if (computer_books >= 7) {
        return 2; // Computer wins
    }

    return 0; // No winner yet
}

// Function to check for books in the current player's hand
int check_for_books(struct player* current_player) {
    int book_count = 0; // Count of books for the current player
    struct hand* current = current_player->card_list; // Pointer to the player's hand

    // Array to count occurrences of each rank (2-10, J, Q, K, A)
    int rank_count[13] = {0}; // 0-12 index corresponds to 2-10, J, Q, K, A

    while (current) {
        // Determine the rank index for the card
        char* rank = current->top.rank;

        // Convert the rank to an index (adjust as necessary for your rank system)
        int index;
        if (strcmp(rank, "A") == 0) index = 12;
        else if (strcmp(rank, "K") == 0) index = 11;
        else if (strcmp(rank, "Q") == 0) index = 10;
        else if (strcmp(rank, "J") == 0) index = 9;
        else if (strcmp(rank, "10") == 0) index = 8;
        else index = atoi(rank) - 2; // Ranks 2-9 correspond to indexes 0-7

        rank_count[index]++;
        
        // Check if four cards of the same rank have been collected
        if (rank_count[index] == 4) {
            book_count++;
            // Optionally, you can remove those cards from the player's hand here
        }

        current = current->next; // Move to the next card in the hand
    }

    return book_count; // Return the number of books found
}

struct card* find_cards(struct player* opponent, int rank) {
    struct card* found_cards = NULL;
    struct hand* current = opponent->card_list;

    while (current) {
        if (atoi(current->top.rank) == rank || 
            (strcmp(current->top.rank, "J") == 0 && rank == 11) ||
            (strcmp(current->top.rank, "Q") == 0 && rank == 12) ||
            (strcmp(current->top.rank, "K") == 0 && rank == 13) ||
            (strcmp(current->top.rank, "A") == 0 && rank == 14)) {
            struct card* new_card = malloc(sizeof(struct card));
            if (new_card) {
                *new_card = current->top; // Copy card data
                new_card->next = found_cards; // Insert at the beginning
                found_cards = new_card; // Update found_cards
            }
        }
        current = current->next; // Move to the next card
    }
    return found_cards; // Return found cards or NULL
}

void player_turn(struct player* current_player, struct player* opponent) {
    int rank;
    char input[3];

    // Display current player's hand and book
    display_hand(current_player);
    display_books(current_player);

    printf("Player %s's turn, enter a Rank: ", (current_player == &user) ? "1" : "2");
    fgets(input, sizeof(input), stdin);
    rank = atoi(input);

    // Check if the current player has at least one card of the requested rank
    if (search(current_player, rank)) {
        printf("Error - must have at least one card from rank to play\n");
        return; // End the turn if invalid
    }

    // Check if opponent has cards of the requested rank
    struct card* found_cards = find_cards(opponent, rank);
    if (found_cards) {
        printf("    - Player %s has ", (opponent == &user) ? "1" : "2");
        struct card* current_card = found_cards;
        while (current_card) {
            printf("%s%c ", current_card->rank, current_card->suit); // Display found cards
            current_card = current_card->next; // Move to the next found card
        }
        printf("\n");

        // Move cards from opponent to current player and check for books
        while (found_cards) {
            struct card* temp = found_cards; // Temporary store to keep track of the card
            add_card(current_player, found_cards); // Add the found card to the current player's hand
            found_cards = found_cards->next; // Update to the next found card
            remove_card(opponent, temp); // Remove the card from opponent's hand
            check_for_books(current_player); // Check for books
            free(temp); // Free the memory of the moved card
        }
    } else {
        printf("    - Player %s has no %ds\n", (opponent == &user) ? "1" : "2", rank);
        printf("    - Go Fish, Player %s draws ", (current_player == &user) ? "1" : "2");
        struct card* drawn_card = next_card(); // Draw a card from the deck
        if (drawn_card) {
            add_card(current_player, drawn_card); // Add the drawn card to the player's hand
            printf("%s%c\n", drawn_card->rank, drawn_card->suit); // Display the drawn card
        } else {
            printf("no more cards!\n");
        }
    }

    // Check if the current player has made a book after their turn
    int books_count = check_for_books(current_player);
    if (books_count > 0) {
        printf("    - Player %s books %d\n", (current_player == &user) ? "1" : "2", books_count);
    }
}

void free_hand(struct hand* hand) {
    struct hand* current = hand;
    while (current) {
        struct hand* temp = current;
        current = current->next;
        free(temp); // Free each node
    }
}

void cleanup() {
    free_hand(user.card_list);
    free_hand(computer.card_list);
}

int main() {
    char play_again;

    do {
        initialize_game();

        while (1) {
            player_turn(&user, &computer);
            if (check_victory(&user, &computer) == 1) {
                printf("Player 1 Wins!\n");
                break;
            }

            player_turn(&computer, &user);
            if (check_victory(&user, &computer) == 2) {
                printf("Player 2 Wins!\n");
                break;
            }
        }

        printf("Do you want to play again [Y/N]: ");
        scanf(" %c", &play_again);
        getchar(); // Consume the newline character left by scanf

        cleanup(); // Clean up before next game

    } while (play_again == 'Y' || play_again == 'y');

    printf("Exiting.\n");
    return 0;
}
