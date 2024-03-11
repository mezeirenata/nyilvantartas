from diak import *

diakok: list[Diak] = []

def main():
    readFile("diakok.csv")
    print(diakok[0].jegyek["tortenelem"])

def readFile(filename):
    f = open(filename, "r",encoding="utf-8")
    f.readline()
    for sor in f:
        diakok.append(Diak(sor))
    f.close()

main()