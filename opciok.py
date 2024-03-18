from diak import *
from tanar import *
import math

# diak.py -> diakok lista


def KitunoTanulok() -> list[Diak]:
    kituno_diakok: list[Diak] = []
    for d in diakok:
        d.tan_atlag = int(round(d.tan_atlag))
        if d.tan_atlag == 5:
            kituno_diakok.append(d)
    return kituno_diakok


def BukasraAllnak() -> list[Diak]:
    buko_diakok: list[Diak] = []
    for d in diakok:
        for key, value in d.jegyek.items():
            if int(round(value)) < 2:
                buko_diakok.append(d)
    return buko_diakok


# return-öl egy listát a bukásra álló tanulókkal: a meghívás során lehet egyeztetni tanuló nevet,
# így akár kiírja a bejelentkezett tanulónak hogy bukásra-e áll


def BukoTantargy() -> list[str]:
    buko_tantargyak_diak: list[str] = []
    for d in diakok:
        bukasraallo_tantargyak: list[str] = []
        for key, value in d.jegyek.items():
            if int(round(value)) < 2:
                bukasraallo_tantargyak.append(key)
        if len(bukasraallo_tantargyak) > 0:
            buko_tantargyak_diak.append(f"{d.nev};{bukasraallo_tantargyak[0:]}")
    return buko_tantargyak_diak


def Tanarok_bukodiakjai() -> list[str]:
    # tanar neve, buko diak, bukodiak osztalya, bukasra allo tantargyai
    tanarok_buko_diakjai: list[str]
    for t in tanarok:
        for d in BukasraAllnak():
            for key, value in d.jegyek.items():
                bukasos_tantargyak: list[str] = []
                value = Tantargyi_atlag(value)
                if int(round(value)) < 2:
                    if key in t.targyak:
                        bukasos_tantargyak.append(key)
                if d.osztaly in t.osztalyok or d.osztaly == t.osztalyok:
                    tanarok_buko_diakjai.append(
                        f"{t.nev};{d.nev};{d.osztaly};{bukasos_tantargyak[0:]}"
                    )
    return tanarok_buko_diakjai


def Tantargyi_atlag(value_a: list[int]) -> float:
    sum = 0
    for x in value_a:
        sum += x
    return sum / len(value_a)


def Tanarok_bukoosztalyai(tanar: str) -> dict:
    bukoosztalyok = {}
    for t in tanarok:
        if t.nev == tanar:
            for x in t.osztalyok:
                if x not in bukoosztalyok.keys():
                    bukoosztalyok[x] = None

    for d in diakok:
        if d.osztaly in bukoosztalyok.keys():
            if bukasra_vagynem(d.nev, tanar):
                if bukoosztalyok[d.osztaly] == None:
                    bukoosztalyok[d.osztaly] = d.nev
                else:
                    bukoosztalyok[d.osztaly] += d.nev + ", "
    return bukoosztalyok


def bukasra_vagynem(diak_neve: str, tanar) -> bool:
    for d in diakok:
        if d.nev == diak_neve:
            for key, value in d.jegyek.items():
                for t in tanarok:
                    if t.nev == tanar:
                        if key in t.targyak:
                            value = Tantargyi_atlag(value)
                            if round(value) == 1:
                                return True
    return False

def Felhasznalo_lekerese(felhasznalo:str) -> Diak|Tanar|None:
    for d in diakok:
        if d.nev == felhasznalo:
            return d
    for t in tanarok:
        if t.nev == felhasznalo:
            return t
    return None 

def DiákVagyNem(felhasznalo:str) -> bool|None:
    # True = Diák
    # False - Tanár
    # None - egyik sem
    for d in diakok:
        if d.nev == felhasznalo:
            return True
    for t in tanarok:
        if t.nev == felhasznalo:
            return False
    return None

def Eletkor(szuletesi_datum:str, mai_datum:str) -> int:
    #2000.01.01
    eletkor = 0
    ev,honap,nap = szuletesi_datum.split('.')
    ev2,honap2,nap2 = mai_datum.split('.')
    ev = int(ev) 
    ev2 = int(ev2)
    eltelt_evek = ev2 - ev

    if honap2 == honap and nap == nap2:
        eletkor = eltelt_evek
    else:
        eletkor  = eltelt_evek-1
    return eletkor

def MentesHozzaadas(tanarok_file:str, jegyek_file:str,diakok_file:str) -> None:
    tanar_vagy_diak = input('Feljegyzendő személy: 0 - Tanár, 1 - Tanuló: ')
    match tanar_vagy_diak:
        case '0':
            #Tanár
            tanar_nev = str(input('Pedagógus neve (Vezetéknév Keresztnév): '))
            tanar_osztalyok = str(input('A tanító által tanított osztály(ok) (11NY, 9B): '))
            tanar_email = str(input('A pedagógus E-mail címe:(vezeteknev.keresztnev@gmail.com): '))
            tanar_jelszo = str(input('Az új felhasználó belépési jelszava: '))
            tanar_targyak = str('A tanító által tanított tantárgy(ak) :')

            f = open(tanarok_file, 'w', encoding='utf-8')
            f.write(f'{tanar_nev};{tanar_osztalyok};{tanar_email};{tanar_jelszo};{tanar_targyak}\n')
            f.close()
            f = open(tanarok_file,'r',encoding='utf-8')
            tanarok = []
            for row in f:
                tanarok.append(Tanar(row))
            f.close()

        case '1':
            #Diák
            diak_nev = str(input('Tanuló neve (Vezetéknév Keresztnév): '))
            diak_osztaly = str(input('Tanuló osztálya (11NY): '))
            diak_email = str(input('Tanuló E-mail címe:(vezeteknev.keresztnev@gmail.com): '))
            diak_jelszo = str(input('Az új felhasználó belépési jelszava: '))
            tori = str(input('Az új tanuló meglévő Történelem jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            info = str(input('Az új tanuló meglévő Informatika jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            angol = str(input('Az új tanuló meglévő Angol idegennyelv jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            irod = str(input('Az új tanuló meglévő Irodalom jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            nyt = str(input('Az új tanuló meglévő Nyelvtan jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            tesi = str(input('Az új tanuló meglévő Testnevelés jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            matek = str(input('Az új tanuló meglévő Matematika jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            fizika = str(input('Az új tanuló meglévő Fizika jegyei: (1,2,3,4,5..stb, jegyek:1-től 5-ig)'))
            diak_jegyei = tori + ";" + info + ";" + angol + ";" + irod + ";" + nyt + ";" + tesi + ";" + matek + ";" + fizika
            f = open(diakok_file, "w", encoding = 'utf-8')
            f.write(f'{diak_nev};{diak_osztaly};{diak_email};{diak_jelszo}\n')
            f.close()

            f = open(diakok_file, 'r', encoding='utf-8')
            for row in f:
                diakok = []
                row = row + ";" + diak_jegyei
                diakok.append(Diak(row))
            f.close()

            f = open(jegyek_file, 'w', encoding = 'utf-8')
            f.write(f'{diak_nev};{diak_jegyei}\n')
            f.close()

    
def EltavolitasTanuloDiak(eltavolitando_neve:str) -> None:
    eltavolitando = Felhasznalo_lekerese(eltavolitando_neve)
    if eltavolitando in diakok:
        diakok.remove(eltavolitando)
        f = open("csv/diakok.csv", 'w', encoding='utf-8')
        for row in f:
            f.remove(row)
        for d in diakok:
            f.write(f'{d}\n')
        f.close()

        f = open("csv/jegyek.csv", 'w', encoding='utf-8')
        for row in f:
            if eltavolitando.nev in row:
                f.remove(row)
        f.close()

    elif eltavolitando in tanarok:
        tanarok.remove(eltavolitando)
        f = open("csv/tanarok.csv", 'w', encoding='utf-8')
        for row in f:
            f.remove(row)
        for t in tanarok:
            f.write(f'{t}\n')
        f.close()