import math
import random
from datetime import datetime
import pandas as pd

radius = float(input("Type in uber number: "))

area = math.pi * radius**2
circumference = 2 * math.pi * radius

print(area)
print(circumference)


#============================#

names_list = ["Apple", "Banaan", "Lennon"]

def random_names(names_list):
    return random.choice(names_list)

print(random_names(names_list))



#==========#

def get_date_difference(date1, date2):
    format_str = "%Y-%m-%d"
    d1 = datetime.strptime(date1, format_str)
    d2 = datetime.strptime(date2, format_str)
    return abs(d1 - d2)

print(get_date_difference("2015-02-24", "2024-02-24"))


#==========#
df = pd.read_csv("vgsales.csv")
print(df.head(10))
print(df.groupby("Name").sum(numeric_only=True))