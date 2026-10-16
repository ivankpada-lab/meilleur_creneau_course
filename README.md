# Meilleur créneau pour courir à Casablanca

Un petit programme Python qui interroge une API météo et propose, pour chacun des 7 prochains jours, le meilleur créneau pour courir en soirée.

## Le problème

Courir dehors dépend de la pluie, du vent et de la température, et ces conditions changent d'heure en heure. Plutôt que de consulter les prévisions à la main, le programme applique des critères précis et affiche un créneau par jour.

## Comment ça marche

1. **Récupération des données** : requête `GET` vers l'API [Open-Meteo](https://open-meteo.com/) (gratuite, sans clé d'API) pour obtenir les prévisions horaires de Casablanca : température, précipitations et vitesse du vent, sur 7 jours (168 heures).
2. **Mise en forme** : les données JSON sont converties en `DataFrame` pandas, avec des colonnes `jour` et `heure` extraites de la date.
3. **Filtre** : on ne garde que les heures qui respectent tous les critères :
   - aucune précipitation ;
   - vent inférieur à 20 km/h ;
   - température entre 15 et 25 °C ;
   - heure comprise entre 20 h et 23 h.
4. **Score** : chaque heure retenue reçoit un score, plus il est bas, meilleur est le créneau :
   `score = |température - 18| + vent / 5`
5. **Choix du meilleur créneau** : pour chaque jour (`groupby`), on garde l'heure au score le plus bas.
6. **Jours sans créneau** : si aucune heure d'un jour ne respecte les critères, le programme le signale.

Le code gère aussi les erreurs : un code de statut différent de 200 (`if` / `else`) et une coupure de connexion (`try` / `except`).

## Installation

```bash
git clone https://github.com/ivankpada-lab/meilleur_creneau_course.git
cd meilleur_creneau_course
pip install -r requirements.txt
```

## Utilisation

```bash
python meteo.py
```

## Exemple de sortie

```
2026-10-16 : 23h, 19.9 °C, vent 2.3 km/h
2026-10-17 : 23h, 20.9 °C, vent 5.8 km/h
2026-10-18 : 23h, 18.6 °C, vent 2.2 km/h
2026-10-19 : 23h, 18.0 °C, vent 4.3 km/h
2026-10-20 : 21h, 18.3 °C, vent 2.5 km/h
2026-10-21 : 22h, 18.0 °C, vent 5.9 km/h
2026-10-22 : 22h, 18.0 °C, vent 3.6 km/h
Tous les jours ont un créneau
```

Les valeurs dépendent de la date d'exécution, car les prévisions changent chaque jour.

## Personnaliser les critères

Tout se règle dans le filtre et dans la formule du score :

| Paramètre | Où le modifier |
|---|---|
| Fenêtre horaire | `df["heure"].between(20, 23)` |
| Température acceptée | `df["temperature_2m"].between(15, 25)` |
| Seuil de vent | `df["wind_speed_10m"] < 20` |
| Température idéale | le `18` dans la formule du score |
| Localisation | `latitude` et `longitude` dans `params` |

Pour changer de ville, il suffit de remplacer les coordonnées (par exemple depuis Google Maps : clic droit sur l'endroit voulu).

## Limites

- Le score est une règle simple choisie arbitrairement, pas un modèle validé : il favorise les heures proches de la température idéale avec peu de vent.
- La fenêtre 20 h - 23 h ne couvre pas la nuit après minuit.
- Les données sont des prévisions, donc moins fiables à mesure qu'on s'éloigne dans le temps.
- L'éclairage du parcours et la sécurité ne sont pas pris en compte.

## Technologies

Python, `requests`, `pandas`, API Open-Meteo.
