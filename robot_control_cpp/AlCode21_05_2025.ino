#include <Servo.h>

// === PIN DEFINITIONS ===
#define ENA_A 2
#define IN1_A 4 // m1 frente
#define IN2_A 3 // m1 trás
#define IN3_A 6 // m2 frente
#define IN4_A 5 // m2 trás
#define ENB_A 7

#define ENA_B 8
#define IN1_B 9  // m3 frente
#define IN2_B 10 // m3 trás
#define IN4_B 11 // m4 trás
#define IN3_B 12 // m4 frente
#define ENB_B 13

#define SERVO_CAM 45

// === CONFIG ===
bool devMode = true; // Mostrar mensagens de debug

// === AJUSTES DE POTÊNCIA DOS MOTORES ===
int motorAdjustments[4] = {-55, -65, -80, 0}; // M1, M2, M3, M4

Servo servo;

// === PROTÓTIPO ===
void driveMotor(int motor, bool forward, int baseSpeed, bool accelerate = false, bool decelerate = false);
String getToken(String data, int index);
void processCommand(String cmd);
void stopAll();
void moveFwd(int speed, int time);
void moveBwd(int speed, int time);
void turnLeft(int speed, int time);
void turnRight(int speed, int time);
void move_right(int speed, int time);
void move_left(int speed, int time);

// === SETUP ===
void setup() {
  Serial.begin(9600);
  servo.attach(SERVO_CAM);
  servo.write(90);

  int pins[] = {IN1_A, IN2_A, ENA_A, IN3_A, IN4_A, ENB_A, IN1_B, IN2_B, ENA_B, IN3_B, IN4_B, ENB_B};
  for (int i = 0; i < 12; i++) pinMode(pins[i], OUTPUT);

  stopAll();
  if (devMode) Serial.println("Code started!");
}

// === MAIN LOOP ===
void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command.length() > 0) {
      if (devMode) {
        Serial.print("Received: ");
        Serial.println(command);
      }
      processCommand(command);
    }
  }
}

// === COMANDO SERIAL ===
void processCommand(String cmd) {
  String name = getToken(cmd, 0);
  int val1 = getToken(cmd, 1).toInt();
  int val2 = getToken(cmd, 2).toInt();

  if (name == "move_Fwd") moveFwd(val1, val2);
  else if (name == "move_Bwd") moveBwd(val1, val2);
  else if (name == "turn_Left") turnLeft(val1, val2);
  else if (name == "turn_Right") turnRight(val1, val2);
  else if (name == "move_Right") move_right(val1, val2);
  else if (name == "move_Left") move_left(val1, val2);
  else if (name == "stop") stopAll();
  else if (name == "servo") {
    servo.write(constrain(val1, 0, 180));
    if (devMode) {
      Serial.print("Servo set to ");
      Serial.println(val1);
    }
  }
  else if (name == "set_adjust_all") {
    int adj0 = getToken(cmd, 1).toInt();
    int adj1 = getToken(cmd, 2).toInt();
    int adj2 = getToken(cmd, 3).toInt();
    int adj3 = getToken(cmd, 4).toInt();

    motorAdjustments[0] = adj0;
    motorAdjustments[1] = adj1;
    motorAdjustments[2] = adj2;
    motorAdjustments[3] = adj3;

    if (devMode) {
      Serial.println("Motor adjustments updated:");
      for (int i = 0; i < 4; i++) {
        Serial.print("Motor ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(motorAdjustments[i]);
      }
    }
  }
  else if (devMode) {
    Serial.println("Invalid command!");
  }
}

String getToken(String data, int index) {
  int start = 0, end = -1;
  for (int i = 0; i <= index; i++) {
    start = end + 1;
    end = data.indexOf(' ', start);
    if (end == -1) end = data.length();
  }
  return data.substring(start, end);
}

// === MOTOR DRIVER FUNCTIONS ===
void driveMotor(int motor, bool forward, int baseSpeed, bool accelerate, bool decelerate) {
  int targetSpeed = abs(baseSpeed);
  int adjustedSpeed = constrain(targetSpeed + motorAdjustments[motor], 0, 255);
  const int stepDelay = 10;

  if (accelerate) {
    for (int pwm = 0; pwm <= adjustedSpeed; pwm += 5) {
      applyPWM(motor, forward, constrain(pwm, 0, 255));
      delay(stepDelay);
    }
  }

  if (!accelerate && !decelerate) {
    applyPWM(motor, forward, adjustedSpeed);
  }

  if (decelerate) {
    for (int pwm = adjustedSpeed; pwm >= 0; pwm -= 5) {
      applyPWM(motor, forward, constrain(pwm, 0, 255));
      delay(stepDelay);
    }
    applyPWM(motor, forward, 0);
  }
}

void driveMotorRaw(int motor, bool forward, int pwm) {
  pwm = constrain(pwm, 0, 255);
  forward = !forward; // <<< INVERTE A LÓGICA GLOBAL

  switch (motor) {
    case 0:
      digitalWrite(IN1_A, !forward);
      digitalWrite(IN2_A, forward);
      analogWrite(ENA_A, pwm);
      break;
    case 1:
      digitalWrite(IN3_A, forward);
      digitalWrite(IN4_A, !forward);
      analogWrite(ENB_A, pwm);
      break;
    case 2:
      digitalWrite(IN1_B, !forward);
      digitalWrite(IN2_B, forward);
      analogWrite(ENA_B, pwm);
      break;
    case 3:
      digitalWrite(IN3_B, !forward);
      digitalWrite(IN4_B, forward);
      analogWrite(ENB_B, pwm);
      break;
  }
}

void applyPWM(int motor, bool forward, int pwm) {
  driveMotorRaw(motor, forward, pwm);
}

void stopAll() {
  digitalWrite(IN1_A, LOW); digitalWrite(IN2_A, LOW);
  digitalWrite(IN3_A, LOW); digitalWrite(IN4_A, LOW);
  digitalWrite(IN1_B, LOW); digitalWrite(IN2_B, LOW);
  digitalWrite(IN3_B, LOW); digitalWrite(IN4_B, LOW);

  analogWrite(ENA_A, 0);
  analogWrite(ENB_A, 0);
  analogWrite(ENA_B, 0);
  analogWrite(ENB_B, 0);

  if (devMode) Serial.println("Motors stopped.");
}

// === MOVIMENTOS PADRÕES ===
void moveFwd(int speed, int time) {
  for (int i = 0; i < 4; i++) driveMotor(i, true, speed);
  if (devMode) Serial.println("Moving forward...");
  delay(time * 1000);
  stopAll();
}

void moveBwd(int speed, int time) {
  for (int i = 0; i < 4; i++) driveMotor(i, false, speed);
  if (devMode) Serial.println("Moving backward...");
  delay(time * 1000);
  stopAll();
}

void turnLeft(int speed, int time) {
  driveMotorRaw(0, true, speed);
  driveMotorRaw(1, true, speed);
  driveMotorRaw(2, false, speed);
  driveMotorRaw(3, false, speed);
  if (devMode) Serial.println("Turning left...");
  delay(time * 1000);
  stopAll();
}

void turnRight(int speed, int time) {
  driveMotorRaw(0, false, speed);
  driveMotorRaw(1, false, speed);
  driveMotorRaw(2, true, speed);
  driveMotorRaw(3, true, speed);
  if (devMode) Serial.println("Turning right...");
  delay(time * 1000);
  stopAll();
}

void move_right(int speed, int time) {
  driveMotorRaw(0, true, speed);
  driveMotorRaw(1, false, speed);
  driveMotorRaw(2, false, speed);
  driveMotorRaw(3, true, speed);
  if (devMode) Serial.println("Moving right...");
  delay(time * 1000);
  stopAll();
}

void move_left(int speed, int time) {
  driveMotorRaw(0, false, speed);
  driveMotorRaw(1, true, speed);
  driveMotorRaw(2, true, speed);
  driveMotorRaw(3, false, speed);
  if (devMode) Serial.println("Moving left...");
  delay(time * 1000);
  stopAll();
}
