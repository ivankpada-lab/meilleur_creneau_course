import requests
import pandas as pd
import sys
sys.stdout.reconfigure(encoding="utf-8")

url = "https://api.open-meteo.com/v1/forecast"
params = {"latitude": 33.5731, "longitude": -7.5898,
          "hourly": "temperature_2m,precipitation,wind_speed_10m"}

try:
    reponse = requests.get(url, params=params)
    if reponse.status_code == 200:
        donnees = reponse.json()

        df = pd.DataFrame(donnees["hourly"])
        df["time"] = pd.to_datetime(df["time"])
        df["heure"] = df["time"].dt.hour
        df["jour"] = df["time"].dt.date
        df["score"] = (df["temperature_2m"] - 18).abs() + df["wind_speed_10m"] / 5

        bons_creneaux = df[(df["precipitation"] == 0)
                           & (df["wind_speed_10m"] < 20)
                           & (df["temperature_2m"].between(15, 25))
                           & (df["heure"].between(20, 23))]

        meilleurs = bons_creneaux.loc[bons_creneaux.groupby("jour")["score"].idxmin()]

        for _, ligne in meilleurs.iterrows():
            print(f"{ligne['jour']} : {ligne['heure']}h, {ligne['temperature_2m']} °C, vent {ligne['wind_speed_10m']} km/h")

        jours_sans_creneaux=set(df["jour"].unique())-set(meilleurs["jour"])
        if jours_sans_creneaux:
            for jour in sorted(jours_sans_creneaux):
                print(f"{jour} : Aucun créneau")

        else:
            print("Tous les jours ont un créneau")
        
    else:
        print("Echec de la requete, code :", reponse.status_code)
except requests.exceptions.ConnectionError:
    print("Erreur de connexion")



