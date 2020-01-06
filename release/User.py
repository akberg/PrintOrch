'''
User interface for PrintOrch
Andreas Klavenes Berg
08.02.2019
'''

# Imports
from easygui import diropenbox
import Util
'''
import tkinter as tk


window = tk.Tk()
window.title("PrintOrch")
'''

def max_(a, b):
    return a if a > b else b


def display(path, save_path, work, save_name, content, nums, n):
    print('\n'*20) # "clear screen"
    
    length = 0
    if len(content) > 0:
        for c in content:
            length = max_(length, len(Util.get_instrument(c, work)) + 5)
        #length = len(Util.get_instrument(content[0], work)) + 10
    if work != "":
        print("-"*40)
        print(work)
        print("-"*40)
    print("Valgt mappe:", path)
    print("Valgt målmappe:", save_path)
    print("Innhold")
    print("-"*33)
    [print(Util.get_instrument(content[i], work).ljust(length) + " Antall: {:3}".format(nums[i])) for i in range(n)]
    print("-"*33)
    print("\nLagres som:", save_name)
    print()

    menu = [
        "0) Avlutt",
        "1) Velg notemappe",
        "2) Veldg målmappe",
        "3) Endre navn på målfil",
        "4) Endre antall kopier",
        "5) Fullfør",
    ]
    choices = [0, 1, 2, 3]
    if path != "":
    #    choices.insert()
        choices.append(4)
        if save_path != "" and save_name != "":
            choices.append(5)
    [print(menu[i]) for i in choices]
    print("6) ")
    while 1:
        alt = -1
        try:
            alt = int(input("Ditt valg: "))
        except:
            alt = -1
        if alt in choices:
            return alt


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
        except Exception: pass


def msg_complete():
    print("Lagring var vellykket!")
    input("Trykk enter for å fortsette...")

