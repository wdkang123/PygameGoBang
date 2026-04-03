"""Pygame UI application."""

from typing import Optional

import pygame

from pygobang.ai.base import Bot
from pygobang.core.constants import BLACK, BOARD_SIZE, GRID_SIZE, WHITE, WINDOW_SIZE
from pygobang.core.game import Game


class PygameApp:
    """Main Pygame application for Gomoku."""

    def __init__(
        self,
        opponent_bot: Optional[Bot] = None,
        board_size: int = BOARD_SIZE,
    ) -> None:
        pygame.init()
        self.screen = pygame.display.set_caption("Gobang - PygameGoBang AI Platform")
        self.screen = pygame.display.set_mode([WINDOW_SIZE + 80, WINDOW_SIZE])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.board_size = board_size
        self.game = Game(board_size)
        self.opponent_bot = opponent_bot

        self.cursor_x = board_size // 2
        self.cursor_y = board_size // 2

    def run(self) -> None:
        """Main game loop."""
        running = True
        while running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)

            self._draw()

            # AI move
            if self.opponent_bot and not self.game.is_over():
                if self.game.get_current_role() != BLACK:  # Human is black
                    bot_role = self.game.get_current_role()
                    x, y = self.opponent_bot.next_move(self.game.board, bot_role)
                    self.game.make_move(x, y)

            pygame.display.flip()

        pygame.quit()

    def _handle_key(self, key: int) -> None:
        """Handle keyboard input."""
        if self.game.is_over():
            if key == pygame.K_r:
                self.game.reset()
            return

        if self.game.get_current_role() != BLACK:
            return  # Only control during human's turn

        if key == pygame.K_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        if key == pygame.K_RIGHT:
            self.cursor_x = min(self.board_size - 1, self.cursor_x + 1)
        if key == pygame.K_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        if key == pygame.K_DOWN:
            self.cursor_y = min(self.board_size - 1, self.cursor_y + 1)
        if key == pygame.K_SPACE:
            self.game.make_move(self.cursor_x, self.cursor_y)
        if key == pygame.K_r:
            self.game.reset()

    def _draw(self) -> None:
        """Draw the game state."""
        self.screen.fill([255, 255, 255])

        # Draw grid
        for i in range(self.board_size):
            pygame.draw.line(
                self.screen, [0, 0, 0], [0, i * GRID_SIZE], [WINDOW_SIZE, i * GRID_SIZE], 1
            )
            pygame.draw.line(
                self.screen, [0, 0, 0], [i * GRID_SIZE, 0], [i * GRID_SIZE, WINDOW_SIZE], 1
            )

        # Draw pieces
        for y in range(self.board_size):
            for x in range(self.board_size):
                piece = self.game.board.get(x, y)
                if piece == BLACK:
                    pygame.draw.circle(self.screen, [255, 0, 0], [x * GRID_SIZE, y * GRID_SIZE], 8)
                elif piece == WHITE:
                    pygame.draw.circle(self.screen, [0, 0, 0], [x * GRID_SIZE, y * GRID_SIZE], 8)

        # Draw cursor
        if not self.game.is_over():
            pygame.draw.circle(
                self.screen,
                [0, 200, 0],
                [self.cursor_x * GRID_SIZE, self.cursor_y * GRID_SIZE],
                8,
                2,
            )

        # Draw status text
        if self.game.is_over():
            winner = self.game.get_winner()
            if winner == BLACK:
                text = self.font.render("Black Wins!", True, [255, 0, 0])
            elif winner == WHITE:
                text = self.font.render("White Wins!", True, [0, 0, 255])
            else:
                text = self.font.render("Draw!", True, [0, 0, 0])
        else:
            role = self.game.get_current_role()
            text = self.font.render(
                "Black" if role == WHITE else "White",
                True,
                [0, 0, 255] if role == WHITE else [255, 0, 0],
            )

        self.screen.blit(text, (WINDOW_SIZE + 10, 10))

        # Instructions
        hint = self.font.render("R: Restart", True, [100, 100, 100])
        self.screen.blit(hint, (WINDOW_SIZE + 10, 50))
