from diak import Diak

class Jegyek:
    def __init__(self, sor) -> None:
        data = sor.strip().split(";")
        self.nev = nevDiak('diakok.csv')
        #elsődleges kulcs
        self.jegyek = self.jegyekDict()

    def jegyekDict(self):
        dictionary = {}
        f = open("csv/jegyek.csv", "r", encoding="utf-8")
        for i, sor in enumerate(f):
            splitted = sor.strip().split(";")
            if i == 0:
                targyak = sor.strip().split(";")
                for t in targyak:
                    if t != "nev":
                        dictionary[t] = []
            else:
                if splitted[0] == self.nev:
                    for x, s in enumerate(splitted[1:]):
                        splitted2 = s.split(",")
                        for a in splitted2:
                            keys = list(dictionary)
                            dictionary[keys[x]].append(int(a))

        f.close()
        return dictionary
    def nevDiak(filename:str):
        f = open(filename, 'r', encoding= 'utf-8')
        elsodleges_kulcs = 'None'
        for sor in f:
            
        
        f.close()



# nev;tortenelem;informatika;angol;irodalom;nyelvtan;testneveles;matek;fizika
# Kiss János;3,5,3;4,3,2;3,4,5;2,3,4;1,2,2,3;4,5,6;4,4,4;3,3
