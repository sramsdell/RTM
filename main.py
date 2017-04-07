#4/6/17
import sys
from stats_2 import *

pygame.init()
screen = pygame.display.set_mode(SIZE)

def main():
    clock = pygame.time.Clock()
    running = True
    manager = TransitionManager(screen)

    while running:
        running = manager.state.event_handler(pygame.event.get())

        manager.update()
        manager.render(screen)
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


class TransitionManager:

    def __init__(self,screen):
        self.change(IntroState(screen))

    def change(self,state):
        self.state = state
        self.state.currentstate = self

    def update(self):
        self.state.update()

    def render(self,screen):
        self.state.render(screen)


class MasterState:
    def __init__(self,screen):
        self.screen = screen

    def quit(self,event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return False
        
    def update(self):
        self.N = ui.get_N()
        self.total = ui.get_total()
        self.ave = ui.get_ave()

        self.font = pygame.font.SysFont("fixedsys", 18)
        
        self._label = self.font.render("Distribution of Bus wait times " +
                                       "for half hour ave. arrivals",
                                         1, RED)
        
        self.text = self.font.render("X scale = 10 minutes",
                                     1, BLACK)
        
        self.text2 = self.font.render("Calculated Ave. wait time = "
                                      + str(self.ave) + " minutes",
                                     1, BLACK)
        
        self.text3 = self.font.render("Sample Size =  "
                                      + str(self.N),
                                     1, BLACK)
        
        self.text4 = self.font.render("Toggle View press T",
                                     1, BLACK)
        
        self.text5 = self.font.render("Y scale = 10 samples",
                                     1, BLACK)

class Hist_1(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)
        
        self.count = 120
        self.tick = 10

        self.N = 0
        self.total = 0
        self.ave = 0

    def render(self,screen):
        self.count += 1
        screen.fill(WHITE)
        screen.blit(self._label,(20,20))
        screen.blit(self.text,(250,120))
        screen.blit(self.text2,(20,50))
        screen.blit(self.text3,(20,70))
        screen.blit(self.text4,(250,70))
        screen.blit(self.text5,(250, 140))

        #vert ticks
        for i in range((SIZE[0] - OFF_SET) // self.tick):
            pygame.draw.rect(screen, BLACK,
                             [OFF_SET + (self.tick * i),
                              SIZE[0] - OFF_SET,
                              2,
                              10])
        #Horz ticks
        for i in range((SIZE[0] - (OFF_SET * 3) + self.tick) // self.tick):
            pygame.draw.rect(screen, BLACK,
                             [OFF_SET,
                              OFF_SET * 2 + (self.tick * i),
                              -8,
                              2])
        #Vert line
        pygame.draw.rect(screen, BLACK,
                         [OFF_SET - 1,
                          (OFF_SET * 2),
                          2,
                          SIZE[0] - OFF_SET * 3])
        
        #horz line
        pygame.draw.rect(screen, BLACK,
                         [OFF_SET,
                          SIZE[0] - OFF_SET,
                          SIZE[0],
                          2])
  
        scale = 10
        if (ui.get_N() < MAX_POINTS):
            temp = spawn_points(self.count, ui)

            ui.add_total(temp)
            if (temp != 0):
                ui.add_N()
                ui.alt_ave(ui.get_total() / (ui.get_N() * 2))
                
                for i in range(ui.get_dist_len()):
                
                    if (temp >= (i * scale) and temp < (i * scale) + scale):
                        ui.add_dist_10(i)
                    if (temp > scale * ui.get_dist_len()):
                        ui.add_dist_10(ui.get_dist_len() - 1)

                    
        for i in range(ui.get_dist_len()):
            #draw bars
            if (i % 2 == 0):
                color = RED
            else:
                color = PINK
            pygame.draw.rect(screen, color,
                     [(i * scale) + OFF_SET,
                      SIZE[0] - OFF_SET,
                      scale,
                      - ui.get_dist_10()[i]])  
                
    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.currentstate.change(Hist_2(screen))
        return True


class Hist_2(MasterState):
    def __init__(self,screen):
        MasterState.__init__(self,screen)

        self.count = 120
        self.tick = 10

        self.N = 0
        self.total = 0
        self.ave = 0
 
    def render(self,screen):
        self.count += 1
        screen.fill(WHITE)
        screen.blit(self.text,(250,120))
        screen.blit(self._label,(20,20))
        screen.blit(self.text2,(20,50))
        screen.blit(self.text3,(20,70))
        screen.blit(self.text4,(250,70))
        screen.blit(self.text5,(250, 140))

        #vert ticks
        for i in range((SIZE[0] - OFF_SET) // self.tick):
            pygame.draw.rect(screen, BLACK,
                             [OFF_SET + (self.tick * i),
                              SIZE[0] - OFF_SET,
                              2,
                              10])
        #Horz ticks
        for i in range((SIZE[0] - (OFF_SET * 3) + self.tick) // self.tick):
            pygame.draw.rect(screen, BLACK,
                             [OFF_SET,
                              OFF_SET * 2 + (self.tick * i),
                              -8,
                              2])
        #Vert line
        pygame.draw.rect(screen, BLACK,
                         [OFF_SET - 1,
                          (OFF_SET * 2),
                          2,
                          SIZE[0] - OFF_SET * 3])
        
        #horz line
        pygame.draw.rect(screen, BLACK,
                         [OFF_SET,
                          SIZE[0] - OFF_SET,
                          SIZE[0],
                          2])
  
        
        if (ui.get_N() < MAX_POINTS):
            temp = spawn_points(self.count, ui)

            ui.add_total(temp)
            if (temp != 0):
                ui.add_N()
                ui.alt_ave(ui.get_total() / (ui.get_N() * 2))
                
        for point in ui.get_points():
            point.render(screen)

    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.currentstate.change(Hist_1(screen))
        return True


class IntroState(MasterState):
    def __init__(self, screen):
        MasterState.__init__(self,screen)
        self.intro_font = pygame.font.SysFont("fixedsys", 24)
        self.intro_text = self.intro_font.render("Bus wait time simulation " +
                                                 "for half hour ave. arrival",
                                                 1, BLACK)
        self.intro_text2 = self.intro_font.render("Space to Start",
                                                  1, BLACK)

    def update(self):
        pass

    def render(self,screen):
        screen.fill(RED)
        screen.blit(self.intro_text,(20,SIZE[1]/2))
        screen.blit(self.intro_text2,(SIZE[0]/2-70,SIZE[1]/2 + 30))

    def event_handler(self,events):

        for event in events:
            self.quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.currentstate.change(Hist_1(screen))
        return True

ui = UI()

if __name__ == '__main__':
    main()
