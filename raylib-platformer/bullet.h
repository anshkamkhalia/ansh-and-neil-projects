#include <time.h>
#include <stdlib.h>

#include "raylib.h"
#include "player.h"
#include "game.h"
#include "zombie.h"

#ifndef BULLET_H
#define BULLET_H

typedef struct Bullet {
    float x, y;               
    float speed;              
    int width, height;        
    bool active;
    bool movingRight;              
} Bullet;
        

#define MAX_BULLETS 20  
void LoadBullets(Bullet* bullets, Player* player, float* delta, float* shootCooldown, float shootCooldownTime, bool* shooting, float* frameTimer, int currentFrame);
void CheckBulletCollision(Bullet* bullets, Zombie* zombies, Player* player);
void DrawBullets(Bullet* bullets);

#endif
