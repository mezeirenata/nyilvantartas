from diak import *
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
