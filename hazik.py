
class Hazi():
    def __init__(self, osztaly, targy, hatarido, feladat) -> None:
        self.osztaly = osztaly
        self.targy = targy
        self.hatarido = hatarido
        self.feladat = feladat





hazik = []
def readHazik():
    f = open("csv/hazik.csv", "r", encoding="utf-8")
    f.readline()
    osszesHazi = ""
    first = bool
    for line in f:
        line = line.strip()
        if line == "START":
            first = True
        elif first:
            osszesHazi += f"{line};"
        if line == "END":
            first = False
            
            
        
        


    
    
    splitted = osszesHazi.split(";")
    lista = []
    a = ""
    for i, s in enumerate(splitted):
        if s != "END":
            lista.append(s)
        else:
            a = i
    hazik.append(Hazi(lista[0], lista[1], lista[2], lista[3:a]))
        

    f.close()

readHazik()
print(hazik[0].feladat)
