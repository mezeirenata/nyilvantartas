from random import choice, choices, randint
import unicodedata


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def writeTanarok():
    f = open("csv/tanarok.csv", "w", encoding="utf-8")
    f.write("Név;Osztályok;Email;Jelszó;Tárgyak\n")
    names = [
        "Soma Balogh",
        "Angéla Rácz",
        "Andrea Somogyi",
        "Jázmin Gulyás",
        "Ramóna Dobos",
        "Balázs Takács",
        "Benedek Szabó",
        "Albert Nagy",
        "Botond Farkas",
        "Sára Biró",
        "Andrea Simon",
        "Szervác Katona",
        "Barna Kozma",
        "Kristóf Deák",
        "Marianna Fekete",
        "Mihály Pintér",
        "Dorottya Szalai",
        "Jázmin Vörös",
    ]
    for i in range(16):
        osztalyok = []
        for d in diakok:
            if d.osztaly not in osztalyok:
                osztalyok.append(d.osztaly)

        name = choice(names)
        names.remove(name)

        nameList = name.split(" ")
        nameList.reverse()
        name = f"{nameList[0]} {nameList[1]}"
        f.write(f"{name};")

        osztaly = []
        for i in range(randint(2, 4)):
            a = choice(osztalyok)
            if a not in osztaly:
                osztaly.append(a)
        for p, x in enumerate(osztaly):
            if p == 0:
                f.write(x)
            else:
                f.write(f",{x}")

        f.write(";")

        f.write(f"{email(nameList)};{password(nameList)};")

        targyak = list(diakok[0].jegyek)
        targy = []
        for i in range(randint(2, 3)):
            a = choice(targyak)
            if a not in targy:
                targy.append(a)
        for p, x in enumerate(targy):
            if p == 0:
                f.write(x)
            else:
                f.write(f",{x}")

        f.write("\n")
    f.close()


diakNames = []


def writeDiakok():
    f = open("csv/diakok.csv", "w", encoding="utf-8")
    f.write("Név;Osztály;Email;Jelszó\n")
    names = [
        "Patrik Csonka",
        "Árpád Váradi",
        "Liliána Kelemen",
        "Ernő Gulyás",
        "Gabriella Soós",
        "Henriett Orsós",
        "Hunor Balázs",
        "Magyar Virág",
        "Olivér Szűcs",
        "Ádám Fazekas",
        "Liza Budai",
        "Liza Novák",
        "Boróka Pásztor",
        "Georgina Papp",
        "Patrícia Somogyi",
        "Patrik Junó",
        "Péter Balázs",
    ]
    for i in range(16):
        numbers = [9, 10, 11, 12]
        letters = ["A", "B", "C", "D", "NY"]

        name = choice(names)
        names.remove(name)

        nameList = name.split(" ")
        nameList.reverse()
        name = f"{nameList[0]} {nameList[1]}"
        f.write(f"{name};")
        diakNames.append(name)

        tagozat = choice(numbers)
        f.write(f"{tagozat}{choice(letters)}")

        f.write(";")

        f.write(f"{email(nameList)};{password(nameList)}")

        f.write("\n")
    f.close()


def writeJegyek():
    f = open("csv/jegyek.csv", "w", encoding="utf-8")
    firstLine = (
        "Név;Történelem;Informatika;Angol;Irodalom;Nyelvtan;Testnevelés;Matek;Fizika"
    )
    f.write(f"{firstLine}\n")
    targyak = []
    splitted = firstLine.strip().split(";")
    for t in splitted:
        if t != "Név":
            targyak.append(t)

    for i in diakNames:

        f.write(f"{i};")
        for y, d in enumerate(targyak):
            for x, a in enumerate(range(randint(2, 5))):
                if x != 0:
                    f.write(",")
                    f.write(
                        choices(
                            ["1", "2", "3", "4", "5"], weights=[10, 20, 30, 40, 50], k=1
                        )[0]
                    )

                else:
                    f.write(
                        choices(
                            ["1", "2", "3", "4", "5"], weights=[10, 20, 30, 40, 50], k=1
                        )[0]
                    )

            if y < len(targyak) - 1:

                f.write(";")

        f.write("\n")
    f.close()


def writeOrarend():
    f = open("csv/orarendek.csv", "w", encoding="utf-8")
    f.write("Osztály;Nap;Tárgyak\n")

    targyak = list(diakok[0].jegyek)
    targyak.append("-")
    osztalyok = []
    for d in diakok:
        if d.osztaly not in osztalyok:
            osztalyok.append(d.osztaly)
    for o in osztalyok:
        for i in range(5):
            match i:
                case 0:
                    i = "Hétfő"
                case 1:
                    i = "Kedd"
                case 2:
                    i = "Szerda"
                case 3:
                    i = "Csütörtök"
                case 4:
                    i = "Péntek"
            h = choices(targyak, k=randint(4, 7))
            f.write(f"{o};{i};")
            for k, q in enumerate(h):
                if k != 0:
                    f.write(f",{q}")
                else:
                    f.write(q)
            f.write("\n")

    f.close()


def email(nameList):
    email = f"{strip_accents(nameList[0].lower())}.{strip_accents(nameList[1].lower())}@gmail.com"

    return email


def password(nameList):
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    nums = ""

    for n in choices(numbers, k=randint(3, 5)):
        nums += str(n)
    password = f"{strip_accents(nameList[1]).capitalize()}{nums}"

    return password


writeDiakok()
writeJegyek()
from diak import *

writeOrarend()
writeTanarok()
