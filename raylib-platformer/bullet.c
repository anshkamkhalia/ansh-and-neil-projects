
#include <time.h>
#include <stdlib.h>
#include "raylib.h"
#include "player.h"
#include "bullet.h"
#include "zombie.h"
#include "game.h"


void LoadBullets(Bullet* bullets, Player* player, float* delta, float* shootCooldown, float shootCooldownTime, bool* shooting, float* frameTimer, int currentFrame) {
    if (*shootCooldown > 0.0f) {
        *shootCooldown -= *delta;
    }

    if (IsKeyPressed(KEY_F) && *shootCooldown <= 0.0f) {
        for (int i = 0; i < MAX_BULLETS; i++) {
            if (!bullets[i].active) {
                bullets[i].active = true;
                bullets[i].x = player->facingRight ? player->x + player->width : player->x;
                bullets[i].y = player->y + 100;
                bullets[i].width = 10;
                bullets[i].height = 1.5f;
                bullets[i].speed = 8.0f;
                bullets[i].movingRight = player->facingRight;
                *shootCooldown = shootCooldownTime;
                *shooting = true;
                *frameTimer = 0.0f;
                currentFrame = 0;
                break;
            }
        }
    }

    for (int i = 0; i < MAX_BULLETS; i++) {
        if (bullets[i].active) {
            bullets[i].x += bullets[i].movingRight ? bullets[i].speed : -bullets[i].speed;
            if (bullets[i].x > screenW || bullets[i].x < 0) bullets[i].active = false;
        }
    }
}

void CheckBulletCollision(Bullet* bullets, Zombie* zombies, Player* player) {
    for (int i = 0; i < MAX_BULLETS; i++) {
        if (bullets[i].active) {
            Rectangle bulletRect = { bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height };
            for (int j = 0; j < MAX_ZOMBIES; j++) {
                if (zombies[j].active) {
                    Rectangle zombieRect = { zombies[j].x, zombies[j].y, zombies[j].width, zombies[j].height };
                    if (CheckCollisionRecs(bulletRect, zombieRect)) {
                        zombies[j].active = false;
                        bullets[i].active = false;
                        player->killCount++;
                    }
                }
            }
        }
    }
}

void DrawBullets(Bullet* bullets) {
    for (int i = 0; i < MAX_BULLETS; i++) {
        if (bullets[i].active) {
            DrawRectangle(bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height, YELLOW);
        }
    }
}


