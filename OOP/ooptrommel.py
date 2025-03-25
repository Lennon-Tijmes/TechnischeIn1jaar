class Trommel:
    def __init__(self, kleur, lengte, breedte, hoogte, brand, inhoud):
        self.kleur = kleur
        self.lengte = lengte
        self.breedte = breedte
        self.hoogte = hoogte
        self.brand = brand
        self.inhoud = inhoud


    def print_info(self):
        result = "== BROODTROMMEL FABRIEK\n"
        result += f"Kleur: {self.lengte}\n"
        result += f"Kleur: {self.breedte}\n"
        result += f"Kleur: {self.hoogte}\n"
        result += f"Kleur: {self.brand}\n"
        result += f"Kleur: {self.inhoud}\n"
        return result

trommel1 = Trommel("roze", "21,5", "16,4", "7", "curve", "leeg")
trommel2 = Trommel("cyan", "11,8", "9", "5", "lidl", "mentos kauwgom")
trommel3 = Trommel("oud roze", "24,5", "15,3", "8", "naamloos", "6 plakjes brood")

trommels = [trommel1, trommel2, trommel3]

for trommel in trommels:
    print(trommel.print_info())