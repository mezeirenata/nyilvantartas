
class Jegyek:
    def __init__(self, sor) -> None:
        data = sor.strip().split(";")
        self.nev = data[0]
        #elsődleges kulcs ^
        self.jegyek = str(data[1:])
        self.tortenelem,self.informatika,self.angol,self.irodalom,self.nyelvtan,self.testneveles,self.matek,self.fizika = self.jegyek.strip(';')
        
        self.tortenelem = self.tantargy("tortenelem")
        self.informatika = self.tantargy("informatika")
        self.angol = self.tantargy("angol")
        self.irodalom = self.tantargy("irodalom")
        self.nyelvtan = self.tantargy("nyelvtan")
        self.testneveles = self.tantargy("testneveles")
        self.matek = self.tantargy("matek")
        self.fizika = self.tantargy("fizika")

        self.


    def tantargy(self, tantargy:str) -> list:
        list = []
        for jegy in self.tantargy:
            list.append(int(jegy))
        return list


    # def nevDiak(self, filename:str, nev:str) -> tuple:
    #     f = open(f"csv/{filename}", 'r', encoding= 'utf-8')
    #     elsodleges_kulcs = 'None'
    #     f.readline()
    #     for sor in f:
    #         splitted = sor.split(';')
    #         if nev == str(splitted[0]):
    #             self.nev = str(splitted[0])
    #             self.osztaly = splitted[1]
    #             self.email = splitted[2]
    #             self.jelszo = splitted[3]
    #             self.osztondij = int(splitted[4])
    #             return self.nev,self.osztaly,self.email,self.jelszo,self.osztondij
            
    #     f.close()


# nev;tortenelem;informatika;angol;irodalom;nyelvtan;testneveles;matek;fizika
# Kiss János;3,5,3;4,3,2;3,4,5;2,3,4;1,2,2,3;4,5,6;4,4,4;3,3
