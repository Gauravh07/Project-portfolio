#include <stdio.h>
#include "player.h"
#include "player.h"
#include "card.h"
#include <stdlib.h> // Ensure this is at the top



// Add a return statement in other non-void functions where applicable

/*
 * Instance Variables: user, computer   
 * ----------------------------------
 *  
 *  We only support 2 users: a human and a computer
 */
struct player user;
struct player computer;

// struct hand {
//     struct card* top;
//     struct hand* next;
// };

int add_card(struct player* target, struct card* new_card) {
    struct hand* new_hand = malloc(sizeof(struct hand));
    if (!new_hand) return -1; // Check for memory allocation failure
    
    new_hand->top = *new_card; // Copy card data
    new_hand->next = target->card_list; // Insert at the beginning
    target->card_list = new_hand; // Update card list
    target->hand_size++; // Increase hand size
    return 0; // Success
}



void remove_card(struct player* target, struct card* old_card) {
    struct hand** current = &target->card_list; // Pointer to pointer for easy removal
    while (*current != NULL) {
        // Change strcmp to direct character comparison if rank is char
        if ((*current)->top.rank[0] == old_card->rank[0]) { // Compare ranks
            struct hand* to_remove = *current; // Node to remove
            *current = (*current)->next; // Bypass the node to remove it
            free(to_remove); // Free the memory
            return; // Exit after removal
        }
        current = &((*current)->next); // Move to the next node
    }
}

char check_add_book(struct player* target) {
    if (target == NULL) {
        return 0;
    }
    for (int i = 0; i < target->hand_size; i++) {
        struct hand* current = target->card_list;
        struct hand* previous = NULL;
        int count = 0;
        while (current != NULL) {
            // Check if ranks are the same using direct character comparison
            if (current->top.rank[0] == current->top.rank[0]) {
                count++;
                if (previous == NULL) {
                    target->card_list = current->next;
                } else {
                    previous->next = current->next;
                }
                free(current);
                target->hand_size--;
            }
            previous = current;
            current = current->next;
        }
        if (count == 4) {
            for (int j = 0; j < 7; j++) {
                if (target->book[j] == 0) {
                    target->book[j] = current->top.rank[0]; // Assuming rank is char
                    return current->top.rank[0];
                }
            }
        }
    }
    return 0;
}

int search(struct player* target, char rank) {
    if (target == NULL) {
        return 0;
    }
    struct hand* current = target->card_list;
    while (current != NULL) {
        if (current->top.rank[0] == rank) { // Direct character comparison
            return 1;
        }
        current = current->next;
    }
    return 0;
}

int transfer_cards(struct player* src, struct player* dest, char rank) {
    if (src == NULL || dest == NULL) {
        return -1;
    }
    struct hand* current = src->card_list;
    struct hand* previous = NULL;
    while (current != NULL) {
        if (current->top.rank[0] == rank) { // Direct character comparison
            if (previous == NULL) {
                src->card_list = current->next;
            } else {
                previous->next = current->next;
            }
            add_card(dest, &(current->top));
            free(current);
            src->hand_size--;
            dest->hand_size++;
        }
        previous = current;
        current = current->next;
    }
    return 0;
}

int game_over(struct player* target) {
    if (target == NULL) {
        return 0;
    }
    for (int i = 0; i < 7; i++) {
        if (target->book[i] == 0) {
            return 0;
        }
    }
    return 1;
}

int reset_player(struct player* target) {
    if (target == NULL) {
        return -1;
    }
    struct hand* current = target->card_list;
    while (current != NULL) {
        struct hand* temp = current;
        current = current->next;
        free(temp);
    }
    target->card_list = NULL;
    target->hand_size = 0;
    for (int i = 0; i < 7; i++) {
        target->book[i] = 0;
    }
    return 0;
}

char computer_play(struct player* target) {
    if (target == NULL) {
        return 0;
    }
    struct hand* current = target->card_list;
    int count = 0;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    int random = rand() % count;
    current = target->card_list;
    for (int i = 0; i < random; i++) {
        current = current->next;
    }
    return current->top.rank[0]; // Assuming rank is char
}

char user_play(struct player* target) {
    if (target == NULL) {
        return 0;
    }
    char rank;
    int found = 0;
    while (found == 0) {
        printf("Please enter a rank: ");
        scanf(" %c", &rank);
        found = search(target, rank);
        if (found == 0) {
            printf("Error - must have at least one card from rank to play\n");
        }
    }
    return rank;
}

