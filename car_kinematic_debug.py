import pygame


class Debug:
    @staticmethod
    def check_background(screen, color, x, y):
        pygame.draw.line(screen, color, (x, 0), (x, 720), 3)
        pygame.draw.line(screen, color, (0, y), (1280, y), 3)

    @staticmethod
    def debug_text(screen, input):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text = myfont.render(input, False, (255, 0, 255))
        screen.blit(text, (30, 30))

		