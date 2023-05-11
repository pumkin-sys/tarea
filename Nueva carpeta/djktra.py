from tkinter import messagebox, Tk
import pygame
import sys

windows_width=800;
windows_heigth=444;

window=pygame.display.set_mode((windows_width,windows_heigth));

grid=[]
queque=[]
path=[]
columns=27
rows=20
box_width=windows_width//columns
box_heigth=windows_heigth//rows


class Box:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.start=False
        self.visited=False
        self.queque=False
        self.target=False
        self.wall=False
        self.neighrborns=[]
        self.prior=None
    
        
    def draw(self,win,color):
        x = self.x * box_width
        y = self.y * box_heigth
        pygame.draw.rect(win,color,(x,y,box_width-1,box_heigth-1))
      
    def draw_img(self, window, image_file):
        image = pygame.image.load(image_file)
        x = self.x * box_width
        y = self.y * box_heigth
        window.blit(image, (x, y))
   
    def set_neighrborns(self):
        if self.x>0:
            self.neighrborns.append(grid[self.x-1][self.y])
        if self.x<columns-1:
            self.neighrborns.append(grid[self.x+1][self.y])
        if self.y>0:
            self.neighrborns.append(grid[self.x][self.y-1])
        if self.y<rows-1:
            self.neighrborns.append(grid[self.x][self.y+1])
        
for i in range(columns):
    array=[]
    for j in range(rows):
        array.append(Box(i,j))
    grid.append(array)
            
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighrborns()
                
def main():

    background=pygame.image.load('pasto.png')
    begin_search=False
    start_box_set=False
    target_box_set=False
    searching=True
    window.blit(background,(0,0)) 
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and not start_box_set:
                x,y=pygame.mouse.get_pos()
                i=x//box_width
                j=y//box_heigth
                start_box=grid[i][j]
                start_box.start=True
                start_box_set=True
                start_box.visited=True
                queque.append(start_box)
            elif event.type==pygame.MOUSEMOTION:
                x=pygame.mouse.get_pos()[0]
                y=pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    i=x//box_width
                    j=y//box_heigth
                    grid[i][j].wall=True
                if event.buttons[2] and not target_box_set:
                    i=x//box_width
                    j=y//box_heigth
                    target_box=grid[i][j]
                    target_box.target=True
                    target_box_set=True
            if event.type==pygame.KEYDOWN and target_box_set:
                begin_search=True
                                       
        if begin_search:
            if len(queque)>0 and searching:
                current_box=queque.pop(0)
                current_box.visited=True
                if current_box == target_box:
                    searching=False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box=current_box.prior
                else:
                    for neighrborn in current_box.neighrborns:
                        if not neighrborn.queque and not neighrborn.wall:
                            neighrborn.queque=True
                            neighrborn.prior=current_box
                            queque.append(neighrborn)
            else:
                if searching:
                    messagebox.showinfo("Mensaje","No hay solucion")
                    searching=False                                
         
        for i in range(columns):
            for j in range(rows):
                box=grid[i][j]
                if box.queque:
                    box.draw(window,(0, 100, 0))
                if box.visited:
                    box.draw(window,(0,200,0))
                if box in path:
                    box.draw(window,(139, 69, 19))                  
                if box.start:
                    box.draw_img(window,('oso.png'))
                if box.wall:
                    box.draw_img(window,('arbol.png'))
                if box.target:
                    box.draw_img(window,('casa.png'))
                    
        pygame.display.flip()
        
main()   
            