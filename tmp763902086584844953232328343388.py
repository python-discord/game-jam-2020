import y

defend=y.load('d')
climb=y.load('c')
atari=y.load('a')
reactions=y.load('b')
scores=y.load('x')

from tkinter import Tk, Frame, Entry, Label
from tkinter.ttk import Button


class Arcade(Tk):
    def __init__(self):
        super().__init__()
        self.title('Arcade')

        self.menu = Frame(self)
        Button(self.menu, text='Defend', command=self.defend).pack()
        Button(self.menu, text='Climb', command=self.climb).pack()
        Button(self.menu, text='Atari', command=self.atari).pack()
        Button(self.menu, text='Reactions', command=self.reactions).pack()
        Button(self.menu, text='Leaderboard', command=self.lbs).pack()
        self.menu.pack()

        self.lbmenu = Frame(self)
        for game in ('defend', 'climb', 'atari', 'reactions'):
            Button(
                self.lbmenu, text=game.title(),
                command=lambda g=game: self.lb(g)
            ).pack()
        Button(
            self.lbmenu, text='Back', command=lambda: self.back(self.lbmenu)
        ).pack()

        self.gametype = None
        self.frame = None

    def defend(self):
        self.gametype = 'defend'
        self.play(defend)

    def climb(self):
        self.gametype = 'climb'
        self.play(climb)

    def atari(self):
        self.gametype = 'atari'
        self.play(atari)

    def reactions(self):
        self.gametype = 'reactions'
        self.play(reactions)

    def play(self, game):
        self.menu.pack_forget()
        self.frame = Frame(self)
        game.Game(self.frame).pack()
        Button(self.frame, text='Back', command=self.back).pack()
        self.frame.pack()

    def gameover(self, score):
        self.frame.destroy()
        self.frame = Frame(self)
        Label(self.frame, text='Name:').pack()
        entry = Entry(self.frame)
        entry.pack()
        Button(
            self.frame, text='Go!',
            command=lambda: self.score(entry, score)
        ).pack()
        self.frame.pack()

    def score(self, entry, score):
        name = entry.get()
        name = name.replace('\n', '')[:10]
        scores.add(self.gametype, name, score)
        self.back()

    def back(self, frame=None):
        if frame:
            frame.pack_forget()
        else:
            self.frame.destroy()
        self.menu.pack()

    def lbs(self):
        self.menu.pack_forget()
        self.lbmenu.pack()

    def lb(self, game):
        self.lbmenu.pack_forget()
        data = scores.get(game)
        self.frame = Frame(self)
        title = Label(self.frame, text=game.title())
        title.grid(row=0, column=0, columnspan=2)
        row = 1
        for score, name in data:
            Label(self.frame, text=name).grid(row=row, column=0, sticky='w')
            s = Label(self.frame, text=str(score))
            s.grid(row=row, column=1, sticky='e')
            row += 1
        b = Button(self.frame, text='Back', command=self.back)
        b.grid(row=row, column=0, columnspan=2)
        self.frame.pack()


Arcade().mainloop()
