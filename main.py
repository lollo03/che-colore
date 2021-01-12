import io
import pandas as pd
import requests
from datetime import date, timedelta

regioni = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", "Molise", "P.A. Bolzano", "P.A. Trento", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", "Umbria", "Valle d'Aosta", "Veneto"]
abitanti = [1293941, 553254, 1894110, 5712143, 4464119, 1206216, 5755700, 1524826, 10027602, 1512672, 300516, 520891, 538223 ,4311217, 3953305, 4875290,4875290 ,3692555,870165,125034,4879133]
DATA_URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

r = requests.get(DATA_URL)
df = pd.read_csv(
    io.StringIO(r.text)
)

giorni = []
for i in range(1,8):
    giorni.append(str(date.today() - timedelta(days = i)))

dati = []
j=0
for regione in regioni:
    dati.append(0)
    for giorno in giorni:
        x = (df[df['data'].str.contains(giorno)])
        y = int(x[x['denominazione_regione'].str.contains(regione)].nuovi_positivi)
        dati[j] = dati[j] + y
    dati[j] = round((dati[j] / (abitanti[j]/100000)), 1)
    j+=1

#print(dati)


#Generate template
with open("template.html", "r+") as f:
    with open("index.html", "w+") as wf:
        for line in f.read().splitlines():
            #if "<!-- totalVaccinations -->" in line:
            #    line = f"{totalVaccines}"
            if "<!--" in line:
                x = line.split("<!-- ")[1].split(" -->")[0]
                j=0
                for regione in regioni:
                    if regione.find(x) != -1:
                        line = f"{dati[j]},"
                    j+=1
                    
            wf.write("\n" + line)
