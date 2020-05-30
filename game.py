import random
import tkinter
import time
import re


class Game:
    def __init__(self):
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-'],
        ]

        self.master = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.master, bg='black', height=300, width=580)
        self.master.resizable(False, False)

        self.player1 = 'X'
        self.player2 = 'O'

        self.winner = None

        self.player1_score = 0
        self.player2_score = 0

        self.loopCheck = True
        self.stepCount = 0

        self.players = [self.player1, self.player2]
        random.shuffle(self.players)
        self.turn = self.players[0]
        self.check_button = False

    def check_winner(self, board, letter):
        if (board[0][0] == letter and board[0][1] == letter and board[0][2] == letter) or \
                (board[1][0] == letter and board[1][1] == letter and board[1][2] == letter) or \
                (board[2][0] == letter and board[2][1] == letter and board[2][2] == letter) or \
                (board[0][0] == letter and board[1][0] == letter and board[2][0] == letter) or \
                (board[0][1] == letter and board[1][1] == letter and board[2][1] == letter) or \
                (board[0][2] == letter and board[1][2] == letter and board[2][2] == letter) or \
                (board[0][0] == letter and board[1][1] == letter and board[2][2] == letter) or \
                (board[0][2] == letter and board[1][1] == letter and board[2][0] == letter):
            self.winner = letter
            self.end()
            if self.winner == self.player1:
                self.player1_score += 1
            else:
                self.player2_score += 1
            return True
        elif self.stepCount == 9 and self.winner is None:
            self.end()
            return True
        return False

    def playAgain(self):
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-'],
        ]

        self.player1 = 'X'
        self.player2 = 'O'

        self.winner = None

        self.stepCount = 0

        self.players = [self.player1, self.player2]
        random.shuffle(self.players)
        self.turn = self.players[0]
        self.btn.pack_forget()
        self.btn1.pack_forget()
        self.canvas.create_rectangle((0, 0), (580, 300), fill='black')
        self.run()

    def draw_button(self):
        self.check_button = True
        self.btn = tkinter.Button(self.master, text='Play again', command=self.playAgain)
        self.btn1 = tkinter.Button(self.master, text='<- Back', command=self.draw_startMenu)

        self.btn.pack()
        self.btn1.pack()

    def draw_turn(self):
        if self.winner is None or self.stepCount != 9:
            self.canvas.delete('turn')
            self.canvas.create_text(515, 150, fill="white", font="Roboto 25 bold",
                                    text="{} Turn".format(self.turn), tag='turn')
        else:
            self.canvas.delete('turn')

    def draw_score(self):
        self.canvas.create_text(505, 25, fill="white", font="Roboto 15 bold",
                                text="Player X: {}".format(self.player1_score), tag='turn')
        self.canvas.create_text(505, 55, fill="white", font="Roboto 15 bold",
                                text="Player O: {}".format(self.player2_score), tag='turn')

    def draw_symbol(self, cell, player):
        if player == 'X':
            self.canvas.create_line(((int(str(cell[0]) + '00') + 10),
                                     (int(str(cell[1]) + '00') + 10)),
                                    ((int(str(cell[0]) + '00') + 90),
                                     (int(str(cell[1]) + '00') + 90)),
                                    fill='white', width='3')
            self.canvas.create_line(((int(str(cell[0]) + '00') + 90),
                                     (int(str(cell[1]) + '00') + 10)),
                                    ((int(str(cell[0]) + '00') + 10),
                                     (int(str(cell[1]) + '00') + 90)),
                                    fill='white', width='3')
            if self.turn == self.player1:
                self.turn = self.player2
            else:
                self.turn = self.player1
        else:
            self.canvas.create_oval(((int(str(cell[0]) + '00') + 10),
                                     (int(str(cell[1]) + '00') + 10)),
                                    ((int(str(cell[0]) + '00') + 90),
                                     (int(str(cell[1]) + '00') + 90)),
                                    fill='black', width='3', outline='white')
            if self.turn == self.player2:
                self.turn = self.player1
            else:
                self.turn = self.player1

    def check_move(self, cell):
        if cell[0] < 300:
            x = cell[0] // 100
            y = cell[1] // 100
            if self.board[y][x] in '-':
                self.do_step([x, y])
                self.draw_symbol([x, y], self.turn)
                o = self.check_winner(self.board, 'O')
                x = self.check_winner(self.board, 'X')
                if o is True or x is True:
                    self.canvas.delete('turn')
                    self.draw_button()
                else:
                    self.draw_turn()
                self.draw_score()

    def createServer(self):
        if hasattr(self, 'mainText'):
            self.canvas.delete('title')
        if hasattr(self, 'mainMenuBtn'):
            self.mainMenuBtn.place_forget()
        if hasattr(self, 'createServerBtn'):
            self.createServerBtn.place_forget()
        if hasattr(self, 'joinServerBtn'):
            self.joinServerBtn.place_forget()
        self.multiplayerMenuBtn = tkinter.Button(self.master,
                                                 text="    Back    ",
                                                 command=self.draw_multiplayerMenu,
                                                 font='Roboto 15 bold')
        self.multiplayerMenuBtn.place(x=250, y=180)
        self.loopCheck = True
        frame = 0
        while self.loopCheck:
            if frame == 0:
                self.canvas.delete('title')
                self.canvas.create_text(290, 100, fill="white", font="Roboto 28 bold",
                                        text="Waiting for opponent", tag='title')
                self.canvas.update()
                frame += 1
            elif frame == 1:
                self.canvas.delete('title')
                self.canvas.create_text(290, 100, fill="white", font="Roboto 28 bold",
                                        text="Waiting for opponent.", tag='title')
                self.canvas.update()
                frame += 1
            elif frame == 2:
                self.canvas.delete('title')
                self.canvas.create_text(290, 100, fill="white", font="Roboto 28 bold",
                                        text="Waiting for opponent..", tag='title')
                self.canvas.update()
                frame += 1
            else:
                self.canvas.delete('title')
                self.canvas.create_text(290, 100, fill="white", font="Roboto 28 bold",
                                        text="Waiting for opponent...", tag='title')
                frame = 0
                self.canvas.update()
            time.sleep(1)

    def checkIP(self):
        enteredIp = self.entry1.get()
        pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        test = pat.match(enteredIp)
        if test:
            print('Joining...')
        else:
            self.canvas.create_text(290, 285, fill="white", font="Roboto 17 bold",
                                    text="IP is not correct", tag='ipStatus')

    def joinGame(self):
        if hasattr(self, 'mainText'):
            self.canvas.delete('title')
        if hasattr(self, 'mainMenuBtn'):
            self.mainMenuBtn.place_forget()
        if hasattr(self, 'createServerBtn'):
            self.createServerBtn.place_forget()
        if hasattr(self, 'joinServerBtn'):
            self.joinServerBtn.place_forget()

        self.canvas.create_text(170, 115, fill="white", font="Roboto 25 bold",
                                text="Enter server IP", tag='title')

        self.entry1 = tkinter.Entry(self.master, width='20', font='Roboto 18 bold')
        self.entry1.place(x=55, y=150)
        self.checkEntered = tkinter.Button(self.master, text="       Join        ",
                                           command=self.checkIP, font='Roboto 15 bold')
        self.backToMultiMenu = tkinter.Button(self.master, text="      Back        ",
                                              command=self.draw_multiplayerMenu, font='Roboto 15 bold')
        self.checkEntered.place(x=400, y=100)
        self.backToMultiMenu.place(x=400, y=160)

    def draw_startMenu(self):
        if hasattr(self, 'mainMenuBtn'):
            self.mainMenuBtn.place_forget()
        if hasattr(self, 'createServerBtn'):
            self.createServerBtn.place_forget()
        if hasattr(self, 'joinServerBtn'):
            self.joinServerBtn.place_forget()
        self.canvas.unbind("<Button-1>")
        if self.check_button:
            self.btn.pack_forget()
            self.btn1.pack_forget()
        self.canvas.create_rectangle((0, 0), (580, 300), fill='black')
        self.startSingle = tkinter.Button(self.master, text="       Play       ",
                                          command=self.run, font='Roboto 15 bold')
        self.startMulti = tkinter.Button(self.master, text="  Multiplayer ",
                                         command=self.draw_multiplayerMenu, font='Roboto 15 bold')
        self.exitBtn = tkinter.Button(self.master, text="       Exit        ",
                                      command=self.exit, font='Roboto 15 bold')
        self.startSingle.place(x=405, y=50)
        self.startMulti.place(x=405, y=115)
        self.exitBtn.place(x=405, y=180)
        self.canvas.create_text(200, 80, fill="white", font="Roboto 30 bold",
                                text="Tic-Tac-Toe", tag='title')
        self.canvas.create_text(95, 286, fill="white", font="Roboto 12 bold",
                                text="© By Rafayel & Martin", tag='title')
        self.canvas.create_line((100, 115), (185, 200), fill='white', width='2')
        self.canvas.create_line((185, 115), (100, 200), fill='white', width='2')
        self.canvas.create_line((200, 110), (200, 215), fill='white', width='4')
        self.canvas.create_oval((215, 115), (305, 205), fill='black', width='2', outline='white')
        self.board = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-'],
        ]

        self.player1 = 'X'
        self.player2 = 'O'

        self.winner = None

        self.stepCount = 0

        self.player1_score = 0
        self.player2_score = 0

        self.players = [self.player1, self.player2]
        random.shuffle(self.players)
        self.turn = self.players[0]
        self.canvas.pack()
        self.master.mainloop()

    def draw_multiplayerMenu(self):
        if hasattr(self, 'multiplayerMenuBtn'):
            self.multiplayerMenuBtn.place_forget()
        if hasattr(self, 'backToMultiMenu'):
            self.backToMultiMenu.place_forget()
        if hasattr(self, 'checkEntered'):
            self.checkEntered.place_forget()
        if hasattr(self, 'entry1'):
            self.entry1.place_forget()

        self.loopCheck = False
        self.startSingle.place_forget()
        self.startMulti.place_forget()
        self.exitBtn.place_forget()

        self.canvas.create_rectangle((0, 0), (580, 300), fill='black')
        self.canvas.create_text(290, 70, fill="white", font="Roboto 24 bold",
                                text="Choose variant", tag='title')
        self.mainText = True

        self.createServerBtn = tkinter.Button(self.master, text="Create Server",
                                              command=self.createServer, font='Roboto 15 bold')
        self.joinServerBtn = tkinter.Button(self.master, text=" Join Server ",
                                            command=self.joinGame, font='Roboto 15 bold')
        self.mainMenuBtn = tkinter.Button(self.master, text="    Back    ",
                                          command=self.draw_startMenu, font='Roboto 15 bold')
        self.createServerBtn.place(x=155, y=120)
        self.joinServerBtn.place(x=330, y=120)
        self.mainMenuBtn.place(x=250, y=180)

    def do_step(self, cell):
        self.board[cell[1]][cell[0]] = self.turn 
        self.stepCount += 1
        return True

    def end(self):
        if self.winner == 'X' or self.winner == 'O':
            self.canvas.create_text(515, 150, fill="white", font="Roboto 25 bold",
                                    text="Won {}".format(self.winner))
        else:
            self.canvas.create_text(515, 150, fill="white", font="Roboto 25 bold",
                                    text="Draw")

    def drawUI(self):
        self.draw_turn()
        self.draw_score()

    def click(self, event):
        if self.winner is None:
            cell_x = event.x
            cell_y = event.y
            self.check_move((cell_x, cell_y))

    def exit(self):
        self.master.destroy()

    def run(self):
        self.startSingle.place_forget()
        self.startMulti.place_forget()
        self.exitBtn.place_forget()
        self.canvas.create_rectangle((0, 0), (580, 300), fill='black')
        self.canvas.create_line((100, 0), (100, 300), fill='white', width='3')
        self.canvas.create_line((200, 0), (200, 300), fill='white', width='3')
        self.canvas.create_line((300, 0), (300, 300), fill='white', width='3')
        self.canvas.create_line((0, 100), (300, 100), fill='white', width='3')
        self.canvas.create_line((0, 200), (300, 200), fill='white', width='3')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.drawUI()


game = Game()
game.draw_startMenu()
