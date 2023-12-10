from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Bicikli(ABC):
    def __init__(self, tipus, ar, allapot="Elérhető"):
        self.tipus = tipus
        self.ar = ar
        self.allapot = allapot

    @abstractmethod
    def leiras(self):
        pass

class OrszagutiBicikli(Bicikli):
    def leiras(self):
        return f"Országúti bicikli - Típus: {self.tipus}, Ár: {self.ar} Ft/nap, Állapot: {self.allapot}"

class HegyiBicikli(Bicikli):
    def leiras(self):
        return f"Hegyi bicikli - Típus: {self.tipus}, Ár: {self.ar} Ft/nap, Állapot: {self.allapot}"

class VarosiBicikli(Bicikli):
    def leiras(self):
        return f"Városi bicikli - Típus: {self.tipus}, Ár: {self.ar} Ft/nap, Állapot: {self.allapot}"

class BMX(Bicikli):
    def leiras(self):
        return f"Bmx - Típus: {self.tipus}, Ár: {self.ar} Ft/nap, Állapot: {self.allapot}"

class Kolcsonzes:
    def __init__(self, bicikli, datum):
        self.bicikli = bicikli
        self.datum = datum

    def __str__(self):
        return f"{self.bicikli.leiras()} - Kölcsönzés időpontja: {self.datum}"

class Kolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.biciklik = []
        self.kolcsonzesek = []

    def bicikli_hozzaad(self, bicikli):
        self.biciklik.append(bicikli)

    def kolcsonoz(self, bicikli, datum):
        if bicikli in self.biciklik and bicikli.allapot == "Elérhető" and datum >= datetime.now():
            kolcsonzes = Kolcsonzes(bicikli, datum)
            self.kolcsonzesek.append(kolcsonzes)
            bicikli.allapot = "Kölcsönzés alatt"
            return kolcsonzes
        else:
            return None

    def kolcsonzes_lemondasa(self, kolcsonzes):
        if kolcsonzes in self.kolcsonzesek and kolcsonzes.datum > datetime.now():
            kolcsonzes.bicikli.allapot = "Elérhető"
            self.kolcsonzesek.remove(kolcsonzes)
            return True
        else:
            return False

    def kolcsonzesek_listazasa(self):
        for kolcsonzes in self.kolcsonzesek:
            print(kolcsonzes)

def tesztadatok_feltoltese():
    bicikli1 = OrszagutiBicikli("Neuzer", 15000)
    bicikli2 = HegyiBicikli("Cannondale", 13500)
    bicikli3 = VarosiBicikli("Cruiser", 10000)
    bicikli4 = BMX("Mongoose", 7500)

    kolcsonzo = Kolcsonzo("BikeRental")
    kolcsonzo.bicikli_hozzaad(bicikli1)
    kolcsonzo.bicikli_hozzaad(bicikli2)
    kolcsonzo.bicikli_hozzaad(bicikli3)
    kolcsonzo.bicikli_hozzaad(bicikli4)

    kolcsonzo.kolcsonoz(bicikli1, datetime.now() + timedelta(days=1))
    kolcsonzo.kolcsonoz(bicikli2, datetime.now() + timedelta(days=2))
    kolcsonzo.kolcsonoz(bicikli3, datetime.now() + timedelta(days=3))
    kolcsonzo.kolcsonoz(bicikli4, datetime.now() + timedelta(days=4))

    return kolcsonzo

def main():
    kolcsonzo = tesztadatok_feltoltese()

    while True:
        print("\nBiciklikölcsönző rendszer")
        print("1. Biciklik listázása")
        print("2. Bicikli kölcsönzése")
        print("3. Kölcsönzések listázása")
        print("4. Kölcsönzés lemondása")
        print("5. Kilépés")

        valasztas = input("Válassz egy menüpontot: ")

        if valasztas == "1":
            print("\nBiciklik:")
            for bicikli in kolcsonzo.biciklik:
                print(bicikli.leiras())

        elif valasztas == "2":
            bicikli_nev = input("Add meg a bicikli típusát: ")
            datum_str = input("Add meg a kölcsönzés dátumát (ÉÉÉÉ-HH-NN): ")

            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
            except ValueError:
                print("Hibás dátumformátum!")
                continue

            for bicikli in kolcsonzo.biciklik:
                if bicikli.tipus == bicikli_nev:
                    kolcsonzo.kolcsonoz(bicikli, datum)
                    print("Sikeres kölcsönzés!")
                    break
            else:
                print("Nincs ilyen típusú bicikli.")

        elif valasztas == "3":
            print("\nKölcsönzések:")
            kolcsonzo.kolcsonzesek_listazasa()

        elif valasztas == "4":
            print("\nKölcsönzés lemondása:")
            for i, kolcsonzes in enumerate(kolcsonzo.kolcsonzesek):
                print(f"{i + 1}. {kolcsonzes}")

            lemondas_index = input("Válassz egy kölcsönzést a lemondáshoz (szám): ")

            try:
                lemondas_index = int(lemondas_index)
                if 1 <= lemondas_index <= len(kolcsonzo.kolcsonzesek):
                    if kolcsonzo.kolcsonzes_lemondasa(kolcsonzo.kolcsonzesek[lemondas_index - 1]):
                        print("Sikeres kölcsönzés lemondás!")
                    else:
                        print("Hibás kölcsönzési információ vagy a kölcsönzés már lejárt.")
                else:
                    print("Érvénytelen sorszám.")
            except ValueError:
                print("Érvénytelen input. Kérlek, válassz számot.")

        elif valasztas == "5":
            print("Kilépés.")
            break

        else:
            print("Érvénytelen választás. Kérlek, válassz egy érvényes menüpontot.")

if __name__ == "__main__":
    main()
