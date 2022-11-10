# GUI for keeping track of basketball stats during a game. INCOMPLETE
# Date: 10-11-2022
# Author: Samir Gupta

# type: ignore

import os
import tkinter as tk
from collections import deque
from tkinter import ttk

os.environ['TK_SILENCE_DEPRECATION'] = '1'

DEFAULT_COLOUR = 'gray19'
PRIMARY_COLOUR = 'SeaGreen'
SECONDARY_COLOUR = 'IndianRed'
PRIMARY_TEXT_COLOUR = 'white'
SECONDARY_TEXT_COLOUR = 'gray42'
PRIMARY_LABEL_COLOURS = {'fg': PRIMARY_TEXT_COLOUR, 'bg': DEFAULT_COLOUR}
SECONDARY_LABEL_COLOURS = {'fg': SECONDARY_TEXT_COLOUR, 'bg': DEFAULT_COLOUR}
TEAM1_LABEL_COLOURS = {'fg': PRIMARY_TEXT_COLOUR, 'bg': PRIMARY_COLOUR}
TEAM2_LABEL_COLOURS = {'fg': PRIMARY_TEXT_COLOUR, 'bg': SECONDARY_COLOUR}
PADDING_NORMAL = {'padx': 10, 'pady': 10}
PADDING_SMALL = {'padx': 2, 'pady': 5}
FONT_TITLE = {'font': ('calibri', 30)}
FONT_SUBTITLE = {'font': ('calibri', 25)}
FONT_REG_TEXT = {'font': ('calibri', 15)}
FONT_SMALL = {'font': ('calibri', 8)}

TOTAL_PLAYERS = 10

START_PAGE_GEO = '800x800+320+20'
MAIN_GEO = '360x900+0+20'
ACTION_GEO = '360x900+360+20'
TEAM_GEO = '360x900+720+20'
LINEUP_GEO = '360x600+1080+20'
INDIVIDUAL_GEO = '360x600+540+20'


class Player:
    def __init__(self, name):
        
        self.name = name
        self.twos_m = self.twos_a = self.threes_m = self.threes_a = 0
        self.frees_m = self.frees_a = self.points = 0
        self.off_reb = self.def_reb = self.rebounds = self.assists = 0
        self.turnovers = self.steals = self.blocks = self.fouls = 0
        self.shot_summary = []
        self.threes_pct = self.twos_pct = self.frees_pct = 0
        self.total_shots_m = self.total_shots_a = self.total_pct = 0
        self.minutes = 0

    def __repr__(self):
        det_sum = f'{self.name}'
        score_sum = f'{self.points} PTS - {self.total_shots_m}/{self.total_shots_a} FG, {self.threes_m}/{self.threes_a} 3PT, {self.frees_m}/{self.frees_a} FT'
        reb_sum = f'{self.rebounds} REB ({self.off_reb} OFF, {self.def_reb} DEF)'
        ast_sum = f'{self.assists} AST, {self.turnovers} TO'
        def_sum = f'{self.steals} STL, {self.blocks} BLK, {self.fouls} FLS'
        mins = f'{self.minutes} MINS'
        return f'{det_sum}\n{score_sum}\n{reb_sum}\n{ast_sum}\n{def_sum}\n{mins}'

    def shot(self, shot_type, make):  # , xy):
        if shot_type == '2':
            self.twos_a += 1
            self.total_shots_a += 1
            if make:
                self.twos_m += 1
                self.points += 2
                self.total_shots_m += 1
            self.twos_pct = round(self.twos_m/self.twos_a, 3)

        elif shot_type == '3':
            self.threes_a += 1
            self.total_shots_a += 1
            if make:
                self.threes_m += 1
                self.points += 3
                self.total_shots_m += 1
            self.threes_pct = round(self.threes_m/self.threes_a, 3)
        else:
            self.frees_a += 1
            if make:
                self.frees_m += 1
                self.points += 1
            self.frees_pct = round(self.frees_m/self.frees_a, 3)
        
        self.total_pct = round(self.total_shots_m/self.total_shots_a, 3) if self.total_shots_a != 0 else 0.0
        self.shot_summary.append({'type': shot_type, 'make': make})  # , 'x': xy[0], 'y': xy[1]})

    def rebound(self, types):
        if types == 'offensive':
            self.off_reb += 1
        else:
            self.def_reb += 1
        self.rebounds += 1

    def assist(self):
        self.assists += 1

    def steal(self):
        self.steals += 1

    def block(self):
        self.blocks += 1

    def turnover(self):
        self.turnovers += 1

    def foul(self):
        self.fouls += 1


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.stats = Player(self.name)

    def __repr__(self):
        return f'{self.name} - {[self.players[i].name for i in range(len(self.players))]}\n{self.stats}'


class Start(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(START_PAGE_GEO)
        self.title('Start Page')
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        title = tk.Label(self, text='Basketball Simulation',
                         **PRIMARY_LABEL_COLOURS, **FONT_TITLE)
        title.grid(column=0, row=0, columnspan=2, **PADDING_NORMAL)

        self.team1_en = tk.Entry(justify=tk.CENTER, **
                                 TEAM1_LABEL_COLOURS, **FONT_SUBTITLE)
        self.team2_en = tk.Entry(justify=tk.CENTER, **
                                 TEAM2_LABEL_COLOURS, **FONT_SUBTITLE)
        self.team1_en.insert(tk.INSERT, 'OKC')
        self.team2_en.insert(tk.INSERT, 'SAS')
        self.team1_en.grid(column=0, row=1, **PADDING_NORMAL)
        self.team2_en.grid(column=1, row=1, **PADDING_NORMAL)

        players_title = tk.Label(
            self, text='Enter Player Names', **PRIMARY_LABEL_COLOURS, **FONT_SUBTITLE)
        players_title.grid(column=0, row=2, columnspan=2, **PADDING_NORMAL)

        names1 = ['Josh Giddey', 'Darius Bazley', 'Tre Mann', 'Aleksej Pokusevski',
                  'Aaron Wiggins', 'Theo Maledon', 'Isaiah Roby', 'Derrick Favours', 'Vit Krejci', 'Lindy Waters-III']
        names2 = ['Keldon Johnson', 'Dejounte Murray', 'Devin Vassell', 'Jakob Poeltl', 'Lonnie Walker-IV',
                  'Doug McDermott', 'Zach Collins', 'Josh Richardson', 'Joshua Primo', 'Keita Bates-Diop']

        row = 3
        for i in range(TOTAL_PLAYERS):
            exec(
                f'self.name_entry{i}_0 = tk.Entry(self, justify=tk.LEFT, **TEAM1_LABEL_COLOURS, **FONT_REG_TEXT)')
            exec(
                f'self.name_entry{i}_0.grid(column=0, row=row, sticky=tk.W, **PADDING_NORMAL)')
            exec(f'self.name_entry{i}_0.insert(tk.INSERT, "{names1[i]}")')
            exec(
                f'self.name_entry{i}_1 = tk.Entry(self, justify=tk.RIGHT, **TEAM2_LABEL_COLOURS, **FONT_REG_TEXT)')
            exec(
                f'self.name_entry{i}_1.grid(column=1, row=row, sticky=tk.E, **PADDING_NORMAL)')
            exec(f'self.name_entry{i}_1.insert(tk.INSERT, "{names2[i]}")')
            row += 1

        go_button = ttk.Button(self, text='GO', command=self.go)
        go_button.grid(column=0, row=row, columnspan=2, **PADDING_NORMAL)

        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('TButton', background=PRIMARY_COLOUR,
                        foreground=PRIMARY_TEXT_COLOUR, **FONT_TITLE)
        style.map('TButton', background=[("active", SECONDARY_COLOUR)])

    def go(self):
        teams = []
        for i in range(2):
            team = []
            for t in range(TOTAL_PLAYERS):
                name = eval(f'self.name_entry{t}_{i}.get()')
                if name:
                    team.append(Player(name))
            exec(f'teams.append(Team(self.team{i+1}_en.get(), team))')

        self.destroy()
        app = Main(teams)
        app.mainloop()


class Main(tk.Tk):
    def __init__(self, teams):
        super().__init__()
        self.geometry(MAIN_GEO)
        self.title('MAIN')
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        self.action = Action(teams)
        self.summary = Summary(teams)
        self.lineup = Lineup(teams)

        self.TEAMS = teams

        for c in range(4):
            self.columnconfigure(c, weight=1)

        self.poss_label = tk.Label(text='Possession', **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.poss_button_t1 = ttk.Button(text=teams[0].name, command=lambda: self.poss(0))
        self.poss_button_t2 = ttk.Button(text=teams[1].name, command=lambda: self.poss(1))
        self.poss_label.grid(column=0, row=0, columnspan=4, **PADDING_SMALL)
        self.poss_button_t1.grid(column=0, row=1, columnspan=2, **PADDING_SMALL)
        self.poss_button_t2.grid(column=2, row=1, columnspan=2, **PADDING_SMALL)

        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('TButton', background=SECONDARY_TEXT_COLOUR, foreground=PRIMARY_TEXT_COLOUR, **FONT_SMALL)
        style.map('TButton', background=[("active", SECONDARY_TEXT_COLOUR)])
        style.configure('W.TButton', background=DEFAULT_COLOUR, foreground=PRIMARY_TEXT_COLOUR, **FONT_SMALL)
        style.map('W.TButton', background=[("active", DEFAULT_COLOUR)])

    def find_team(self, player):
        for team in self.TEAMS:
            for p in team.players:
                if p.name == player.name:
                    return team

    def poss(self, t_w):
        self.FIRST_TEAM = t_w

        self.poss_button_t1.destroy()
        self.poss_button_t2.destroy()
        self.poss_label.configure(
            text=f'Choose Player ({self.TEAMS[self.FIRST_TEAM].name})')

        self.r, self.c = 1, 0
        for p in self.TEAMS[t_w].players:
            name = p.name.split(' ')[0]
            exec(f'self.p_{name}_b = ttk.Button(text=name, command=lambda self=self, p=p: self.player_select1(p))')
            exec(f'self.p_{name}_b.grid(column=self.c, row=self.r, **PADDING_SMALL)')
            self.r = self.r if self.c != 3 else self.r + 1
            self.c = self.c + 1 if self.c != 3 else 0
        self.r_1, self.c_1 = self.r, self.c

    def player_select1(self, player):
        self.FIRST_PLAYER = player

        for p in self.TEAMS[self.FIRST_TEAM].players:
            name = p.name.split(' ')[0]
            if p.name == player.name:
                exec(f'self.p_{name}_b.configure(style="W.TButton")')
            else:
                exec(f'self.p_{name}_b.configure(style="TButton")')

        self.things = ['miss1', 'miss2', 'miss3', 'turnover', 'make1', 'make2', 'make3', 'foul']

        self.r, self.c = self.r_1, self.c_1
        self.r += 1 if self.c != 0 else 0
        self.action_label = tk.Label(text='Enter Action', **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.action_label.grid(column=0, row=self.r, columnspan=4, **PADDING_SMALL)
        self.r += 1
        self.c = 0

        for t in self.things:
            exec(f'self.{t}_b = ttk.Button(text=t, command=lambda self=self,t=t: self.action_select(t))')
            exec(f'self.{t}_b.grid(column=self.c, row=self.r, **PADDING_SMALL)')
            self.r = self.r if self.c != 3 else self.r + 1
            self.c = self.c + 1 if self.c != 3 else 0
        self.r_2, self.c_2 = self.r, self.c

    def action_select(self, action):
        self.ACTION = action

        for t in self.things:
            if t == action:
                exec(f'self.{t}_b.configure(style="W.TButton")')
            else:
                exec(f'self.{t}_b.configure(style="TButton")')

        label = ''
        if action == 'turnover':
            label = 'Stealer'
            self.FIRST_TEAM = int(not self.FIRST_TEAM)
        elif action[:4] == 'miss':
            label = 'Blocker'
            self.FIRST_TEAM = int(not self.FIRST_TEAM)
        elif action[:4] == 'make':
            label = 'Assist'
        elif action == 'foul':
            label = 'Fouler'
            self.FIRST_TEAM = int(not self.FIRST_TEAM)

        label += f' ({self.TEAMS[self.FIRST_TEAM].name})'

        self.r, self.c = self.r_2, self.c_2
        self.r += 1 if self.c != 0 else 0
        self.secondary_label = tk.Label(text=label, width=20, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.secondary_label.grid(column=0, row=self.r, columnspan=4, **PADDING_SMALL)
        self.r += 1
        self.c = 0

        for p in self.TEAMS[self.FIRST_TEAM].players + ['none']:
            name = 'none' if p == 'none' else p.name.split(' ')[0]
            exec(
                f'self.p2_{name}_b = ttk.Button(text=name, command=lambda self=self, p=p: self.player_select2(p))')
            exec(
                f'self.p2_{name}_b.grid(column=self.c, row=self.r, **PADDING_SMALL)')
            self.r = self.r if self.c != 3 else self.r + 1
            self.c = self.c + 1 if self.c != 3 else 0
        self.r_3, self.c_3 = self.r, self.c

    def player_select2(self, p):
        self.SECOND_PLAYER = p

        for p in self.TEAMS[self.FIRST_TEAM].players + ['none']:
            name = 'none' if p == 'none' else p.name.split(' ')[0]
            if p == self.SECOND_PLAYER:
                exec(f'self.p2_{name}_b.configure(style="W.TButton")')
            else:
                exec(f'self.p2_{name}_b.configure(style="TButton")')

        if self.ACTION[:4] != 'miss':
            self.add_play(0)
            return

        self.r, self.c = self.r_3, self.c_3
        self.r += 1 if self.c != 0 else 0
        self.secondary_label = tk.Label(
            text='Rebounder', width=20, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.secondary_label.grid(
            column=0, row=self.r, columnspan=4, **PADDING_SMALL)
        self.r += 1
        self.c = 0

        for p in self.TEAMS[self.FIRST_TEAM].players + self.TEAMS[int(not self.FIRST_TEAM)].players + [self.TEAMS[0].name, self.TEAMS[1].name]:
            name = p if type(p) == type('') else p.name.split(' ')[0]
            exec(
                f'self.p3_{name}_b = ttk.Button(text=name, command=lambda self=self, p=p: self.final_step(p))')
            exec(
                f'self.p3_{name}_b.grid(column=self.c, row=self.r, **PADDING_SMALL)')
            self.r = self.r if self.c != 3 else self.r + 1
            self.c = self.c + 1 if self.c != 3 else 0

    def final_step(self, p):
        self.THIRD_PLAYER = p
        for p in self.TEAMS[self.FIRST_TEAM].players + self.TEAMS[int(not self.FIRST_TEAM)].players + [self.TEAMS[0].name, self.TEAMS[1].name]:
            name = p if type(p) == type('') else p.name.split(' ')[0]
            if p == self.THIRD_PLAYER:
                exec(f'self.p3_{name}_b.configure(style="W.TButton")')
            else:
                exec(f'self.p3_{name}_b.configure(style="TButton")')

        self.add_play(1)

    def add_play(self, n):
        text = ''
        one, two = self.FIRST_PLAYER, self.SECOND_PLAYER
        one_t = self.find_team(one)
        two_t = self.find_team(two) if type(two) != type('') else two
        if not n:
            if self.ACTION[:4] == 'make':
                shot = self.ACTION[4:]
                text += f'{one.name} ({one_t.name}) makes a {shot} point shot'
                one.shot(shot, True)
                one_t.stats.shot(shot, True)
                if two != 'none':
                    text += f', {two.name} ({two_t.name}) with the assist.'
                    two.assist()
                    two_t.stats.assist()
                else:
                    text += '.'
            elif self.ACTION == 'turnover':
                if two != 'none':
                    text += f'{two.name} ({two_t.name}) steals the ball from {one.name} ({one_t.name}).'
                    two.steal()
                    two_t.stats.steal()
                else:
                    text += f'{one.name} ({one_t.name}) turns it over.'
                one.turnover()
                one_t.stats.turnover()
            elif self.ACTION == 'foul':
                text += f'{two.name} ({two_t.name}) fouls {one.name} ({one_t.name}).'
                two.foul()
                two_t.stats.foul()
        else:
            shot = self.ACTION[4:]
            three = self.THIRD_PLAYER
            three_t = self.find_team(three) if type(three) != type('') else three
            reb_type = ''
            one.shot(shot, False)
            one_t.stats.shot(shot, False)
            if type(two) != type(''):
                third = f'{three.name} ({three_t.name})' if type(three) != type('') else f'{three}'
                reb_type = 'a defensive' if two_t == three_t else 'an offensive'
                text += f'{two.name} ({two_t.name}) blocks a {one.name} ({one_t.name}) {shot} pointer, {third} with a {reb_type} rebound.'
                two.block()
                two_t.stats.block()
            elif type(three) != type(''):
                reb_type = 'an offensive' if one_t == three_t else 'a defensive'
                text += f'{one.name} ({one_t.name}) misses a {shot} pointer, {three.name} ({three_t.name}) with {reb_type} rebound.'
            else:
                reb_type = 'an offensive' if one_t.name == three else 'a defensive'
                text += f'{one.name} ({one_t.name}) misses a {shot} pointer, {three} with {reb_type} rebound.'

            if type(three) != type(''):
                three.rebound(reb_type.split(' ')[1])
                three_t.stats.rebound(reb_type.split(' ')[1])

        self.action.print_action(text, self.ACTION)
        self.summary.show_stats()
        self.lineup.show_stats()
        self.restart()

    def restart(self):
        for w in self.winfo_children():
            w.destroy()

        self.poss_label = tk.Label(
            text='Possession', **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.poss_button_t1 = ttk.Button(
            text=self.TEAMS[0].name, command=lambda: self.poss(0))
        self.poss_button_t2 = ttk.Button(
            text=self.TEAMS[1].name, command=lambda: self.poss(1))
        self.poss_label.grid(column=0, row=0, columnspan=4, **PADDING_SMALL)
        self.poss_button_t1.grid(
            column=0, row=1, columnspan=2, **PADDING_SMALL)
        self.poss_button_t2.grid(
            column=2, row=1, columnspan=2, **PADDING_SMALL)


class Action(tk.Tk):
    def __init__(self, teams):
        super().__init__()
        self.geometry(ACTION_GEO)
        self.title('ACTION')
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        for c in range(8):
            self.columnconfigure(c, weight=1)

        self.TEAMS = teams

        self.team1_l = tk.Label(self, text=teams[0].name, **TEAM1_LABEL_COLOURS, **FONT_REG_TEXT)
        self.team2_l = tk.Label(self, text=teams[1].name, **TEAM2_LABEL_COLOURS, **FONT_REG_TEXT)
        self.score_l = tk.Label(self, text='0 - 0', **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.team1_l.grid(column=1, row=0, sticky=tk.E, columnspan=2, **PADDING_SMALL)
        self.score_l.grid(column=3, row=0, columnspan=2, **PADDING_SMALL)
        self.team2_l.grid(column=5, row=0, sticky=tk.W, columnspan=2, **PADDING_SMALL)

        self.existing = deque([])

    def print_action(self, text, action):
        make, colours = '-', PRIMARY_LABEL_COLOURS
        if action[:4] == 'make':
            make = action[4:]
            name = f'{text.split(" ")[0]} {text.split(" ")[1]}'
            i = 0
            for t in range(len(self.TEAMS)):
                for p in self.TEAMS[t].players:
                    if name == p.name:
                        i = t
                        break
            colours = TEAM2_LABEL_COLOURS if i else TEAM1_LABEL_COLOURS

            updated_score = ' - '.join([str(self.TEAMS[0].stats.points), str(self.TEAMS[1].stats.points)])
            self.score_l.configure(text=updated_score)

        time = 'Q1-11:30'
        mess = int(len(time)-2) * ' ' + f'{make}\n{time}'
        self.make_symbol = tk.Message(self, text=mess, **FONT_SMALL, **colours)
        self.new_label = tk.Message(self, text=text, width=270, **PRIMARY_LABEL_COLOURS, **FONT_SMALL)
        self.existing.appendleft([self.make_symbol, self.new_label])
        
        for i in range(len(self.existing)):
            self.existing[i][0].grid(column=0, row=i+1, columnspan=2, padx=2, pady=2)
            self.existing[i][1].grid(column=2, row=i+1, columnspan=6, sticky=tk.W, **PADDING_SMALL)


class Summary(tk.Tk):
    def __init__(self, teams):
        super().__init__()
        self.geometry(TEAM_GEO)
        self.title('TEAMS')
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.TEAMS = teams

        self.team1_l = tk.Label(self, text=teams[0].name, **TEAM1_LABEL_COLOURS, **FONT_REG_TEXT)
        self.team2_l = tk.Label(self, text=teams[1].name, **TEAM2_LABEL_COLOURS, **FONT_REG_TEXT)
        self.team1_l.grid(column=0, row=0, columnspan=2, **PADDING_SMALL)
        self.team2_l.grid(column=2, row=0, columnspan=2, **PADDING_SMALL)

        self.score0 = tk.Label(self, text='0', **PRIMARY_LABEL_COLOURS, **FONT_SUBTITLE)
        self.score1 = tk.Label(self, text='0', **PRIMARY_LABEL_COLOURS, **FONT_SUBTITLE)
        self.score0.grid(column=0, row=1, columnspan=2, **PADDING_NORMAL)
        self.score1.grid(column=2, row=1, columnspan=2, **PADDING_NORMAL)

        score_types = ['2-Point', '3-Point', 'Field Goals', 'Free Throws']
        score_labels = ['two', 'three', 'total', 'free']
        for t in range(2):
            for x in range(len(score_types)):
                x_ = x
                if x == 2:
                    continue
                if x == 3:
                    x_ = x-1
                setattr(self, f'{score_labels[x]}{t}_l', tk.Label(self, text=score_types[x], **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                setattr(self, f'{score_labels[x]}_n{t}', tk.Label(self, text='0', **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                self.__getattribute__(f'{score_labels[x]}{t}_l').grid(column=0+t*2, row=2+x_, sticky=tk.W, padx=20, pady=2)
                self.__getattribute__(f'{score_labels[x]}_n{t}').grid(column=1+t*2, row=2+x_, stick=tk.E, padx=20, pady=2)

        for x in range(len(score_types)):
            setattr(self, f'{score_labels[x]}_label', tk.Label(self, text=score_types[x], **SECONDARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(f'{score_labels[x]}_label').grid(column=0, row=5+3*x, columnspan=4, **PADDING_SMALL)
            for t in range(2):
                setattr(self, f'{score_labels[x]}_pct{t}', tk.Label(self, text=".000", **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT))
                setattr(self, f'{score_labels[x]}_fg{t}', tk.Label(self, text="0 of 0", **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                self.__getattribute__(f'{score_labels[x]}_pct{t}').grid(column=0+2*t, row=6+3*x, columnspan=2, **PADDING_SMALL)
                self.__getattribute__(f'{score_labels[x]}_fg{t}').grid(column=0+2*t, row=7+3*x, columnspan=2, **PADDING_SMALL)

        self.rebound_label = tk.Label(self, text='Rebounds', **SECONDARY_LABEL_COLOURS, **FONT_SMALL)
        self.rebound_label.grid(column=0, row=17, columnspan=4, **PADDING_SMALL)
        rebs = ['Offensive', 'Defensive']
        for x in range(2):
            setattr(self, f'reb_n{x}', tk.Label(self, text="0", **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT))
            self.__getattribute__(f'reb_n{x}').grid(column=0+2*x, row=18, columnspan=2, **PADDING_SMALL)
            for r in range(2):
                setattr(self, f'{rebs[r]}_l{x}', tk.Label(self, text=rebs[r], **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                setattr(self, f'{rebs[r]}_n{x}', tk.Label(self, text="0", **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                self.__getattribute__(f'{rebs[r]}_l{x}').grid(column=0+x*2, row=19+r, padx=20, pady=2, sticky=tk.W)
                self.__getattribute__(f'{rebs[r]}_n{x}').grid(column=1+x*2, row=19+r, padx=20, pady=2, sticky=tk.E)

        others, stick = ['Assists', 'Blocks', 'Fouls', 'Steals', 'Turnovers'], [tk.W, tk.E]
        for x in range(len(others)):
            setattr(self, f'{others[x]}_label', tk.Label(self, text=others[x], **SECONDARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(f'{others[x]}_label').grid(column=0, row=21+2*x, columnspan=4, **PADDING_SMALL)
            for t in range(2):
                setattr(self, f'{others[x]}_n{t}', tk.Label(self, text="0", **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                self.__getattribute__(f'{others[x]}_n{t}').grid(column=0+2*t, row=22+2*x, columnspan=2, sticky=stick[t], padx=40, pady=2) 


    def show_stats(self):
        atts = [
            'points', 
            'twos_m', 'threes_m', 'frees_m',
            'twos_pct', 'threes_pct', 'frees_pct', 'total_pct',
            'twos_m', 'twos_a', 'threes_m', 'threes_a', 'total_shots_m', 'total_shots_a', 'frees_m', 'frees_a',
            'rebounds',
            'off_reb', 'def_reb',
            'assists', 'blocks', 'fouls', 'steals', 'turnovers'
            ]
        names = [
            'score',
            'two_n', 'three_n', 'free_n',
            'two_pct', 'three_pct', 'free_pct', 'total_pct',
            'two_fg', '', 'three_fg', '', 'total_fg', '', 'free_fg', '', 
            'reb_n',
            'Offensive_n', 'Defensive_n',
            'Assists_n', 'Blocks_n', 'Fouls_n', 'Steals_n', 'Turnovers_n'
        ]
        for x in range(len(atts)):
            for t in range(2):
                att = self.TEAMS[t].stats.__getattribute__(atts[x])
                text = ''
                if x in (1, 2, 3):
                    n = 2 if x == 1 else 3 if x == 2 else 1
                    text += f'{n*att}'
                elif x in (4, 5, 6, 7):
                    if int(att) == 1:
                        text += '1.000'
                    else:
                        text += f'.{str(att)[2:]}' + '0' * (3 - len(str(att)[2:]))
                elif x in (8, 10, 12, 14):
                    att_2 = self.TEAMS[t].stats.__getattribute__(atts[x+1])
                    text += f'{att} of {att_2}'
                elif x in (9, 11, 13, 15):
                    continue
                else:
                    text += str(att)
                
                
                self.__getattribute__(names[x]+str(t)).configure(text=text)


class Lineup(tk.Tk):
    def __init__(self, teams):
        super().__init__()
        self.geometry(LINEUP_GEO)
        self.title('LINEUPS')
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        self.TEAMS = teams

        self.columnconfigure(0, weight=2)
        for c in range(6):
            self.columnconfigure(c+1, weight=1)

        self.main_label = tk.Label(self, text="Players", **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.main_label.grid(column=0, row=0, columnspan=7, **PADDING_NORMAL)

        self.sorter = 'points'
        self.rev = True


    def show_stats(self):
        headings = ['NAME', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG']
        p_att = ['name', 'points', 'rebounds', 'assists', 'steals', 'blocks', 'total_pct']
        all_p = self.TEAMS[0].players + self.TEAMS[1].players
        players = sorted(all_p, key=lambda p: p.__getattribute__(self.sorter), reverse=self.rev)
        for i in range(len(players)+1):
            for j in range(len(p_att)):
                w = 7 if j != 0 else 14
                anchor = tk.CENTER if j != 0 else tk.W
                cols = PRIMARY_LABEL_COLOURS
                if i == 0:
                    setattr(self, f'headings{j}', tk.Label(self, text=headings[j], width=w, relief='groove', **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
                    if j != 0:
                        self.__getattribute__(f'headings{j}').bind('<Button-1>', lambda e, j=j: self.change_sort(p_att[j]))
                    self.__getattribute__(f'headings{j}').grid(column=j, row=i+1, ipadx=3, ipady=3, pady=5)
                else:
                    att = players[i-1].__getattribute__(p_att[j])
                    if p_att[j] == 'total_pct':
                            att = '1.000' if int(att) == 1 else f'.{str(att)[2:]}' + '0' * (3 - len(str(att)[2:]))
                    elif p_att[j] == 'name':
                        att = ' ' + att
                        cols = TEAM1_LABEL_COLOURS if players[i-1] in self.TEAMS[0].players else TEAM2_LABEL_COLOURS
                    setattr(self, f'label{i}{j}', tk.Label(self, text=att, width=w, relief='groove', anchor=anchor, **cols, **FONT_SMALL))
                    self.__getattribute__(f'label{i}{j}').grid(column=j, row=i+2, ipadx=3, ipady=3)
                    if j == 0:
                        self.__getattribute__(f'label{i}{j}').bind('<Button-1>', lambda e, i=i: self.launch_individual(players[i-1]))
    
    def change_sort(self, change):
        
        if self.sorter == change:
            self.rev = not self.rev
        else:
            self.sorter = change
        self.show_stats()

    def launch_individual(self, player):
        try:
            self.ind.destroy()
        except:
            pass
        self.ind = Individual(player)
        self.ind.mainloop()

class Individual(tk.Tk):
    def __init__(self, player):
        super().__init__()
        self.geometry(INDIVIDUAL_GEO)
        self.title(player.name)
        self.configure(background=DEFAULT_COLOUR)
        self.attributes('-topmost', 1)

        for c in range(12):
            self.columnconfigure(c, weight=1)

        self.main_l = tk.Label(self, text='STATS', **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.points_l = tk.Label(self, text='POINTS', **SECONDARY_LABEL_COLOURS, **FONT_SMALL)
        self.rebs_l = tk.Label(self, text='REBOUNDS', **SECONDARY_LABEL_COLOURS, **FONT_SMALL)
        self.main_l.grid(column=0, row=0, columnspan=12, **PADDING_NORMAL)
        self.points_l.grid(column=0, row=1, columnspan=6, **PADDING_SMALL)
        self.rebs_l.grid(column=6, row=1, columnspan=6, **PADDING_SMALL)
        
        self.points_n = tk.Label(self, text=player.points, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.rebs_n = tk.Label(self, text=player.rebounds, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT)
        self.points_n.grid(column=0, row=2, columnspan=6, **PADDING_NORMAL)
        self.rebs_n.grid(column=6, row=2, columnspan=6, **PADDING_NORMAL)

        lst_l = ['2-Points', '3-Points', 'Free Throws', 'Offensive', 'Defensive', '']
        lst_a = ['twos_m', 'threes_m', 'frees_m', 'off_reb', 'def_reb', '']
        for x in range(len(lst_l)):
            setattr(self, lst_a[x] + '_l', tk.Label(self, text=lst_l[x], **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(lst_a[x] + '_l').grid(column=0+6*(x//3), row=3+x%3, sticky=tk.W, padx=10, pady=2, columnspan=3)

            n = player.__getattribute__(lst_a[x]) if lst_a[x] != '' else ''
            n *= 2 if lst_l[x] == '2-Points' else 3 if lst_l[x] == '3-Points' else 1
            setattr(self, lst_a[x] + '_n', tk.Label(self, text=n, **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(lst_a[x] + '_n').grid(column=3+6*(x//3), row=3+x%3, sticky=tk.E, padx=5, pady=2, columnspan=3)

        self.empty_row1 = tk.Label(self, **PRIMARY_LABEL_COLOURS)
        self.empty_row1.grid(column=0, row=7, columnspan=12)

        lst_l = ['Assists', 'Steals', 'Blocks', 'Minutes Played', 'Turnovers', 'Personal Fouls']
        lst_a = ['assists', 'steals', 'blocks', 'minutes', 'turnovers', 'fouls']
        for x in range(len(lst_l)):
            n = player.__getattribute__(lst_a[x])
            setattr(self, lst_a[x] + '_n', tk.Label(self, text=n, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT))
            self.__getattribute__(lst_a[x] + '_n').grid(column=0+4*(x%3), row=8+2*(x//3), columnspan=4, **PADDING_NORMAL)

            setattr(self, lst_a[x] + '_l', tk.Label(self, text=lst_l[x], **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(lst_a[x] + '_l').grid(column=0+4*(x%3), row=9+2*(x//3), columnspan=4, **PADDING_SMALL)

        self.empty_row2 = tk.Label(self, **PRIMARY_LABEL_COLOURS)
        self.empty_row2.grid(column=0, row=12, columnspan=12)

        lst_l = ['2-POINT SHOTS', '3-POINT SHOTS', 'FIELD GOALS', 'FREE THROWS']
        lst_pct = ['twos_pct', 'threes_pct', 'total_pct', 'frees_pct']
        lst_m = ['twos_m', 'threes_m', 'total_shots_m', 'frees_m']
        lst_a = ['twos_a', 'threes_a', 'total_shots_a', 'frees_a']
        for x in range(len(lst_l)):
            setattr(self, lst_a[x] + '_l', tk.Label(self, text=lst_l[x], **SECONDARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(lst_a[x] + '_l').grid(column=0+6*(x%2), row=13+3*(x//2), columnspan=6, **PADDING_SMALL)

            pct = player.__getattribute__(lst_pct[x])
            pct = '1.000' if int(pct) == 1 else f'.{str(pct)[2:]}' + '0' * (3 - len(str(pct)[2:]))
            setattr(self, lst_a[x] + '_l', tk.Label(self, text=pct, **PRIMARY_LABEL_COLOURS, **FONT_REG_TEXT))
            self.__getattribute__(lst_a[x] + '_l').grid(column=0+6*(x%2), row=14+3*(x//2), columnspan=6, **PADDING_SMALL)

            fg = f'{player.__getattribute__(lst_m[x])} of {player.__getattribute__(lst_a[x])}'
            setattr(self, lst_a[x] + '_l', tk.Label(self, text=fg, **PRIMARY_LABEL_COLOURS, **FONT_SMALL))
            self.__getattribute__(lst_a[x] + '_l').grid(column=0+6*(x%2), row=15+3*(x//2), columnspan=6, **PADDING_SMALL)

if __name__ == '__main__':
    app = Start()
    app.mainloop()
