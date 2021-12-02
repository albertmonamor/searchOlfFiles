# -*- coding: utf-8 -*-
import ctypes
import os
import threading
from tkinter import ttk, messagebox
from random import choice
from SyncsFoldersV1 import MFolders, SearchOldFile
from tkinter import *
from PermissionsToWin import LetPerForDir
from time import sleep
# // unix time
#   time() is: 1628332183.4353463 == [Sat Aug  7 13:29:43 2021]
#   time()-MONTH {result} [Thu Jul  8 13:29:43 2021']

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# global Ver
S = MFolders()
iSIZE = 0
gSIZE = 0
TEMP = fr"C:\Users\{S.Name}\AppData\Local\Temp"
BY_albert = f"{10 * '*'} \xa9 build With Python By Havrham sabann"


#


def TkinterStatusOutput():
    if not IV2.get() and not IV1.get():
        messagebox.showwarning("Define Option", "select If you want to see all or just garbage")

    ClearStatus()
    buttScan['state'] = DISABLED

    chSe = dropDir.get()
    x = 0  # for Math s.
    AllFiles = 0  # for Math status
    if os.path.exists(chSe) and os.path.isdir(chSe):
        # Graphic
        lisBoxOutput.delete(0, END)
        lisBoxOutput.insert(END, 'Start Mapping this directory...[up to 3 minute]')
        #

        for _dict in SearchOldFile(chSe):
            x += 1

            # graphic
            if x == 1:
                AllFiles = _dict
                continue

            xLabRS['text'] = f'{x * 100 // AllFiles}.0%'
            Path = f"{_dict['path'][:35]}...{_dict['path'][-15:]}" if len(_dict['path']) > 35 else _dict['path']
            ReturnStatus(Path, _dict, AllFiles)

        lisBoxOutput.insert(END, f'\n\n\t\t{10 * "*"} [the scan is completed! ] {10 * "*"}')

    else:
        messagebox.showerror("Have Error with Path", f"Path {chSe} Invalid ")

    buttScan['state'] = NORMAL


def ReturnStatus(Path, _d, nfs):
    global iSIZE, gSIZE
    if ConfDeleteG() and ("Garbage" == _d['status'] or dmpAndTemp(_d['path'])):
        try:
            os.remove(f"{_d['path']}")
        except PermissionError:
            try:
                os.rmdir(f"{_d['path']}")
            except OSError:
                pass

    if IV1.get():
        lisBoxOutput.insert(END, f"\n\nfile {Path} is [{_d['status']}]")
        lisBoxOutput.see("end")

    elif IV2.get():
        if ("Proper" != _d['status'] and "used" not in _d['status']) or dmpAndTemp(_d['path']):
            lisBoxOutput.insert(END, f"\n\nfile {Path} is [{_d['status']}]")
            lisBoxOutput.see("end")

    if (0 == _d['level'] or 1 == _d['level']) and not dmpAndTemp(_d['path']):
        xLabPF['text'] = f"{int(xLabPF['text']) + 1}"
        xLabPRate['text'] = f"[{int(xLabPF['text']) * 100 // nfs}.0 %]"

    elif 2 == _d['level'] and not dmpAndTemp(_d['path']):
        iSIZE += _d['size']
        _all_ = RetFSize(str(iSIZE))
        xLabIF['text'] = f"{int(xLabIF['text']) + 1}"
        xLabIRate['text'] = f"[{int(xLabIF['text']) * 100 // nfs}.0 %]"
        xLabISize['text'] = f"{_all_['s']} {_all_['f']}"

    elif 3 == _d['level'] or dmpAndTemp(_d['path']):
        gSIZE += _d['size']
        _all_ = RetFSize(str(gSIZE))
        xLabGF['text'] = f"{int(xLabGF['text']) + 1}"
        xLabGRate['text'] = f"[{int(xLabGF['text']) * 100 // nfs}.0 %]"
        xLabGSize['text'] = f"{_all_['s']} {_all_['f']}"


def ClearStatus():
    global gSIZE, iSIZE
    gSIZE, iSIZE = 0, 0
    xLabPF['text'], xLabPRate['text'] = 0, "[0.0%]"
    xLabGF['text'], xLabGRate['text'] = 0, "[0.0%]"
    xLabIF['text'], xLabIRate['text'] = 0, "[0.0%]"
    xLabRS['text'] = 0

    xLabGSize['text'], xLabISize['text'] = "0 bytes", "0 bytes"


def ConfOutput():
    All = IV1.get()
    just = IV2.get()
    if All:
        IV2.set(0)
    if just:
        IV1.set(0)


def ConfDeleteG(key=None):
    if "NO" in xLabReStatus['text']:
        if key == "ImButton":
            xLabReStatus['text'] = "[ YES ]"
        return False
    else:
        if key == "ImButton":
            xLabReStatus['text'] = "[ NO ]"
        return True


# return format size
def RetFSize(ns: str):
    if 4 <= len(ns) <= 6:
        a = ns[:len(ns) - 3]
        return {"s": f"{a[:len(a) - 1]}.{a[-1]}", "f": "KB"}

    elif 7 <= len(ns) <= 9:
        a = ns[:len(ns) - 6]
        return {"s": f"{a[:len(a) - 1]}.{a[-1]}", "f": "MB"}

    elif 10 <= len(ns) <= 12:
        a = ns[:len(ns) - 8]
        return {"s": f"{a[:len(a) - 1]}.{a[-1]}", "f": "GB"}
    elif 12 < len(ns) <= 15:
        pass
    else:
        return {"s": ns, "f": 'bytes'}


def ConfTextInGui(lang="en", key=None):
    dictData = {"en_c": "complete :", "he_c": "הושלם :", "fr_c": "complet:",
                "en_if": "Invalid Files :", "he_if": "לא תקין :", "fr_if": "dossier invalide:",
                "en_pf": "Proper Files :", "he_pf": "קובץ תקין :", "fr_pf": "dossier valide:",
                "en_gf": "Garbage Files :", "he_gf": "קבצי זבל :", "fr_gf": "dossier dechet:",
                "en_si": "Search In :", "he_si": "חפש בנתיב :", "fr_si": "rechercher: dans:",
                "en_sof": "SEARCH OLD FILES", "he_sof": "חפש קבצים ישנים", "fr_sof": "Rechercher anciens Dossiers",
                "en_s": "settings", "he_s": "הגדרות", "fr_s": "Paramètres",
                "en_a": "Advanced", "he_a": "מתקדם", "fr_a": "Avancer",
                "en_rgf": "Remove Garbage Files", "he_rgf": "מחק קבצי זבל", "fr_rgf": "effacer dossiers dechets",
                "en_bl": "language : English", "he_bl": "שפה : עברית", "fr_bl": "Langue: Francais",
                }

    listLabel = [xLabResultScan,
                 xLabInvalidFiles,
                 xLabProperFiles,
                 xLabGarbageFiles,
                 xLabDir,
                 buttScan,
                 xLabSystem,
                 xLabAdvanced,
                 buttRemoveG,
                 buttLang]

    for txt, lab in zip(dictData.keys(), range(len(dictData))):
        listLabel[lab//3]['text'] = dictData.get(lang + txt[2::])
        if key == "sleep":
            sleep(0.01)


def dmpAndTemp(_f):
    if (_f.endswith(".dmp") or _f.endswith(".tmp") or _f.endswith(".log")) or TEMP.lower() in _f.lower():
        return True

    # else
    return False


MWin = Tk()
MWin.geometry("730x499")

# objects
# Labels

#  1
xLabResultScan = Label(MWin, font="italic 13")
xLabResultScan.place(x=5, y=20)
# CreateLabel(MWin, 5, 20)

xLabRS = Label(MWin, text="", font="italic 13", fg="green")
xLabRS.place(x=100, y=20)
# CreateLabel(MWin, 100, 20, fg="green")
##

#  2
xLabGarbageFiles = Label(MWin, font="italic 13")
xLabGarbageFiles.place(x=260, y=115)

xLabGF = Label(MWin, text=0, font="italic 13", fg="red")
xLabGF.place(x=375, y=115)

xLabGRate = Label(MWin, text='[0.0%]', font="italic 10")
xLabGRate.place(x=440, y=115)

xLabGSize = Label(MWin, text="0 bytes", font=("Comic Sans MS", 9))
xLabGSize.place(x=500, y=115)

##

#  3
xLabInvalidFiles = Label(MWin, font="italic 13")
xLabInvalidFiles.place(x=260, y=20)

xLabIF = Label(MWin, text=0, font="italic 13", fg="orange")
xLabIF.place(x=365, y=20)

xLabIRate = Label(MWin, text='[0.0%]', font="italic 10")
xLabIRate.place(x=440, y=20)

xLabISize = Label(MWin, text="0 bytes", font=("Comic Sans MS", 9))
xLabISize.place(x=500, y=20)

##

#  4
xLabProperFiles = Label(MWin, font="italic 13")
xLabProperFiles.place(x=260, y=70)

xLabPF = Label(MWin, text=0, font='italic 13', fg="green")
xLabPF.place(x=370, y=70)

xLabPRate = Label(MWin, text='[0.0%]', font="italic 10")
xLabPRate.place(x=440, y=70)
##

# Label setting
xLabSystem = Label(MWin, font=("Comic Sans MS", 15))
xLabSystem.place(x=550, y=150)

xLabAdvanced = Label(MWin, font=("Comic Sans MS", 15))
xLabAdvanced.place(x=550, y=300)

xLabReStatus = Label(MWin, text="[ NO ]", fg="red")
xLabReStatus.place(x=630, y=350)
##

xLabDir = Label(MWin, font="times 14")
xLabDir.place(x=3, y=155)

# drops
dropDir = ttk.Combobox(MWin, values=['c:\\', 'c:\\Users\\', f'c:\\Users\\{S.Name}',
                                     f'c:\\Users\\{S.Name}\\Desktop', 'c:\\Windows'],
                       font=("Courier", 10, "bold"), width=30)
dropDir.place(x=90, y=158)
dropDir.bind("<<ComboboxSelected>>", SelectedFromDrop)

# buttons
buttScan = ttk.Button(MWin,
                      command=lambda: threading.Thread(target=TkinterStatusOutput).start())
buttScan.place(x=570, y=20)

buttRemoveG = ttk.Button(MWin, command=lambda: ConfDeleteG(key="ImButton"))
buttRemoveG.place(x=500, y=350)

buttLang = ttk.Button(MWin, text="",
                      command=lambda :threading.Thread(target=ConfTextInGui, args=(choice(['en', 'he', 'fr']), 'sleep')).start())
buttLang.place(x=500, y=400)

# scroll
ScroView = Scrollbar(MWin)
ScroView.pack(side=RIGHT, fill=BOTH)

# listBox
lisBoxOutput = Listbox(MWin, yscrollcommand=ScroView.set, width=80, height=18, selectbackground="green",
                       selectmode=EXTENDED)
lisBoxOutput.place(x=3, y=200)
lisBoxOutput.insert(END, f"{BY_albert}", "",
                    rf'[Access] c:\Windows\LiveKernelReports [state] ---:'
                    + LetPerForDir(r"c:\Windows\LiveKernelReports"), "",
                    rf'[Access] c:\Windows.old [state] ---:' + LetPerForDir(r"c:\Windows.old"), "",
                    rf'[Access] c:\Windows\Temp [state] ---:' + LetPerForDir(r"C:\Windows\Temp"))

# for DmpFile need access to folder and subs [!] not for TempFile

# buttonBox
IV1 = IntVar()
IV2 = IntVar()
buttBoxAll = ttk.Checkbutton(MWin, variable=IV1, text="see all in Terminal output \n\t[Slows process!]",
                             command=lambda: ConfOutput())
buttBoxAll.place(x=500, y=195)

buttBoxIAG = ttk.Checkbutton(MWin, variable=IV2, text="Just Garbage and Invalid \n\t[Faster Processes!]",
                             command=lambda: ConfOutput())
buttBoxIAG.place(x=500, y=250)
IV2.set(1)
ConfTextInGui("he")

# Configs And Protocols
ScroView.config(command=lisBoxOutput.yview)
MWin.mainloop()

r"""
C:\Windows.old
C:\Users\IDK\AppData\Local\Temp
C:\Windows\Logs\WindowsUpdate
"""
