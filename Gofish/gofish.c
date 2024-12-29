#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_HAND_SIZE 7
#define MAX_LINE_SIZE 100
#define MAX_NAME_SIZE 100
#define MAX_CARDS 52
#define MAX_RANKS 13
#define MAX_SUITS 4
#define MAX_BOOKS 13 // Maximum number of books

// Define the card structure
typedef struct card {
    char rank;
    char suit;
} card;

// Define the player structure
typedef struct player {
    char name[MAX_NAME_SIZE];
    card hand[MAX_CARDS];
    int hand_size;
    int books[MAX_BOOKS]; // Store the number of books for each rank
    int book_count;       // Total number of books collected
} player;

// Function prototypes
void initialize_deck(card deck[]);
void shuffle_deck(card deck[]);
void deal_cards(card deck[], player players[], int num_players);
void print_hand(player *p);
void print_books(player *p);
int ask_for_card(player *asker, player *askee, char rank);
void go_fish(card deck[], int *deck_index, player *p, int player_num);
int check_books(player *p);
int game_over(card deck[], int deck_index, player players[], int num_players);
int has_card_of_rank(player *p, char rank);
void reset_players(player players[], int num_players);
char get_random_rank_from_hand(player *p);
void sort_hand(player *p); // New function to sort Player 1's hand
int get_rank_index(char rank);  // New function to get the index of a rank

// Main function
int main() {
    srand(time(NULL)); // Seed the random number generator

    int play_again = 1;
    while (play_again) {
        // Print shuffling message
        printf("Shuffling deck...\n");

        // Create the deck of cards
        card deck[MAX_CARDS];
        initialize_deck(deck);
        shuffle_deck(deck);

        int num_players = 2;

        // Create the players
        player players[num_players];
        strcpy(players[0].name, "Player 1"); // Player 1's name
        strcpy(players[1].name, "Player 2"); // Player 2's name
        players[0].hand_size = 0;
        players[0].book_count = 0;
        memset(players[0].books, 0, sizeof(players[0].books));

        players[1].hand_size = 0;
        players[1].book_count = 0;
        memset(players[1].books, 0, sizeof(players[1].books));

        // Deal the cards
        deal_cards(deck, players, num_players);

        // Initialize deck index
        int deck_index = num_players * MAX_HAND_SIZE;

        int player_num = 0; // Start with Player 1
        char rank;
        int turn_over = 0;

        while (!game_over(deck, deck_index, players, num_players)) {
            printf("\n%s's Hand - ", players[0].name);

            // Sort Player 1's hand before printing
            sort_hand(&players[0]);

            print_hand(&players[0]); // Show Player 1's hand only
            print_books(&players[0]);
            print_books(&players[1]);

            turn_over = 0;
            while (!turn_over) {
                if (player_num == 0) {
                    // Player 1's turn to ask for a card
                    printf("%s's turn, enter a Rank: ", players[player_num].name);
                    scanf(" %c", &rank);

                    if (!has_card_of_rank(&players[player_num], rank)) {
                        printf("Error - must have at least one card from rank to play\n");
                        continue;
                    }

                    int cards_transferred = ask_for_card(&players[0], &players[1], rank);
                    if (cards_transferred > 0) {
                        printf("    - Player 2 has %d %c's\n", cards_transferred, rank);
                        if (check_books(&players[0])) {
                            printf("    - Player 1 books %c\n", rank);
                        }
                    } else {
                        printf("    - Player 2 has no %c's\n", rank);
                        go_fish(deck, &deck_index, &players[0], player_num);
                        turn_over = 1; // Player 1's turn ends
                        printf("    - Player 2's turn\n");
                    }
                } else {
                    // Player 2's turn (randomly pick a rank from Player 2's hand)
                    rank = get_random_rank_from_hand(&players[1]);
                    printf("%s's turn, asks for Rank: %c\n", players[player_num].name, rank);

                    int cards_transferred = ask_for_card(&players[1], &players[0], rank);
                    if (cards_transferred > 0) {
                        printf("    - Player 1 has %d %c's\n", cards_transferred, rank);
                        if (check_books(&players[1])) {
                            printf("    - Player 2 books %c\n", rank);
                        }
                    } else {
                        printf("    - Player 1 has no %c's\n", rank);
                        go_fish(deck, &deck_index, &players[1], player_num);
                        turn_over = 1; // Player 2's turn ends
                        printf("    - Player 1's turn\n");
                    }
                }
            }

            // Next player's turn
            player_num = (player_num + 1) % num_players;
        }

        // Determine the winner
        printf("\nGame Over!\n");
        print_books(&players[0]);
        print_books(&players[1]);

        if (players[0].book_count > players[1].book_count) {
            printf("Player %s Wins!\n", players[0].name);
        } else if (players[1].book_count > players[0].book_count) {
            printf("Player %s Wins!\n", players[1].name);
        } else {
            printf("It's a tie!\n");
        }

        // Ask to play again
        char choice;
        printf("Do you want to play again [Y/N]: ");
        scanf(" %c", &choice);
        play_again = (toupper(choice) == 'Y');

        // Reset players if playing again
        if (play_again) {
            reset_players(players, num_players);
        }
    }

    printf("Exiting.\n");
    return 0;
}

// Initialize the deck of cards
void initialize_deck(card deck[]) {
    char ranks[MAX_RANKS] = "23456789TJQKA";
    char suits[MAX_SUITS] = "CDHS";
    int index = 0;
    for (int i = 0; i < MAX_RANKS; i++) {
        for (int j = 0; j < MAX_SUITS; j++) {
            deck[index].rank = ranks[i];
            deck[index].suit = suits[j];
            index++;
        }
    }
}

// Shuffle the deck of cards
void shuffle_deck(card deck[]) {
    for (int i = 0; i < MAX_CARDS; i++) {
        int j = rand() % MAX_CARDS;
        card temp = deck[i];
        deck[i] = deck[j];
        deck[j] = temp;
    }
}

// Deal the cards to the players
void deal_cards(card deck[], player players[], int num_players) {
    int index = 0;
    for (int i = 0; i < MAX_HAND_SIZE; i++) {
        for (int j = 0; j < num_players; j++) {
            players[j].hand[i] = deck[index];
            players[j].hand_size++;
            index++;
        }
    }
}

// Print the hand of a player (only for Player 1)
void print_hand(player *p) {
    for (int i = 0; i < p->hand_size; i++) {
        printf("%c%c ", p->hand[i].rank, p->hand[i].suit);
    }
    printf("\n");
}

// Sort a player's hand by rank (Player 1's hand will be sorted for display)
void sort_hand(player *p) {
    for (int i = 0; i < p->hand_size - 1; i++) {
        for (int j = i + 1; j < p->hand_size; j++) {
            if (p->hand[i].rank > p->hand[j].rank) {
                card temp = p->hand[i];
                p->hand[i] = p->hand[j];
                p->hand[j] = temp;
            }
        }
    }
}

// Print the books of a player
void print_books(player *p) {
    printf("%s's Book - ", p->name);
    char rank_map[] = "23456789TJQKA";  // Correct rank map for printing
    for (int i = 0; i < MAX_BOOKS; i++) {
        if (p->books[i]) {
            printf("%c ", rank_map[i]);  // Print the corresponding rank
        }
    }
    printf("\n");
}


// Ask for a card from another player and transfer the cards
int ask_for_card(player *asker, player *askee, char rank) {
    int count = 0;

    // Transfer matching cards from askee to asker
    for (int i = 0; i < askee->hand_size; i++) {
        if (askee->hand[i].rank == rank) {
            asker->hand[asker->hand_size] = askee->hand[i];
            asker->hand_size++;
            count++;

            // Remove card from askee's hand
            for (int j = i; j < askee->hand_size - 1; j++) {
                askee->hand[j] = askee->hand[j + 1];
            }
            askee->hand_size--;
            i--;
        }
    }

    return count;
}

// Draw a card from the deck
void go_fish(card deck[], int *deck_index, player *p, int player_num) {
    if (*deck_index >= MAX_CARDS) {
        printf("    - Deck is empty!\n");
        return;
    }

    // Player 1 (human)
    if (player_num == 0) {
        printf("    - Player %d Go Fish: ", player_num + 1);
        p->hand[p->hand_size] = deck[*deck_index];
        printf("%c%c\n", deck[*deck_index].rank, deck[*deck_index].suit); // Show the card picked by Player 1
    } else {
        // Player 2 (CPU)
        printf("    - Player %d Go Fish.\n", player_num + 1);
        p->hand[p->hand_size] = deck[*deck_index]; // Don't show the card picked by Player 2
    }

    p->hand_size++;
    (*deck_index)++;
}

int get_rank_index(char rank) {
    switch (rank) {
        case '2': return 0;
        case '3': return 1;
        case '4': return 2;
        case '5': return 3;
        case '6': return 4;
        case '7': return 5;
        case '8': return 6;
        case '9': return 7;
        case 'T': return 8;
        case 'J': return 9;
        case 'Q': return 10;
        case 'K': return 11;
        case 'A': return 12;
        default: return -1;  // Error case (shouldn't happen)
    }
}

int check_books(player *p) {
    int book_formed = 0;
    int rank_counts[MAX_RANKS] = {0};  // Array to store the count of each rank

    // Count the number of cards for each rank in the player's hand
    for (int i = 0; i < p->hand_size; i++) {
        int rank_index = get_rank_index(p->hand[i].rank);
        if (rank_index != -1) {
            rank_counts[rank_index]++;
        }
    }

    // Check if any rank has 4 cards (which means a book is formed)
    for (int i = 0; i < MAX_RANKS; i++) {
        if (rank_counts[i] == 4) {
            p->books[i] = 1;  // Mark the rank as booked
            p->book_count++;  // Increment the player's book count

            // Remove all cards of this rank from the player's hand
            for (int j = 0; j < p->hand_size;) {
                int rank_index = get_rank_index(p->hand[j].rank);
                if (rank_index == i) {
                    // Shift cards left to remove the booked card
                    for (int k = j; k < p->hand_size - 1; k++) {
                        p->hand[k] = p->hand[k + 1];
                    }
                    p->hand_size--;  // Decrease the hand size
                } else {
                    j++;  // Only increment if no card was removed
                }
            }

            printf("    - Player books %c\n", "23456789TJQKA"[i]);  // Announce the book formed
            book_formed = 1;
        }
    }

    return book_formed;
}


// Check if the game is over (when the deck is empty or a player has 7 or more books)
int game_over(card deck[], int deck_index, player players[], int num_players) {
    if (deck_index >= MAX_CARDS) {
        return 1; // Deck is empty
    }

    // Check if any player has at least 7 books
    for (int i = 0; i < num_players; i++) {
        if (players[i].book_count >= 7) {
            return 1; // A player has 7 or more books
        }
    }

    return 0;
}


// Check if a player has a card of the requested rank
int has_card_of_rank(player *p, char rank) {
    for (int i = 0; i < p->hand_size; i++) {
        if (p->hand[i].rank == rank) {
            return 1; // Player has at least one card of the rank
        }
    }
    return 0; // Player does not have the rank
}

// Get a random rank from the player's hand
char get_random_rank_from_hand(player *p) {
    int index = rand() % p->hand_size;
    return p->hand[index].rank;
}

// Reset players' hands, books, and counts for a new game
void reset_players(player players[], int num_players) {
    for (int i = 0; i < num_players; i++) {
        players[i].hand_size = 0;
        players[i].book_count = 0;
        memset(players[i].books, 0, sizeof(players[i].books));
    }
}
