#include "player.h"
#include <stdio.h>
#include <string.h>

struct player user;
struct player computer;

int add_card(struct player *target, struct card *new_card) {
    struct hand *new_hand = (struct hand *)malloc(sizeof(struct hand));
    new_hand->top = *new_card;
    new_hand->next = target->card_list;
    target->card_list = new_hand;
    target->hand_size++;

    // Count how many cards of the same rank are in the player's hand
    struct hand *temp = target->card_list;
    int count = 0;
    while (temp != NULL) {
        if (temp->top.rank == new_card->rank) {
            count++;
        }
        temp = temp->next;
    }

    // Call Check_book() only if the player has exactly 4 cards of that rank
    if (count == 4) {
        Check_book(target, new_card->rank, 1);
    }

    return 0;
}

int remove_card(struct player *target, struct card *old_card) {
  struct hand **ptr = &(target->card_list);
  while (*ptr != NULL) {
    if ((*ptr)->top.rank == old_card->rank &&
        (*ptr)->top.suit == old_card->suit) {
      struct hand *temp = *ptr;
      *ptr = (*ptr)->next;
      // free(temp);
      target->hand_size--;
      return 0;
    }
    ptr = &((*ptr)->next);
  }
  return -1;
}

void remove_duplicates(struct player *target) {
  struct hand *ptr1, *ptr2, *dup;
  ptr1 = target->card_list;

  while (ptr1 != NULL && ptr1->next != NULL) {
    ptr2 = ptr1;

    while (ptr2->next != NULL) {
      if (ptr1->top.rank == ptr2->next->top.rank &&
          ptr1->top.suit == ptr2->next->top.suit) {
        dup = ptr2->next;
        ptr2->next = ptr2->next->next;
        // free(dup);
        target->hand_size--;
      } else {
        ptr2 = ptr2->next;
      }
    }
    ptr1 = ptr1->next;
  }
}

int printAllCommon(char rank, struct player *p1) {
  struct hand *ptr1 = user.card_list;
  struct hand *ptr2 = computer.card_list;
  int c1 = 0;
  int c2 = 0;

  struct player *p2 = p1 == &user ? &computer : &user;

  printf("\t- Player 1 has ");
  while (ptr1 != NULL) {
    int flg = 0;
    if (ptr1->top.rank == rank) {
      c1++;
      printf("%c%c ", ptr1->top.rank, ptr1->top.suit);
      struct card *c = &ptr1->top;
      add_card(p1, c);
      flg = 1;
      ptr1 = ptr1->next;
      remove_card(p2, c);
      remove_duplicates(p1);
    }
    if (!flg)
      ptr1 = ptr1->next;
  }
  printf("\n");

  printf("\t- Player 2 has ");
  while (ptr2 != NULL) {
    int flg = 0;
    if (ptr2->top.rank == rank) {
      c2++;
      printf("%c%c ", ptr2->top.rank, ptr2->top.suit);
      struct card *c = &ptr2->top;
      add_card(p1, c);
      flg = 1;
      ptr2 = ptr2->next;
      remove_card(p2, c);
      remove_duplicates(p1);
    }
    if (!flg)
      ptr2 = ptr2->next;
  }
  printf("\n");
  return c1 + c2;
}

void Check_book(struct player *p1, char rank, int c) {
    int count = 0;

    if (c == 0) {
        count = printAllCommon(rank, p1);
    }

    if (count == 4 || c == 1) {
        // Check if the rank is already booked
        if (strchr(p1->book, rank) == NULL) {
            if (c == 0) {
                printf("\t- Player %d books %c\n\t- Player %d gets another turn\n\n",
                       p1 == &user ? 1 : 2, rank, p1 == &user ? 1 : 2);
            }

            // Add the rank to the player's book
            int len = strlen(p1->book);
            p1->book[len] = rank;
            p1->book[len + 1] = '\0';

            // Remove the cards with the booked rank from both players
            remove_all_occurance_of_rank(p1 == &user ? &computer : &user, p1, rank);
        }
    }
}


int search(struct player *target, char rank) {
  struct hand *ptr = target->card_list;
  while (ptr != NULL) {
    if (ptr->top.rank == rank) {
      return 1;
    }
    ptr = ptr->next;
  }
  return 0;
}

int game_over(struct player *target) { return strlen(target->book) == 7; }

int reset_player(struct player *target) {
  while (target->card_list != NULL) {
    struct hand *temp = target->card_list;
    target->card_list = target->card_list->next;
    // free(temp);
  }
  target->hand_size = 0;
  memset(target->book, 0, sizeof(target->book));
  return 0;
}

char computer_play(struct player *target) {
  printf("Player %d's turn, enter a rank: %c\n", target == &user ? 1 : 2,
         target->card_list->top.rank);
  return target->card_list->top.rank;
}

char user_play(struct player *target) {
    char rank[3];
    printf("Player 1's turn, enter a rank: ");
    fgets(rank, sizeof(rank), stdin);

    // Ensure the player has the rank they are asking for
    while (search(target, rank[0]) == 0) {
        printf("Error - must have at least one card of that rank to play\n");
        printf("Enter a rank: ");
        fgets(rank, sizeof(rank), stdin);
    }

    return rank[0];
}

void show_user_cards(struct player *target) {
    struct hand *ptr = target->card_list;
    printf("Player 1's Hand - ");
    while (ptr != NULL) {
        printf("%c%c ", ptr->top.rank, ptr->top.suit);
        ptr = ptr->next;
    }
    printf("\n");
}

void show_player_books(struct player *user, struct player *computer) {
  printf("Player 1 books: ");
  for (int i = 0; i < strlen(user->book); i++) {
    printf("%c ", user->book[i]);
  }
  printf("\n");
  printf("Player 2 books: ");
  for (int i = 0; i < strlen(computer->book); i++) {
    printf("%c ", computer->book[i]);
  }
  printf("\n");
}

void remove_all_occurance_of_rank(struct player *p1, struct player *p2,
                                  char rank) {
  struct hand **ptr1 = &(p1->card_list);
  while (*ptr1 != NULL) {
    if ((*ptr1)->top.rank == rank) {
      struct hand *temp = *ptr1;
      *ptr1 = (*ptr1)->next;
      // free(temp);
      p1->hand_size--;
    } else {
      ptr1 = &((*ptr1)->next);
    }
  }

  struct hand **ptr2 = &(p2->card_list);
  while (*ptr2 != NULL) {
    if ((*ptr2)->top.rank == rank) {
      struct hand *temp = *ptr2;
      *ptr2 = (*ptr2)->next;
      // free(temp);
      p2->hand_size--;
    } else {
      ptr2 = &((*ptr2)->next);
    }
  }
}
