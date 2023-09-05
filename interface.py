from tkinter import *
import random 
import pygame
from PIL import ImageTk, Image
from tkinter import Tk
import time

pygame.mixer.init()
pygame.init()
    
pygame.mixer.music.load("music.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=0)
# pygame.mixer.music.stop()


class Jeu(Tk):
    def __init__(self):     
        super().__init__()
        self.columnconfigure(0, weight = 1) 
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        
        self.son = pygame.mixer.Sound("clic.ogg")
    
        self.title("Colt Express")
        self.resizable(FALSE, FALSE)

        self.plateau = Orient_Express(self, width=500, height=750)
        self.plateau.grid(row=0, column = 1,sticky='nse')
        self.plateau.e1.focus_set()
        self.plateau.e1.bind('<Return>',lambda event : self.plateau.valider())

        self.frame_btn = Frame(self,width=500, height=750,bg="#06022A")
        self.frame_btn.grid(row = 0, column = 2, sticky= "nwes")
        for i in range(8):
            self.frame_btn.rowconfigure(i,weight=2) 
                             
        self.imgFermer = Image.open("fermer.png").resize((160, 80))
        self.imgFermer = ImageTk.PhotoImage(self.imgFermer)
        self.btn_fermer = Button(self.frame_btn,image=self.imgFermer, command=self.fermer, highlightthickness=0)
        self.btn_fermer.grid(row=0,columnspan=3)
        self.bind("<p>", lambda event: self.fermer())

        self.imgAction = Image.open("action.png").resize((160, 80))
        self.imgAction = ImageTk.PhotoImage(self.imgAction)
        self.btn_action = Button(self.frame_btn,image= self.imgAction, command=self.action, highlightthickness=0)
        self.btn_action.grid(row=1,columnspan=3)
        self.bind("<Return>", lambda event: self.action())

        self.imgHaut = Image.open("flechehaut.png").resize((60, 60))
        self.imgHaut = ImageTk.PhotoImage(self.imgHaut)
        self.btn_haut = Button(self.frame_btn,image=self.imgHaut, command= self.a_haut, highlightthickness=0)
        self.btn_haut.grid(row=2,column=1)
        self.bind("<Up>", lambda event: self.a_haut())

        self.imgDroite = Image.open("flechedroite.png").resize((60, 60))
        self.imgDroite = ImageTk.PhotoImage(self.imgDroite)
        self.btn_droite = Button(self.frame_btn,image=self.imgDroite, command= self.a_droit, highlightthickness=0)
        self.btn_droite.grid(row=3,column=2)
        self.bind("<Right>", lambda event: self.a_droit())
        
        self.imgGauche = Image.open("flechegauche.png").resize((60, 60))
        self.imgGauche = ImageTk.PhotoImage(self.imgGauche)
        self.btn_gauche = Button(self.frame_btn,image=self.imgGauche, command= self.a_gauche, highlightthickness=0)
        self.btn_gauche.grid(row=3,column=0)
        self.bind("<Left>", lambda event: self.a_gauche())

        self.imgBas = Image.open("flechebas.png").resize((60, 60))
        self.imgBas = ImageTk.PhotoImage(self.imgBas)
        self.btn_bas = Button(self.frame_btn,image=self.imgBas, command= self.a_bas, highlightthickness=0)
        self.btn_bas.grid(row=4,column=1)
        self.bind("<Down>", lambda event: self.a_bas())

        self.imgBraquage = Image.open("braquage.png").resize((80, 80))
        self.imgBraquage = ImageTk.PhotoImage(self.imgBraquage)
        self.btn_braquage = Button(self.frame_btn,image=self.imgBraquage, command=self.a_braquage, highlightthickness=0)
        self.btn_braquage.grid(row = 5,column=0)
        self.bind("<b>", lambda event: self.a_braquage())

        self.imgTir = Image.open("tir.png").resize((80,80))
        self.imgTir = ImageTk.PhotoImage(self.imgTir)
        self.btn_tir = Button(self.frame_btn,image=self.imgTir, command=self.a_tir, highlightthickness=0)
        self.btn_tir.grid(row = 5,column=2)
        self.bind("<t>", lambda event: self.a_tir())

        scrollbar = Scrollbar(self)
        self.liste = Listbox(self.frame_btn,width=40, yscrollcommand = scrollbar.set, bg= '#06022A', fg="white", font="Arial 12")
        self.liste.grid(row=9,columnspan=3, sticky= "news")
        scrollbar.config(command = self.liste.yview )
        
        self.NB_ACTION = 3 # nb_action total pour le joueur = 3
        self.NB_ACTION_ACTUELLE = 0
        
        self.liste_action_1 = []
        self.liste_action_2 = []
        self.liste_action_3 = []
        
        self.NB_TOURS = 10
        self.NB_TOURS_ACTUELLE = 1

        self.NB_JOUEUR = 0
        self.NB_JOUEUR_ACTUELLE = 0
        
        self.ACTION_POSSIBLE = 0
        self.ACTION_AUTORISATION = FALSE
        
        self.ACTION_ACTUELLE = 0
        self.PARAMETRABLE = TRUE
        self.ACTION_EXECUTER = 0

    def get_nb_joueur(self):
        self.NB_JOUEUR = self.plateau.max_dalton

    def validation(self):
        self.plateau.focus_set()
        self.plateau.valider()

    def fermer(self):
        self.son.play()
        newWindow = Toplevel(self)
        lbl=Label(newWindow,text="Fermer ?")
        lbl.pack(side=TOP,pady=40)
        btnQuitNew=Button(newWindow,text="No",command=newWindow.destroy)
        btnQuitNew.pack(side=LEFT)
        btnQuitAll=Button(newWindow,text="Yes",command=self.destroy)
        btnQuitAll.pack(side=TOP)

    def remplir_action(self,action):
        self.get_nb_joueur()
        # Partis de gestion des actions
        self.son.play()
        
        if (self.NB_ACTION_ACTUELLE == 0):
            self.liste_action_1.append(action)
        if (self.NB_ACTION_ACTUELLE == 1):
            self.liste_action_2.append(action)
        if (self.NB_ACTION_ACTUELLE == 2):
            self.liste_action_3.append(action)

        # Partis interface automatique pour le joueur 
        self.NB_ACTION_ACTUELLE += 1
        
        if self.NB_ACTION_ACTUELLE >= self.NB_ACTION:
            self.NB_ACTION_ACTUELLE = 0
            self.liste.insert(END, "Le joueur : " + (str) (self.NB_JOUEUR_ACTUELLE + 1) + " a finis de préparer son tour")
            
            self.NB_JOUEUR_ACTUELLE += 1 #Le joueur suivant prend la main
            if (self.NB_JOUEUR_ACTUELLE <= self.NB_JOUEUR-1):
                self.liste.insert(END, "Le joueur : " + (str) (self.NB_JOUEUR_ACTUELLE + 1) + " peux commencer à préparer son tour")
        
        if self.NB_JOUEUR_ACTUELLE > self.NB_JOUEUR-1:
            # le joueur 0 reprend la main
            self.NB_JOUEUR_ACTUELLE = 0
            self.liste.insert(END, "Le tour : " + (str) (self.NB_TOURS_ACTUELLE) + " est finis")

            self.NB_TOURS_ACTUELLE += 1
            self.ACTION_AUTORISATION = TRUE
            self.liste.insert(END, "Le tour : " + (str) (self.NB_TOURS_ACTUELLE) + " peux commencer à être préparer")
             
            if self.NB_TOURS_ACTUELLE == self.NB_TOURS-1:
                self.liste.insert(END, "Le tour : " + (str) (self.NB_TOURS_ACTUELLE) + " est l'avant dernier tour")            
        
            self.liste.insert(END, "Le joueur : " + (str) (self.NB_JOUEUR_ACTUELLE+1) + " peux commencer à préparer son tour")
        
        # fin de partie
        if self.NB_TOURS_ACTUELLE >= self.NB_TOURS:
            self.liste.insert(END, "Le tour : " + (str) (self.NB_TOURS_ACTUELLE) + " est finis")
            self.liste.insert(END, "La partie : " + (str) (self.NB_TOURS_ACTUELLE) + " est finis")
        self.liste.see(self.liste.size())
        
        
    def listeAction(self,liste,i):
        print(liste)
        print(liste[i + self.ACTION_EXECUTER])
        if liste[i + self.ACTION_EXECUTER] == 'HAUT':
            self.haut(i)
        if liste[i + self.ACTION_EXECUTER] == 'GAUCHE':
            self.gauche(i)
        if liste[i + self.ACTION_EXECUTER] == 'DROITE':
            self.droit(i)
        if liste[i + self.ACTION_EXECUTER] == 'BAS':
            self.bas(i)
        if liste[i + self.ACTION_EXECUTER] == 'BRAQUAGE':
            self.braquage(i)
        if liste[i + self.ACTION_EXECUTER] == 'TIR':
            self.tir(i)
        if liste[i + self.ACTION_EXECUTER] == 'LACHER':
            self.lacher(i)
        if liste[i + self.ACTION_EXECUTER] == 'FUITE':
            self.fuite(i)

    def action(self):
        if self.ACTION_AUTORISATION == FALSE:
            return
        else:
            self.ACTION_ACTUELLE += 1
            if (self.ACTION_ACTUELLE == 1):
                print("action 1")
                for i in range(self.NB_JOUEUR):
                    self.listeAction(self.liste_action_1, i)
                self.plateau.liste_l[0].deplacement()
                self.tir_marechal()
                    # time.sleep(3)
            if (self.ACTION_ACTUELLE == 2):
                print("action 2")            
                for i in range(self.NB_JOUEUR):
                    self.listeAction(self.liste_action_2, i)
                self.plateau.liste_l[0].deplacement()
                self.tir_marechal()
                    # time.sleep(3)
            if (self.ACTION_ACTUELLE == 3):
                print("action 3")
                for i in range(self.NB_JOUEUR):
                    self.listeAction(self.liste_action_3, i)
                self.plateau.liste_l[0].deplacement()
                self.tir_marechal()
                    # time.sleep(3)
                print(self.ACTION_EXECUTER)
                self.ACTION_EXECUTER += self.NB_JOUEUR
                print(self.ACTION_EXECUTER)
                self.ACTION_POSSIBLE -= 1
                self.ACTION_ACTUELLE = 0
                if (self.ACTION_POSSIBLE <= 0):
                    self.ACTION_AUTORISATION = FALSE

    
    def haut(self, dalton):
        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " grimpe sur le toit ")
        if (self.plateau.liste_d[dalton].row == 1): 
            self.plateau.liste_d[dalton].move_y(-1)
            
    def gauche(self, dalton):
        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " va sur le wagon de gauche ")
        if (self.plateau.liste_d[dalton].col - (2+self.plateau.max_dalton) >= 0): 
            self.plateau.liste_d[dalton].move_x(-(2+self.plateau.max_dalton))
            
    def droit(self, dalton):
        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " va sur le wagon de droite ")
        if (self.plateau.liste_d[dalton].col <= self.plateau.liste_w[-1].span + 1): 
            self.plateau.liste_d[dalton].move_x((self.plateau.max_dalton+2))
    
    def bas(self, dalton):
        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " descend dans le wagon ")
        if (self.plateau.liste_d[dalton].row == 0): 
            self.plateau.liste_d[dalton].move_y(1)

    def braquage(self, dalton):
        if (self.plateau.liste_d[dalton].row == 0):
            print("tu est sur le toit")
        else:
            for i in self.plateau.liste_w: #recupere le wagon la oû il y a le joueur 
                if (i.col <= self.plateau.liste_d[dalton].col and self.plateau.liste_d[dalton].col <= (i.col+i.span)): 
                    wagon = i
            for j in self.plateau.liste_b: #recupere le richeman la oû il y a le wagon 
                if (wagon.col <= j.col and j.col <= (wagon.col+wagon.span)):
                    f = random.randint(0,len(j.poche_riche)-1)
                    self.plateau.liste_d[dalton].poche.append(j.poche_riche[f])
                    print(j.poche_riche)
                    print(j.poche_riche[f])
                    print(j.poche_riche)
                    print(self.plateau.liste_d[dalton].poche)
                    if j.poche_riche[f] <= 500:
                        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " à récupérer un bijou " + (str) (j.poche_riche[f]))
                    if j.poche_riche[f] > 500 and j.poche_riche[f] <= 800 :
                        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " à récupérer un bourse " + (str) (j.poche_riche[f]))
                    if j.poche_riche[f] >= 1000 :
                        self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " à récupérer un magot " + (str) (j.poche_riche[f]))
                    j.poche_riche.remove(j.poche_riche[f])
                    self.liste.see(self.liste.size())        
            
    def tir(self, dalton):
        if (self.plateau.liste_d[dalton].row == 0):
            for i in self.plateau.liste_w: #recupere le wagon la oû il y a le joueur 
                if (i.col <= self.plateau.liste_d[dalton].col and self.plateau.liste_d[dalton].col <= (i.col+i.span)): 
                    wagon = i
            for j in self.plateau.liste_d: #recupere le deuxieme joueur la oû il y a le wagon 
                if (wagon.col <= j.col and j.col <= (wagon.col+wagon.span)):
                    if self.plateau.liste_d[dalton].col == j.col:
                        pass
                    else:
                        if len(j.poche) > 0:
                            f = random.randint(0,len(j.poche)-1)
                            self.plateau.liste_d[dalton].poche.append(j.poche[f])
                            self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " a tiré et a récupéré " + (str) (j.poche[f]) + " de Dalton " + (str) (self.plateau.liste_d.index(j)))
                            j.poche.remove(j.poche[f])
                            self.liste.see(self.liste.size())
                            return 
                        else: 
                            self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " a tiré sur Dalton " + (str) (self.plateau.liste_d.index(j)))
                            self.liste.see(self.liste.size()) 
                            return 
        else:
            for i in self.plateau.liste_w: #recupere le wagon la oû il y a le joueur 
                if (i.col <= self.plateau.liste_d[dalton].col and self.plateau.liste_d[dalton].col <= (i.col+i.span)): 
                    wagon = i
            for j in self.plateau.liste_d: #recupere le deuxieme joueur la oû il y a le wagon 
                if (wagon.col <= j.col and j.col <= (wagon.col+wagon.span)):
                    if self.plateau.liste_d[dalton].col == j.col:# Si nous même
                        pass
                    else:
                        if len(j.poche) > 0:
                            f = random.randint(0,len(j.poche)-1)
                            self.plateau.liste_d[dalton].poche.append(j.poche[f])
                            self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " a tiré et a récupéré " + (str) (j.poche[f]) + " de Dalton " + (str) (self.plateau.liste_d.index(j)))
                            j.poche.remove(j.poche[f])
                            self.liste.see(self.liste.size())
                            return 
                        else: 
                            self.liste.insert(END, "Le Dalton " + (str) (dalton + 1) + " a tiré sur Dalton " + (str) (self.plateau.liste_d.index(j)))
                            self.liste.see(self.liste.size()) 
                            return 
                           
    def tir_marechal(self):
        list_temp = []
        for i in self.plateau.liste_w: #recupere le wagon la oû il y a le marechal
            if (i.col <= self.plateau.liste_l[0].col and self.plateau.liste_l[0].col <= (i.col+i.span)): 
                wagon = i
        for j in self.plateau.liste_d: #recupere le joueur la oû il y a le wagon 
            if (wagon.col <= j.col and j.col <= (wagon.col+wagon.span)):
                list_temp.append(j)
        print(list_temp)
        for r in self.plateau.liste_b: #recupere le richeman la oû il y a le wagon 
            if (wagon.col <= r.col and r.col <= (wagon.col+wagon.span)):
                riche = r 
        if (len(list_temp) > 0 ):
            x = random.randint(0,len(list_temp)-1) # attrape un joueur aléatoire possible
            j = list_temp[x] # récupere le joueur 
            if len(j.poche) > 0: #si poche non vide 
                f = random.randint(0,len(j.poche)-1) # choisi un élément aléatoire dans la poche du joueur 
                r.poche_riche.append(j.poche[f]) # rend l'argent 
                self.plateau.liste_d[self.plateau.liste_d.index(j)].move_y(-1)
                self.liste.insert(END, "Luck Lucky à tiré et à rendu " + (str) (j.poche[f]) + " de Dalton ")
                self.liste.insert(END, (str) (self.plateau.liste_d.index(j)+1) + ", il a fuit !!!")
                j.poche.remove(j.poche[f]) # retire l'argent du joueur 
                self.liste.see(self.liste.size())
                list_temp = []
                return 
            else: 
                self.plateau.liste_d[self.plateau.liste_d.index(j)].move_y(-1)
                self.liste.insert(END, "Luck Lucky à tiré plus vite que ton ombre sur ")
                self.liste.insert(END, "Dalton " + (str) (self.plateau.liste_d.index(j)+1) + ", il a fuit !!!")
                self.liste.see(self.liste.size()) 
                list_temp = []
                return 

    def a_haut(self):
        self.son.play()
        # self.liste.insert(END, "Le Dalton " + (str) (0) + " monte ")
        self.remplir_action("HAUT")
    def a_gauche(self):
        self.son.play()
        # self.liste.insert(END, "Le Dalton " + (str) (0) + " va à gauche ")
        self.remplir_action("GAUCHE")
    def a_droit(self):
        self.son.play()
        # self.liste.insert(END, "Le Dalton " + (str) (0) + " va à droite ")
        self.remplir_action("DROITE")
    def a_bas(self):
        self.son.play()
        # self.liste.insert(END, "Le Dalton " + (str) (0) + " descend ")
        self.remplir_action("BAS")
    def a_braquage(self):
        self.son.play()
        self.remplir_action("BRAQUAGE")
    def a_tir(self):
        self.son.play()
        self.remplir_action("TIR")
 
class Orient_Express(Canvas):
    def __init__(self,fenetre : Tk, width, height):
        super().__init__(fenetre, width= width, height =height)

        #self.img = Image.open("Background.png")
        #self.img.resize((width, height))
        #self.photo = ImageTk.PhotoImage(self.img)
        #self.create_image(width/2,height/2, image=self.photo)
        #self.place(x=0,y=0)
        self.image = PhotoImage(file="Background.png")
        self.label2 = Label(self, image=self.image)
        self.label2.place(x=0, y=0)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.liste_w = [] 
        self.liste_d = []
        self.liste_l = []
        self.liste_b = []
        
        # self.img = Image.open("Background.png")
        # self.img = self.img.resize((width,height))
        # self.photo = ImageTk.PhotoImage(self.img)
        # self.create_image(width/2,height/2, image=self.photo)
        # self.grid(row= 0,column=0,rowspan=2, columnspan=100)
        
        self.label = Label(self, text= "Veuillez saisir un nombre de joueurs")
        self.e1 = Entry(self, validatecommand=self.valider)
        self.label.place(x = 0, y = 0)
        self.e1.place(x= 250 , y = 0)

        self.btn_valider = Button(self,text = "Valider", command=self.valider, width= 7, bg='orange')
        self.btn_valider.place(x= 425 , y = -1)
        self.max_dalton = 0
        

    def valider(self):
        self.label.destroy()       
        self.btn_valider.destroy()
        self.max_dalton = (int) (self.e1.get())
        self.e1.destroy()
        return self.create_wagons(self.max_dalton)
    
    def create_wagons(self,n):
        c=0
        c2 = 2+self.max_dalton
        for i in range(n):
            self.liste_w.append(Wagon(self,"Wagon.png",300,100,1,c,c2))
            self.liste_b.append(Butin(self,"Riche.png",60,60,1,c+c2-2))
            c += c2
            # c2 = 2+self.max_dalton
        self.liste_w.append(Locomotive(self,"Tchoutchou.png",300,100,1,c,c+c2+1))
        self.liste_b.append(Butin(self,"Riche.png",60,60,1,c+c2-2))
        for h in range(n):
            self.liste_d.append(Dalton(self,"Bandit" + (str) (h+1) + ".png",75,75,1,h))
        self.liste_l.append(Luck_lucky(self,"Sherif.png", 70,70,1,c+self.max_dalton+2))
        for i in self.liste_b:
            i.randomButin() 

    @classmethod
    def return_img(cls,file,x,y):
        image = Image.open(file)
        image = image.resize((x,y))
        return ImageTk.PhotoImage(image)
    
class Butin(Orient_Express):
    def __init__(self,master, file, width, height,row,col):
        super().__init__(master, width= width, height= height)  
        self.poche_riche = []   
        self.valeur = 0
        self.nom = ""
        self.row = row 
        self.col = col
        self.img = Image.open(file)
        self.img = self.img.resize((width,height))
        self.photo = ImageTk.PhotoImage(self.img)
        self.create_image(width/2,height/2, image=self.photo)
        self.grid(row=row,column=col)
        self.label.destroy()
        self.e1.destroy()
        self.label2.destroy()
        
    def randomButin(self):
        n = random.randint(1,4)
        for i in range(n):
            c = random.randint(0, 1) 
            if (c == 0):
                # create bijou
                self.bijou()
            elif (c == 1):
                # create butin
                self.bourse()
            
    def magot(self):
        self.valeur = 2000
        self.poche_riche.append(self.valeur)
        
    def bijou(self):
        self.valeur = random.randint(100,500)
        self.poche_riche.append(self.valeur)
        
    def bourse(self):
        self.valeur = random.randint(501,800)
        self.poche_riche.append(self.valeur)
        

class Locomotive(Orient_Express):
        def __init__(self,master, file, width,height,row,col,span):
            super().__init__(master, width, height)
            self.img = Image.open(file)
            self.col = col
            self.row =row
            self.span = span
            self.img = self.img.resize((width,height))
            self.photo = ImageTk.PhotoImage(self.img)
            self.create_image(width/2,height/2, image=self.photo)
            self.grid(row=row,column=col,columnspan=span)
            self.label.destroy()
            self.e1.destroy()
            self.label2.destroy()

class Wagon(Orient_Express):
        def __init__(self,master, file, width,height,row,col,span):
            super().__init__(master, width, height)
            self.col = col 
            self.row = row 
            self.span = span
            self.img = Image.open(file)
            self.img = self.img.resize((width,height))
            self.photo = ImageTk.PhotoImage(self.img)
            self.create_image(width/2,height/2, image=self.photo)
            self.grid(row=row,column=col, columnspan=span)
            self.label.destroy()
            self.e1.destroy()
            self.label2.destroy()

class Luck_lucky(Orient_Express):
    def __init__(self, master, file, width, height,row, col):
        super().__init__(master, width = width, height = height)
        self.row = row 
        self.col = col
        self.fin = col + (2+self.max_dalton)
        self.img = Image.open(file)
        self.img = self.img.resize((width,height))
        self.photo = ImageTk.PhotoImage(self.img)
        self.create_image(width/2,height/2, image=self.photo)
        self.grid(row=row,column=col)
        self.label.destroy()
        self.e1.destroy()
        self.label2.destroy()
    
    def deplacement(self):
        x = random.randint(0, 1)
        if x == 0:
            if self.col - (2+self.max_dalton) > 0:
                self.move_x(-(2+self.max_dalton))
            else:
                self.deplacement()
        if x == 1:
            if self.col + (2+self.max_dalton) < self.fin:
                self.move_x(2+self.max_dalton)
            else:
                self.deplacement()
    
    def move_x(self, value):
        print("col = " + (str) (self.col))
        self.col = self.col + value
        # self.grid_forget()
        return self.grid(row= self.row,column=self.col)
        # print("col = " + (str) (self.col))

class Dalton(Orient_Express):
    def __init__(self,master,file,width,height,row,col):
        super().__init__(master,width = width, height = height)
        self.row = row 
        self.col = col 
        self.coldepart = col 
        self.img = Image.open(file) 
        self.img = self.img.resize((width,height))
        self.photo = ImageTk.PhotoImage(self.img)
        self.configure(borderwidth=0, highlightthickness=0)
        self.create_image(width/2,height/2, image=self.photo)
        self.grid(row=self.row,column=self.col)
        self.label.destroy()
        self.e1.destroy()
        self.label2.destroy()
        
        self.poche = []
        
    def move_y(self, value):
        self.row += value
        self.grid_forget()
        return self.grid(row= self.row,column=self.col)
        # print("row = " + (str) (self.row))

    def move_x(self, value):
        print("col = " + (str) (self.col))
        self.col = self.col + value
        # self.grid_forget()
        return self.grid(row= self.row,column=self.col)
        # print("col = " + (str) (self.col))


if __name__ == '__main__':
    root = Jeu()
    root.mainloop()