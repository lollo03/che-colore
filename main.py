import io
import pandas as pd
import requests
from datetime import datetime, timedelta, date
from pytz import timezone

regioni = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardia",
           "Marche", "Molise", "P.A. Bolzano", "P.A. Trento", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", "Umbria", "Valle d'Aosta", "Veneto"]
abitanti = [1285256, 547579, 1877728, 5679759, 4445549, 1198753, 5720796, 1509805, 9966992, 1501406,
            296547, 533715, 544745, 4273210, 3926931, 1598225, 4840876, 3668333, 865013, 123895, 4852453]
DATA_URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

r = requests.get(DATA_URL)
df = pd.read_csv(
    io.StringIO(r.text)
)

giorni = []
for i in range(1, 8):
    giorni.append(str(date.today() - timedelta(days=i)))

dati = []
j = 0
for regione in regioni:
    dati.append(0)
    for giorno in giorni:
        x = (df[df['data'].str.contains(giorno)])
        y = int(x[x['denominazione_regione'].str.contains(regione)].nuovi_positivi)
        dati[j] = dati[j] + y
    dati[j] = round((dati[j] / (abitanti[j]/100000)), 1)
    j += 1

# print(dati)


# Generate template
with open("template.html", "r+") as f:
    with open("index.html", "w+") as wf:
        for line in f.read().splitlines():
            # if "<!-- totalVaccinations -->" in line:
            #    line = f"{totalVaccines}"
            if "<!--" in line:
                x = line.split("<!-- ")[1].split(" -->")[0]
                j = 0
                for regione in regioni:
                    if regione.find(x) != -1:
                        line = f"{dati[j]},"
                    j += 1
            if "<!-- data_ora -->" in line:
                line = f"{datetime.now(timezone('Europe/rome')).strftime('%d/%m/%Y alle %H:%M')}"
            wf.write("\n" + line)
