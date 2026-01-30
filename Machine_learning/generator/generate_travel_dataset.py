import pandas as pd
import numpy as np
import random
from datetime import datetime

# Configuration du seed pour la reproductibilité
np.random.seed(42)
random.seed(42)

# Listes de données pour générer le dataset
cities = [
    "Paris", "Londres", "New York", "Tokyo", "Barcelone", "Rome", "Amsterdam",
    "Bangkok", "Dubaï", "Sydney", "Bali", "Singapour", "Istanbul", "Berlin",
    "Prague", "Vienne", "Budapest", "Lisbonne", "Athènes", "Dublin", "Édimbourg",
    "Copenhague", "Stockholm", "Oslo", "Helsinki", "Reykjavik", "Zurich",
    "Marrakech", "Le Caire", "Cape Town", "Nairobi", "Casablanca", "Tunis",
    "Rio de Janeiro", "Buenos Aires", "Lima", "Mexico City", "Cancún", "Bogotá",
    "Santiago", "Quito", "La Havane", "San José", "Panama City",
    "Los Angeles", "Miami", "Las Vegas", "San Francisco", "Seattle", "Chicago",
    "Boston", "Washington DC", "Vancouver", "Toronto", "Montréal",
    "Pékin", "Shanghai", "Hong Kong", "Séoul", "Hanoi", "Ho Chi Minh",
    "Kuala Lumpur", "Jakarta", "Manille", "Mumbai", "Delhi", "Bangalore",
    "Dubaï", "Doha", "Abu Dhabi", "Tel Aviv", "Jérusalem",
    "Melbourne", "Auckland", "Queenstown", "Fiji", "Tahiti",
    "Venise", "Florence", "Milan", "Naples", "Santorini", "Mykonos",
    "Dubrovnik", "Split", "Porto", "Séville", "Madrid", "Valence",
    "Bruges", "Genève", "Monaco", "Luxembourg", "Malte",
    "Kyoto", "Osaka", "Phuket", "Chiang Mai", "Siem Reap", "Luang Prabang"
]

countries = [
    "France", "Royaume-Uni", "États-Unis", "Japon", "Espagne", "Italie",
    "Pays-Bas", "Thaïlande", "Émirats Arabes Unis", "Australie", "Indonésie",
    "Singapour", "Turquie", "Allemagne", "République Tchèque", "Autriche",
    "Hongrie", "Portugal", "Grèce", "Irlande", "Écosse", "Danemark", "Suède",
    "Norvège", "Finlande", "Islande", "Suisse", "Maroc", "Égypte",
    "Afrique du Sud", "Kenya", "Maroc", "Tunisie", "Brésil", "Argentine",
    "Pérou", "Mexique", "Mexique", "Colombie", "Chili", "Équateur", "Cuba",
    "Costa Rica", "Panama", "États-Unis", "États-Unis", "États-Unis",
    "États-Unis", "États-Unis", "États-Unis", "États-Unis", "États-Unis",
    "Canada", "Canada", "Canada", "Chine", "Chine", "Hong Kong", "Corée du Sud",
    "Vietnam", "Vietnam", "Malaisie", "Indonésie", "Philippines", "Inde",
    "Inde", "Inde", "Émirats Arabes Unis", "Qatar", "Émirats Arabes Unis",
    "Israël", "Israël", "Australie", "Nouvelle-Zélande", "Nouvelle-Zélande",
    "Fidji", "Polynésie Française", "Italie", "Italie", "Italie", "Italie",
    "Grèce", "Grèce", "Croatie", "Croatie", "Portugal", "Espagne", "Espagne",
    "Espagne", "Belgique", "Suisse", "Monaco", "Luxembourg", "Malte", "Japon",
    "Japon", "Thaïlande", "Thaïlande", "Cambodge", "Laos"
]

continents = [
    "Europe", "Europe", "Amérique du Nord", "Asie", "Europe", "Europe", "Europe",
    "Asie", "Asie", "Océanie", "Asie", "Asie", "Asie", "Europe", "Europe",
    "Europe", "Europe", "Europe", "Europe", "Europe", "Europe", "Europe", "Europe",
    "Europe", "Europe", "Europe", "Europe", "Afrique", "Afrique", "Afrique",
    "Afrique", "Afrique", "Afrique", "Amérique du Sud", "Amérique du Sud",
    "Amérique du Sud", "Amérique du Nord", "Amérique du Nord", "Amérique du Sud",
    "Amérique du Sud", "Amérique du Sud", "Amérique du Nord", "Amérique du Nord",
    "Amérique du Nord", "Amérique du Nord", "Amérique du Nord", "Amérique du Nord",
    "Amérique du Nord", "Amérique du Nord", "Amérique du Nord", "Amérique du Nord",
    "Amérique du Nord", "Amérique du Nord", "Amérique du Nord", "Amérique du Nord",
    "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Asie",
    "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Asie", "Océanie",
    "Océanie", "Océanie", "Océanie", "Océanie", "Europe", "Europe", "Europe",
    "Europe", "Europe", "Europe", "Europe", "Europe", "Europe", "Europe",
    "Europe", "Europe", "Europe", "Europe", "Europe", "Europe", "Europe",
    "Asie", "Asie", "Asie", "Asie", "Asie", "Asie"
]

# Fonction pour générer des températures moyennes réalistes
def generate_temperature(continent):
    if continent == "Europe":
        return round(random.uniform(8, 22), 1)
    elif continent == "Asie":
        return round(random.uniform(18, 32), 1)
    elif continent == "Afrique":
        return round(random.uniform(22, 35), 1)
    elif continent == "Amérique du Nord":
        return round(random.uniform(10, 28), 1)
    elif continent == "Amérique du Sud":
        return round(random.uniform(20, 30), 1)
    elif continent == "Océanie":
        return round(random.uniform(18, 26), 1)
    return round(random.uniform(15, 25), 1)

# Fonction pour générer des budgets réalistes
def generate_budget():
    budget_ranges = [
        (500, 1000),   # Budget économique
        (1000, 2000),  # Budget moyen
        (2000, 4000),  # Budget confortable
        (4000, 8000)   # Budget luxe
    ]
    range_choice = random.choice(budget_ranges)
    return round(random.uniform(range_choice[0], range_choice[1]), 2)

# Génération du dataset
data = []

for i in range(len(cities)):
    city = cities[i]
    country = countries[i]
    continent = continents[i]
    
    # Caractéristiques de base
    avg_temperature = generate_temperature(continent)
    budget_per_day = generate_budget()
    
    # Activités disponibles (score 0-1)
    beach = random.uniform(0, 1) if continent in ["Océanie", "Asie", "Amérique du Sud"] else random.uniform(0, 0.5)
    mountain = random.uniform(0, 1) if continent in ["Europe", "Amérique du Sud", "Asie"] else random.uniform(0, 0.4)
    culture = random.uniform(0.5, 1) if continent == "Europe" else random.uniform(0.3, 0.8)
    adventure = random.uniform(0, 1)
    nightlife = random.uniform(0, 1)
    shopping = random.uniform(0.3, 1)
    nature = random.uniform(0, 1)
    historical = random.uniform(0.5, 1) if continent in ["Europe", "Asie"] else random.uniform(0.2, 0.7)
    family_friendly = random.uniform(0.4, 1)
    romantic = random.uniform(0.3, 0.9)
    
    # Critères pratiques
    safety_score = round(random.uniform(6, 10), 1)
    english_spoken = random.uniform(0.3, 1)
    visa_required = random.choice([0, 1])
    
    # Climat
    climate_type = random.choice([
        "Tropical", "Tempéré", "Continental", "Méditerranéen", 
        "Désertique", "Océanique", "Subtropical"
    ])
    
    # Saison idéale (1-12 pour les mois)
    best_season_start = random.randint(1, 12)
    best_season_end = (best_season_start + random.randint(2, 5)) % 12 + 1
    
    # Popularité et rating
    popularity_score = round(random.uniform(5, 10), 1)
    average_rating = round(random.uniform(3.5, 5.0), 1)
    number_of_reviews = random.randint(50, 5000)
    
    # Informations supplémentaires
    cost_level = "Low" if budget_per_day < 1000 else "Medium" if budget_per_day < 2500 else "High" if budget_per_day < 5000 else "Luxury"
    tourist_density = random.choice(["Low", "Medium", "High", "Very High"])
    
    # Création de l'enregistrement
    record = {
        "destination_id": i + 1,
        "city": city,
        "country": country,
        "continent": continent,
        "avg_temperature": avg_temperature,
        "budget_per_day_usd": budget_per_day,
        "beach": round(beach, 2),
        "mountain": round(mountain, 2),
        "culture": round(culture, 2),
        "adventure": round(adventure, 2),
        "nightlife": round(nightlife, 2),
        "shopping": round(shopping, 2),
        "nature": round(nature, 2),
        "historical": round(historical, 2),
        "family_friendly": round(family_friendly, 2),
        "romantic": round(romantic, 2),
        "safety_score": safety_score,
        "english_spoken": round(english_spoken, 2),
        "visa_required": visa_required,
        "climate_type": climate_type,
        "best_season_start": best_season_start,
        "best_season_end": best_season_end,
        "popularity_score": popularity_score,
        "average_rating": average_rating,
        "number_of_reviews": number_of_reviews,
        "cost_level": cost_level,
        "tourist_density": tourist_density,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data.append(record)

# Création du DataFrame
df = pd.DataFrame(data)

# Affichage des informations
print("=" * 80)
print("DATASET DE DESTINATIONS DE VOYAGE GÉNÉRÉ")
print("=" * 80)
print(f"\nNombre total de destinations: {len(df)}")
print(f"\nColonnes générées: {len(df.columns)}")
print("\nListe des colonnes:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\n" + "=" * 80)
print("STATISTIQUES DU DATASET")
print("=" * 80)
print(f"\nBudget moyen par jour: ${df['budget_per_day_usd'].mean():.2f}")
print(f"Budget minimum: ${df['budget_per_day_usd'].min():.2f}")
print(f"Budget maximum: ${df['budget_per_day_usd'].max():.2f}")
print(f"\nTempérature moyenne: {df['avg_temperature'].mean():.1f}°C")
print(f"Température minimum: {df['avg_temperature'].min():.1f}°C")
print(f"Température maximum: {df['avg_temperature'].max():.1f}°C")

print("\n" + "=" * 80)
print("APERÇU DES PREMIÈRES LIGNES")
print("=" * 80)
print(df.head(10).to_string())

print("\n" + "=" * 80)
print("DISTRIBUTION PAR CONTINENT")
print("=" * 80)
print(df['continent'].value_counts())

print("\n" + "=" * 80)
print("DISTRIBUTION PAR NIVEAU DE COÛT")
print("=" * 80)
print(df['cost_level'].value_counts())

# Sauvegarde du dataset en plusieurs formats
df.to_csv('travel_destinations_dataset.csv', index=False, encoding='utf-8')


print("\n" + "=" * 80)
print("FICHIERS GÉNÉRÉS")
print("=" * 80)
print("✓ travel_destinations_dataset.csv")


# Génération d'un dataset de préférences utilisateurs (exemple)
print("\n" + "=" * 80)
print("GÉNÉRATION DU DATASET DE PRÉFÉRENCES UTILISATEURS")
print("=" * 80)

user_preferences = []
for i in range(50):
    user_pref = {
        "user_id": i + 1,
        "budget_min": round(random.uniform(300, 2000), 2),
        "budget_max": round(random.uniform(2000, 10000), 2),
        "preferred_temperature_min": round(random.uniform(10, 20), 1),
        "preferred_temperature_max": round(random.uniform(20, 35), 1),
        "beach_preference": round(random.uniform(0, 1), 2),
        "mountain_preference": round(random.uniform(0, 1), 2),
        "culture_preference": round(random.uniform(0, 1), 2),
        "adventure_preference": round(random.uniform(0, 1), 2),
        "nightlife_preference": round(random.uniform(0, 1), 2),
        "shopping_preference": round(random.uniform(0, 1), 2),
        "nature_preference": round(random.uniform(0, 1), 2),
        "historical_preference": round(random.uniform(0, 1), 2),
        "family_friendly_preference": round(random.uniform(0, 1), 2),
        "romantic_preference": round(random.uniform(0, 1), 2),
        "min_safety_score": round(random.uniform(5, 8), 1),
        "visa_flexibility": random.choice([0, 1]),
        "preferred_continents": random.sample(["Europe", "Asie", "Amérique du Nord", "Amérique du Sud", "Afrique", "Océanie"], random.randint(1, 3)),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    user_preferences.append(user_pref)

df_users = pd.DataFrame(user_preferences)
df_users.to_csv('user_preferences_dataset.csv', index=False, encoding='utf-8')
df_users.to_json('user_preferences_dataset.json', orient='records', indent=2)

print(f"\nNombre d'utilisateurs: {len(df_users)}")
print("✓ user_preferences_dataset.csv")
print("✓ user_preferences_dataset.json")


print("\n" + "=" * 80)
print("GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
print("=" * 80)
