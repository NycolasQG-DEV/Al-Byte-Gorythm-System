#ifndef FUNCOES_H
#define FUNCOES_H

//====================================================//
//definindo as opções das funções
//====================================================//

//func ligarmotor()
#define M_ESQUERDO 0
#define M_DIREITO 1

//func mover()
#define   TEMPO   1

//====================================================//

void inicializar();
void ligarMotor(int motor_index, int motor_spd);
void pararMotor(int motor_index, int vel);
void brecarMotor(int motor_index);
void moverTanque(int vel_motor_esquerdo, int vel_motor_direito, int config_type, int config_value);
void servom(int angle);

#endif
