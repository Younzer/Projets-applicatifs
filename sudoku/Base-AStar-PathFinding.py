import sys, math, random
import pygame
import pygame.draw
import numpy

__screenSize__ = (1600,1280)
__cellSize__ = 20
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))

__wallcolor = (10,10,10)

def getColorCell(n):
    if n == 0:
        return (255,255,255)
    tmp = (1-n)*240 + 10
    return (tmp, tmp, tmp)

class Grid:
    _grid= None
    def __init__(self):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self._grid = numpy.zeros(__gridDim__)

    def addWallFromMouse(self, coord, w):
        x = int(coord[0] / __cellSize__)
        y = int(coord[1] / __cellSize__)
        self._grid[x,y] = w

    def drawMe(self):
        pass

class Scene:
    _mouseCoords = (0,0)
    _grid = None
    _font = None

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self._grid = Grid()

    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((128,128,128))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen, 
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))


    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        pass

    def eventClic(self,coord,b): # ICI METTRE UN A* EN TEMPS REEL
        pass
    def recordMouseMove(self, coord):
        pass

def main():
    buildingGrid = False # True if the user can add / remove walls / weights
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    buildingTrack = True
    wallWeight = 1
    while done == False:
        clock.tick(20)
        scene.update()
        scene.drawMe()
        if buildingTrack:
            additionalMessage = ": BUILDING (" + str(int(wallWeight*100)) + "%)"
        scene.drawText("Super A*" + additionalMessage, (10,10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                print("Exiting")
                done=True
            if event.type == pygame.KEYDOWN: 
                if event.unicode in [str(i) for i in range (10)]:
                    wallWeight = min(1, .1 + 1 - int(event.unicode)/10) 
                    break
                if event.key == pygame.K_q or event.key==pygame.K_ESCAPE: # q
                    print("Exiting")
                    done = True
                    break
                if event.key == pygame.K_s: # s
                    numpy.save("matrix.npy",scene._grid._grid)
                    print("matrix.npy saved")
                    break
                if event.key == pygame.K_l: # l
                    print("matrix.npy loaded")
                    scene._grid._grid = numpy.load("matrix.npy")
                    break
                if event.key == pygame.K_n:
                    buildingTrack = False
                    break
                if event.key == pygame.K_b :
                    buildingTrack = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buildingTrack:
                    scene._grid.addWallFromMouse(event.dict['pos'], wallWeight)
                else:
                    scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: main()

