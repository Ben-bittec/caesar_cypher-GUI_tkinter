#!/usr/bin/python

import tkinter as tk
import string


lower = list(string.ascii_lowercase)
upper = list(string.ascii_uppercase)
numb = list(string.digits)
pun = list(string.punctuation)
pun.append(" ")

symbols = [lower, upper, numb, pun]


class Gui:
    # master window and variables
    def __init__(self, master, sym):
        self.master = master
        # Center le screen
        screen_w, screen_h = master.winfo_screenwidth(), master.winfo_screenheight()
        w, h = 1000, 700
        pos_x, pos_y = (screen_w//2) - (w//2), (screen_h//2) - (h//2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, pos_x, pos_y))
        self.master.title("Caesar Cypher Encrypt/Decrypt")
        self.symbols = sym

        self.orgtext = ""
        self.enctext = ""
        self.shift = tk.IntVar()
        self.abc_frames = []
        self.sabc_frames = []
        self.checkvar = tk.IntVar(value=1)
        # Frames
        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(fill=tk.BOTH, side=tk.TOP)
        self.frame_but = tk.Frame(self.master)
        self.frame_org = tk.LabelFrame(self.master, text="Original message", bg="grey")
        self.frame_sol = tk.LabelFrame(self.master, text="Crypted message", bg="red")
        self.frame_abc = tk.LabelFrame(self.frame_top, text="Alphabet")

        self.frame_top.pack(side=tk.TOP)
        self.frame_org.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH, padx=50, pady=40)
        self.frame_but.pack(side=tk.LEFT)
        self.frame_sol.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.BOTH, padx=50, pady=40)
        self.frame_abc.pack(side=tk.BOTTOM, expand=tk.TRUE)
        self.make_alphabet()

        # shift scale
        self.scale_frame = tk.LabelFrame(self.frame_but, text="Set shift Level", bg="grey")
        self.scale = tk.Scale(
            self.scale_frame,
            orient=tk.HORIZONTAL,
            length=152,
            from_=0,
            to_=25,
            variable=self.shift,
            command=lambda x: self.encode()
        )
        self.scale_frame.grid(row=2)
        self.scale.pack()

        # tkinter meat and potatoes
        self.naslov = tk.Label(
               self.frame_top,
               text="Happy Crypting ;)!",
               font=("", 20),
               pady=20,
               padx=10,
               )

        self.naslov.pack()

        self.inputtxtorg = tk.Text(self.frame_org, width=20, height=20)
        self.inputtxtorg.pack(expand=tk.TRUE, fill=tk.BOTH)
        self.inputtxtsol = tk.Text(self.frame_sol, width=20, height=20)
        self.inputtxtsol.pack(expand=tk.TRUE, fill=tk.BOTH)

        # Buttons
        self.butcode = tk.Button(
             self.frame_but,
             text="Encode the message\n------->",
             fg="red",
             command=lambda: self.encode(),
             width=20
             )
        self.checkbox = tk.Checkbutton(
            self.frame_but,
            text="Encrypt",
            variable=self.checkvar,
            pady=20,
            command=lambda: self.update_check(),
            width=8,
            anchor="w"
        )
        self.butcode.grid(row=0)
        self.checkbox.grid(row=1)

    # Fun in functions

    # Alphabet
    def make_alphabet(self):
        for broj, cap in enumerate(self.symbols[1]):
            abc_label = tk.Label(self.frame_abc, text=cap)
            self.abc_frames.append(abc_label)
            abc_label.grid(row=0, column=broj)
            arrow_label1 = tk.Label(self.frame_abc, text="|")
            arrow_label1.grid(row=1, column=broj)
            sabc_label = tk.Label(self.frame_abc, text=cap, fg="red")
            self.sabc_frames.append(sabc_label)
            sabc_label.grid(row=3, column=broj)

    def update_check(self):
        if self.checkvar.get() == 1:
            self.checkbox.configure(text="Encrypt")
            self.butcode.configure(text="Encode the message\n------->", fg="red")
        else:
            self.butcode.configure(text="Decode the message\n<------", fg="black")
            self.checkbox.configure(text="Decrypt")

    def encode(self):
        crypto = self.checkvar.get()
        shift = self.shift.get()
        caps = self.symbols[1]
        if crypto:
            text = self.inputtxtorg.get(1.0, tk.END)
            self.enctext = ""
        else:
            text = self.inputtxtsol.get(1.0, tk.END)
            self.orgtext = ""
            shift = -shift

        for letter in text:
            for s in self.symbols:
                if letter in s:
                    fpos = s.index(letter)
                    newpos = fpos + shift
                    if crypto:
                        while newpos >= len(s):
                            newpos -= len(s)
                        self.enctext += s[newpos]
                    else:
                        while newpos < 0:
                            newpos += len(s)
                        self.orgtext += s[newpos]
        if crypto:
            self.inputtxtsol.delete(1.0, tk.END)
            self.inputtxtsol.insert(tk.END, self.enctext)
            still_abc = self.abc_frames
            moved_abc = self.sabc_frames

        else:
            self.inputtxtorg.delete(1.0, tk.END)
            self.inputtxtorg.insert(tk.END, self.orgtext)
            still_abc = self.sabc_frames
            moved_abc = self.abc_frames
            # Alphabet update
        for position, lbl in enumerate(still_abc):
            lbl.configure(text=caps[position])
        for lbl in moved_abc:
            lbl_pos = moved_abc.index(lbl)
            change_pos = lbl_pos + shift
            while change_pos >= len(moved_abc):
                change_pos -= len(moved_abc)
            lbl.configure(text=caps[change_pos])


def main():
    root = tk.Tk()
    Gui(root, symbols)
    root.mainloop()


if __name__ == '__main__':
    main()