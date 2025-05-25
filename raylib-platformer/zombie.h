#ifndef ZOMBIE_H
#define ZOMBIE_H
#include "constants.h"
#include <time.h>
#include <stdlib.h>
#include "raylib.h"
#include "player.h"


typedef struct Zombie {
    float x, y;               
    float speed;              
    int width, height;        
    bool active;  
    bool right;            
} Zombie;

#define MAX_ZOMBIES 10 


void LoadZombies(Zombie* zombies, float spawnInterval, float* spawnTimer, float* delta);
void UpdateZombies(Zombie* zombies, float delta);
void CheckZombieCollision(Zombie* zombies, Player* player);
void DrawZombies(Zombie* zombies, int currentFrame, Texture2D zombieWalkingLeftwards, Texture2D zombieWalkingRightwards);

#endif

