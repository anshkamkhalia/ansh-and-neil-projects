#include "zombie.h"
#include "raylib.h"
#include "game.h"
#include <stdlib.h> // rand()

void LoadZombies(Zombie* zombies, float spawnInterval, float* spawnTimer, float* delta) {
    *spawnTimer += *delta;
    if (*spawnTimer >= spawnInterval) {
        *spawnTimer = 0.0f;
        for (int i = 0; i < MAX_ZOMBIES; i++) {
            if (!zombies[i].active) {
                zombies[i].active = true;
                zombies[i].width = 50;
                zombies[i].height = 70;
                zombies[i].y = 310;

                int randomNumber = (rand() % 2);
                if (randomNumber == 0) {
                    zombies[i].x = -zombies[i].width;
                    zombies[i].speed = 100.0f;
                    zombies[i].right = true;
                } else {
                    zombies[i].x = screenW + zombies[i].width;
                    zombies[i].speed = -100.0f;
                    zombies[i].right = false;
                }

                break;
            }
        }
    }
}

void UpdateZombies(Zombie* zombies, float delta) {
    for (int i = 0; i < MAX_ZOMBIES; i++) {
        if (zombies[i].active) {
            zombies[i].x += zombies[i].speed * delta;

            // Remove if offscreen
            if (zombies[i].x < -zombies[i].width || zombies[i].x > screenW + zombies[i].width) {
                zombies[i].active = false;
            }
        }
    }
}

void CheckZombieCollision(Zombie* zombies, Player* player) {
    for (int i = 0; i < MAX_ZOMBIES; i++) {
        if (zombies[i].active) {
            Rectangle zombieRect = { zombies[i].x, zombies[i].y, zombies[i].width, zombies[i].height };
            Rectangle playerRect = { player->x, player->y, player->width, player->height };
            if (CheckCollisionRecs(playerRect, zombieRect)) {
                player->isDead = true;
            }
        }
    }
}

void DrawZombies(Zombie* zombies, int currentFrame, Texture2D zombieWalkingLeftwards, Texture2D zombieWalkingRightwards) {
    int zombieFrameWidth = zombieWalkingRightwards.width / 8;
    int zombieFrameHeight = zombieWalkingRightwards.height;

    for (int i = 0; i < MAX_ZOMBIES; i++) {
        if (zombies[i].active) {
            Rectangle frameRec = { currentFrame * zombieFrameWidth, 0, zombieFrameWidth, zombieFrameHeight };
            Vector2 position = { zombies[i].x, zombies[i].y };

            if (zombies[i].right)
                DrawTextureRec(zombieWalkingRightwards, frameRec, position, WHITE);
            else
                DrawTextureRec(zombieWalkingLeftwards, frameRec, position, WHITE);
        }
    }
}
