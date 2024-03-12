from diak import *
from jegyek import *

diakok: list[Diak] = []
jegyek: list[Jegyek] = []
def main():
    readFile("diakok.csv")
    readFile2("jegyek.csv")
    print(diakok[0].jegyek["tortenelem"])
    print(jegyek[0])

def readFile(filename):
    f = open(f"csv/{filename}", "r",encoding="utf-8")
    f.readline()
    for sor in f:
        diakok.append(Diak(sor))
    f.close()

def readFile2(filename:str) -> None:
    f = open(f"csv/{filename}","r", encoding='utf-8' )
    f.readline()
    for sor in f:
        jegyek.append(Jegyek(sor))
    f.close()

main()