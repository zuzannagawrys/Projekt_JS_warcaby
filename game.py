from tkinter import *
from tkinter import ttk
from tkinter import messagebox


ROWS, COLS = 8, 8
class Pionek:
    """ Klasa Pionek jest klasa bazowa dla klas Pionki i Damka
    przechowuje ona pozycje danej instancji (row, col), 
    gracza (player) do ktorego nalezy dany pionek
    oraz flage(capture_flag) ktora informuje czy mozliwe jest bicie tym pionem.
    Metody tej klasy pozwalaja na ocenienie mozliwych bic danego pionka oraz na zmienienie jego pozycji """
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        self.capture_flag=False
    
    def move(self, row, col): 
        """ zmiana pozycji pionka """
        self.row = row
        self.col = col
        
    def __repr__(self):
        return "Pionek ["+str(self.row)+","+str(self.col)+"] - "+self.player

    def left_captureC(self,pieceBoard): 
        """ ocena mozliwosci bicia w lewo dla gracza C """
        movesC={}
        if(self.col-2>=0 and self.row+2<ROWS):
            if(pieceBoard[self.row+1][self.col-1]!=0 and pieceBoard[self.row+1][self.col-1].player!=self.player and pieceBoard[self.row+2][self.col-2]==0):
                movesC[(self.row+2,self.col-2)]=[pieceBoard[self.row+1][self.col-1]]
        return movesC
    
    def right_captureC(self,pieceBoard): 
        """ ocena mozliwosci bicia w prawo dla gracza C """
        movesC={}
        if(self.col+2<COLS and self.row+2<ROWS):
            if(pieceBoard[self.row+1][self.col+1]!=0 and pieceBoard[self.row+1][self.col+1].player!=self.player and pieceBoard[self.row+2][self.col+2]==0):
                movesC[(self.row+2,self.col+2)]=[pieceBoard[self.row+1][self.col+1]]
        return movesC

    def left_captureB(self,pieceBoard): 
        """ ocena mozliwosci bicia w lewo dla gracza B """
        movesB={}
        if(self.col-2>=0 and self.row-2>=0):
            if(pieceBoard[self.row-1][self.col-1]!=0 and pieceBoard[self.row-1][self.col-1].player!=self.player and pieceBoard[self.row-2][self.col-2]==0):
                movesB[(self.row-2,self.col-2)]=[pieceBoard[self.row-1][self.col-1]]
        return movesB
    
    def right_captureB(self,pieceBoard): 
        """ ocena mozliwosci bicia w prawo dla gracza B """
        movesB={}
        if(self.col+2<COLS and self.row-2>=0):
            if(pieceBoard[self.row-1][self.col+1]!=0 and pieceBoard[self.row-1][self.col+1].player!=self.player and pieceBoard[self.row-2][self.col+2]==0):
                movesB[(self.row-2,self.col+2)]=[pieceBoard[self.row-1][self.col+1]]
        return movesB

class Pionki(Pionek):
    """ Klasa Pionki dziedziczy po klasie Pionek
    metody tej klasy pozwalaja na ocenienie mozliwych ruchow danego pionka biorac pod uwage ze jest pionkiem, a nie damka"""
    def __repr__(self):
        return "Pionek ["+str(self.row)+","+str(self.col)+"] - "+self.player

    def get_valid_normal_movesC(self,pieceBoard):   
        """ ocena mozliwosci zwyklych ruchow (bez bicia) do przodu dla gracza C """
        movesC={}
        if(self.col+1<COLS):
            if(pieceBoard[self.row+1][self.col+1]==0):
                movesC[(self.row+1,self.col+1)]=[]
        if(self.col-1>=0):
            if(pieceBoard[self.row+1][self.col-1]==0):
                movesC[(self.row+1,self.col-1)]=[]
        return movesC    
    def get_valid_normal_movesB(self,pieceBoard):   
        """ ocena mozliwosci zwyklych ruchow (bez bicia) do przodu dla gracza B """
        movesB={}
        if(self.col+1<COLS):
            if(pieceBoard[self.row-1][self.col+1]==0):
                movesB[(self.row-1,self.col+1)]=[]
        if(self.col-1>=0):
            if(pieceBoard[self.row-1][self.col-1]==0):
                movesB[(self.row-1,self.col-1)]=[]
        return movesB

    def get_valid_capturesC(self,pieceBoard):   
        """ ocena mozliwosci najblizszych bic (wykorzystujac funkcje klasy Pionek) dla gracza C """
        movesC={}
        movesC.update(self.left_captureC(pieceBoard))
        movesC.update(self.right_captureC(pieceBoard))
        return movesC

    def get_valid_capturesB(self,pieceBoard): 
        """ ocena mozliwosci najblizszych bic (wykorzystujac funkcje klasy Pionek) dla gracza B """
        movesC={}
        movesC.update(self.left_captureB(pieceBoard))
        movesC.update(self.right_captureB(pieceBoard))
        return movesC

    def get_all_valid_captures(self,pieceBoard): 
        """ ocena mozliwosci najblizszych bic danego pionka w zaleznosci od gracza, do ktorego nalezy """
        moves={}
        if(self.player=='B'):
            moves.update(self.get_valid_capturesB(pieceBoard))
        else:
            moves.update(self.get_valid_capturesC(pieceBoard))
        return moves

    def get_all_valid_moves(self,pieceBoard): 
        """ ocena mozliwosci wszystkich ruchow danego pionka w zaleznosci od tego do ktorego gracza nalezy """
        moves={}
        if(self.player=='B'):
            moves.update(self.get_valid_capturesB(pieceBoard))
            self.capture_flag=True
            if not moves:
                 moves.update(self.get_valid_normal_movesB(pieceBoard ))
                 self.capture_flag=False
        else:
            moves.update(self.get_valid_capturesC(pieceBoard))
            self.capture_flag=True
            if not moves:
                 moves.update(self.get_valid_normal_movesC(pieceBoard))
                 self.capture_flag=False
        return moves
    
class Damka(Pionek):
    
    def __repr__(self):
        return "Damka ["+str(self.row)+","+str(self.col)+"] - "+self.player

    def left_backward_captureB(self,pieceBoard):    
        """ ocena mozliwosci bicia w lewo do tylu dla gracza B """
        movesC={}
        if(self.col-2>=0 and self.row+2<ROWS):
            if(pieceBoard[self.row+1][self.col-1]!=0 and pieceBoard[self.row+1][self.col-1].player!=self.player and pieceBoard[self.row+2][self.col-2]==0):
                movesC[(self.row+2,self.col-2)]=[pieceBoard[self.row+1][self.col-1]]
        return movesC
    
    def right_backward_captureB(self,pieceBoard):   
        """ ocena mozliwosci bicia w prawo do tylu dla gracza B """
        movesC={}
        if(self.col+2<COLS and self.row+2<ROWS):
            if(pieceBoard[self.row+1][self.col+1]!=0 and pieceBoard[self.row+1][self.col+1].player!=self.player and pieceBoard[self.row+2][self.col+2]==0):
                movesC[(self.row+2,self.col+2)]=[pieceBoard[self.row+1][self.col+1]]
        return movesC

    def left_backward_captureC(self,pieceBoard):    #
        """ ocena mozliwosci bicia w lewo do tylu dla gracza C """
        movesB={}
        if(self.col-2>=0 and self.row-2>=0):
            if(pieceBoard[self.row-1][self.col-1]!=0 and pieceBoard[self.row-1][self.col-1].player!=self.player and pieceBoard[self.row-2][self.col-2]==0):
                movesB[(self.row-2,self.col-2)]=[pieceBoard[self.row-1][self.col-1]]
        return movesB
    
    def right_backward_captureC(self,pieceBoard):   #
        """ ocena mozliwosci bicia w prawo do tylu dla gracza C """
        movesB={}
        if(self.col+2<COLS and self.row-2>=0):
            if(pieceBoard[self.row-1][self.col+1]!=0 and pieceBoard[self.row-1][self.col+1].player!=self.player and pieceBoard[self.row-2][self.col+2]==0):
                movesB[(self.row-2,self.col+2)]=[pieceBoard[self.row-1][self.col+1]]
        return movesB
    def get_valid_normal_movesC(self,pieceBoard): 
        """ ocena mozliwosci zwyklych ruchow (bez bicia) do przodu dla gracza C """
        movesC={}
        if(self.col+1<COLS and self.row+1<ROWS):
            if(pieceBoard[self.row+1][self.col+1]==0):
                movesC[(self.row+1,self.col+1)]=[]
        if(self.col+1<COLS and self.row-1>=0):
            if(pieceBoard[self.row-1][self.col+1]==0):
                movesC[(self.row-1,self.col+1)]=[]
        if(self.col-1>=0 and self.row+1<ROWS):
            if(pieceBoard[self.row+1][self.col-1]==0):
                movesC[(self.row+1,self.col-1)]=[]
        if(self.col+1>=0 and self.row-1>=0):
            if(pieceBoard[self.row-1][self.col-1]==0):
                movesC[(self.row-1,self.col-1)]=[]
        return movesC    
    def get_valid_normal_movesB(self,pieceBoard):   #
        """ ocena mozliwosci zwyklych ruchow (bez bicia) do przodu dla gracza B """
        movesB={}
        if(self.col+1<COLS and self.row+1<ROWS):
            if(pieceBoard[self.row+1][self.col+1]==0):
                movesB[(self.row+1,self.col+1)]=[]
        if(self.col+1<COLS and self.row-1>=0):
            if(pieceBoard[self.row-1][self.col+1]==0):
                movesB[(self.row-1,self.col+1)]=[]
        if(self.col-1>=0 and self.row+1<ROWS):
            if(pieceBoard[self.row+1][self.col-1]==0):
                movesB[(self.row+1,self.col-1)]=[]
        if(self.col+1>=0 and self.row-1>=0):
            if(pieceBoard[self.row-1][self.col-1]==0):
                movesB[(self.row-1,self.col-1)]=[]
        return movesB

    def get_valid_capturesC(self,pieceBoard): #
        """ ocena mozliwosci najblizszych bic (wykorzystujac funkcje klasy Pionek i Damka) dla gracza C """
        movesC={}
        movesC.update(self.left_captureC(pieceBoard))
        movesC.update(self.right_captureC(pieceBoard))
        movesC.update(self.left_backward_captureC(pieceBoard))
        movesC.update(self.right_backward_captureC(pieceBoard))
        return movesC

    def get_valid_capturesB(self,pieceBoard):   
        """ ocena mozliwosci najblizszych bic (wykorzystujac funkcje klasy Pionek i Damka) dla gracza B """
        movesB={}
        movesB.update(self.left_captureB(pieceBoard))
        movesB.update(self.right_captureB(pieceBoard))
        movesB.update(self.left_backward_captureB(pieceBoard))
        movesB.update(self.right_backward_captureB(pieceBoard))
        return movesB

    def get_all_valid_captures(self,pieceBoard): 
        """ ocena mozliwosci najblizszych bic danego pionka w zaleznosci od gracza, do ktorego nalezy """
        moves={}
        if(self.player=='B'):
            moves.update(self.get_valid_capturesB(pieceBoard))
        else:
            moves.update(self.get_valid_capturesC(pieceBoard))
        return moves

    def get_all_valid_moves(self,pieceBoard):   
        """ ocena mozliwosci wszystkich ruchow danego pionka w zaleznosci od tego do ktorego gracza nalezy """
        moves={}
        if(self.player=='B'):
            moves.update(self.get_valid_capturesB(pieceBoard))
            self.capture_flag=True
            if not moves:
                 moves.update(self.get_valid_normal_movesB(pieceBoard))
                 self.capture_flag=False
        else:
            moves.update(self.get_valid_capturesC(pieceBoard))
            self.capture_flag=True
            if not moves:
                 moves.update(self.get_valid_normal_movesC(pieceBoard))
                 self.capture_flag=False
        return moves

class Game:
    """ klasa w ktorej odbywa sie gra"""
    def __init__(self): 
        """tworzenie okienka i wywolywanie funkcji ktora rozpocznie tworzenie gry"""
        self.window = Tk()
        self.window.title("Warcaby ttk")
        self.mainframe = ttk.Frame(self.window)
        self.mainframe.grid(column = 0, row = 0, sticky=(N, W, E, S), padx=35, pady=30)
        self.initializeGame()
        self.window.mainloop()

    def initializeGame(self): 
        """funkcja tworzy potrzebne dla gry atrybuty klasy tworzy przycisk RESET oraz etykiete wskazujaca ktorego gracza jest kolej"""
        self.selected = None    #pionek ktory wybralismy do wykonania ruchu
        self.btnBoard = []  #tablica przechowujaca guziki
        self.pieceBoard = []    #tablica przechowujaca instancje pionkow
        self.turn = 'B' #zmienna informujaca ktorego gracza jest tura
        self.valid_moves = {}   #zmienna zawierajaca liste dostepnych ruchow dla wybranego piona
        self.capture_flag = False   #flaga informujaca czy wybrany pion ma w dostepnych ruchach zbicie innego piona
        self.ongoing_capture_flag=False #flaga informujaca czy trwa wielokrotne zbijanie pionow przeciwnika
        self.playerCLeft = self.playerBLeft = 12 #ilosc pionow jaka pozostala graczom

        #konfiguracja przyciskow i etykiety informujacej kogo jest tura 
        self.mainframe.grid_columnconfigure(7, weight= 1)
        ResetBtn = ttk.Button(self.mainframe, text="RESET", command=lambda :self.initializeGame()).grid(row = 5, column = 9, padx = 15)
        self.turnLabel = Label(self.mainframe, text="B turn").grid(row=2, column= 9, padx = 15)
        self.createBoard()

    def select(self, r, c, txt):
        """ funkcja obsluguje wybranie danego pola.
            Rozpoznaje ona zamiar wybrania pionka ktorym chcemy sie ruszyc oraz zamiar przesuniecia sie tym pionkiem """
        
        #wypisywanie pozycji i wlasciciela pionka ktory wybralismy (z informacja czy jest damka)
        if isinstance(self.pieceBoard[r][c], Damka):
            txt = self.pieceBoard[r][c].player +"d"
        print(str(r) +" "+ str (c) + txt)

        if self.selected:   #   jeżeli gracz wybrał już pionka
            if(self.capture_flag): #jezeli dostepne jest bicie
                result=self.capture(r,c)
                if not result: #jezeli do zbicia wybralismy niepoprawna komorke
                    messagebox.showinfo("Błąd", "Niepoprawny ruch")
                    if self.ongoing_capture_flag == False: #jezeli nie jestesmy w trakcie wielokrotnego bicia mozemy jeszcze zmienic pion ktorym chcemy wykonac ruch
                        if isinstance(self.selected, Damka):
                            temp = self.selected.player +"d"
                        else:
                            temp = self.selected.player
                        self.btnBoard[self.selected.row][self.selected.col] =(ttk.Button(self.mainframe, text=temp, command=lambda row=self.selected.row, col=self.selected.col, text=self.selected.player:self.select(row,col,text)).grid(row = self.selected.row, column = self.selected.col))
                        self.selected = None
                        self.select(r, c, txt)
            else: #jezeli nie jest dostepne bicie
                result= self.move(r, c)
                if not result:
                    if isinstance(self.selected, Damka):
                        temp = self.selected.player +"d"
                    else:
                        temp = self.selected.player
                    self.btnBoard[self.selected.row][self.selected.col] =(ttk.Button(self.mainframe, text=temp, command=lambda row=self.selected.row, col=self.selected.col, text=self.selected.player:self.select(row,col,text)).grid(row = self.selected.row, column = self.selected.col))
                    self.selected = None
                    self.select(r, c, txt)
                    messagebox.showinfo("Błąd", "Niepoprawny ruch")
                else:
                    self.selected = None

        piece = self.pieceBoard[r][c]
        if piece != 0 and piece.player == self.turn and self.ongoing_capture_flag==False:    # wybieranie jakiegoś pionka przed wykonaniem ruchu
            self.selected = piece
            temp = "["+txt+"]"
            self.btnBoard[r][c] = (ttk.Button(self.mainframe, text= temp, command=lambda row=r, col=c, text=txt:self.select(row,col,text)).grid(row = r, column=c))
            self.valid_moves = piece.get_all_valid_moves(self.pieceBoard)
            self.capture_flag = piece.capture_flag
            return True
        return False
    
    def capture(self,r,c):
        """ Potrzebne operacje aby wykonać bicie pionkiem, aktualizowanie listy przycisków i listy pionków, 
            usuwanie zbitych pionków, sprawdzanie czy po ruchu pionek nie będzie damką i zmiana tury"""
        piece = self.pieceBoard[r][c] #pole na ktrym chcemy wyladowac
        if self.selected and piece == 0 and (r, c) in self.valid_moves: #jezeli pionek zostal wybrany, miejsce na  ktore chcemy przejsc jest puste i jest to w dozwolonych ruchach
            #zmieniamy polozenie pionka w tablicy pionkow i guzikow
            self.pieceBoard[self.selected.row][self.selected.col], self.pieceBoard[r][c] = self.pieceBoard[r][c], self.pieceBoard[self.selected.row][self.selected.col]
            self.btnBoard[self.selected.row][self.selected.col] = (ttk.Button(self.mainframe, text="", command=lambda row=self.selected.row, col=self.selected.col, text="":self.select(row,col,text)).grid(row = self.selected.row, column = self.selected.col))
        
            skipped = self.valid_moves[(r, c)]  #zbity pion przeciwnika
            if skipped:
                self.remove(skipped)    #usuwamy zbity pion

            #wyswietlamy nowa pozycje pionka na odpowiednim guziku
            if isinstance(self.selected, Damka):
                temp = self.selected.player +"d"
            else:
                temp = self.selected.player
            self.btnBoard[r][c] = (ttk.Button(self.mainframe, text=temp, command=lambda row=r, col=c, text=temp:self.select(row,col,text)).grid(row = r, column = c))
            
            #zmieniamy polozenie pionka w atrybutach instancji potomka klasy Pionek
            self.selected.move(r,c)

            #jezeli pionek dotarl do konca planszy zamiana w damke i koniec tury
            if r == ROWS-1 and self.pieceBoard[r][c].player == 'C' and not isinstance(self.pieceBoard[r][c], Damka):
                print("Damka - C")
                self.pieceBoard[r][c] = Damka(r, c, 'C')
                self.btnBoard[r][c] = (ttk.Button(self.mainframe, text='Cd', command=lambda row=r, col=c, text='C':self.select(row,col,text)).grid(row = r, column = c))
                self.changeTurn()
                self.ongoing_capture_flag=False
                self.selected=None
            elif r == 0 and self.pieceBoard[r][c].player == 'B' and not isinstance(self.pieceBoard[r][c], Damka):
                print("Damka - B")
                self.pieceBoard[r][c] = Damka(r, c, 'B')
                self.btnBoard[r][c] = (ttk.Button(self.mainframe, text='Bd', command=lambda row=r, col=c, text='B':self.select(row,col,text)).grid(row = r, column = c))
                self.changeTurn()
                self.ongoing_capture_flag=False
                self.selected=None
            else:
                #sprawdzenie czy mamy dostepne kolejne zbicia tym pionem
                moves={}
                if isinstance(self.selected,Damka):
                    pionek=Damka(r,c,self.selected.player)
                else:    
                    pionek=Pionki(r,c,self.selected.player)
                moves.update(pionek.get_all_valid_captures(self.pieceBoard))
    
                if not moves: #jezeli nie sa dostepne konczymy ture gracza
                    self.changeTurn()
                    self.selected=None
                    self.ongoing_capture_flag=False
                else:   #jezeli sa dostepne czekamy az gracz zrobi nastepny ruch
                    if isinstance(self.selected, Damka):
                        txt = self.selected.player +"d"
                    else:
                        txt=self.selected.player
                    print(str(r) +" "+ str (c) + txt)
                    self.valid_moves=moves
                    self.selected=pionek
                    temp = "["+txt+"]"
                    self.btnBoard[r][c] = (ttk.Button(self.mainframe, text= temp, command=lambda row=r, col=c, text=txt:self.select(row,col,text)).grid(row = r, column=c))
                    self.ongoing_capture_flag=True
                
        else: #else do pierwszego if'a jezeli ktorys podstawowych z warunkow nie zostal spelniony wzracamy false
            return False
        
        return True #jezeli wszystko sie powiodlo zwracamy true

    def move(self, row, col):
        """ Potrzebne operacje aby wykonać ruch pionkiem, aktualizowanie listy pzycisków i listy pionków, 
            usuwanie zbitych pionków, sprawdzanie czy po ruchu pionek nie będzie damką i zmiana tury"""
        piece = self.pieceBoard[row][col]   #pole na ktrym chcemy wyladowac
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #jezeli pionek zostal wybrany, miejsce na  ktore chcemy przejsc jest puste i jest to w dozwolonych ruchach
            
            #zmieniamy polozenie pionka w tablicy pionkow i guzikow
            self.pieceBoard[self.selected.row][self.selected.col], self.pieceBoard[row][col] = self.pieceBoard[row][col], self.pieceBoard[self.selected.row][self.selected.col]
            self.btnBoard[self.selected.row][self.selected.col] = (ttk.Button(self.mainframe, text="", command=lambda row=self.selected.row, col=self.selected.col, text="":self.select(row,col,text)).grid(row = self.selected.row, column = self.selected.col))

            #wyswietlamy nowa pozycje pionka na odpowiednim guziku
            if isinstance(self.selected, Damka):
                temp = self.selected.player +"d"
            else:
                temp = self.pieceBoard[row][col].player
            self.btnBoard[row][col] = (ttk.Button(self.mainframe, text=temp, command=lambda row=row, col=col, text=temp:self.select(row,col,text)).grid(row = row, column = col))
            self.selected.move(row,col)

             #jezeli pionek dotarl do konca planszy zamiana w damke i koniec tury
            if row == ROWS-1 and self.pieceBoard[row][col].player == 'C' and not isinstance(self.pieceBoard[row][col], Damka):
                print("Damka - C")
                self.pieceBoard[row][col] = Damka(row, col, 'C')
                self.btnBoard[row][col] = (ttk.Button(self.mainframe, text='Cd', command=lambda row=row, col=col, text='C':self.select(row,col,text)).grid(row = row, column = col))
            elif row == 0 and self.pieceBoard[row][col].player == 'B' and not isinstance(self.pieceBoard[row][col], Damka):
                print("Damka - B")
                self.pieceBoard[row][col] = Damka(row, col, 'B')
                self.btnBoard[row][col] = (ttk.Button(self.mainframe, text='Bd', command=lambda row=row, col=col, text='B':self.select(row,col,text)).grid(row = row, column = col))
            #zmiana tury
            self.changeTurn()

        else: #else do pierwszego if'a jezeli ktorys podstawowych z warunkow nie zostal spelniony wzracamy false
            return False
        
        return True #jezeli wszystko sie powiodlo zwracamy true

    def changeTurn(self):
        """ funkcja zmieniajaca ture gracza z B na C albo  odwrotnie """
        self.valid_moves = {}
        self.valid_captures ={}
        if self.turn == 'C':
            self.turn = 'B'
            self.turnLabel = Label(self.mainframe, text="B turn").grid(row=2, column= 9, padx = 15)
        else:
            self.turn = 'C'
            self.turnLabel = Label(self.mainframe, text="C turn").grid(row=2, column= 9, padx = 15)
        print("Turn "+self.turn)
    

    def createBoard(self):
        """ funckja zapelnia dwie tablice:
                -btnBoard (tablica guzikow):
                    - w miejscach w ktorych nie ma pionow brak tekstu
                     - w miejscach gdzie stoja piony gracza B litera "B"
                    -w miejscach gdzie stoja piony gracza C litera "C"
                -pieceBoard (tablica pionow) tablica odzwierciedlajaca ustawienie pionow:
                    - w miejscach w ktorych nie ma pionow, ale bedzie dalo sie tam stanac w przyszosci przyjmuje wartosc 0
                    - w miejscach gdzie stoja piony gracza B i C instancje klasy Pionki z odpowiednimi atrybutami  """
        for r in range(ROWS):
            self.btnBoard.append([])
            self.pieceBoard.append([])
            for c in range(COLS):
                #gdy nacisniemy stworzone guziki wywola sie funkcja select (wyzej)
                if (c % 2 == r % 2):
                    self.btnBoard[r].append(ttk.Button(self.mainframe, text="", command=lambda row=r, col=c, text="":self.select(row,col,text)).grid(row = r, column = c))
                    self.pieceBoard[r].append(0)
                else:
                    if (r < 3):
                        self.btnBoard[r].append(ttk.Button(self.mainframe, text="C", command=lambda row=r, col=c, text="C":self.select(row,col,text)).grid(row = r, column = c))
                        self.pieceBoard[r].append(Pionki(r,c,'C'))
                    elif (r > 4):
                        self.btnBoard[r].append(ttk.Button(self.mainframe, text="B", command=lambda row=r, col=c, text="B":self.select(row,col,text)).grid(row = r, column = c))
                        self.pieceBoard[r].append(Pionki(r,c,'B'))
                    else:
                        self.btnBoard[r].append(ttk.Button(self.mainframe, text="", command=lambda row=r, col=c, text="":self.select(row,col,text)).grid(row = r, column = c))
                        self.pieceBoard[r].append(0)
    

    

    def remove(self, pieces):
        """ usuwanie pionka z tablicy guzikow oraz pionkow """
        for piece in pieces:
            self.pieceBoard[piece.row][piece.col] = 0
            self.btnBoard[piece.row][piece.col] = (ttk.Button(self.mainframe, text="", command=lambda row=piece.row, col=piece.col, text="":self.select(row,col,text)).grid(row = piece.row, column = piece.col))
            if piece != 0:
                if piece.player == 'B':
                    self.playerBLeft -= 1
                else:
                    self.playerCLeft -= 1
        self.winner()

    def winner(self):
        """ oglaszanie wygranej jednego z graczy """
        if self.playerBLeft <= 0:
            messagebox.showinfo("WYGRANA", " Wygrał gracz 2 (gracz C)")
        elif self.playerCLeft <= 0:
            messagebox.showinfo("WYGRANA", " Wygrał gracz 1 (gracz B)")
        
            

game = Game()