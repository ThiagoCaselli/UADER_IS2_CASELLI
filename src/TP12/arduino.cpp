const int PIN_BOTON = 2;
const int PIN_POT = A0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PIN_POT, INPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP); 
  Serial.begin(9600); 
}

void loop() {
  int estadoBoton = digitalRead(PIN_BOTON); 

  if (estadoBoton == LOW) {
    int valorPot = analogRead(PIN_POT); 
    if (valorPot <= 255) {
      digitalWrite(LED_BUILTIN, HIGH); 
      Serial.println(valorPot);        
    } else {
      digitalWrite(LED_BUILTIN, LOW);  
    }
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000); 
    digitalWrite(LED_BUILTIN, LOW);
  }
  delay(500); 
}