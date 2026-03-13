#include "funcoes.h"

#define M_ESQUERDO 0
#define M_DIREITO 1

int vel_motor_direito = 0;
int vel_motor_esquerdo = 0;

void setup() {
    Serial.begin(9600);
    inicializar(); // Inicializa o hardware ou motores, conforme necessário
    pararMotor(M_ESQUERDO, vel_motor_esquerdo);
    pararMotor(M_DIREITO, vel_motor_direito);
}

void loop() {
    if (Serial.available() > 0) {
        // Lê a linha completa recebida
        String receivedString = Serial.readStringUntil('\n');
        
        // Separa a string em comando e valores
        int separatorIndex = receivedString.indexOf(' '); // Encontra o índice do primeiro espaço

        if (separatorIndex != -1) {
            char commando = receivedString.substring(0, separatorIndex).charAt(0); // Obtém o comando

            // Remove o comando da string
            String remainingString = receivedString.substring(separatorIndex + 1);
            
            // Encontra os próximos espaços
            int secondSeparatorIndex = remainingString.indexOf(' ');
            int thirdSeparatorIndex = remainingString.indexOf(' ', secondSeparatorIndex + 1);
            
            if (secondSeparatorIndex != -1 && thirdSeparatorIndex != -1) {
                // Obtém os valores
                int valor = remainingString.substring(0, secondSeparatorIndex).toInt();
                int valor2 = remainingString.substring(secondSeparatorIndex + 1, thirdSeparatorIndex).toInt();
                int valor3 = remainingString.substring(thirdSeparatorIndex + 1).toInt();
                
                Serial.print("Comando: ");
                Serial.println(commando); // Mensagem de depuração
                Serial.print("Valor: ");
                Serial.println(valor); // Mensagem de depuração
                Serial.print("Valor2: ");
                Serial.println(valor2); // Mensagem de depuração
                Serial.print("Valor3: ");
                Serial.println(valor3); // Mensagem de depuração

                // Aciona os motores com base no comando recebido
                switch (commando) {
                    case 'd':
                        vel_motor_direito = valor;
                        ligarMotor(M_ESQUERDO, -valor);
                        ligarMotor(M_DIREITO, valor);
                        break;
                    case 'e':
                        vel_motor_esquerdo = valor;
                        ligarMotor(M_ESQUERDO, valor);
                        ligarMotor(M_DIREITO, -valor);
                        break;
                    case 'f':
                        vel_motor_direito = valor;
                        vel_motor_esquerdo = valor;
                        ligarMotor(M_ESQUERDO, -valor);
                        ligarMotor(M_DIREITO, -valor);
                        break;
                    case 't':
                        vel_motor_direito = valor;
                        vel_motor_esquerdo = valor;
                        ligarMotor(M_ESQUERDO, valor);
                        ligarMotor(M_DIREITO, valor);
                        break;
                    case 'p':
                        pararMotor(M_ESQUERDO, vel_motor_esquerdo);
                        pararMotor(M_DIREITO, vel_motor_direito);
                        break;
                    case 'b':
                        brecarMotor(M_ESQUERDO);
                        brecarMotor(M_DIREITO);
                        break;
                    case 'm':
                        vel_motor_esquerdo = valor;
                        vel_motor_direito = valor2;
                        moverTanque(-valor, -valor2, TEMPO, valor3);
                        break;
                    case 's':
                        servom(valor);
                        break;
                    default:
                        Serial.println("Comando inválido.");
                        break;
                }
            } else {
                Serial.println("Formato de mensagem inválido.");
            }
        } else {
            Serial.println("Formato de mensagem inválido.");
        }
    }
}
