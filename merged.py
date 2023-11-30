import cv2
import mediapipe as mp
import pyautogui
import pygame, sys, random
from pygame.locals import *
import threading

handPos = [-1000,-1000]

def gameTest():
    WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_RED = (200, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 200, 0)
    DARK_YELLOW = (200, 200, 0)
    YELLOW = (255, 255, 0)
    BG_COLOUR = (133, 203, 230)
    GAME_FONT = 'arial'
    NUM_BALLOONS = 3
    MIN_SPEED, MAX_SPEED = 1, 2
    BALLOON_SIZE = 200
    pygame.init()
    def draw_text(surf, font, msg, pos, topleft=False, topright=False,
                  midtop=False, midbottom=False):
        FONT = pygame.font.SysFont(GAME_FONT, font['size'])
        textSurf = FONT.render(msg, True, font['col'])
        textRect = textSurf.get_rect()
        if topleft:
            textRect.topleft = pos
        elif topright:
            textRect.topright = pos
        elif midtop:
            textRect.midtop = pos
        elif midbottom:
            textRect.midbottom = pos
        elif not (topleft and topright):
            textRect.center = pos
        surf.blit(textSurf, textRect)
    def button(surf, msg, x, y, w, h, ac, ic, func, mouseClick):
        mousePos = pygame.mouse.get_pos()
        if x + w > mousePos[0] > x and y + h > mousePos[1] > y:
            pygame.draw.rect(surf, ac, (x, y, w, h))
            if mouseClick: func()
        else:
            pygame.draw.rect(surf, ic, (x, y, w, h))
        pygame.draw.rect(surf, BLACK, (x, y, w, h), 2)
        draw_text(surf, {'size': 18, 'col': BLACK},
                  msg, (x + (w / 2), y + (h / 2)))
    class Balloon:
        def __init__(self, speed, y, direction):
            self.speed = speed
            self.image = pygame.transform.scale(pygame.image.load(
                'balloon.png'), (BALLOON_SIZE, BALLOON_SIZE))
            self.direction = direction
            self.rect = self.image.get_rect()
            self.rect.y = y
            if self.direction == 0:
                self.rect.x = WINDOW_WIDTH
            else:
                self.rect.x = -BALLOON_SIZE
        def update(self):
            if self.direction == 0:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
    class Game:
        def __init__(self):
            self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('Balloon Shooter')
            pygame.display.set_icon(pygame.image.load('balloon.png'))
            self.FPS = 40
            self.CLOCK = pygame.time.Clock()
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            self.mouseClick = False
            self.clickPos = [-100, -100]
            self.gameStarted = False
        def quit(self):
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        def new_game(self):
            self.balloons = []
            self.missedBalloons = 0
            self.score = 0
            self.hitBalloons = 0
            self.numBalloons = NUM_BALLOONS
            self.i = 1
            self.run()
        def run(self):
            self.playing = True
            while self.playing:
                self.mouseClick = False
                self.clickPos = [-100, -100]
                self.events()
                self.update()
                self.draw()
                self.CLOCK.tick(self.FPS)
        def events(self):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouseClick = True
                    self.clickPos = event.pos
        def update(self):
            if(0 <= handPos[0] <= WINDOW_WIDTH and 0 <= handPos[1] <= WINDOW_HEIGHT):
                pygame.mouse.set_pos(handPos)
            print(handPos)
            if len(self.balloons) < self.numBalloons:
                self.balloons.append(Balloon(random.randrange(MIN_SPEED, MAX_SPEED),
                                             random.randrange(0, WINDOW_HEIGHT - 99),
                                             random.randrange(0, 2)))
            for balloon in self.balloons:
                balloon.update()
                if balloon.rect.right < 0 or balloon.rect.left > WINDOW_WIDTH:
                    self.balloons.remove(balloon)
                    self.missedBalloons += 1
                if balloon.rect.x + BALLOON_SIZE > self.clickPos[0] > \
                        balloon.rect.x and balloon.rect.y + BALLOON_SIZE > \
                        self.clickPos[1] > balloon.rect.y:
                    if balloon in self.balloons:
                        self.balloons.remove(balloon)
                        self.score += (balloon.speed * 10)
                        self.hitBalloons += 1
            if self.missedBalloons >= 5: self.playing = False
            if self.score / 1000 > self.i:
                self.numBalloons += 1
                self.i += 1
        def draw(self):
            self.WINDOW.fill(BG_COLOUR)
            for balloon in self.balloons:
                self.WINDOW.blit(balloon.image, balloon.rect)
            draw_text(self.WINDOW, {'size': 20, 'col': WHITE},
                      'Score: {}'.format(self.score),
                      (10, 0), topleft=True)
            draw_text(self.WINDOW, {'size': 20, 'col': WHITE},
                      'Missed Balloons: {}'.format(self.missedBalloons),
                      (WINDOW_WIDTH - 10, 0), topright=True)
            draw_text(self.WINDOW, {'size': 20, 'col': WHITE},
                      'Hit Balloons: {}'.format(self.hitBalloons),
                      (WINDOW_WIDTH / 2, 0), midtop=True)
            button(self.WINDOW, 'Salir', WINDOW_WIDTH - 100, WINDOW_HEIGHT - 50,
                   100, 50, DARK_YELLOW, YELLOW, self.quit, self.mouseClick)
            pygame.display.flip()
        def game_over(self):
            self.gameOver = True
            while self.gameOver:
                self.mouseClick = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.quit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.quit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouseClick = True
                self.WINDOW.fill(WHITE)
                draw_text(self.WINDOW, {'size': 50, 'col': BLACK}, 'Game Over',
                          (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5))
                draw_text(self.WINDOW, {'size': 20, 'col': BLACK},
                          'Score: {}'.format(self.score),
                          (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 5) + 50))
                draw_text(self.WINDOW, {'size': 20, 'col': WHITE},
                          'Hit Balloons: {}'.format(self.hitBalloons),
                          (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 5) + 150))
                button(self.WINDOW, 'Play again', (WINDOW_WIDTH / 2) - 180,
                       (WINDOW_HEIGHT / 5) * 4, 100, 50, DARK_GREEN, GREEN,
                       self.restart, self.mouseClick)
                button(self.WINDOW, 'Quit', (WINDOW_WIDTH / 2) + 80,
                       (WINDOW_HEIGHT / 5) * 4, 100, 50, DARK_RED, RED,
                       self.quit, self.mouseClick)
                pygame.display.flip()
                self.CLOCK.tick(self.FPS)
        def start(self):
            self.gameStarted = True
        def back(self):
            self.inInfo = False
        def restart(self):
            self.gameOver = False
        def end(self):
            self.playing = False
    game = Game()
    while True:
        game.new_game()
        game.game_over()

dragMode = False
draw_landmarks = False
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

gameThread = threading.Thread(target=gameTest)
gameThread.start()

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            if draw_landmarks:
                drawing_utils.draw_landmarks(frame, hand)

            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    if dragMode:
                        pyautogui.dragTo(index_x, index_y)
                    else:
                        pyautogui.moveTo(index_x, index_y)


                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    if abs(index_y - thumb_y) < 50 and not dragMode:
                        pyautogui.click()
                        pyautogui.sleep(0.5)
        print(pyautogui.position())

    cv2.waitKey(1)


