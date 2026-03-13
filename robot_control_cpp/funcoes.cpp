#include <Servo.h>

#include <Arduino.h>
#include <Wire.h>
#include "funcoes.h"

// Definindo os pinos da Ponte H
#define    IN1    3
#define    IN2    2
#define    IN3    7
#define    IN4    6
#define    ENA    5
#define    ENB    4

// Definindo as opções das funções
#define M_ESQUERDO 0
#define M_DIREITO 1
#define TEMPO 1


Servo myservo;

// Funções
void inicializar() {
  // Configurando os pinos como saída

  
  myservo.attach(11);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Inicializando os motores
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

}

void servom(int angle) {
  myservo.write(angle);
}

void ligarMotor(int motor_index, int motor_spd) {
  switch (motor_index) {
    case M_ESQUERDO:
      if (motor_spd > 0) {
        digitalWrite(IN1, HIGH); 
        digitalWrite(IN2, LOW); 
      } else {
        digitalWrite(IN1, LOW); 
        digitalWrite(IN2, HIGH); 
      }
      analogWrite(ENA, abs(motor_spd) - 25);
      break;

    case M_DIREITO:
      if (motor_spd > 0) {
        digitalWrite(IN3, HIGH); 
        digitalWrite(IN4, LOW); 
      } else {
        digitalWrite(IN3, LOW); 
        digitalWrite(IN4, HIGH); 
      }
      analogWrite(ENB, abs(motor_spd));
      break;
  }
}

void pararMotor(int motor_index, int vel) {
  switch (motor_index) {
    case M_ESQUERDO:

      for (int vaux = abs(vel); vaux >= 0; vaux-=5)
      {
        delay(10);
        analogWrite(ENA, vaux);
        if (vaux <= 0){
          digitalWrite(IN1, LOW); 
          digitalWrite(IN2, LOW); 
        }
      }
      break;

    case M_DIREITO:

      for (int vaux = abs(vel); vaux >= 0; vaux-=5)
      {
        delay(10);
        analogWrite(ENB, vaux);
        if (vaux <= 0){
          digitalWrite(IN3, LOW); 
          digitalWrite(IN4, LOW); 
        }
      }

      

      break;
  }
}


void brecarMotor(int motor_index) {
  switch (motor_index) {
    case M_ESQUERDO:
      digitalWrite(IN1, LOW); 
      digitalWrite(IN2, LOW);
      break;
    case M_DIREITO:
      digitalWrite(IN3, LOW); 
      digitalWrite(IN4, LOW); 
      break;
  }
}


void moverTanque(int vel_motor_esquerdo, int vel_motor_direito, int config_type, int config_value) {
  ligarMotor(M_ESQUERDO, vel_motor_esquerdo);
  ligarMotor(M_DIREITO, vel_motor_direito);

  switch(config_type) {
    case TEMPO:
      delay(config_value * 1000);
      pararMotor(M_ESQUERDO, vel_motor_esquerdo);
      pararMotor(M_DIREITO, vel_motor_direito);
      break;
  }
}

