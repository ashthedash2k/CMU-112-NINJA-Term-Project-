#Ashley Czumak (aczumak)
from cmu_112_graphics import *
import time
import math
import random 

def appStarted(app):
    app.centerX = app.width/2
    app.centerY = app.height/2

    #background
    background = "backgroundninja.png"
    title = "title3.png"
    app.background = Image.open(background)
    app.background = app.background.resize((app.width, app.height))
    app.title = Image.open(title)
    app.title = app.title.resize((500, app.height//2))

    #scoreing
    app.livesCount = 0
    app.highScore = 0
    app.score = 0
    app.allScores = open("scores.txt", "r+")
    app.allScoresList = []

    #functionality for updating the scores
    for line in app.allScores.readlines():
        app.allScoresList.append(int(line))
        app.allScoresList.sort()

    if len(app.allScoresList) > 0:
        app.highScore = app.allScoresList[-1]
    app.allScores.close() 
    
    #mouse related
    app.mouseX = 0
    app.mouseY = 0
    app.dragged = False
    app.released = True
    app.paused = False
    app.listMouseCoord = []

    #images
    instructions = "instructions3.png"
    goToHome = "homefinal.png"
    allLives = "alllives.png"
    twoLives = "twolives.png"
    oneLive = "onelive.png"
    noLives = "nolives.png"
    howToPlayGame = "how2playgame3.png"
    gameOverIcon = "gameover.png"
    readyIcon = "ready.png"
    goIcon = "go.png"
    app.animatedSliceToPlay = loadAnimatedGif("animateddragon.gif")
    app.animatedSliceToPlayCounter = 0
    app.animatedHome = loadAnimatedGif("animatedhome.gif")
    app.animatedHomeCounter = 0

    app.instructions = Image.open(instructions)
    app.instructions = app.instructions.resize((250, app.height//6))
    
    app.goToHome = Image.open(goToHome)
    app.goToHome = app.goToHome.resize((app.width//2, app.height//4))

    app.allLives = Image.open(allLives)
    app.allLives = app.allLives.resize((300, app.height//4))

    app.twoLives = Image.open(twoLives)
    app.twoLives = app.twoLives.resize((300, app.height//4))

    app.oneLive = Image.open(oneLive)
    app.oneLive = app.oneLive.resize((300, app.height//4))

    app.noLives = Image.open(noLives)
    app.noLives = app.noLives.resize((300, app.height//4))

    app.howToPlayGame = Image.open(howToPlayGame)
    app.howToPlayGame = app.howToPlayGame.resize((app.width//2, app.height//6))

    app.gameOverIcon = Image.open(gameOverIcon)
    app.gameOverIcon = app.gameOverIcon.resize((app.width//2, app.height//4))

    app.readyIcon = Image.open(readyIcon)
    app.readyIcon = app.readyIcon.resize((app.width//2, app.height//4))

    app.goIcon = Image.open(goIcon)
    app.goIcon = app.goIcon.resize((app.width//2, app.height//4))

    '''
    If we hit a bomb, we want to empty our list and end game. But we don't want our list
    to start off as being empty, so we have test default ball, and generate randomness from 
    there
    '''
    app.defaultBomb = FlyingObject(300, 300, 400, 400, 150, 180, -3, 90, 99, -70, "black", 'bomb')
    app.listOfFlyingObjects = [app.defaultBomb]
    #list to keep track of Piece objects created (the broken fruit pieces)
    app.listOfBrokenPieces = []

    #used across all levels
    app.fruitColors = ['red', 'pink', 'blue', 'yellow', 'green', 'orange']
    app.randomAccelerationY = [-50, -70, -90, -120]
    
    #level 1 (easy)
    '''
    more fruit, less bomb, bigger fruit
    '''
    app.typeOfObjectLevel1 = ['fruit', 'fruit', 'fruit', 'fruit', 'fruit', 'bomb', 'fruit', 'fruit','fruit' ]
    app.firstFruitCoordinatesLevel1 = [100, 150, 200, 250]
    app.secondFruitCoordinatesLevel1 = [100, 150, 200, 250]
    app.bombCoordinatesLevel1 = [50, 100]
    app.changeInXsLevel1 = [100, 200, 200, 300, 300]
    app.changeInYsLevel1 = [50, 50, 100, 200, 200, 300, 300]

    #level 2 (medium)
    '''
    addition of more bombs, smaller fruit
    '''
    app.typeOfObjectLevel2 = ['fruit', 'fruit', 'fruit', 'fruit', 'bomb', 'bomb', 'bomb', 'fruit','fruit' ]
    app.firstFruitCoordinatesLevel2 = [100, 150, 200]
    app.secondFruitCoordinatesLevel2 = [100, 150, 200]
    app.bombCoordinatesLevel2 = [100, 150, 200]
    app.changeInXsLevel2 = [100, 200, 200, 300, 300, 400, 500]
    app.changeInYsLevel2 = [50, 50, 100, 200, 300, 300, 400, 400]

    #level 3 (hard)
    '''
    addition of many bombs, smallest fruit variations
    '''
    app.typeOfObjectLevel3 = ['fruit', 'fruit', 'fruit', 'bomb', 'bomb', 'bomb', 'bomb', 'bomb','bomb', 'fruit', 'fruit', 'fruit', 'fruit', 'fruit']
    app.firstFruitCoordinatesLevel3 = [50, 100, 125]
    app.secondFruitCoordinatesLevel3 = [50, 100, 125]
    app.bombCoordinatesLevel3 = [200, 300, 350]
    app.changeInXsLevel3 = [100, 200, 200, 300, 300, 400, 500, 600]
    app.changeInYsLevel3 = [50, 50, 100, 200, 200, 300, 300, 400, 400, 400]

    #slices
    app.currentSlice = None

    #time to measure elapsed time
    app.timeElapsed = 0
    app.startTime = time.time()

def loadAnimatedGif(path):
    #cited from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

def keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    if (event.key == 'p'):
        app.mode = 'playMode'
    if (event.key == 'e'):
        app.mode = ''

#help mode
def helpMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    if (event.key == 'p'):
        app.mode = 'playMode'
    if (event.key == 'e'):
        app.mode = ''

def helpMode_timerFired(app):
    app.background = app.background.resize((app.width, app.height))
    app.animatedSliceToPlayCounter = (1 + app.animatedHomeCounter) % len(app.animatedHome)

def helpMode_mouseDragged(app, event):
    app.dragged = True 
    app.mouseX = event.x
    app.mouseY = event.y
    app.released = False
    app.listMouseCoord.append((event.x, event.y))

def helpMode_mouseReleased(app, event):
    app.dragged = False
    app.listMouseCoord = []

def helpMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    font = 'Arial 26 bold'

    canvas.create_image(app.width/2, app.height/3, image=ImageTk.PhotoImage(app.howToPlayGame))
    canvas.create_text(app.width/2, app.height/2, text='''
    Use your mouse to slice the coloured flying fruit on the screen! 
    Be sure to not hit the black bombs :O 
    Everytime you hit a fruit you get 10 pts added to your score, 
    but even more for combos and if you hit special fruits!
    Navigate with keys H for instructions, E for home and P for play :)''',
                       font=font, fill='white')

    for coord in range(len(app.listMouseCoord) -1 ):
        canvas.create_line(app.listMouseCoord[coord][0], app.listMouseCoord[coord][1], 
        app.listMouseCoord[coord + 1][0], app.listMouseCoord[coord + 1][1], fill='white')

#play mode
class FlyingObject:
    '''
    class that simulates the parabolic arc of an object being thrown, used with real
    kinematics
    '''
    def __init__(self, initialX0, initialY0, initialX1, initialY1,
    changeInX, changeInY, timeRun, velocityX, velocityY, accelerationY, color, typeObject):
        self.initialX0 = initialX0
        self.initialY0 = initialY0
        self.initialX1 = initialX1
        self.initialY1 = initialY1
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.changeInX = changeInX #make negative 
        self.changeInY = changeInY
        self.timeRun = timeRun
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.accelerationY = accelerationY 
        self.color = color
        self.typeObject = typeObject #differentiates fruit and bomb, same behaviour of movement but some different properties
        self.isSliced = False
        self.increaseTimeRun = 0.1 #defalt speed, but increase with level increase
        self.offScreen = 0
    
    def calculateArc(self, app):
        '''
        Function calculates the coordinates of the arc of the fruit for every time frame.
        '''
        self.timeRun +=  self.increaseTimeRun #change this to influence speed of the objects
        self.y0 = self.initialY0 + self.changeInY + self.velocityY * self.timeRun + (self.accelerationY//2) * (self.timeRun**2)
        self.x0 = self.initialX0 + self.changeInX + self.velocityX * self.timeRun + self.timeRun**2
        self.y1 = self.initialY1 + self.changeInY + self.velocityY * self.timeRun + (self.accelerationY//2) * (self.timeRun**2)
        self.x1 = self.initialX1 + self.changeInX + self.velocityX * self.timeRun + self.timeRun**2

        x0 = app.width-self.x0
        y0 = app.height-self.y0
        x1 = app.width-self.x1
        y1 = app.height-self.y1
        return (x0, y0, x1, y1)
  
    def drawArc(self, canvas, app):
        '''
        function that actually draws the fruit on the screen at its correct coordinates
        '''
        x0 = app.width-self.x0
        y0 = app.height-self.y0
        x1 = app.width-self.x1
        y1 = app.height-self.y1
        canvas.create_oval(x0, y0, x1, y1, fill=self.color, outline='black')

    def isTouched(self, app):
        '''
        Collison method to detect of a slice has collided with a fruit object.
        '''
        x0 = app.width-self.x0
        y0 = app.height-self.y0
        x1 = app.width-self.x1
        y1 = app.height-self.y1
        centerX = (x1 + x0)/2
        centerY = (y1 + y0)/2

        #no calculations if no mouse coordinates!
        if len(app.listMouseCoord) == 0:
            return False
        '''
        loop through all the mouse coordinates and check the first one that is true, this is good
        for slicing accuracy
        '''
        for pairs in range(len(app.listMouseCoord) - 1):
            distance = math.sqrt((app.listMouseCoord[pairs][0] - (centerX))**2 + (app.listMouseCoord[pairs][1] - (centerY))**2)
            if distance <= abs((self.x0 - self.x1)/2):
                self.isSliced = True
                break
            else:
                self.isSliced = False

        return self.isSliced

    #getters and setters for writing clean code
    def setTimeRun(self, value):
        self.increaseTimeRun = value

    def returnIsSliced(self):
        return self.isSliced

    def returnTypeObject(self):
        return self.typeObject
    
    def incrementOffScreen(self):
        self.offScreen += 1
    
    def returnOffScreen(self):
        return self.offScreen 
    
    def returnTimeRun(self):
        return self.timeRun
    
    def __repr__(self):
        #debugging purposes
        return f'{self.color}'
 
class Pieces(FlyingObject):
    '''
    class that created objects of the broken pieces of fruit. Inherits main functionality 
    from flying object class, however now two semi circles are drawn to represent the broken
    fruit.
    '''
    def __init__(self, initialX0, initialY0, initialX1, initialY1,
    changeInX, changeInY, timeRun, velocityX, velocityY, accelerationY, color, x0, y0, x1, y1):
        super().__init__(initialX0, initialY0, initialX1, initialY1, changeInX, changeInY, timeRun, velocityX, velocityY, accelerationY, color, "fruit")
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.rotateOne = 20
        self.rotateTwo = 200

    def changeRotation(self):
        '''
        Function to change the rotation of the pieces while they fall.
        '''
        self.rotateOne += -20
        self.rotateTwo += 20

    def drawArc(self, canvas,app):
        x0 = app.width-self.x0
        y0 = app.height-self.y0
        x1 = app.width-self.x1
        y1 = app.height-self.y1
                
        #adjust coordinates to add space between the slices
        canvas.create_arc(x0, y0, x1, y1, start=self.rotateOne, extent=180, fill=self.color, outline='black')
        canvas.create_arc(x0 + 10, y0 + 10, x1 + 10, y1 + 10, start=self.rotateTwo, extent=180, fill=self.color, outline='black')

class Slice(FlyingObject):
    '''
    Create instances of slices to have combos. Additional points added per combo. 
    '''
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.combo = -1

    def slicedTimes(self):
        '''
        Counts how many times objects have been sliced per slice instance. 
        Combo is calculated based on this factor.
        '''
        self.combo += 1
        return self.combo

    def returnCombo(self):
        return self.combo

class SpecialFruit(FlyingObject):
    def __init__(self, initialX0, initialY0, initialX1, initialY1,
    changeInX, changeInY, timeRun, velocityX, velocityY, accelerationY, color, x0, y0, x1, y1):
        super().__init__(initialX0, initialY0, initialX1, initialY1, changeInX, changeInY, timeRun, velocityX, velocityY, accelerationY, color, "fruit")
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

def playMode_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'
    if (event.key == 'e'):
        app.mode = ''
    if (event.key == 'p'):
        app.mode = 'playMode' 

def playMode_mouseDragged(app, event):
    app.dragged = True 
    app.mouseX = event.x
    app.mouseY = event.y
    app.released = False
    app.listMouseCoord.append((event.x, event.y))

    if not app.currentSlice:
        app.currentSlice = Slice(app.listMouseCoord)

def playMode_mouseReleased(app, event):
    app.dragged = False
    app.listMouseCoord = []
    #get combo data outa current slice before destroy 
    app.currentSlice = None
   
def playMode_timerFired(app):
    app.background = app.background.resize((app.width, app.height))
    app.timeElapsed += 1
    timedPlay = time.time() - app.startTime
    
    #level 1
    if int(timedPlay) <= 50:
        if app.timeElapsed % 20 == 0 and len(app.listOfFlyingObjects):
            #we want the same respective coordinates
            x0 = random.choice(app.firstFruitCoordinatesLevel1)
            y0 = x0
            x1 = random.choice(app.secondFruitCoordinatesLevel1)
            y1 = x1
            while x0 == x1:
                x0 = random.choice(app.firstFruitCoordinatesLevel1)
                y0 = x0
                x1 = random.choice(app.secondFruitCoordinatesLevel1)
                y1 = x1

            #fruit/bomb properties
            #handle type of fruits
            typeOfFruit = random.choice(app.typeOfObjectLevel1)
            color = ''
            
            #directions
            changeInX = random.choice(app.changeInXsLevel1)
            changeInY = random.choice(app.changeInYsLevel1)

            if typeOfFruit == 'bomb':
                color = 'black'
                x0 = random.choice(app.bombCoordinatesLevel1)
                y0 = x0
                x1 = random.choice(app.bombCoordinatesLevel1)
                y1 = x1
                while x0 == x1:
                    x0 = random.choice(app.firstFruitCoordinatesLevel1)
                    y0 = x0
                    x1 = random.choice(app.secondFruitCoordinatesLevel1)
                    y1 = x1
            else:
                color = random.choice(app.fruitColors)

            app.listOfFlyingObjects.append(FlyingObject(
                x0, 
                y0, 
                x1, 
                y1, 
                changeInX, 
                changeInY,
                -3, 40, 50, -70, color, typeOfFruit))
    #level 2
    if int(timedPlay) > 50 and int(timedPlay) <=100:
        if app.timeElapsed % 10 == 0 and len(app.listOfFlyingObjects):
            #we want the same respective coordinates
            x0 = random.choice(app.firstFruitCoordinatesLevel2)
            y0 = x0
            x1 = random.choice(app.secondFruitCoordinatesLevel2)
            y1 = x1
            while x0 == x1:
                x0 = random.choice(app.firstFruitCoordinatesLevel1)
                y0 = x0
                x1 = random.choice(app.secondFruitCoordinatesLevel1)
                y1 = x1

            #fruit/bomb properties
            #handle type of fruits
            typeOfFruit = random.choice(app.typeOfObjectLevel2)
            color = ''
            
            #directions
            changeInX = random.choice(app.changeInXsLevel2)
            changeInY = random.choice(app.changeInYsLevel2)
            accelerationY = random.choice(app.randomAccelerationY)

            if typeOfFruit == 'bomb':
                color = 'black'
                x0 = random.choice(app.bombCoordinatesLevel2)
                y0 = x0
                x1 = random.choice(app.bombCoordinatesLevel2)
                y1 = x1
                while x0 == x1:
                    x0 = random.choice(app.firstFruitCoordinatesLevel1)
                    y0 = x0
                    x1 = random.choice(app.secondFruitCoordinatesLevel1)
                    y1 = x1
            else:
                color = random.choice(app.fruitColors)
                
            addedFruit = FlyingObject(
                x0, 
                y0, 
                x1, 
                y1, 
                changeInX,
                changeInY,
                -4, 90, 20, accelerationY, color, typeOfFruit)
            #increase speed
            addedFruit.setTimeRun(0.18)
            app.listOfFlyingObjects.append(addedFruit)
    
    #level 3
    if int(timedPlay) > 100:
        if app.timeElapsed % 5 == 0 and len(app.listOfFlyingObjects):
            #we want the same respective coordinates
            x0 = random.choice(app.firstFruitCoordinatesLevel3)
            y0 = x0
            x1 = random.choice(app.secondFruitCoordinatesLevel3)
            y1 = x1
            while x0 == x1:
                x0 = random.choice(app.firstFruitCoordinatesLevel1)
                y0 = x0
                x1 = random.choice(app.secondFruitCoordinatesLevel1)
                y1 = x1

            #fruit/bomb properties
            #handle type of fruits
            typeOfFruit = random.choice(app.typeOfObjectLevel3)
            color = ''
            
            #directions
            changeInX = random.choice(app.changeInXsLevel3)
            changeInY = random.choice(app.changeInYsLevel3)
            accelerationY = random.choice(app.randomAccelerationY)

            if typeOfFruit == 'bomb':
                color = 'black'
                color = 'black'
                x0 = random.choice(app.bombCoordinatesLevel3)
                y0 = x0
                x1 = random.choice(app.bombCoordinatesLevel3)
                y1 = x1
                while x0 == x1:
                    x0 = random.choice(app.firstFruitCoordinatesLevel1)
                    y0 = x0
                    x1 = random.choice(app.secondFruitCoordinatesLevel1)
                    y1 = x1
            else:
                color = random.choice(app.fruitColors)

            addedFruit = FlyingObject(
                x0, 
                y0, 
                x1, 
                y1, 
                changeInX, 
                changeInY,
                -4, 90, 20, accelerationY, color, typeOfFruit)
            #throw faster
            addedFruit.setTimeRun(0.3)
            app.listOfFlyingObjects.append(addedFruit)

    for flyingObjects in app.listOfFlyingObjects:
        (x0, y0, x1, y1) = flyingObjects.calculateArc(app)
        if len(app.listOfBrokenPieces) > 0:
            #if broken pieces exist, we want to iterate through these objects and calculate their coordinates instead
            for pieces in app.listOfBrokenPieces:
                pieces.calculateArc(app)
                pieces.changeRotation()
        
        #use screen bounds, type of fruit, and kinematics considerations to conclude when object is off screen
        # FIXME: Use stored temp value locations instead of calling this multiple times
        if y0 > 700 and y1 > 700 and flyingObjects.returnTypeObject() == 'fruit' and flyingObjects.returnTimeRun() > 0:
            flyingObjects.incrementOffScreen()
            
            #following conditionals handle lives counter (X X X)
            if flyingObjects.returnOffScreen() == 2:
                app.livesCount += 2
                if app.livesCount % 2 == 0:
                    app.listOfFlyingObjects.remove(flyingObjects)
            
            #game over state, clear screen, upate score
            if app.livesCount == 6:
                app.listOfFlyingObjects = []
                app.allScoresList.append(app.score)
                with open('scores.txt', 'w') as f:
                    for line in app.allScoresList:
                        f.write(str(line))
                        f.write('\n')

        #handles what a fruit looks like after its been sliced
        if flyingObjects.isTouched(app) == True and flyingObjects.returnTypeObject() == 'fruit':
            #be sure to pass in exact attribute values of the flying object so that pieces travel in the same path
            brokenPiece = Pieces(flyingObjects.initialX0,
                                flyingObjects.initialY0,
                                flyingObjects.initialX1,
                                flyingObjects.initialY1,
                                flyingObjects.changeInX, 
                                flyingObjects.changeInY, 
                                flyingObjects.timeRun, 
                                flyingObjects.velocityX, 
                                flyingObjects.velocityY, 
                                flyingObjects.accelerationY, 
                                flyingObjects.color, 
                                flyingObjects.x0,
                                flyingObjects.y0, 
                                flyingObjects.x1, 
                                flyingObjects.y1)

            app.listOfFlyingObjects.remove(flyingObjects)
            app.score += 10 #now we can update score
            app.listOfBrokenPieces.append(brokenPiece)

            #bonus points for combo 
            if app.currentSlice.slicedTimes() > 1:
                app.score += 10

        elif flyingObjects.isTouched(app) == True and flyingObjects.returnTypeObject() == 'bomb':
            #if a bomb is touched, end the game and update the score
            app.listOfFlyingObjects = []
            app.allScoresList.append(app.score)
            with open('readme.txt', 'w') as f:
                for line in app.allScoresList :
                    f.write(str(line))
                    f.write('\n')
            break

def playMode_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))

    canvas.create_image((app.width) - app.allLives.size[0]//2, (0 + app.allLives.size[1]//2),
    image=ImageTk.PhotoImage(app.allLives))

    textSize = app.height // 20
    canvas.create_text(app.width/10, app.height/12 - textSize//2, text= f'POINTS: {app.score}',
                       fill='white', font=f'Helvetica {textSize} bold')

    for flyingObjects in app.listOfFlyingObjects:
        flyingObjects.drawArc(canvas, app)
        if len(app.listOfBrokenPieces) > 0:
            for pieces in app.listOfBrokenPieces:
                pieces.drawArc(canvas,app)

        if app.livesCount == 2:
            canvas.create_image((app.width) - app.allLives.size[0]//2, (0 + app.allLives.size[1]//2), image=ImageTk.PhotoImage(app.twoLives))
        elif app.livesCount == 4:
            canvas.create_image((app.width) - app.allLives.size[0]//2, (0 + app.allLives.size[1]//2), image=ImageTk.PhotoImage(app.oneLive))
        
        if app.currentSlice and not flyingObjects.returnIsSliced() and flyingObjects.returnTypeObject() == 'fruit':
            if flyingObjects.isTouched(app):    
                if app.currentSlice.slicedTimes() > 0:
                    canvas.create_text(app.listMouseCoord[-1][0], app.listMouseCoord[-1][1], text=f'combo: {app.currentSlice.returnCombo() + 1}', fill= 'gold', font='Times 28 bold')
    
    if len(app.listOfFlyingObjects) == 0:
        canvas.create_image(app.width/2, app.height/2,
    image=ImageTk.PhotoImage(app.gameOverIcon))
        canvas.create_image((app.width) - app.allLives.size[0]//2, (0 + app.allLives.size[1]//2), image=ImageTk.PhotoImage(app.noLives))

    for coord in range(len(app.listMouseCoord) -1 ):
        canvas.create_line(app.listMouseCoord[coord][0], app.listMouseCoord[coord][1], 
        app.listMouseCoord[coord + 1][0], app.listMouseCoord[coord + 1][1], fill='white')

#Home mode
def timerFired(app):
    app.background = app.background.resize((app.width, app.height))
    app.animatedSliceToPlayCounter = (1 + app.animatedSliceToPlayCounter) % len(app.animatedSliceToPlay )

def mouseDragged(app, event):
    app.dragged = True 
    app.mouseX = event.x
    app.mouseY = event.y
    app.released = False
    app.listMouseCoord.append((event.x, event.y))

def mouseReleased(app, event):
    app.dragged = False
    app.listMouseCoord = []

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.background))
    canvas.create_image(app.width/2, app.height/4, image=ImageTk.PhotoImage(app.title))
    canvas.create_image((app.instructions.size[0])//2 + 50, (app.instructions.size[1])//2 + 20, 
    image=ImageTk.PhotoImage(app.instructions))

    animatedDragonImage = app.animatedSliceToPlay[app.animatedSliceToPlayCounter]
    canvas.create_image(app.width//2, app.height/1.8, image=animatedDragonImage)
    canvas.create_text(app.width//2, app.height/1.2, text=f' Highscore:{app.highScore}', 
    font='Helvetica 26 bold', fill='white')

    for coord in range(len(app.listMouseCoord) -1 ):
        canvas.create_line(app.listMouseCoord[coord][0], app.listMouseCoord[coord][1], 
        app.listMouseCoord[coord + 1][0], app.listMouseCoord[coord + 1][1], fill='white')

def main():
    runApp(width=1200, height=700, title='CMU NINJA')

if __name__ == '__main__':
    main()
