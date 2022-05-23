import random
import operator
import time
from nonogram import Nonogram
from resitev import Resitev

class GenetskiAlgoritem (object):

    global nonogram
    global populacija
    global fitness # stevilo omejitev, ki zadostijo igralni plosci
    global VRSTICE
    global STOLPCI
    global ST_VRSTIC
    global ST_STOLPCEV
    global VELIKOST_POPULACIJE
    global VERJETNOST_MUTACIJE
    global VERJETNOST_CROSSOVER

    nonogram = Nonogram()
    populacija = []
    fitness = []

    VRSTICE = nonogram.omejitveVrstice()
    STOLPCI = nonogram.omejitveStolpca()
    ST_VRSTIC = len(VRSTICE)
    ST_STOLPCEV = len(STOLPCI)

    VELIKOST_POPULACIJE = 300
    VERJETNOST_MUTACIJE = 3
    VERJETNOST_CROSSOVER = 65

    def generirajPopulacijo (self): # nakljucna populacija primernih resitev, glede na omejitve vrstic
        populacija = []
        for x in range(0, VELIKOST_POPULACIJE):
            stanje = nonogram.nakljucnoStanje(VRSTICE, STOLPCI)
            populacija.append(stanje[0])
        return populacija
    
    def oceniFitness (self, populacija): # fitness za vsako resitev v populaciji
        fitness = []
        for x in populacija:
            fitness.append(nonogram.preveriVse(x))
        return fitness

    def selekcija (self, pari): # glede na fitness izberi 2 resitvi
        urejeniPari = sorted(pari, key=operator.attrgetter('fitness'))
        izbrani = [urejeniPari[0].dobiStanje(), urejeniPari[1].dobiStanje()]
        return izbrani

    def crossover (self, starsi): # crossover preko starsev -> nov otrok
        verjetnost = random.randint(0, 100)
        if verjetnost < VERJETNOST_CROSSOVER:
            crossoverTocka = random.randint(0, ST_VRSTIC)
            otrok = []
            for i in range(0, crossoverTocka): # kopiraj od prvega starsa vse pred nakljucno tocko 'crossoverTocka'
                otrok.append(starsi[0][i])
            for i in range(crossoverTocka, ST_VRSTIC): # kopiraj od drugega starsa vse za nakljucno tocko 'crossoverTocka'
                otrok.append(starsi[1][i])
        else:
            otrok = starsi[0]
        return otrok

    def mutacija (self, otrok): # mutiraj novega otroka z vsako pozicijo zacetne populacije
        novOtrok = []
        for i in range(0, ST_VRSTIC):
            verjetnost = random.randint(0, 100)
            if verjetnost <= VERJETNOST_MUTACIJE:
                rand = nonogram.nakljucnaVrstica(i)
                novOtrok.append(rand)
            else:
                novOtrok.append(otrok[i])
        return novOtrok
        
    def ustvariNovoPopulacijo (self, pari):
        novaPopulacija = []
        starsi = self.selekcija(pari) # selekcija
        while len(novaPopulacija) <= VELIKOST_POPULACIJE:
            cross = self.crossover(starsi) # crossover
            otrok = self.mutacija(cross) # mutacija
            novaPopulacija.append(otrok) # potrditev
        #print("Starsi so\n")
        #print(nonogram.izpisiStanje(starsi[0]))
        #print("\n\n")
        #print(nonogram.izpisiStanje(starsi[1]))
        #print("\n\n")
        return novaPopulacija

    def preveriKoncno (self, populacija): # vrne resitev, ce ni nobenih krsitev
        for resitev in populacija:
            if nonogram.preveriVse(resitev) == 0:
                return resitev
        return None

    def zdruzi (self, populacija, fitness): # zdruzi vsako resitev z njenim fitness-om
        pari = []
        dolzina = len(populacija)
        for i in range(0, dolzina):
            resitev = Resitev(populacija[i], fitness[i])
            pari.append(resitev)
        return pari
    
    def __init__(self):
        global VERJETNOST_MUTACIJE
        global populacija
        global fitness

        VERJETNOST_MUTACIJE = 30

        zacetek = time.time()

        populacija = self.generirajPopulacijo() # nakljucna populacija

        # vrni najboljso resitev trenutne populacije
        oznaka = None
        stevec = 0
        while oznaka is None:
            stevec += 1
            fitness = self.oceniFitness(populacija)
            pari = self.zdruzi(populacija, fitness)
            populacija = self.ustvariNovoPopulacijo(pari)
            oznaka = self.preveriKoncno(populacija) # preveri, ce je zadosceno koncnemu pogoju

            konec = time.time()
            casIzvajanja = konec - zacetek

        print("Čas izvajanja: %s" % casIzvajanja)
        print("Število iteracij: %s" % stevec)
        print("\n")
        print(nonogram.izpisiStanje(oznaka))

GenetskiAlgoritem()