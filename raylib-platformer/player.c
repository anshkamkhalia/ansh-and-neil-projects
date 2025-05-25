#include "player.h"
#include "raylib.h"
#include "game.h"

void InitPlayer(Player* player) {
    player->x =  screenW/2-50;
    player->y = 300;
    player->width = 100;
    player->height = 100;
    player->velocity = 0.0;
    player->isJumping = false;
    player->facingRight = true;
    player->isDead = false;
    player->killCount = 0;
}

void HandlePlayerInput(Player* player) {
    if (IsKeyDown(KEY_D)) {
        player->x += 5;
        player->facingRight = true;
    }
    if (IsKeyDown(KEY_A)) { 
        player->x -= 5;
        player->facingRight = false;
    }  

    // Jumping
    if (IsKeyPressed(KEY_W) && !player->isJumping) {
        player->velocity = -10.0;
        player->isJumping = true;
    }
}

void Gravity(Player* player, int playerHeight) {
    player->velocity += 0.5;
    player->y += player->velocity;

    // Ground collision
    if (player->y + playerHeight >= groundY) {
        player->y = groundY - playerHeight;
        player->velocity = 0;
        player->isJumping = false;
    }
}

void DrawPlayer(Player* player, int* currentFrame, int* deathFrame, float frameTime, float* frameTimer, bool* shooting,
    Texture2D soldierWalkingLeft,
    Texture2D soldierWalkingRight,
    Texture2D soldierShootingLeft,
    Texture2D soldierShootingRight,
    Texture2D soldierDead) {

    int walkingFrameWidth = soldierWalkingRight.width / 8;
    int walkingFrameHeight = soldierWalkingRight.height;

    int shootFrameWidth = soldierShootingRight.width / 4;
    int shootFrameHeight = soldierShootingRight.height;

    int deathFrameWidth = soldierDead.width / 4;
    int deathFrameHeight = soldierDead.height;

    if (player->isDead) {
        Vector2 deathPos = { player->x, player->y };
        Rectangle frameRec = { *deathFrame * deathFrameWidth, 0, deathFrameWidth, deathFrameHeight };
        DrawTextureRec(soldierDead, frameRec, deathPos, WHITE);

        if (*frameTimer >= frameTime && *deathFrame < 4) {
            *frameTimer = 0.0f;
            (*deathFrame)++;
        }

        if (*deathFrame >= 4) {
            Vector2 textSize = MeasureTextEx(GetFontDefault(), "GAME OVER", 50, GetFontDefault().glyphPadding);
            int gameOverX = screenW / 2 - textSize.x / 2;
            int gameOverY = screenH / 2 - textSize.y / 2;
            DrawText("GAME OVER", gameOverX, gameOverY, 50, GREEN);
        }
    } else {
        if (*shooting) {
            Texture2D shootTex = player->facingRight ? soldierShootingRight : soldierShootingLeft;
            Rectangle frameRec = { *currentFrame * shootFrameWidth, 0, shootFrameWidth, shootFrameHeight };
            Vector2 position = { player->x, player->y };
            DrawTextureRec(shootTex, frameRec, position, WHITE);

            if (*frameTimer >= frameTime) {
                *frameTimer = 0.0f;
                (*currentFrame)++;
                if (*currentFrame >= 4) {
                    *currentFrame = 0;
                    *shooting = false;
                }
            }
        } else {
            Texture2D walkTex = player->facingRight ? soldierWalkingRight : soldierWalkingLeft;
            Rectangle frameRec = { *currentFrame * walkingFrameWidth, 0, walkingFrameWidth, walkingFrameHeight };
            Vector2 position = { player->x, player->y };
            DrawTextureRec(walkTex, frameRec, position, WHITE);

            if (*frameTimer >= frameTime) {
                *frameTimer = 0.0f;
                (*currentFrame)++;
                if (*currentFrame >= 8) *currentFrame = 0;
            }
        }
    }
}
