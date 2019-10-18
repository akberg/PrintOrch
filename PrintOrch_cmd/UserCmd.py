'''
User interface for PrintOrch
Andreas Klavenes Berg
08.02.2019
'''

# Imports
from easygui import diropenbox
from os import system
import keyboard as key
import Util
'''
import tkinter as tk


window = tk.Tk()
window.title("PrintOrch")
'''

global index
index = 0


def display(path, save_path, work, save_name, content, nums, n):
    system("cls")
    # Menu index for displaying current choice
    # 0: Select fetch directory
    # 1: Select save directory
    # 2 + i (for i in content): Select part
    # imax +
    # 3: Select save name
    # 4: Proceed
    # 5: Quit
    index = 0
    m_index = ["  ", "  ", "  ", "  ", "  "] + ["  "]*n
    m_index[index] = ">>"
    while 1:
        length = 0
        if len(content) > 0:
            for i in content:
                length = max(length, len(Util.get_instrument(i, work)) + 2)
        if work != "":
            print("-"*40)
            print(work)
            print("-"*40)
        print(m_index[0], "Valgt mappe:", path)
        print(m_index[1], "Valgt målmappe:", save_path)
        print("Innhold")
        print("-"*36)
        [print(m_index[2+i], Util.get_instrument(content[i], work).ljust(length) + "|Antall: {:3}".format(nums[i])) for i in range(n)]
        print("-"*36)
        print(m_index[2 + n], "Lagres som:", save_name)
        if path != "" and save_name != "" and save_name != "":
            print(m_index[3 + n], "Fullfør")
        print(m_index[4 + n], "Avslutt")

        if key.is_pressed(key.KEY_DOWN) and index < len(m_index - 1):
            index+=1
        elif key.is_pressed(key.KEY_UP) and index > 0:
            index-=1





def prompt_fetch_dir():
    return diropenbox("Velg mappen som inneholder stykket som skal skrives ut.", "Hent notemappe")


def prompt_save_dir():
    return diropenbox("Velg mappen hvor du vil lagre utskriftfilen.", "Velg målmappe")


def prompt_num(instrument, n):
    sv = input("Antall utskrifter for " + instrument + " (verdi: {}): ".format(n))
    if sv == "":
        return n
    else:
        try:
            return int(sv)
        except TypeError:
            print("Feil: Antall må være et heltall! Ingen endring gjort.")
            return n


def prompt_save_name(save_name):
    new = input("Lagre som (Tomt felt for å beholde filnavnet {}: ".format(save_name))
    if new == "":
        return save_name
    else:
        return new


def prompt_continue(content, nums, n, save_path):
    print("Valgte filer:")
    [print(content[i].ljust(30) + "Antall: {:3}".format(nums[i])) for i in range(n)]
    print("\nLagres som", save_path, "\n")
    sv = input("Fullføre? (tast [N] for å avbryte): ")
    if sv.lower() == "n":
        return False
    return True


def prompt_overwrite(path, name):
    while 1:
        sv = input("Filen " + path + "\\" + name +
                   ".pdf finnes allerede. Er du sikker på at du vil overskrive den? [ja=1/nei=0]: ")
        try:
            if int(sv) == 1:
                return True
            elif int(sv) == 0:
                return False
        except TypeError: pass


def msg_complete():
    print("Lagring var vellykket!")
    input("Trykk enter for å fortsette...")
