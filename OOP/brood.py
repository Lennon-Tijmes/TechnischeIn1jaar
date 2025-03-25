def print_broodtrommel(kleur, lengte, breedte, hoogte, brand, inhoud):
    result = "== BROODTROMMEL FABRIEK\n"
    result += f"Kleur: {lengte}\n"
    result += f"Kleur: {breedte}\n"
    result += f"Kleur: {hoogte}\n"
    result += f"Kleur: {brand}\n"
    result += f"Kleur: {inhoud}\n"
    return result

kleur1 = "roze"
lengte1 = "21,5"
breedte1= "16,4"
hoogte1 = "7"
brand1 = "curve"
inhoud1 = "leeg"

kleur2 = "cyan"
lengte2 = "11,8"
breedte2 = "9"
hoogte2 = "5"
brand2 = "lidl"
inhoud2 = "mentos kauwgom"

kleur3 = "oud roze"
lengte3 = "24,5"
breedte3 = "15,3"
hoogte3 = "8"
brand3 = "naamloos"
inhoud3 = "6 plakjes brood"

trommel1 = (kleur1, lengte1, breedte1, hoogte1, brand1, inhoud1)
trommel2 = (kleur2, lengte2, breedte2, hoogte2, brand2, inhoud2)
trommel3 = (kleur3, lengte3, breedte3, hoogte3, brand3, inhoud3)

trommels = [trommel1, trommel2, trommel3]

print("De procedural trommel fabriek")
print("1 voor 1")
print(print_broodtrommel(*trommel1))
print(print_broodtrommel(*trommel2))
print(print_broodtrommel(*trommel3))