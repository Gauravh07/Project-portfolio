// Music Library
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978

//Initializing melody when player 1 wins
int redmelody[25] = {
  NOTE_A4, NOTE_E5, NOTE_A4, NOTE_D5, NOTE_E5, NOTE_G5, NOTE_E5, NOTE_D5, NOTE_A4, NOTE_E5, NOTE_A4, NOTE_G5

};
//Initializing melody when player 2 wins
int greenmelody[25] ={
  NOTE_E4, NOTE_D5, NOTE_E4, NOTE_D5, NOTE_E4, NOTE_D5, NOTE_E4, NOTE_D5, NOTE_G4,
  NOTE_A4, NOTE_B4, NOTE_A4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_A4, NOTE_G4, NOTE_A4,
  NOTE_G4, NOTE_A4, NOTE_E4, NOTE_D5, NOTE_E4, NOTE_D5, NOTE_E4
};

//Initializing melody when a Tie condition occurs
int tiemelody[3] = {
  NOTE_A4, NOTE_E4, NOTE_C4
};
bool playerOneTurn = true;
int winner = 0;

// creating an array of variables attached to buttons
int BUTTONS[] = { A0, A1, A2, A3, A4, A5, A6, A7, A8 };

// attaching LEDs to pins 2->21 (skipped 12 & 13)
int L1_red = 2;
int L1_green = 3;
int L2_red = 4;
int L2_green = 5;
int L3_red = 6;
int L3_green = 7;
int L4_red = 8;
int L4_green = 9;
int L5_red = 10;
int L5_green = 11;
int L6_red = 14;
int L6_green = 15;
int L7_red = 16;
int L7_green = 17;
int L8_red = 18;
int L8_green = 19;
int L9_red = 20;
int L9_green = 21;
int BUZZER = 12;

//Library for LCD
#include <LiquidCrystal.h>
LiquidCrystal lcd(22, 23, 24, 25, 26, 27);
//Initializing the state array which contains the state of the LED panel (the Game Board) ie, This contains the colour information
int state[9] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };

//Initializing the arrays containing the green and red LED's
int green_leds[9] = { L1_green, L2_green, L3_green, L4_green, L5_green, L6_green, L7_green, L8_green, L9_green };
int red_leds[9] = { L1_red, L2_red, L3_red, L4_red, L5_red, L6_red, L7_red, L8_red, L9_red };

//Function for playing the winning melody for player 1
void Redmelody(){
   for (int i = 0; i < 25; i++) {
    int noteDuration = 1000 / 10; // Change this value to modify the speed of the melody
    tone(BUZZER, redmelody[i], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(8);
  }
}

//Function for playing the winning melody for player 2
void Greenmelody(){
   for (int i = 0; i < 25; i++) {
    int noteDuration = 1000 / 10; // Change this value to modify the speed of the melody
    tone(BUZZER, greenmelody[i], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(8);
  }
}
//Function for playing the Tie melody when a tie occurs
void Tiemelody(){
   for (int i = 0; i < 25; i++) {
    int noteDuration = 1000 / 6; // Change this value to modify the speed of the melody
    tone(BUZZER, tiemelody[i], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(8);
  }
}

//Function used to update the LED's state based on the updated state array
void updateState() {
  for (int i = 0; i < 9; i++) {
    if (state[i] == 1) {              // If player 1 has placed their move
      digitalWrite(green_leds[i], 0);  // Turn off blue
      digitalWrite(red_leds[i], 1);   // Turn on red
    } else if (state[i] == -1) {
      digitalWrite(green_leds[i], 1);
      digitalWrite(red_leds[i], 0);
    } else {  // ALL OFF
      digitalWrite(green_leds[i], 0);
      digitalWrite(green_leds[i], 0);
    }
  }
}

void setup() {
  Serial.begin(9600);//set the baud rate

  //LCD display giving the initial game name output
  lcd.begin(16,2);
  lcd.clear();
  lcd.setCursor(0,0);
  const char a[10] = "TIC-TAC-TOE";
  lcd.clear();
  lcd.print(a);// Printing the name of the game on the LCD display
  delay(3000);

  





  // settinng A0->8 as inputs from 9 buttons
  for (int x = 0; x < 9; x++) {
    pinMode(BUTTONS[x], INPUT);
    digitalWrite(BUTTONS[x], HIGH);  // Pullup
  }


  pinMode(L1_red, OUTPUT);
  pinMode(L1_green, OUTPUT);
  pinMode(L2_red, OUTPUT);
  pinMode(L2_green, OUTPUT);
  pinMode(L3_red, OUTPUT);
  pinMode(L3_green, OUTPUT);
  pinMode(L4_red, OUTPUT);
  pinMode(L4_green, OUTPUT);
  pinMode(L5_red, OUTPUT);
  pinMode(L5_green, OUTPUT);
  pinMode(L6_red, OUTPUT);
  pinMode(L6_green, OUTPUT);
  pinMode(L7_red, OUTPUT);
  pinMode(L7_green, OUTPUT);
  pinMode(L8_red, OUTPUT);
  pinMode(L8_green, OUTPUT);
  pinMode(L9_red, OUTPUT);
  pinMode(L9_green, OUTPUT);

  pinMode(BUZZER, OUTPUT);
}

//Main code
void loop() {
  //If its player 1's turn LCD returns player 1 and if it is player 2's turn LCD returns Player 2
  if (playerOneTurn) { 
    Serial.println("Player 1:");
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("Player 1's Turn");
  } else {
    Serial.println("Player 2's Turn");
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print("Player 2");
  }
//initializing the exit variable
  int e = 0;
  // code left for debugging
  for (int x = 0; x <= 8; x++) {
    Serial.print(state[x]);
  }
  Serial.println();
 
  //While loop controlling buttons with high and low commands using updatestate
  while (true) {
    for (int x = 0; x < 9; x++) {
      if (digitalRead(BUTTONS[x]) == LOW) {
        if (state[x] == 0) {
          if (playerOneTurn) {
            state[x] = 1;
            e = 1;
            updateState();
          } else {
            state[x] = -1;
            e = 1;
            updateState();
          }
        } else {
          //Serial.println("Illegal move, please try again");
        }
      }
    }
    if (e > 0) {
      e = 0;
      break;
    }
  }

// checking the winner function 
  winner = checkWin();
//LCD giving output when player 1 wins, this loop also plays the winner melody for red win
  if (winner == 1) {
    for (int x = 0; x < 9; x++) {
      state[x] = 1;
      Serial.println("1 WON");
      lcd.clear();
      lcd.println("Player 1 wins");
    }
    
    updateState();
    Redmelody();
  }
//LCD giving output when player 2 wins, this loop also plays the winner melody for green wins
  if (winner == -1) {
    for (int x = 0; x < 9; x++) {
      state[x] = -1;
      Serial.println("-1 WON");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.println("Player 2 wins");
      
    }

    updateState();
    Greenmelody();
  }
 //check if TIe is occuring 
  checkTie(winner);
  
  
//change which player is playing(player 1 to player 2)
  if (winner == 0) {
  }

  playerOneTurn = !playerOneTurn;
  
}
// This contains all the winning conditions for red and green LED's
int checkWin() {
  int results[9];

  // Rows
  results[0] = state[0] + state[1] + state[2];
  results[1] = state[3] + state[4] + state[5];
  results[2] = state[6] + state[7] + state[8];
  // Col
  results[3] = state[0] + state[3] + state[6];
  results[4] = state[1] + state[4] + state[7];
  results[5] = state[2] + state[5] + state[8];
  // Diags
  results[6] = state[0] + state[4] + state[8];
  results[7] = state[2] + state[4] + state[6];
  for (int x = 0; x < 9; x++) {
    if (results[x] == 3) {
      for (int x = 0; x <= 8; x++) {
        Serial.print(results[x]);
        Serial.print(" ");
      }
      Serial.println();
      
      return 1;
    }
    if (results[x] == -3) {
      return -1;
    }
  }
  return 0;
}

//This function checks for ties and also prints TIE in the LCD screen. It also resets the game board when the result of a game is a TIE
void checkTie(int win) {
  for (int x = 0; x <= 8; x++) {
    if (state[x] == 0) {
      return;  // not a tie
    }

    if(win == 0){

    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("TIE");
    Tiemelody();
    }
      
    delay(2500);

    
    // only reaches this line when it's a tie
    for (int x = 0; x <= 8; x++) {
      state[x] = 0;
      updateState();


    
   
    }  
  
  
  }  
       
    
}