#ifndef PLAYER_H
#define PLAYER_H

#include "raylib.h"
#include <stdbool.h>


typedef struct Player {
    int x, y;
    int width, height;
    double velocity;
    bool isJumping;
    bool facingRight;
    bool isDead;
    int killCount;
} Player;


void InitPlayer(Player* player);
void HandlePlayerInput(Player* player);
void Gravity(Player* player, int playerHeight);
void DrawPlayer(Player* player, int* currentFrame, int* deathFrame, float frameTime, float* frameTimer, bool* shooting,
    Texture2D soldierWalkingLeft,
    Texture2D soldierWalkingRight,
    Texture2D soldierShootingLeft,
    Texture2D soldierShootingRight,
    Texture2D soldierDead);

#endif
