# GUI for keeping track of tennis scores.
# Date: 10-11-2022
# Author: Samir Gupta

# type: ignore

import tkinter as tk
from tkinter import ttk
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

WINDOW_LENGTH = 800
WINDOW_HEIGHT = 300
WINDOW_X = 320
WINDOW_Y = 20
WINDOW_GEO = f'{WINDOW_LENGTH}x{WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}'

PRIMARY_COLOUR = 'dodger blue'
SECONDARY_COLOUR = 'deep sky blue'
TERTIARY_COLOUR = 'grey'
DEFAULT_COLOUR = 'white'
FONT = 'calibri'
REG_TEXT = 18
LABEL_FONT = {'font':(FONT, REG_TEXT)}
MAIN_RELIEF = {'relief':'groove'}
DEFAULT_RELIEF = {'relief': 'flat'}
PRIMARY_TEXT_COLOUR = 'black'
SECONDARY_TEXT_COLOUR = 'gold'
DEF_PLAYER_NAME_WIDTH = 9
WIDTH_DEFAULT = {'width':10}
WIDTH_SMALL = {'width': 3}
WIDTH_XSMALL = {'width': 2}

NAMES_LABEL = {'x': WINDOW_LENGTH // 2 - 55, 'y': 50}
PLAYER_ENTRY_1 = {'x': WINDOW_LENGTH // 2 - 90, 'y': 80}
PLAYER_ENTRY_2 = {'x': WINDOW_LENGTH // 2 - 90, 'y': 120}
BEST_OF_LABEL = {'x': WINDOW_LENGTH // 2 - 90, 'y': 173}
BEST_OF_ENTRY = {'x': 425, 'y': 170}
GO_BUTTON = {'x': WINDOW_LENGTH // 2 - 45, 'y': 230}

P1_LABEL = {'x': 200, 'y': 100}
P2_LABEL = {'x': 200, 'y': 125}
BOX_START_X = 200
BOX_START_Y = 100
BOX_W_DX = 11.5
BOX_DX = 40
BOX_DY = 25
MESSAGE = {'x': 200, 'y': 73}
P1_BUTTON = {'x': 175, 'y': 100}
P2_BUTTON = {'x': 175, 'y': 125}
WIN_TEXT = {'x': 200, 'y': 160}
RESTART_TEXT = {'x': 200, 'y': 190}
YES_BUTTON = {'x': 200, 'y': 220}
NO_BUTTON = {'x': 250, 'y': 220}


class Score:
    def __init__(self, p1, p2, best):
        self.p1, self.p2, self.best = p1, p2, best
        self.sets, self.game, self.server, self.set_w = [], [0, 0], True, [0, 0]
    
    def __repr__(self):
        return f'Tennis Score: {self.p1} vs {self.p2}, sets: {self.sets}, game: {self.game}'

    def point(self, w, l):
        if type(self.game[0]) == type(self.game[1]) and type(self.game[0]) == type(''):
            if self.game[0] == '':
                self.game = ['0', '0']
            if int(self.game[w]) >= 6 and int(self.game[w]) - int(self.game[l]) >= 1:
                self.win_game(w, l)
            else:
                self.game[w] = str(int(self.game[w]) + 1)
                if (int(self.game[w]) + int(self.game[l])) % 2 != 0:
                    self.server = not self.server
        elif self.game[w] == None:
            self.game[w], self.game[l] = 40, 40
        elif self.game[w] == 'AD':
            self.win_game(w, l)
        elif self.game[w] < 30:
            self.game[w] += 15
        elif self.game[w] == 30:
            self.game[w] += 10
        else:
            if self.game[l] == self.game[w]:
                self.game[w], self.game[l] = 'AD', None
            else:
                self.win_game(w, l)

    def win_game(self, w, l):
        self.game = [0, 0]
        if not len(self.sets):
            self.sets.append([0, 0])
        n = len(self.sets) - 1
        if self.sets[n][w] == '':
            self.sets[n] = [0, 0]
        self.sets[n][w] += 1
        if self.sets[n][l] == 6 and self.sets[n][w] == 6:
            self.game = ['', '']
        elif self.sets[n][w] == 7 or (self.sets[n][w] == 6 and self.sets[n][l] < 5):
            self.sets.append(['', ''])
            self.set_w[w] += 1
        self.server = not self.server

    def message_check(self):
        n = len(self.sets) - 1
        if type(self.game[0]) == type(self.game[1]) and type(self.game[0]) == type(''):
            if self.game[0] == '':
                return 'Tiebreak'
            if (int(self.game[0]) >= 6 and int(self.game[0]) - int(self.game[1]) >= 1):
                return 'Match Point' if self.set_w[0] > (self.best-1)/2 - 1 else 'Set Point'
            if (int(self.game[1]) >= 6 and int(self.game[1]) - int(self.game[0]) >= 1):
                return 'Match Point' if self.set_w[1] > (self.best-1)/2 - 1 else 'Set Point'
            else:
                return 'Tiebreak'
        if n >= 0 and self.sets[n][0] != '':
            if (self.game[0] == 40 and self.game[1] != 40 and self.sets[n][0]-self.sets[n][1] >= 1 and self.sets[n][0] >= 5):
                return 'Match Point' if self.set_w[0] > (self.best-1)/2 - 1 else 'Set Point'
            if (self.game[1] == 40 and self.game[0] != 40 and self.sets[n][1] - self.sets[n][0] >= 1 and self.sets[n][1] >= 5):
                return 'Match Point' if self.set_w[1] > (self.best-1)/2 - 1 else 'Set Point'
            if (self.game[0] == 'AD' and self.sets[n][0]-self.sets[n][1] >= 1 and self.sets[n][0] >= 5):
                return 'Match Point' if self.set_w[0] > (self.best-1)/2 - 1 else 'Set Point'
            if (self.game[1] == 'AD' and self.game[0] != 40 and self.sets[n][1] - self.sets[n][0] >= 1 and self.sets[n][1] >= 5):
                return 'Match Point' if self.set_w[1] > (self.best - 1) / 2 - 1 else 'Set Point'
        if (self.game[0] == 40 and self.game[1] != 40 and not self.server) or (self.game[1] == 40 and self.game[0] != 40 and self.server):
            return 'Break Point'
        if (self.game[0] == 'AD' and not self.server) or (self.game[1] == 'AD' and self.server):
            return 'Break Point'
        return ''
    
    def winner(self):
        return self.p1 if self.set_w[0] >= (self.best + 1)//2 else self.p2 if self.set_w[1] >= (self.best + 1)//2 else None


class Start(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(WINDOW_GEO)
        self.title("Tennis")
        self.attributes('-topmost', 1)

        p1, p2, best = tk.StringVar(), tk.StringVar(), tk.StringVar()

        name_label = tk.Label(self, text="Enter Player Names", bg=SECONDARY_COLOUR, **LABEL_FONT)
        name_label.place(**NAMES_LABEL)
        p1_entry = tk.Entry(self, textvariable=p1, **LABEL_FONT, bg=TERTIARY_COLOUR)
        p2_entry = tk.Entry(self, textvariable=p2, **LABEL_FONT, bg=TERTIARY_COLOUR)
        p1_entry.insert(tk.INSERT, 'Player 1')
        p2_entry.insert(tk.INSERT, 'Player 2')
        p1_entry.place(**PLAYER_ENTRY_1)
        p2_entry.place(**PLAYER_ENTRY_2)

        bestof_label = tk.Label(self, text="Enter Best Of", bg=SECONDARY_COLOUR, **LABEL_FONT)
        bestof_label.place(**BEST_OF_LABEL)
        best_of_entry = tk.Entry(self, textvariable=best, justify=tk.CENTER, bg=TERTIARY_COLOUR, **LABEL_FONT, **WIDTH_SMALL)
        best_of_entry.insert(tk.INSERT, '3')
        best_of_entry.place(**BEST_OF_ENTRY)

        go_button = ttk.Button(self, text="Go", style='GO.TButton', command=lambda: self.start_game(p1.get(), p2.get(), int(best.get())))
        go_button.place(**GO_BUTTON)

        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('GO.TButton', background=TERTIARY_COLOUR, **LABEL_FONT)
        style.map('GO.TButton', background=[("active", TERTIARY_COLOUR)])

    def start_game(self, p1, p2, best):
        self.destroy()
        new_app = MainApp(p1, p2, best)
        new_app.mainloop()


class MainApp(tk.Tk):
    def __init__(self, p1, p2, best):
        super().__init__()
        self.geometry(WINDOW_GEO)
        self.title("Tennis")
        self.attributes('-topmost', 1)

        score = Score(p1, p2, best)
        w = max(max(len(score.p1), len(score.p2)), DEF_PLAYER_NAME_WIDTH)
        l_att = {'bg':PRIMARY_COLOUR, 'width':w}
        p1_label = tk.Label(self, text=p1, **l_att, **LABEL_FONT, **MAIN_RELIEF)
        p2_label = tk.Label(self, text=p2, **l_att, **LABEL_FONT, **MAIN_RELIEF)
        p1_label.place(**P1_LABEL)
        p2_label.place(**P2_LABEL)

        for x in range(best + 1):
            for y in range(2):
                box = tk.Label(self, **WIDTH_SMALL, **LABEL_FONT)
                box.place(x=BOX_START_X + w * BOX_W_DX + x * BOX_DX, y=BOX_START_Y + y * BOX_DY)

        message = tk.Label(self, **WIDTH_DEFAULT, **LABEL_FONT)
        message.place(**MESSAGE)

        p1_b = ttk.Button(self, text='>', style='W.TButton', command=lambda: self.update_score(score, 0, 1), **WIDTH_XSMALL)
        p2_b = ttk.Button(self, style='W.TButton', command=lambda: self.update_score(score, 1, 0), **WIDTH_XSMALL)
        p1_b.place(**P1_BUTTON)
        p2_b.place(**P2_BUTTON)

        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('W.TButton', background=PRIMARY_COLOUR)
        style.map('W.TButton', background=[("active", PRIMARY_COLOUR)])
        
    def update_score(self, score, w, l):
        all_w = self.winfo_children()
        score.point(w, l)
        
        # update server
        server = score.server
        all_w[-1 - int(server)].configure(text='>')
        all_w[-2 + int(server)].configure(text='')

        # update sets
        sets = score.sets
        n = 2
        for i in range(len(sets)):
            for p in range(len(sets[i])):
                t = sets[i][p] if sets[i][p] != '' else ''
                b = SECONDARY_COLOUR if sets[i][p] != '' else DEFAULT_COLOUR
                all_w[n].configure(text=t, bg=b)
                n += 1
        n -= 2 if len(sets) and sets[-1][0] == '' else 0

        game = score.game
        for g in range(len(game)):
            t = game[g] if game[g] != None and (game[0] or game[1]) else ''
            b = SECONDARY_COLOUR if game[0] or game[1] else DEFAULT_COLOUR
            all_w[n].configure(text=t, bg=b)
            n += 1

        message = score.message_check()
        if message:
            all_w[-3].configure(text=message, **MAIN_RELIEF, bg=SECONDARY_COLOUR)
        else:
            all_w[-3].configure(text='', **DEFAULT_RELIEF, bg=DEFAULT_COLOUR)

        winner = score.winner()
        if winner:
            for x in (-1, -2):
                all_w[x].configure(command='')
                win_text = tk.Label(text=f'{winner} wins!', bg=TERTIARY_COLOUR, **MAIN_RELIEF, **LABEL_FONT)
                res_text = tk.Label(text='Restart?', **LABEL_FONT)
                yes = ttk.Button(text="Yes", style='X.TButton', command=self.restart, **WIDTH_SMALL)
                no = ttk.Button(text="No", style='X.TButton', command=self.destroy, **WIDTH_SMALL)
                win_text.place(**WIN_TEXT)
                res_text.place(**RESTART_TEXT)
                yes.place(**YES_BUTTON)
                no.place(**NO_BUTTON)
                style = ttk.Style(self)
                style.theme_use('alt')
                style.configure('X.TButton', background=TERTIARY_COLOUR, **LABEL_FONT)
                style.map('X.TButton', background=[("active", TERTIARY_COLOUR)])
        
    def restart(self):
        self.destroy()
        app = Start()
        app.mainloop()


app = Start()
app.mainloop()
