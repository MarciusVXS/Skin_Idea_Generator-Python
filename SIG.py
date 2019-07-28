import tkinter as tk
import linecache as lc
import os
import re
import yaml
import random

ColorMain = '#20232c'
ColorActivatedMain = '#0f1014'
ColorBits = '#907852'
ColorText = '#908b90'
ColorActivatedText = '#FFFFFF'
WindowsMode = False


class Win(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        if WindowsMode:
            self.overrideredirect(False)
        else:
            self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)

    def dragwin(self, event):
        if event.widget is not MovingTab:
            return
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y


if os.path.exists("SIG-generated/"):
    pass
else:
    os.mkdir("SIG-generated/")
if os.path.exists("SIG-generated/config.yaml"):
    with open('SIG-generated/config.yaml') as f:
        data = yaml.safe_load(f)
    WindowsMode = data["WindowsMode"]
    ColorMode = data["ColorTheme"]
    if ColorMode == 3:
        ColorMain = data["Colors"]["ColorMain"]
        ColorActivatedMain = data["Colors"]["ColorActivatedMain"]
        ColorBits = data["Colors"]["ColorBits"]
        ColorText = data["Colors"]["ColorText"]
        ColorActivatedText = data["Colors"]["ColorActivatedText"]
    elif ColorMode == 2:
        ColorMain = '#262d44'
        ColorActivatedMain = '#161b2a'
        ColorBits = '#e22028'
        ColorText = '#e22028'
        ColorActivatedText = '#ffffff'
    else:
        pass
else:
    import requests
    url = 'https://raw.githubusercontent.com/marcius922/Skin_Idea_Generator-Python/master/config.yaml'  # url of paste
    r = requests.get(url)
    content = r.text
    intcfg = open("SIG-generated/config.yaml", "w")
    intcfg.write(content)
    intcfg.close()

with open('SIG-generated/config.yaml') as f:
    data = yaml.safe_load(f)


Root = Win()
ThemeButton = {'bg': ColorMain,'bd': 0, 'fg':ColorText, 'activebackground': ColorActivatedMain,
               'activeforeground': ColorActivatedText}
ThemeEntry = {'bg': ColorActivatedMain, 'relief': 'flat', 'fg': ColorText, 'insertbackground': ColorActivatedText}
Root.minsize(960, 540)
Root.maxsize(960, 540)
Root.title("SIG by Martin")

MainCanvas = tk.Canvas(Root, height=540, width=960)
MainCanvas.pack()


FrameLeft = tk.Frame(MainCanvas, bg=ColorMain)
FrameLeft.place(y=0, x=0, relwidth=0.35, relheight=1)
FrameLeftText = tk.Label(FrameLeft, text='SKIN IDEA GENERATOR', bg=ColorMain,
                         fg=ColorText, anchor='c', padx=10, font=25)
FrameLeftText.place(x=0, y=0, relwidth=1, height=30)
MovingTab = tk.Label(FrameLeft, text='⛶', bg=ColorMain, fg=ColorText, anchor='c', padx=10, font=25)
if WindowsMode:
    pass
else:
    MovingTab.place(x=0, y=0, width=30, height=30)

ChampLock = tk.BooleanVar()
ChampLockToggle = tk.Checkbutton(FrameLeft, text="Lock Champion", variable=ChampLock,
                                 **ThemeButton, relief='flat', anchor='w')
ChampLockToggle.place(y=70, x=205, height=40, width=132)
ChampLockInput = tk.Entry(FrameLeft, **ThemeEntry)
ChampLockInput.place(x=20, y=70, width=183, height=40)
ChampLockInputPre = tk.Frame(FrameLeft, width=20, height=80, bg=ColorBits)
ChampLockInputPre.place(x=0, y=30)
FrameLeftLine = tk.Frame(FrameLeft, bg=ColorBits)
FrameLeftLine.place(x=203, y=30, height=80, width=2)

SkinLock = tk.BooleanVar()
SkinLockToggle = tk.Checkbutton(FrameLeft, text="Lock Skin", variable=SkinLock,
                                **ThemeButton, relief='flat', anchor='w')
SkinLockToggle.place(y=30, x=205, height=40, width=132)
SkinLockInput = tk.Entry(FrameLeft, **ThemeEntry)
SkinLockInput.place(x=20, y=30, width=183, height=40)

FrameLeftText = tk.Label(FrameLeft, text='How many to generate:', bg=ColorActivatedMain, relief='flat', fg=ColorText)
FrameLeftText.place(relx=0, y=480, relwidth=0.5, height=30)


def genideas(theme, champion):
    FrameRightText.insert('end', theme)
    FrameRightText.insert('end', ' ')
    FrameRightText.insert('end', champion)
    FrameRightText.insert('end', '\n')


def funcgenerate():
    try:
        GenAmount = int(GenEntry.get())
    except:
        FrameRightText.delete('1.0', 'end')
        FrameRightText.insert('1.0', "Please Enter A Number")
    else:
        if SkinLock.get() and ChampLock.get():
            FrameRightText.delete('1.0', 'end')
            FrameRightText.insert('1.0', 'Why? (both champions and skins are Locked)')
        elif SkinLock.get() and not ChampLock.get():
            if SkinLockInput.get() == "":
                FrameRightText.delete('1.0', 'end')
                FrameRightText.insert('1.0', 'Input Skin Theme to generate ideas or uncheck the "Lock Skin" Button')
            else:
                FrameRightText.delete('1.0', 'end')
                for i in range(0, GenAmount):
                    genideas(SkinLockInput.get(), data["Champions"][random.randrange(0, len(data["Champions"]))])
        elif not SkinLock.get() and ChampLock.get():
            if ChampLockInput.get() == "":
                FrameRightText.delete('1.0', 'end')
                FrameRightText.insert('1.0', 'Input Skin Theme to generate ideas or uncheck the "Lock Skin" Button')
            else:
                FrameRightText.delete('1.0', 'end')
                for i in range(0, GenAmount):
                    genideas(data["Themes"][random.randrange(0, len(data["Themes"]))], ChampLockInput.get())
        else:
            FrameRightText.delete('1.0', 'end')
            for i in range(0, GenAmount):
                genideas(data["Themes"][random.randrange(0, len(data["Themes"]))], data["Champions"][random.randrange(0, len(data["Champions"]))])


def funcexport():
    opint = 1
    while True:
        opfile = 'SIG-generated/output' + str(opint) + '.txt'
        if os.path.exists(opfile):
            opint += 1
            continue
        else:
            outputfile = open(opfile, "w")
            outputfile.write(FrameRightText.get('1.0', 'end'))
            outputfile.close()
            break


GenAmount = 1
GenEntry = tk.Entry(FrameLeft, **ThemeEntry, justify='right')
GenEntry.place(relx=0.5, y=480, height=30, relwidth=0.5)
ButtonGenerate = tk.Button(FrameLeft, text='Generate', **ThemeButton, command=funcgenerate)
ButtonGenerate.place(x=0, y=510, height=30, width=168)
ButtonGenerateExport = tk.Button(FrameLeft, text='Export Output', **ThemeButton, command=funcexport)
ButtonGenerateExport.place(x=168, y=510, height=30, width=168)
ButtonSeparation = tk.Frame(FrameLeft, bg=ColorBits, width=2, height=30)
ButtonSeparation.place(x=167, y=510)


FrameRight = tk.Frame(MainCanvas, bg=ColorMain, bd='0')
FrameRight.place(y=30, relx=0.35, relwidth=0.65, height=510)
FrameRightText = tk.Text(FrameRight, bg='#dddddd', fg=ColorMain, insertbackground=ColorMain,
                         padx=10, pady=10, relief='flat')
FrameRightText.place(y=0, relwidth=1, relheight=1)

FrameTopRight = tk.Frame(MainCanvas, bg=ColorActivatedMain, bd='0')
FrameTopRight.place(relx=0.35, relwidth=0.65, height=30)
FrameTopRightButtonExit = tk.Button(FrameTopRight, text='×', relief='flat', bg=ColorActivatedMain,
                                    fg=ColorText, command=Root.destroy, bd=0,
                                    activebackground=ColorActivatedMain, activeforeground='red')
FrameTopRightButtonExit.config(font=30)
if WindowsMode:
    pass
else:
    FrameTopRightButtonExit.place(x=594, y=0, height=30, width=30)


Root.mainloop()
