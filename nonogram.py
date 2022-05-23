import random

class Nonogram (object):

    global PRAZNO
    global POLNO
    global NEZNANO
    global VRSTICE
    global STOLPCI
    global ST_VRSTIC
    global ST_STOLPCEV
    global igralnaPlosca

    PRAZNO = " "
    POLNO = "X"
    NEZNANO = "?"

    # srce (9x9)
    VRSTICE = [[2, 2],
               [4, 4],
               [9],
               [9],
               [7],
               [5],
               [3],
               [1],
               [0]]
    STOLPCI = [[3], [5], [6], [6], [6], [6], [6], [5], [3]]

    # slon (15x15)
    #VRSTICE = [[3],
    #           [4, 2],
    #           [6, 6],
    #           [1, 4, 2, 1],
    #           [6, 3, 2],
    #           [6, 7],
    #           [6, 8],
    #           [1, 10],
    #           [1, 10],
    #           [1, 10],
    #           [1, 1, 4, 4],
    #           [3, 4, 4],
    #           [4, 4],
    #           [4, 4],
    #           [4, 4]]
    #STOLPCI = [[1], [10], [2, 3, 1], [6, 2], [6], [15], [1, 4, 8], [2, 9], [14], [8], [1, 6], [1, 10], [1, 10], [1, 11], [12]]

    # opica (15x15)
    #VRSTICE = [[9],
    #           [11],
    #           [3, 2],
    #           [2, 2, 1],
    #           [1, 5, 2, 2, 1],
    #           [1, 3, 1, 1, 2],
    #           [2, 4, 2],
    #           [6, 2, 3],
    #           [4, 3],
    #           [3, 2],
    #           [5, 1, 1],
    #           [5, 2, 2],
    #           [6, 2],
    #           [8, 2],
    #           [12]]
    #STOLPCI = [[3, 2], [1, 2, 3], [2, 2, 5], [11], [14], [15], [3, 1, 2, 5], [2, 2], [2, 2, 1], [2, 1, 1, 2, 1], [2, 1, 1, 1], [2, 2, 2], [2, 1, 2, 3], [3, 8], [9]]

    # neresljiv primer
    #VRSTICE = [[5],
    #           [1, 1, 1],
    #           [1],
    #           [1],
    #           [1]]
    #STOLPCI = [[1, 2], [5], [1], [1], [1]]

    ST_VRSTIC = len(VRSTICE)
    ST_STOLPCEV = len(STOLPCI)
    igralnaPlosca = [[NEZNANO for x in range(ST_STOLPCEV)] for y in range(ST_VRSTIC)] # inicializacija igralne plosce

    def nakljucnoStanje (self, omejitveVrstic, omejitveStolpcev): # nakljucna resitev za vsako omejitev
        dolzinaVrstice = len(omejitveStolpcev)
        dolzinaStolpca = len(omejitveVrstic)
        resitevVrstice = []
        resitevStolpca = []
        for vrstica in omejitveVrstic:
            resitevVrstice.append(random.choice(self.permutacije(vrstica, dolzinaVrstice)))
        for stolpec in omejitveStolpcev:
            resitevStolpca.append(random.choice(self.permutacije(stolpec, dolzinaStolpca)))
        return resitevVrstice, resitevStolpca

    def permutacije (self, omejitve, dolzinaVrstice): # vse mozne permutacije v vrstici glede na podane omejitve
        bloki = POLNO * omejitve[0]
        dolzina = len(omejitve)
        if dolzina == 1:
            perm = []
            for i in range(dolzinaVrstice - omejitve[0] + 1):
                pred = PRAZNO * i
                za = PRAZNO * (dolzinaVrstice - i - omejitve[0])
                perm.append(pred + bloki + za)
            return perm
        perm = []
        for i in range(omejitve[0], dolzinaVrstice):
            for p in self.permutacije(omejitve[1:], dolzinaVrstice - i - 1):
                pred = PRAZNO * (i - omejitve[0])
                perm.append(pred + bloki + PRAZNO + p)
        return perm # vse mozne permutacije

    def nakljucnaVrstica (self, stVrstice):
        return random.choice(self.permutacije(VRSTICE[stVrstice], ST_VRSTIC))

    def preveriVrstico (self, stanje, vrstica): # preveri omejitev vrstice
        trenutnaVrstica = stanje[vrstica]
        return self.preveriOmejitev(VRSTICE, vrstica, trenutnaVrstica)

    def preveriStolpec (self, stanje, stolpec): # preveri omejitev stolpca
        trenutniStolpec = []
        for x in range(0, ST_VRSTIC):
            trenutniStolpec.append(stanje[x][stolpec])
        return self.preveriOmejitev(STOLPCI, stolpec, trenutniStolpec)

    def preveriOmejitev (self, seznamOmejitev, indeks, trenutno): # stevilo prekrsenih omejitev
        prekrseno = 0
        for omejitev in seznamOmejitev[indeks]:
            oznaka = False
            dolzina = len(trenutno)
            for i in range(0, dolzina):
                if trenutno[i] is POLNO:
                    stevec = 1
                    for j in range(i + 1, dolzina):
                        stevec += 1
                        if trenutno[j] is not POLNO:
                            stevec -= 1
                            break
                    if stevec == omejitev:
                        for a in range(0, omejitev):
                            trenutno[i + a] = PRAZNO
                        oznaka = True
                        break
                    else:
                        for a in range(0, stevec):
                            trenutno[i + a] = PRAZNO
                        break
            if oznaka is False:
                prekrseno += 1

        for polje in trenutno:
            if polje is POLNO:
                prekrseno += 1

        return prekrseno

    def preveriVse (self, resitev):
        stevec = 0
        for i in range(0, ST_STOLPCEV):
            stevec += self.preveriStolpec(resitev, i)
        return stevec

    def izpisiStanje (self, stanje): # seznam vrstic in stolpcev
        string  = ""
        for vrstica in stanje:
            string += str(vrstica)
            string += "\n"
        return string

    def omejitveVrstice (self):
        return VRSTICE
    
    def omejitveStolpca (self):
        return STOLPCI