import pygame
import random
import colorsys

def random_sorted_by_HSV_colours(n):
    """
    input: n the number of colour needed
    output: a list of n random colours
    """
    colours = []
    for i in range(n):
        colours.append( (random.randint(0,255),random.randint(0,255),random.randint(0,255)) )

    colours.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    return colours 
    

class Tick(pygame.Rect):

    def __init__(self, x, y, width, height, window, disk_width = 0, disk_height = 0, n = 0):
        """
        initialize the tick and the disks
        x,y,width,height,
        window of pygame,
        n: the number of disks
        """
        #tick color
        self.n = n
        self.color = (255,255,255)
        self.window = window
        super().__init__(x, y, width, height)
        pygame.draw.rect(window, self.color, self)
        
        # initialize the rectangles to operate as disks
        self.disk_colours = random_sorted_by_HSV_colours(n)
        self.disks = []
        for i in range(1,n+1):
            tp_width = disk_width*i
            disk_x = x - (tp_width//2) + (width//2)
            self.disks.append((pygame.Rect(disk_x,y+(disk_height*i), tp_width, disk_height), self.disk_colours[i-1]))
            
        self.disks.reverse()
        del(self.disk_colours)
        for i in range(n):
            pygame.draw.rect(window, self.disks[i][1], self.disks[i][0])
            
        
            
            
    def get_disks(self):
        return self.disks
        
    def get_onTop_disk(self):
        return self.disks.pop()
        
    def append_disk(self, disk):
       if len(self.disks) > 0:
           disk[0].y = self.disks[-1][0].y - disk[0].height
       else:
           disk[0].y = self.window.get_height() - disk[0].height
           
       disk[0].x = self.x - disk[0].width//2 + self.width//2
       self.disks.append(disk)
       
    def draw(self):
        pygame.draw.rect(self.window, self.color, self)
        for i in range(len(self.disks)):
            pygame.draw.rect(self.window, self.disks[i][1], self.disks[i][0])
        
       
        

class Hanoi:
    def __init__(self,n):
        """
        initialize the pygame window
        n is the number of disk, max = 11 (2047s or 34mn to solve the problem for n = 11)
        """
        assert (n <= 11 and n >= 2)
        # Base settings of the disks
        self.n_disk = n
        self.height = 12
        self.width = 24
    
        # activate the pygame library .  
        # initiate pygame and give permission  
        # to use pygame's functionality.  
        pygame.init()
  
        # create the display surface object  
        # of specific dimension..e(500, 500).
        self.width_window = 500 + 25*n
        self.height_window =   self.height * n + 100
        self.window = pygame.display.set_mode((self.width_window, self.height_window))
  
        # set the pygame window name 
        pygame.display.set_caption("The Towers of Hanoi")
   
        # set the three emplacement
        
        self.y_tick = self.height_window - self.height*(n+1)
        self.tick_height = self.height*(n+1)
        self.tick_width = 2
        self.tick_A = Tick(self.width_window//4-1, self.y_tick, self.tick_width, self.tick_height, self.window, self.width, self.height, n)
        self.tick_B = Tick(2*self.width_window//4-1, self.y_tick, self.tick_width, self.tick_height, self.window)
        self.tick_C = Tick(3*self.width_window//4-1, self.y_tick, self.tick_width, self.tick_height, self.window)                   
        
        
        
    def move(self, n, source_tick, target_tick, auxilary_tick):
        """
        recursive algorithm to solve the tower of Hanoi
        """
        if n > 0:
            # move n-1 disk to auxilary so the last disk can go to target
            self.move(n-1, source_tick, auxilary_tick, target_tick)
            
            if len(source_tick.get_disks()) > 0:
                current_disk = source_tick.get_onTop_disk()
            else:
                return
           
            target_tick.append_disk(current_disk)
            
            # visualize the process
            pygame.time.wait(1000)
            self.window.fill((0,0,0))
            self.tick_A.draw()
            self.tick_B.draw()
            self.tick_C.draw()
            pygame.display.flip()
            pygame.time.wait(500)
            # move n-1 disk from auxilary to target
            self.move(n-1, auxilary_tick, target_tick, source_tick)
        #else:
            #return
            
            
    
    def solve(self, state):
        """
        solve the game using a recursive algorithm
        """
        pygame.time.wait(2000)
        self.move(self.n_disk, self.tick_A, self.tick_C, self.tick_B)
        state = False
        return state
        
    
    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.time.wait(3000)
            running = self.solve(running)
            pygame.display.flip()
        pygame.quit()
    
