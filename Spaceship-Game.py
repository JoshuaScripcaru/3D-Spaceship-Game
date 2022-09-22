#************ import libraries **************#
import pygame, sys, math, random, time, pymunk

#**** initializes and set global contants ***#
pygame.init()

#Set size of window
width = 800
height = 500

#Sets unseen background color
backgroundcolour = (200, 200, 200)

#Makes and colors window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star Game')
window.fill(backgroundcolour)

#Sets all used fonts
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont2 = pygame.font.SysFont('Comic Sans MS', 100)

class Game():
    
    def game(self): #Main game loop (not starting function)

        #**** Sets up envoriment ***#
        Game.makestars(self)
        Game.makeplanets(self)
        Game.makegates(self)

        #pygame.mixer.music.load('Star Wars Theme Song By John Williams.mp3')
        #pygame.mixer.music.play(-1)
        
        self.score = 0
        
        #**** Runs game play *****#
        while self.gameplay:

            for event in pygame.event.get(): #event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #for stopping python from reading code
            
            Game.gates(self) #Idendifies if players passed gates 
            Game.change_orientation(self) #Allows the player to turn
            
            Game.rotate(self.stars,self) #Rotates the enviorment
            Game.rotate(self.planets,self)
            
            Game.rotate(self.gate1,self) #Rotates each indivisual gate
            Game.rotate(self.gate2,self)
            Game.rotate(self.gate3,self)
            
            Game.moveforward(self.planets,self) #Moves the envoriment
            Game.moveforward(self.gate1,self)
            Game.moveforward(self.gate2,self)
            Game.moveforward(self.gate3,self)
            
            #Game.movemetor(self)   #** NOT USED **#
            
            window.fill((0,0,0))
            
            Game.display(self) #Displays enviroment
            Game.displayrocket(self) #Displays parent
            
            pygame.display.update() #Updates screen
            pygame.event.pump() #Prevents from pygame stopping the loop
            
            pygame.time.delay(int(1000/self.fps)) #Sets the delay


    
    def run(self): #Starts the whole game.

        #****** Sets Game Varibles *********#
        window.fill((0,0,0))
        
        self.score = 0
        self.speed = 1.5
        self.stars = [] #Location of stars 
        self.planets = [] #Location of planets
        self.planetsradius = []

        #**** Non Existant Meteor Varibles ****#
        self.metor = []
        self.metorspeed = []

        #**** Player Varibles ***#
        self.orientation = [0,0] #[Pitch, Yaw]
        self.viewpoint = [0.15,0,0]
        
        #Gates players will inteact with
        self.gate1 = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #Nearest Gate
        self.gate2 = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #Middle Gate
        self.gate3 = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #Furthest Gate
        
        self.fps = 30
        self.gameplay = False #Says of game in running
        self.menue = True #Says of a menue screen is on 
        
        self.R_press = False #Says if R was pressed in the previous frame

        #********************** Sets Up Start Menue ***************************#
        
        for i in range(0,300): #Start screen background plantes
            
            rgb = (int(random.uniform(170,255)),int(random.uniform(170,255)),int(random.uniform(0,100))) #Sets colo4
            xy = [int(random.uniform(0,800)),int(random.uniform(0,800))] #Sets pos
            ra = random.uniform(2,6) #Sets size
            
            if xy[0] > 320 and xy[0] < 490 and xy[1] > 170 and xy[1] < 330: #Prevents over lap with botton
                ra = 0
                
            else:
                pygame.draw.circle(window, rgb, xy , int(ra)) #Draws planets
        
        pygame.display.update()
        
        #pygame.mixer.music.load('Jaws-theme-song.mp3')
        #pygame.mixer.music.play(-1)

        #************* Start Menue Loop ***********************************#
        while self.menue:
            
            xy = pygame.mouse.get_pos()
            pygame.event.pump()
            color = (255,255,0)
            
            if xy[0] > 320 and xy[0] < 490 and xy[1] > 170 and xy[1] < 330: #Changes color when mouse is over the sign
                color = (255,255,255)
                
                if pygame.mouse.get_pressed()[0]: #If mouse gets pressed the user is sent out of menue loop
                    self.menue = False
                    
            textsurface = myfont2.render("Play", False, color)
            window.blit(textsurface,(320,170)) #Displays the text

            for event in pygame.event.get(): #event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #for stopping python from reading code
            
            pygame.display.update()

        self.gameplay = True #Allows the main game loop to 
        Game.game(self) #Sets them code to main game loop


#***************  Math Functions *************************#
        
    def matmul(transform,vector): #Matrix Multiplication
        new = [] #Transformed Vector
        
        for i in range (0,3): #Each dimention of transformend vectore
            d = 0
            
            for j in range (0,3): 
                d += vector[j]*transform[i][j] #Actual Matrix Multiplcation 
                
            new.append(d) #Add dimention to vector

        return new 

    def det(x,y,z): #3D Determinant
        
        det = 0 #Area
        
        for i in range (0,3): #Calculations for each dimention
            det += x[i%3]*y[(i+1)%3]*z[(i+2)%3]
            det -= z[i%3]*y[(i+1)%3]*x[(i+2)%3]
            
        return (det)

    #****************** Restart Menue Enviorment ****************#
    def restart(self):
        
        self.menue = True
        self.gameplay = False
        
        textsurface = myfont2.render(str(self.score), False, (255,255,255))
        window.blit(textsurface,(375,60)) #Shows score
        
        textsurface = myfont2.render("Play Again", False, (230,230,230))
        window.blit(textsurface,(200,170)) #Play Again Button

        #pygame.mixer.music.load('Star Wars- The Imperial March (Darth Vader\'s Theme).mp3')
        #pygame.mixer.music.play(-1)
        
        self.speed = 1.5 #Resets speed
        
        #******** Restart Menue Loop ************#
        
        while self.menue:
            
            xy = pygame.mouse.get_pos()
            pygame.event.pump()  #Prevents from pygame stopping the loop
            
            color = (255,0,0)
            
            pygame.display.update() #Update screen here
            
            if xy[0] > 200 and xy[0] < 680 and xy[1] > 190 and xy[1] < 300:
                color = (255,255,255) #Changes color of sign when mouse is over top
                
                if pygame.mouse.get_pressed()[0]:
                    self.menue = False #Breaks out of loop

            for event in pygame.event.get(): #event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #for stopping python from reading code
                    
            textsurface = myfont2.render("Play Again", False, color)
            window.blit(textsurface,(200,170))

        #Sets and resets varibles of main game loop
        self.gameplay = True
        self.planets = []
        self.planetsradius = []
        self.stars = []
        self.orientation = [0,0]
        
        Game.game(self) #Main game loop

    #***************** Interactions with Gates ************************#

    def gates(self):
        keys = pygame.key.get_pressed()

        #****** Re-Adjust Gates (when tilted ****************#

        delta_x = self.gate1[0][1]-self.gate1[2][1] #finds dimentions of gate appearence
        delta_y = self.gate1[0][2]-self.gate1[2][2]
        distance = (delta_x**2+delta_y**2)**0.5
        
        sin = delta_y/distance #finds the sin and cos of the angle tilted
        cos = delta_x/distance

        if sin > 0.05 or (keys[pygame.K_r] and self.R_press == False) or (sin > 0.005 and self.score > 25): #Starts to rotate gates back
            
            a = [[1,0,0],[0,-cos,-sin],[0,sin,-cos]] #Rotation matrix
        
            for i in range (0,4): #Rotates the gates
                self.gate1[i] = Game.matmul(a,self.gate1[i])
                self.gate2[i] = Game.matmul(a,self.gate2[i])
                self.gate3[i] = Game.matmul(a,self.gate3[i])

            for i in range (0,len(self.planets)): #Rotates the planets
                self.planets[i] = Game.matmul(a,self.planets[i])
                
            for i in range (0,len(self.stars)): #Rotates the stars
                self.stars[i] = Game.matmul(a,self.stars[i])

            self.R_press = True  #Prevents the funtion from running repeatedly
            
        else:
            self.R_press = False
            
        #********************* Adds scoring and makes new gates ***********************#
        
        if abs(Game.det(self.gate1[0],self.gate1[1],self.gate1[2])) < 0.01*self.speed: #finds of player is on the same plane as gate
            
            if self.gate1[0][1] <= 0.005 and self.gate1[0][2] <= 0.005 and self.gate1[3][1] >= -0.005 and self.gate1[3][2] >= -0.005: #Checks of player is in or out of gate
                
                for i in range (0,4):
                    self.gate1[i] = self.gate2[i] #Turns gate 2 into gate 1
                    self.gate2[i] = self.gate3[i] #Turns gate 3 into gate 2
                    
                y = random.uniform(-1.2,1.2) #Position of new gate
                z = random.uniform(-1.2,1.2)
                    
                x_avg = (self.gate3[0][0]+self.gate3[1][0]+self.gate3[2][0]+self.gate3[3][0])*0.25
                y_avg = (self.gate3[0][1]+self.gate3[1][1]+self.gate3[2][1]+self.gate3[3][1])*0.25
                z_avg = (self.gate3[0][2]+self.gate3[1][2]+self.gate3[2][2]+self.gate3[3][2])*0.25
                
                self.gate3[0] = [10 + x_avg, y_avg + y - 0.3, z_avg + z - 0.15] #Establishes new gate
                self.gate3[1] = [10 + x_avg, y_avg + y - 0.3, z_avg + z + 0.15]
                self.gate3[2] = [10 + x_avg, y_avg + y + 0.3, z_avg + z - 0.15]
                self.gate3[3] = [10 + x_avg, y_avg + y + 0.3, z_avg + z + 0.15]
                
                self.score += 1 #Update score
                Game.updateplanets(self) #Makes new set of planets ahead
                self.speed += 0.2 #Updates speed

            else:
                Game.restart(self)
                
    def makegates(self): #Makes the gates in predetermined positions
        
        self.gate1 = [[5,-0.3,-0.15],[5,-0.3,0.15],[5,0.3,-0.15],[5,0.3,0.15]]
        self.gate2 = [[15,-0.3,-0.15],[15,-0.3,0.15],[15,0.3,-0.15],[15,0.3,0.15]]
        self.gate3 = [[25,-0.3,-0.15],[25,-0.3,0.15],[25,0.3,-0.15],[25,0.3,0.15]]

        self.metor = [[10,-0.2,-0.2],[10,-0.2,-0.2],[11,0.2,-0.2],[11,0.6,0.2]]   #** NOT USED **#
        self.metorspeed = [0.05,0.05,0.05]                                        #** NOT USED **#
        
    def display(self): #Puts the envoirment through the show function
        
        starL = len(self.stars) 
        for i in range (0,starL): #Displays each star
            Game.show(self.stars[i],3,False,self,(255,255,255))
        
        planetsL = len(self.planets)
        for i in range (0,planetsL): #Displays each planet
            Game.show(self.planets[i],self.planetsradius[i],True,self,(200,150,0))
        

        Game.showline(self.gate3[0],self.gate3[1],5,True,self,(0,0,255)) #Displays gate 3
        Game.showline(self.gate3[0],self.gate3[2],5,True,self,(0,0,255))
        Game.showline(self.gate3[3],self.gate3[1],5,True,self,(0,0,255))
        Game.showline(self.gate3[3],self.gate3[2],5,True,self,(0,0,255))

        Game.showline(self.gate2[0],self.gate2[1],5,True,self,(255,0,0)) #Displays gate 2
        Game.showline(self.gate2[0],self.gate2[2],5,True,self,(255,0,0))
        Game.showline(self.gate2[3],self.gate2[1],5,True,self,(255,0,0))
        Game.showline(self.gate2[3],self.gate2[2],5,True,self,(255,0,0))

        Game.showline(self.gate1[0],self.gate1[1],5,True,self,(0,255,0)) #Displays gate 1
        Game.showline(self.gate1[0],self.gate1[2],5,True,self,(0,255,0))
        Game.showline(self.gate1[3],self.gate1[1],5,True,self,(0,255,0))
        Game.showline(self.gate1[3],self.gate1[2],5,True,self,(0,255,0))

        textsurface = myfont.render(str(self.score), False, (255, 255, 255)) #Shows score during gameplay
        window.blit(textsurface,(10,5))
            
    def show(p3Dlist,radius,Scale,self,color): #Function for displaying points
        
        screenx = 3 #Distance user pojected screen is
        screeny = 2 #Width of projected screen
        height = 500
        width = 800
        screenz = screeny*height/width #Height of projected screen
        
        xpos = p3Dlist[0]+ self.viewpoint[0] #Accouts for players view
        ypos = p3Dlist[1]+ self.viewpoint[1]
        zpos = p3Dlist[2]+ self.viewpoint[2]
        
        r = radius
        
        if Scale: #For scaling size of planets and editing them
            d = ((p3Dlist[0])**2 +(p3Dlist[1])**2 +(p3Dlist[2])**2)**0.5 #Finds distance
            
            if xpos > 0.01 and d < 70 and d > r: #Filters out far and non visible planets
                
                #r = r/(((d**2-(p3Dlist[2])**2)**0.5+p3Dlist[0])**0.5-r) #** NOT USED **#
                r = 0.7 
                
            #if d <= radius: # Collision check  #**NOT USED **#
                #Game.restart(self)

        ypos = screenx*ypos*width/(xpos*screeny)
        zpos = screenx*zpos*height/(xpos*screenz)
        
        if r > 0 and xpos > 0.01: #Displays only visible planets 
                pygame.draw.circle(window, color, [int(ypos+400),int(-zpos+250)], int(0.9)) #Draws object
                
    def showline(p3Dlist1,p3Dlist2,radius,Scale,self,color): #Function for displaying lines
        screenx = 3 #Distance user pojected screen is
        screeny = 2 #Width of projected screen
        height = 500
        width = 800
        
        screenz = screeny*height/width #Height of projected screen
        
        xpos1 = p3Dlist1[0]+ self.viewpoint[0] #Accouts for players view
        ypos1 = p3Dlist1[1]+ self.viewpoint[1]
        zpos1 = p3Dlist1[2]+ self.viewpoint[2]
        
        xpos2 = p3Dlist2[0]+ self.viewpoint[0]
        ypos2 = p3Dlist2[1]+ self.viewpoint[1]
        zpos2 = p3Dlist2[2]+ self.viewpoint[2]
        
        r = radius
        
        if Scale: #Scaling thinkness of line
            d = 0.5*((xpos1+xpos2)**2 +(ypos1+ypos2)**2 +(zpos1+zpos2)**2)**0.5
            r = (r/d)+1
            
        if xpos1 > 0.001 and xpos2 > 0.001: #Finds the position of line on screen
            
                ypos1 = screenx*ypos1*width/(xpos1*screeny)
                zpos1 = screenx*zpos1*height/(xpos1*screenz)
                
                ypos2 = screenx*ypos2*width/(xpos2*screeny)
                zpos2 = screenx*zpos2*height/(xpos2*screenz)
                
                pygame.draw.line(window, color, [int(ypos1+400),int(-zpos1+250)],[int(ypos2+400),int(-zpos2+250)], int(r)) #Draws line on screen


    def drawtriangle(p3Dlist1,p3Dlist2,p3Dlist3,color,self): #For displaying 3d triangles ****NOT USED IN PROGRAM **** 
        screenx = 3
        screeny = 2
        height = 500
        width = 800
        screenz = screeny*height/width
        
        xpos1 = p3Dlist1[0]+ self.viewpoint[0]
        ypos1 = p3Dlist1[1]+ self.viewpoint[1]
        zpos1 = p3Dlist1[2]+ self.viewpoint[2]
        
        xpos2 = p3Dlist2[0]+ self.viewpoint[0]
        ypos2 = p3Dlist2[1]+ self.viewpoint[1]
        zpos2 = p3Dlist2[2]+ self.viewpoint[2]
        
        xpos3 = p3Dlist3[0]+ self.viewpoint[0]
        ypos3 = p3Dlist3[1]+ self.viewpoint[1]
        zpos3 = p3Dlist3[2]+ self.viewpoint[2]
        
        if xpos1 > 0.001 and xpos2 > 0.001 and xpos3 > 0.001:
                ypos1 = screenx*ypos1*width/(xpos1*screeny) + 400
                zpos1 = -screenx*zpos1*height/(xpos1*screenz) + 250
                ypos2 = screenx*ypos2*width/(xpos2*screeny) + 400
                zpos2 = -screenx*zpos2*height/(xpos2*screenz) + 250
                ypos3 = screenx*ypos3*width/(xpos3*screeny) + 400
                zpos3 = -screenx*zpos3*height/(xpos3*screenz) + 250
                
                pygame.draw.polygon(window, color, [[int(ypos1),int(zpos1)],[int(ypos2),int(zpos2)],[int(ypos3),int(zpos2)]], 0)

    def movemetor(self):   # for moving metors #**** NOT USED IN PROGRAMS ***#
        
        Game.rotate([self.metorspeed],self)
        Game.rotate(self.metor,self)
        Game.moveforward(self.metor,self)
        
        for i in range(0,4):
            for j in range(0,3):
                self.metor[i][j] = float(self.metor[i][j]) + self.metorspeed[j]/self.fps

        Game.drawtriangle(self.metor[0],self.metor[1],self.metor[2],(200,50,50),self)
        Game.drawtriangle(self.metor[0],self.metor[1],self.metor[3],(200,50,50),self)
        Game.drawtriangle(self.metor[0],self.metor[2],self.metor[3],(200,50,50),self)
        Game.drawtriangle(self.metor[1],self.metor[2],self.metor[3],(200,50,50),self)
        
    def rotate(relpoints,self): #Rotates points around user

        p,y = self.orientation #Takes out pitch and yaw
        
        sin_w = math.sin(y) #Yaw angle
        cos_w = math.cos(y)
        sin_p = math.sin(p) #Pitch angle
        cos_p = math.cos(p)

        a = [[cos_w,sin_w,0],[-sin_w,cos_w,0],[0,0,1]] #Right is + (This moves the user left and right)
        for i in range (0,len(relpoints)):
                relpoints[i] = Game.matmul(a,relpoints[i])
        
        a = [[cos_p,0,-sin_p],[0,1,0],[sin_p,0,cos_p]] #Up is + (This moves the user up and down)
        for i in range (0,len(relpoints)):
            relpoints[i] = Game.matmul(a,relpoints[i])

    def change_orientation(self): #Tilts the player's rocket

        MAX_pitch = math.pi/100
        MAX_yaw = math.pi/100
        
        Pc = 0.1 #Speed the user can turn at
        Wc = Pc
        
        PR = 0.7 #Speed the user returns back at flying position
        WR = PR

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.orientation[1] += (MAX_yaw - self.orientation[1])*Wc
            self.orientation[0] *= PR
	    
        elif keys[pygame.K_LEFT]:
            self.orientation[1] -= (MAX_yaw + self.orientation[1])*Wc
            self.orientation[0] *= PR

        elif keys[pygame.K_UP]:
            self.orientation[0] += (-self.orientation[0] - MAX_yaw)*Pc
            self.orientation[1] *= WR

        elif keys[pygame.K_DOWN]:
            self.orientation[0] -= (self.orientation[0] - MAX_yaw)*Pc
            self.orientation[1] *= WR

        else: #When user isn't pressing anything
            self.orientation[0] *= PR
            self.orientation[1] *= WR

    def moveforward(p3Dlist,self): #Moves envoirment towards player
        
        for i in range (0,len(p3Dlist)): #Iliterates through list
            p3Dlist[i][0] = float(p3Dlist[i][0]) - self.speed/self.fps

    def makestars(self): #Makes the stars in eniorment
        
        for i in range(0,100): #Make 100 stars
            
            o = random.uniform(0,6.28)#Angle with x and z axis
            q = random.uniform(0,6.28)
            
            x = 10*math.sin(q)*math.cos(o) #Convert from polar coordinates
            y = 10*math.sin(q)*math.sin(o)
            z = 10*math.cos(q)
            
            self.stars.append([x,y,z]) #Add star to list

    def makeplanets(self): #Makes planets in enviorment
        
        for j in range(0,10): #Makes planets in 10 sets
            for i in range (0,80): #Each set has 20 planets
                
                x = random.uniform(0,10)
                y = random.uniform(-25,25)
                z = random.uniform(-25,25)
                r = random.uniform(1.5,4)
                
                self.planets.append([x+j*10,y,z]) #Adds to list of planets
                self.planetsradius.append(r) #Stores radius in seperate list

    def updateplanets(self): #Updates planet location when player progresses
        for i in range(0,20): #Takes out oldest 2 sets
            
            x = random.uniform(0,10)
            y = random.uniform(-25,25)
            z = random.uniform(-25,25)
            r = random.uniform(1.5,4)
            
            self.planets[i+((self.score-1)%10)*40] = [x+80,y,z] #Change oldest set to new set
            self.planetsradius[i+((self.score-1)%10)*40] = r #Updates the radius
    
    def displayrocket(self): #Displays the rocket
        
        y = self.orientation[1] #Yaw
        p = self.orientation[0] #Pitch
        sin_w = math.sin(y*13) #Sine and Cosine of pitch and yaw
        cos_w = math.cos(y*13)
        sin_p = math.sin(p*10)
        cos_p = math.cos(p*10)
        
        tri = [[400,int(330+80*sin_p+5)],[int(400-50*cos_w-15*sin_p), int(350-50*sin_w-15*sin_p)],[int(400+50*cos_w), int(350+50*sin_w)]] #Main body triangle location
        eng1 = [int(400-25*cos_w), int(350-25*sin_w)] #Booster location
        eng2 = [int(400+25*cos_w), int(350+25*sin_w)]
        
        pygame.draw.polygon(window, (210,210,50), tri) #Draw main body triangle 
        pygame.draw.circle(window, (100,100,100), eng1, int(10)) #Left booster outside
        pygame.draw.circle(window, (255,100,0), eng1, int(7)) #Left booster inside
        pygame.draw.circle(window, (100,100,100), eng2, int(10)) #Right booster outside
        pygame.draw.circle(window, (255,100,0), eng2, int(7)) #Right booster inside


p1 = Game() #Creates a game object
p1.run() #Runs the function to start the game
