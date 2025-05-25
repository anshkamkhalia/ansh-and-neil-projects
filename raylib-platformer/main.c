#include "raylib.h"
#include <stdbool.h>
#include <stdlib.h> // rand() function
#include <time.h>   // time()

#include "game.h"
#include "player.h"
#include "zombie.h"
#include "bullet.h"
        

// ----------  MAIN  ----------

int screenW = 600;
int screenH = 450;
int groundY = 430;
float zombieSpawnInterval = 2.0f;
float shootCooldownTime = 0.5f;

int main(void) {
    // WINDOW INIT

    InitWindow(screenW, screenH, "Ultimate Zombie Survival I");
    SetTargetFPS(60);
    srand(time(NULL));


    // LOADS IN TEXTURES
    Texture2D soldierWalkingLeft = LoadTexture("assets/soldier/walk-left.png");
    Texture2D soldierWalkingRight = LoadTexture("assets/soldier/walk.png");
    Texture2D soldierShootingLeft = LoadTexture("assets/soldier/shoot-left.png");
    Texture2D soldierShootingRight = LoadTexture("assets/soldier/shoot.png");
    Texture2D soldierDead = LoadTexture(".assets/soldier/dead.png");

    Texture2D zombieWalkingRightwards = LoadTexture("assets/zombie/walk.png");
    Texture2D zombieWalkingLeftwards = LoadTexture("assets/zombie/walk-left.png");
    Texture2D bgTexture = LoadTexture("assets/bg.png");
    
    
    Player player;
    InitPlayer(&player);

    Zombie zombies[MAX_ZOMBIES] = {0};
    float zombieSpawnTimer = 0.0f;

    Bullet bullets[MAX_BULLETS] = {0};
    float shootCooldown = 0.0f;

    int currentFrame = 0;
    float frameTime = 0.1f;
    float frameTimer = 0.0f;

    bool shooting = false;
    bool isDying = false;

    int deathFrame = 0;

    // ----------  GAME LOOP  ----------

    while (!WindowShouldClose()) {
        float delta = GetFrameTime();


        Gravity(&player, soldierShootingRight.height);

        if (!player.isDead) {

            HandlePlayerInput(&player);
            
            LoadBullets(bullets, &player, &delta, &shootCooldown, shootCooldownTime, &shooting, &frameTimer, currentFrame);
            
            LoadZombies(zombies, zombieSpawnInterval, &zombieSpawnTimer, &delta);
            UpdateZombies(zombies, delta);

            CheckBulletCollision(bullets, zombies, &player);
            CheckZombieCollision(zombies, &player);
        }

        
        BeginDrawing();
        ClearBackground(RAYWHITE);

        frameTimer += delta;


        DrawTextureEx(bgTexture, (Vector2){ 0, 0 }, 0.0f, 1.0, GRAY);

        DrawScore(&player);
        DrawPlayer(&player, &currentFrame, &deathFrame, frameTime, &frameTimer, &shooting, soldierWalkingLeft, soldierWalkingRight, soldierShootingLeft, soldierShootingRight, soldierDead);
        
        DrawZombies(zombies, currentFrame, zombieWalkingLeftwards, zombieWalkingRightwards);
        DrawBullets(bullets);

        EndDrawing();
    }

    UnloadTexture(soldierWalkingLeft);
    UnloadTexture(soldierWalkingRight);
    UnloadTexture(soldierShootingLeft);
    UnloadTexture(soldierShootingRight);
    UnloadTexture(soldierDead);
    UnloadTexture(zombieWalkingLeftwards);
    UnloadTexture(zombieWalkingRightwards);
    UnloadTexture(bgTexture);
    
    CloseWindow();

    return 0;
}
