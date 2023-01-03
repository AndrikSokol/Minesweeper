import pygame
import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo,showerror
import time
from tkinter import *
from tkinter.ttk import *

colors ={
    1: 'blue',
    2: 'green',
    3: 'red',
    4: 'dark blue',
    5:'brown',
    6:'black',
    7:'orange',
    8:'pink',
    }

#переопределение кнопки 
class MyButton(tk.Button):

    def __init__(self,master,x,y,number=0,*args,**kwargs):
        super(MyButton,self).__init__(master,width = 3, font ='arial 15 bold',*args,**kwargs)
        self.x = x
        self.y=y
        self.is_mine = False
        self.number = number
        self.count_bomb =0
        self.is_open =False

    def __repr__(self):
        return f'fMyButton {self.x} {self.y} {self.number} {self.is_mine}'

def play():
        pygame.mixer.music.load("Sound\saper.mp3")
        pygame.mixer.music.play()

def stop():
        pygame.mixer.music.stop()


class MineSweeper:
    
    hood = tk.Tk()
    hood.resizable(width = False,height = False)
    xloc = (hood.winfo_screenwidth()-hood.winfo_reqwidth())/2 - 200
    yloc = (hood.winfo_screenheight()-hood.winfo_reqheight())/2 - 250
    hood.wm_geometry("+%d+%d" %(xloc,yloc))
    hood.maxsize(width ="1280",height = "720")
    hood.iconphoto(True, tk.PhotoImage(file ="Image\Logo.png"))
    hood.title("MineSweeper")
    ROW = 6
    COLUMNS =6 
    MINES =5
    IS_GAME_OVER = False
    IS_GAME_WIN = False
    defuse =0
    right_defuse =0
    count_open =0
    timer =0
    settings = False

    def __init__(self):
        self.photo = PhotoImage(file = r"C:\Users\Andri_000\source\repos\python game\Image\bomb.png")
        self.photo_is_mine = PhotoImage(file = r"C:\Users\Andri_000\source\repos\python game\Image\bomb1.png")
        pygame.mixer.init()
        self.buttons = []
        for i in range(MineSweeper.ROW+2):
            temp =[]
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(MineSweeper.hood,x =i,y=j)
                btn.config(command =lambda button=btn: self.click(button))
                btn.bind("<Button-3>",self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
            self.Time = tk.Label(self.hood,text ='0',bg = "black", fg="white")
            self.Time.grid(row = 0,column = 3,padx = 1,pady =5)

    def update_clock(self):
        if MineSweeper.IS_GAME_WIN or MineSweeper.IS_GAME_OVER:
            self.hood.after(1000,self.update_clock)
            return
        else:
            MineSweeper.timer +=1
            self.Time.configure(text = MineSweeper.timer,bg ='black',fg ='white')
            self.hood.after(1000,self.update_clock)

    def right_click(self,event):
        if MineSweeper.settings:
            return
        if MineSweeper.IS_GAME_OVER:
            return
        if MineSweeper.IS_GAME_WIN:
            return
        cur_btn = event.widget
        if cur_btn['image']:
            cur_btn['image'] =''
            cur_btn['state'] ='normal'
            MineSweeper.defuse -=1
            Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES- MineSweeper.defuse))
            Mine.grid(row =0,column =1,padx = 1, pady = 5)
            if cur_btn.is_mine:
                MineSweeper.right_defuse -=1
        elif MineSweeper.defuse == MineSweeper.MINES:
            return
        elif cur_btn['state'] =='normal':
            sound_click = pygame.mixer.Sound("Sound\is_mine.mp3")
            sound_click.play()
            MineSweeper.defuse +=1
            cur_btn['state'] ='disabled'
            cur_btn.config( image = self.photo_is_mine, compound =TOP)
            Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES- MineSweeper.defuse))
            Mine.grid(row =0,column =1,padx = 1, pady = 5)
            if cur_btn.is_mine:
                MineSweeper.right_defuse +=1
        if MineSweeper.right_defuse == MineSweeper.MINES and MineSweeper.count_open == MineSweeper.COLUMNS*MineSweeper.ROW - MineSweeper.MINES:
            stop()
            sound_game_win =pygame.mixer.Sound("Sound\game_win.mp3")
            sound_game_win.play()
            showinfo('Game win', 'Вы выйграли!')
            Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES))
            Mine.grid(row =0,column =1,padx = 1, pady = 5)
            MineSweeper.IS_GAME_WIN =True


    def click(self, clicked_button:MyButton):
        if MineSweeper.settings:
            return
                        
        if MineSweeper.IS_GAME_WIN:
            return
                        

        if MineSweeper.IS_GAME_OVER:
            return

        if clicked_button.is_mine:
            stop()
            sound_explosive = pygame.mixer.Sound("Sound\explosive.mp3")
            sound_explosive.play()
            clicked_button.config(image = self.photo,compound =TOP,background = "red",disabledforeground = 'black')
            clicked_button.is_open =True
            MineSweeper.IS_GAME_OVER =True
            sound_game_over = pygame.mixer.Sound("Sound\game_over.mp3")
            sound_game_over.play()
            showinfo('Game over', 'Вы проиграли!')
            Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES))
            Mine.grid(row =0,column =1,padx = 1, pady = 5)
            for i in range(1,MineSweeper.ROW+1):
                    for j in range(1,MineSweeper.COLUMNS+1):
                        btn =self.buttons[i][j]
                        if btn.is_mine:
                            btn['image'] = self.photo
                       
                        if btn['image']  and not btn.is_mine:
                            btn['image'] = ''
        else:
            sound_click = pygame.mixer.Sound("Sound\click.mp3")
            sound_click.play()
            color= colors.get(clicked_button.count_bomb,'black')
            if clicked_button.count_bomb:
                clicked_button.config(text =clicked_button.count_bomb,disabledforeground = color)
                clicked_button.is_open =True
                MineSweeper.count_open+=1
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state ='disabled')
        clicked_button.config(relief =tk.SUNKEN)

        if MineSweeper.count_open == MineSweeper.COLUMNS*MineSweeper.ROW - MineSweeper.MINES:
            MineSweeper.IS_GAME_WIN = True
            stop()
            sound_game_win =pygame.mixer.Sound("Sound\game_win.mp3")
            sound_game_win.play()
            showinfo('Game win', 'Вы выйграли!')
            Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES))
            Mine.grid(row =0,column =1,padx = 1, pady = 5)
            for i in range(1,MineSweeper.ROW+1):
                    for j in range(1,MineSweeper.COLUMNS+1):
                        btn =self.buttons[i][j]
                        if btn.is_mine and  not (btn['image']):
                            btn['image'] = self.photo

    def breadth_first_search(self, btn:MyButton):
        queue =[btn]
        while queue:
            cur_btn = queue.pop()
            color= colors.get(cur_btn.count_bomb,'black')
            if cur_btn.count_bomb:
                cur_btn.config(text =cur_btn.count_bomb,disabledforeground = color)
                MineSweeper.count_open+=1
            else:
                cur_btn.config(text ='',disabledforeground = color)
                MineSweeper.count_open+=1
            cur_btn.is_open =True
            cur_btn.config(state ='disabled')
            cur_btn.config(relief =tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x,y = cur_btn.x,cur_btn.y
                for dx in [-1,0,1]:
                    for dy in[-1,0,1]:
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<= next_btn.x <=MineSweeper.ROW and\
                                1<=next_btn.y <=MineSweeper.COLUMNS  and next_btn not in queue and not next_btn["image"]:
                            queue.append(next_btn)
                            

    def reload(self):
        [child.destroy() for child in self.hood.winfo_children()]
        self.__init__()
        self.print_buttons_on_hood()
        self.insert_mines()
        self.count_mines_in_ceils()
        self.print_buttons()
        MineSweeper.IS_GAME_OVER = False
        MineSweeper.defuse =0
        MineSweeper.right_defuse =0
        MineSweeper.IS_GAME_WIN = False
        MineSweeper.count_open =0
        MineSweeper.timer =0
        MineSweeper.settings = False
        play()

    def create_settings_hood(self):
        MineSweeper.settings = True
        hood_settings = tk.Toplevel(self.hood)
        hood_settings.wm_title('Options')
        tk.Label(hood_settings,text ='Количество строк').grid(row =0,column=0)
        row_entry =tk.Entry(hood_settings)
        row_entry.insert(0,MineSweeper.ROW)
        row_entry.grid(row =0,column=1,padx =20,pady=20)
        tk.Label(hood_settings,text ='Количество столбцов').grid(row =1,column=0)
        column_entry =tk.Entry(hood_settings)
        column_entry.insert(0,MineSweeper.COLUMNS)
        column_entry.grid(row =1,column=1,padx =20,pady=20)
        tk.Label(hood_settings,text ='Количество мин').grid(row =2,column=0)
        mines_entry =tk.Entry(hood_settings)
        mines_entry.insert(0,MineSweeper.MINES)
        mines_entry.grid(row =2,column=1,padx =20,pady=20)
        save_btn =tk.Button(hood_settings, text ='Применить',
                  command =lambda: self.change_settings(row_entry,column_entry,mines_entry),)
        save_btn.grid(row =3,column = 0,columnspan =2,pady = 10)

    def change_settings(self,row: tk.Entry, column: tk.Entry,mines : tk.Entry):
        
        try:
            int(row.get()),int(column.get()),int(mines.get())
        except ValueError:
            showerror('Error','Неверные значения')
            return
        r = MineSweeper.ROW
        c =MineSweeper.COLUMNS
        m = MineSweeper.MINES
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        def defauls():
            MineSweeper.ROW = r
            MineSweeper.COLUMNS = c
            MineSweeper.MINES = m
        if  MineSweeper.ROW <=2  or MineSweeper.COLUMNS <=2:
            showerror('Error','количество строк и столбцов меньше 2')
            defauls()
            return
        elif  MineSweeper.MINES >= MineSweeper.COLUMNS * MineSweeper.ROW:
            showerror('Error','бомб больше чем ячеек')
            defauls()
            return
        elif MineSweeper.ROW >20  or MineSweeper.COLUMNS >20:
            showerror('Error','Столбцы и строки должны быть меньше 20')
            defauls()
            return
        else:
            self.reload()



    def print_buttons_on_hood(self):
        menubar = tk.Menu(self.hood)
        self.hood.config(menu = menubar)
        settings_menu = tk.Menu(menubar,tearoff =0)
        settings_menu.add_command(label ='Restart',command=self.reload)
        settings_menu.add_command(label ='Settings', command = self.create_settings_hood)
        settings_menu.add_command(label ='Exit',command =self.hood.destroy)
        menubar.add_cascade(label ='Game', menu=settings_menu)
        music_menu = tk.Menu(menubar,tearoff =0)
        music_menu.add_command(label ='On',command=play)
        music_menu.add_command(label ='off', command = stop)
        menubar.add_cascade(label ='Music',menu = music_menu)
        Mine = tk.Label(self.hood,text = 'Mines ' +str(MineSweeper.MINES))
        Mine.grid(row =0,column =1,padx = 1, pady = 5)
        Timer =tk.Label(self.hood,text = 'Time')
        Timer.grid(row = 0,column = 2,padx =1,pady = 5)
        for i in range(1,MineSweeper.ROW+1):
            for j in range(1,MineSweeper.COLUMNS+1):
                btn =self.buttons[i][j]
                btn.grid(row = i,column =j,stick = 'NWES', pady =1,padx =1)

        for i in range(1,MineSweeper.ROW+1):
            tk.Grid.rowconfigure(self.hood,i,weight = 1)

        for i in range(1,MineSweeper.COLUMNS+1):
            tk.Grid.columnconfigure(self.hood,i,weight = 1)
                
                
                
    #запуск игры
    def start(self):
        self.reload()
        self.update_clock()
        play()
        MineSweeper.hood.mainloop()


    def print_buttons(self):
        for i in range(1,MineSweeper.ROW+1):
            for j in range(1,MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B',end ='')
                else:
                    print(btn.count_bomb,end='')
            print()


    def insert_mines(self):
        count =1
        index_mines = self.get_mines_places()
        print(index_mines)
        for i in range(1,MineSweeper.ROW+1):
            for j in range(1,MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in index_mines:
                    btn.is_mine =True
                count +=1
              

    def count_mines_in_ceils(self):
        for i in range(1,MineSweeper.ROW+1):
            for j in range(1,MineSweeper.COLUMNS+1):
                btn = self.buttons[i][j]
                count_bomb =0
                if not btn.is_mine:
                    for row_dx in[-1,0,1]:
                        for col_dx in[-1,0,1]:
                            neighbour = self.buttons[i+row_dx][j+col_dx]
                            if neighbour.is_mine:
                                count_bomb +=1
                btn.count_bomb = count_bomb
    @staticmethod
    def get_mines_places():
        indexes = list(range(1,MineSweeper.COLUMNS* MineSweeper.ROW +1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()

game.start()