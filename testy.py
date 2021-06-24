from game import Game, Pionki, Pionek, Damka

ROWS, COLS = 8, 8

class Test(Game):
    def __init__(self):
        self.initializeGame(1)

    def initializeGame(self, typ):
        print("Nowa gra")
        self.selected = None
        self.pieceBoard = []
        self.turn = 'C'
        self.valid_moves = {}
        self.capture_flag = False
        self.ongoing_capture_flag=False
        self.playerCLeft = self.playerBLeft = 12      

        if(typ == 1):
            self.createBoard()
        elif(typ == 2):
            self.playerCLeft = 1
            self.playerBLeft = 2
            self.createBoard2()
        elif(typ == 3):
            self.playerCLeft = 1
            self.playerBLeft = 1
            self.createBoard3()
        elif(typ == 4):
            self.playerCLeft = 1
            self.playerBLeft = 1
            self.createBoard4()

    def createBoard(self):
        for r in range(ROWS):
            self.pieceBoard.append([])
            for c in range(COLS):
                if (c % 2 == r % 2):
                    self.pieceBoard[r].append(0)
                else:
                    if (r < 3):
                        self.pieceBoard[r].append(Pionki(r,c,'C'))
                    elif (r > 4):
                        self.pieceBoard[r].append(Pionki(r,c,'B'))
                    else:
                        self.pieceBoard[r].append(0)
    
    def createBoard2(self):
        for r in range(ROWS):
            self.pieceBoard.append([])
            for c in range(COLS):
                self.pieceBoard[r].append(0)
        self.pieceBoard[1][5]=Pionki(1,5,'C')
        self.pieceBoard[2][4]=Pionki(2,4,'B')
        self.pieceBoard[4][4]=Pionki(4,4,'B')
                
    
    def createBoard3(self):
        for r in range(ROWS):
            self.pieceBoard.append([])
            for c in range(COLS):
                self.pieceBoard[r].append(0)
        self.pieceBoard[6][3]=Pionki(6,3,'C')
    
    def createBoard4(self):
        for r in range(ROWS):
            self.pieceBoard.append([])
            for c in range(COLS):
                self.pieceBoard[r].append(0)
        self.pieceBoard[6][3]=Damka(6,3,'C')
        self.pieceBoard[5][4]=Pionki(5,4,'B')
    
    def printBoard(self):
        for col in range(COLS):
            print(self.pieceBoard[col])
            print("\n")
        print("\n")

    
    def select(self, r, c, txt):

        if isinstance(self.pieceBoard[r][c], Damka):
            txt = self.pieceBoard[r][c].player +"d"
        print(str(r) +" "+ str (c) + txt)

        if self.selected:   #   jeżeli gracz wybrał już pionka to
            if(self.capture_flag):
                result=self.capture(r,c)
                if not result:
                    if self.ongoing_capture_flag == False:
                        if isinstance(self.selected, Damka):
                            temp = self.selected.player +"d"
                        else:
                            temp = self.selected.player

                        self.selected = None
                        self.select(r, c, txt)
            else:
                result= self.move(r, c)
                if not result:
                    if isinstance(self.selected, Damka):
                        temp = self.selected.player +"d"
                    else:
                        temp = self.selected.player
                    self.selected = None
                    self.select(r, c, txt)
                else:
                    self.selected = None

        piece = self.pieceBoard[r][c]
        if piece != 0 and piece.player == self.turn and self.ongoing_capture_flag==False:    # wybieranie jakiegoś pionka przed wykonaniem ruchu
            self.selected = piece
            temp = "["+txt+"]"
            self.valid_moves = piece.get_all_valid_moves(self.pieceBoard)
            self.capture_flag = piece.capture_flag
            return True
        return False
    
    
    def capture(self,r,c):
        piece = self.pieceBoard[r][c]
        if self.selected and piece == 0 and (r, c) in self.valid_moves:
            """ Potrzebne operacje aby wykonać ruch pionkiem, aktualizowanie listy pzycisków i listy pionków, 
            usuwanie zbitych pionków, sprawdzanie czy po ruchu pionek nie będzie damką i zmiana tury"""
            self.pieceBoard[self.selected.row][self.selected.col], self.pieceBoard[r][c] = self.pieceBoard[r][c], self.pieceBoard[self.selected.row][self.selected.col]
            skipped = self.valid_moves[(r, c)]
            if skipped:
                self.remove(skipped)
            if isinstance(self.selected, Damka):
                temp = self.selected.player +"d"
            else:
                temp = self.selected.player
            
            self.selected.move(r,c)

            if r == ROWS-1 and self.pieceBoard[r][c].player == 'C' and not isinstance(self.pieceBoard[r][c], Damka):
                print("Damka - C")
                self.pieceBoard[r][c] = Damka(r, c, 'C')
                self.changeTurn()
                self.ongoing_capture_flag=False
                self.selected=None
            elif r == 0 and self.pieceBoard[r][c].player == 'B' and not isinstance(self.pieceBoard[r][c], Damka):
                print("Damka - B")
                self.pieceBoard[r][c] = Damka(r, c, 'B')
                self.changeTurn()
                self.ongoing_capture_flag=False
                self.selected=None
            else:
                moves={}
                if isinstance(self.selected,Damka):
                    pionek=Damka(r,c,self.selected.player)
                else:    
                    pionek=Pionki(r,c,self.selected.player)
                moves.update(pionek.get_all_valid_captures(self.pieceBoard))
                if not moves:
                    self.changeTurn()
                    self.selected=None
                    self.ongoing_capture_flag=False
                else:
                    if isinstance(self.selected, Damka):
                        txt = self.selected.player +"d"
                    else:
                        txt=self.selected.player
                    print(str(r) +" "+ str (c) + txt)
                    self.valid_moves=moves
                    self.selected=pionek
                    temp = "["+txt+"]"
                    self.ongoing_capture_flag=True
                
        else:
            return False
        
        return True

    def move(self, row, col):
        piece = self.pieceBoard[row][col]
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            """ Potrzebne operacje aby wykonać ruch pionkiem, aktualizowanie listy pzycisków i listy pionków, 
            usuwanie zbitych pionków, sprawdzanie czy po ruchu pionek nie będzie damką i zmiana tury"""
            self.pieceBoard[self.selected.row][self.selected.col], self.pieceBoard[row][col] = self.pieceBoard[row][col], self.pieceBoard[self.selected.row][self.selected.col]

            if isinstance(self.selected, Damka):
                temp = self.selected.player +"d"
            else:
                temp = self.pieceBoard[row][col].player
            
            self.selected.move(row,col)

            if row == ROWS-1 and self.pieceBoard[row][col].player == 'C' and not isinstance(self.pieceBoard[row][col], Damka):
                print("Damka - C")
                self.pieceBoard[row][col] = Damka(row, col, 'C')

            elif row == 0 and self.pieceBoard[row][col].player == 'B' and not isinstance(self.pieceBoard[row][col], Damka):
                print("Damka - B")
                self.pieceBoard[row][col] = Damka(row, col, 'B')
               
            self.changeTurn()

        else:
            return False
        
        return True

    def changeTurn(self):
        self.valid_moves = {}
        if self.turn == 'C':
            self.turn = 'B'
        else:
            self.turn = 'C'
        print("Turn "+self.turn)

    def remove(self, pieces):
        for piece in pieces:
            print("Zbito pionka")
            self.pieceBoard[piece.row][piece.col] = 0
            if piece != 0:
                if piece.player == 'B':
                    self.playerBLeft -= 1
                else:
                    self.playerCLeft -= 1
        self.winner()

    def winner(self):
        if self.playerBLeft <= 0:
            print("WYGRANA", " Wygrał gracz 1 (gracz C)")
        elif self.playerCLeft <= 0:
            print("WYGRANA", " Wygrał gracz 2 (gracz B)")

    def twoMovesEachPlayer(self):
        print("TEST 1")
        self.initializeGame(1)
        self.select(2,3,"C")
        self.select(3,2,"")
        self.select(5,6,"B")
        self.select(4,7,"")
        self.select(3,2,"C")
        self.select(4,1,"")
        self.select(4,7,"B")
        self.select(3,6,"")
        if(self.pieceBoard[3][6].player=='B' and self.pieceBoard[4][1].player=='C'):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")

    
    def failureOfWorngMoveOfAPawn(self):
        print("TEST 2")
        self.initializeGame(1)
        self.select(2,1,"C")
        self.select(0,0,"")
        self.select(5,4,"B")
        self.select(6,7,"B")
        if(self.pieceBoard[2][1].player=='C' and self.pieceBoard[5][4].player=='B'):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")

    def shouldCaptureAPawn(self):
        print("TEST 3")
        self.initializeGame(1)
        self.select(2,3,"C")
        self.select(3,2,"")
        self.select(5,2,"B")
        self.select(4,3,"")
        self.select(2,5,"C")
        self.select(3,6,"")
        self.select(5,4,"B")
        self.select(4,5,"")
        self.select(3,6,"C")
        self.select(5,4,"")
        if(self.pieceBoard[5][4].player=='C' and self.pieceBoard[3][6]==0):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")
        
    def shuldCaptureMultipleTimes(self):
        print("TEST 4")
        self.initializeGame(2)
        self.select(1,5,"C")
        self.select(3,3,"")
        self.select(5,5,"")
        if(self.pieceBoard[5][5].player=='C' and self.pieceBoard[2][4]==0 and self.pieceBoard[4][4]==0):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")
    def shouldTurnIntoQueen(self):
        print("TEST 5")
        self.initializeGame(3)
        self.select(6,3,"C")
        self.select(7,2,"")
        if(isinstance(self.pieceBoard[7][2],Damka)):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")
    def queenShouldCaptureBackward(self):
        print("TEST 6")
        self.initializeGame(4)
        self.select(6,3,"C")
        self.select(4,5,"")
        if(self.pieceBoard[4][5].player=='C' and self.pieceBoard[5][4]==0):
            print("Spelniony \n")
        else:
            print("Nie spelniony \n")

    def playerCShouldWin(self):
        print("TEST 7")
        self.initializeGame(4)
        self.select(6,3,"C")
        self.select(4,5,"")
        print("\n")

    def shouldCreateNewGame(self):
        print("TEST 8")
        self.initializeGame(4)
        self.select(6,3,"C")
        self.select(4,5,"")
        #dalsza czesc testu w sparwozdaniu

test = Test()  
test.twoMovesEachPlayer()  
test.failureOfWorngMoveOfAPawn()
test.shouldCaptureAPawn()
test.shuldCaptureMultipleTimes()
test.shouldTurnIntoQueen()
test.queenShouldCaptureBackward()
test.playerCShouldWin()
test.shouldCreateNewGame()


    