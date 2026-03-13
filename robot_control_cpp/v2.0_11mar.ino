// Definição dos pinos para a primeira ponte H
#define ENA_A 2  // PWM
#define IN1_A 3
#define IN2_A 4
#define IN3_A 5
#define IN4_A 6
#define ENB_A 7 // PWM

// Definição dos pinos para a segunda ponte H
#define ENA_B 13 // PWM
#define IN1_B 12
#define IN2_B 11
#define IN3_B 10
#define IN4_B 9
#define ENB_B 8 // PWM  

void setup() {
    // Configuração dos pinos como saída
    pinMode(IN1_A, OUTPUT);
    pinMode(IN2_A, OUTPUT);
    pinMode(ENA_A, OUTPUT);
    
    pinMode(IN3_A, OUTPUT);
    pinMode(IN4_A, OUTPUT);
    pinMode(ENB_A, OUTPUT);
    
    pinMode(IN1_B, OUTPUT);
    pinMode(IN2_B, OUTPUT);
    pinMode(ENA_B, OUTPUT);
    
    pinMode(IN3_B, OUTPUT);
    pinMode(IN4_B, OUTPUT);
    pinMode(ENB_B, OUTPUT);
}


void move_Fwd(int velocidade){
    digitalWrite(IN1_A, HIGH);
    digitalWrite(IN3_A, HIGH);
    digitalWrite(IN1_B, HIGH);
    digitalWrite(IN3_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
}

void move_Bwd(int velocidade){
    digitalWrite(IN2_A, HIGH);
    digitalWrite(IN4_A, HIGH);
    digitalWrite(IN2_B, HIGH);
    digitalWrite(IN4_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
}

void move_Left(int velocidade){
    digitalWrite(IN1_A, HIGH);
    digitalWrite(IN4_A, HIGH);
    digitalWrite(IN2_B, HIGH);
    digitalWrite(IN3_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
}

void Move_Right(int velocidade){
    digitalWrite(IN2_A, HIGH);
    digitalWrite(IN3_A, HIGH);
    digitalWrite(IN1_B, HIGH);
    digitalWrite(IN4_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
}

void turnRight(int velocidade, int degrees){
    int tempo = ((degrees * 255)/(360 * velocidade));
    digitalWrite(IN1_A, HIGH);
    digitalWrite(IN3_A, HIGH);
    digitalWrite(IN2_B, HIGH);
    digitalWrite(IN4_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
    delay(tempo * 1000);
    digitalWrite(IN1_A, LOW);
    digitalWrite(IN3_A, LOW);
    digitalWrite(IN2_B, LOW);
    digitalWrite(IN4_B, LOW);
}

void turnLeft(int velocidade, int degrees){
    int tempo = ((degrees * 255)/(360 * velocidade));
    digitalWrite(IN2_A, HIGH);
    digitalWrite(IN4_A, HIGH);
    digitalWrite(IN1_B, HIGH);
    digitalWrite(IN3_B, HIGH);
    analogWrite(ENB_B, velocidade + 10);
    analogWrite(ENA_B, velocidade + 10);
    analogWrite(ENB_A, velocidade + 13);
    analogWrite(ENA_A, velocidade);
    delay(tempo * 1000);
    digitalWrite(IN2_A, LOW);
    digitalWrite(IN4_A, LOW);
    digitalWrite(IN1_B, LOW);
    digitalWrite(IN3_B, LOW);
}

void loop() {
  turnLeft(100, 90);
}
