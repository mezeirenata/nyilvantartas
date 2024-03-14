from diak import *
from tanar import *
import math
#diak.py -> diakok lista

def KitunoTanulok() -> list[Diak]:
    kituno_diakok: list[Diak] = []
    for d in diakok:
        d.tan_atlag = int(round(d.tan_atlag))
        if d.tan_atlag== 5:
            kituno_diakok.append(d)
    return kituno_diakok

def BukasraAllnak() -> list[Diak]:
    buko_diakok: list[Diak]  = []
    for d in diakok:
        for key,value in d.jegyek.items():
            if int(round(value)) < 2:
                buko_diakok.append(d)
    return buko_diakok
#return-öl egy listát a bukásra álló tanulókkal: a meghívás során lehet egyeztetni tanuló nevet,
#így akár kiírja a bejelentkezett tanulónak hogy bukásra-e áll

def BukoTantargy() -> list[str]:
    buko_tantargyak_diak: list[str] = []
    for d in diakok:
        bukasraallo_tantargyak: list[str] = []
        for key,value in d.jegyek.items():
            if int(round(value)) < 2:
                bukasraallo_tantargyak.append(key)
        if len(bukasraallo_tantargyak) > 0:
            buko_tantargyak_diak.append(f"{d.nev};{bukasraallo_tantargyak[0:]}")
    return buko_tantargyak_diak

def Tanarok_bukodiakjai() -> list[str]:
    #tanar neve, buko diak, bukodiak osztalya, bukasra allo tantargyai  
    tanarok_buko_diakjai: list[str]
    for t in tanarok:
        for d in BukasraAllnak():
            for key,value in d.jegyek.items():
                bukasos_tantargyak: list[str] = []
                value = Tantargyi_atlag(value)
                if int(round(value))  < 2:
                    if key in t.targyak:
                        bukasos_tantargyak.append(key)
                if d.osztaly in t.osztalyok or d.osztaly == t.osztalyok: 
                    tanarok_buko_diakjai.append(f'{t.nev};{d.nev};{d.osztaly};{bukasos_tantargyak[0:]}')
    return tanarok_buko_diakjai

def Tantargyi_atlag(value_a:list[int]) -> float:
    sum = 0
    for x in value_a:
        sum += x
    return sum/len(value_a)


