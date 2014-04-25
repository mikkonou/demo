
// Numbers for the sequence
int values[10] = {0};

int sequenceLength = 0;
int i;
int receivedInput;
int currentValue;

int inputValue;

int delayValue = 500;
int halfDelay = delayValue / 2;
int shortDelay = 50;

void generateSequence() {
  for (i=0; i < sequenceLength; ++i) {
    values[i] = random(5);
  } 
}

void playbackSequence() {
  for (i=0; i < sequenceLength; ++i) {
    digitalWrite((values[i]) + 2, HIGH);
    delay(delayValue);
    digitalWrite((values[i]) + 2, LOW);
    delay(delayValue);
  }
}

int readInput() {
  receivedInput = 0;
  
  while (!receivedInput) {
    for (i=8; i < 13; ++i) {
      if (!receivedInput) {
        inputValue = digitalRead(i);
        if (inputValue == HIGH) {
          inputValue = i - 8;
          receivedInput = 1;
        }
      }
    }
  }
  
  return inputValue;
}

void playerRepeatSequence() {
  for (i=0; i < sequenceLength; ++i) {
    currentValue = readInput();
    if (values[i] == currentValue) {
      digitalWrite(7, HIGH);
      delay(delayValue);
      digitalWrite(7, LOW);
      delay(delayValue);
    } else {
      defeat();
    }
  }
}

void victory() {
  while(1) {
    digitalWrite(4, HIGH);
    delay(halfDelay);
    digitalWrite(3, HIGH);
    digitalWrite(5, HIGH);
    delay(halfDelay);
    digitalWrite(2, HIGH);
    digitalWrite(6, HIGH);
    delay(halfDelay);
    digitalWrite(2, LOW);
    digitalWrite(6, LOW);
    delay(halfDelay);
    digitalWrite(3, LOW);
    digitalWrite(5, LOW);
    delay(halfDelay);
    digitalWrite(4, LOW);
    delay(halfDelay);
  }
}

void defeat() {
  
  for(i=2; i < 7; ++i) {
    digitalWrite(i, HIGH);
  }
  
  while(1);
}

void setup() {
  // Red LEDs
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  // Green LED
  pinMode(7, OUTPUT);

  // Buttons
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT); 
  pinMode(12, INPUT);
  
  randomSeed(analogRead(0));
}

void loop() {
  if (sequenceLength++ == 10) victory();
  generateSequence();
  playbackSequence();
  playerRepeatSequence();
}
