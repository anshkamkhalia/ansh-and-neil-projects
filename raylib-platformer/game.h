#include "raylib.h"
#include "player.h"

#ifndef GAME_H
#define GAME_H


extern int screenW;
extern int screenH;
extern int groundY;
extern float shootCooldownTime;
extern float zombieSpawnInterval;

void DrawScore(Player* player);

#endif