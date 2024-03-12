class Diak:
    def __init__(self, sor) -> None:
        data = sor.strip().split(";")
        self.nev = data[0]
        self.osztaly = data[1]
        self.email = data[2]
        
        self.jelszo = data[3]
        self.osztondij = int(data[4])
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


