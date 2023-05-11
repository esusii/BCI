import pygame
import sys

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mute Patient Communication App")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(200, 200, 200), (100, 100, 100)]
TEXT_COLORS = [(180, 180, 180), (80, 80, 80)]  # Faded text colors

# Font
FONT = pygame.font.Font(None, 36)

# List of sentences
sentences = [
    # (Same list of sentences as before)
]

# Timer
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # Change the number to adjust the timer duration (in milliseconds)

def draw_sentences(start, end, active_half):
    WIN.fill(WHITE)
    y = 50

    for i in range(start, end):
        in_focus = (i < (start + end) // 2) == active_half
        text_color = BLACK if in_focus else TEXT_COLORS[active_half if i < (start + end) // 2 else 1 - active_half]
        text = FONT.render(sentences[i], True, text_color)
        text_rect = text.get_rect(center=(WIDTH // 2, y))
        text_background = pygame.Surface((WIDTH, 40))
        text_background.fill(COLORS[active_half if i < (start + end) // 2 else 1 - active_half])
        WIN.blit(text_background, (0, y - 20))
        WIN.blit(text, text_rect)
        y += 40

    pygame.display.update()

def main():
    current_list = [0, len(sentences) // 2]
    active_half = 0
    run = True

    draw_sentences(current_list[0], current_list[1], active_half)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == TIMER_EVENT:
                active_half = 1 - active_half
                draw_sentences(current_list[0], current_list[1], active_half)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mid = (current_list[1] - current_list[0]) // 2
                    if mid == 0:
                        print(sentences[current_list[0] + active_half])
                        run = False
                    else:
                        current_list[0] += active_half * mid
                        current_list[1] = current_list[0] + mid

                draw_sentences(current_list[0], current_list[1], active_half)

if __name__ == "__main__":
    main()
