#include "raylib.h"
#include "player.h"

void DrawScore(Player* player) {
    const char* scoreText = TextFormat("score: %d", player->killCount);
    int scoreTextWidth = MeasureText(scoreText, 20);
    int scoreBoxPadding = 10;
    int scoreBoxWidth = scoreTextWidth + 2 * scoreBoxPadding;
    int scoreBoxHeight = 30;
    
    DrawRectangle(10, 10, scoreBoxWidth, scoreBoxHeight, RAYWHITE);
    DrawRectangleLines(10, 10, scoreBoxWidth, scoreBoxHeight, BLACK);
    DrawText(scoreText, 10 + scoreBoxPadding, 10 + 5, 20, BLACK);
}