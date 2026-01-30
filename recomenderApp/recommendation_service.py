import pickle
import os
import pandas as pd
import numpy as np
from django.conf import settings

class ModelNotFoundError(Exception):
    pass

class TravelRecommendationService:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'Machine_learning/models/travel_knn_model.pkl')
        self.package = self._load_package()
        
        # Extraction des composants du package
        self.knn = self.package['knn_model']
        self.kmeans = self.package['kmeans_model']
        self.scaler = self.package['scaler']
        self.df = self.package['destinations_data']
        self.features = self.package['feature_columns']

    def _load_package(self):
        if not os.path.exists(self.model_path):
            raise ModelNotFoundError("Fichier modèle .pkl introuvable.")
        with open(self.model_path, 'rb') as f:
            return pickle.load(f)

    def get_recommendations(self, user_preferences, n_recommendations=5, apply_hard_filters=True):
        """Utilisé par POST /api/recommendations/generate/"""
        working_df = self.df.copy()

        # 1. Filtres stricts (Budget et Sécurité)
        if apply_hard_filters:
            if 'budget_max' in user_preferences:
                working_df = working_df[working_df['budget_per_day_usd'] <= user_preferences['budget_max']]
            if 'min_safety_score' in user_preferences:
                working_df = working_df[working_df['safety_score'] >= user_preferences['min_safety_score']]

        if working_df.empty:
            return []

        # 2. Préparation du vecteur utilisateur
        user_vector = [user_preferences.get(col, 0.5) for col in self.features]
        user_scaled = self.scaler.transform([user_vector])

        # 3. Calcul KNN
        # On cherche un peu plus de voisins pour compenser les filtres
        n_neighbors = min(len(working_df), n_recommendations * 2)
        distances, indices = self.knn.kneighbors(user_scaled, n_neighbors=n_neighbors)

        recommendations = []
        for dist, idx in zip(distances[0], indices[0]):
            # Sécurité : vérifier si l'index existe toujours dans le DF filtré
            if idx not in working_df.index: continue
            
            row = working_df.loc[idx]
            sim_score = 1 / (1 + dist)
            
            # Pondération : 70% similarité, 30% popularité (Défi 4.4.5)
            rel_score = (sim_score * 0.7) + ((row.get('popularity_score', 5)/10) * 0.3)

            recommendations.append({
                'destination_id': int(row.get('destination_id', idx)),
                'similarity_score': float(sim_score),
                'relevance_score': float(rel_score)
            })

        # Tri par pertinence et retour des N premiers
        return sorted(recommendations, key=lambda x: x['relevance_score'], reverse=True)[:n_recommendations]

    def find_similar_destinations(self, destination_id, n_similar=5):
        """Utilisé par GET /api/destinations/{id}/similar/"""
        # Trouver la destination cible
        target_row = self.df[self.df['destination_id'] == destination_id]
        if target_row.empty: return []

        # Préparer le vecteur de la destination
        target_vec = target_row[self.features]
        target_scaled = self.scaler.transform(target_vec)

        # Chercher les voisins
        distances, indices = self.knn.kneighbors(target_scaled, n_neighbors=n_similar + 1)

        similar = []
        for dist, idx in zip(distances[0][1:], indices[0][1:]): # On saute le premier (lui-même)
            row = self.df.iloc[idx]
            similar.append({
                'destination_id': int(row.get('destination_id', idx)),
                'city': row['city'],
                'country': row['country'],
                'similarity_score': float(1 / (1 + dist))
            })
        return similar

    def get_cluster_analysis(self):
        """Utilisé par GET /api/destinations/clusters/"""
        analysis = {}
        for cluster_id in range(self.kmeans.n_clusters):
            cluster_data = self.df[self.df['cluster'] == cluster_id]
            analysis[f"cluster_{cluster_id}"] = {
                "size": len(cluster_data),
                "avg_budget": round(cluster_data['budget_per_day_usd'].mean(), 2),
                "top_destinations": cluster_data.nlargest(3, 'popularity_score')[['city', 'country']].to_dict(orient='records')
            }
        return analysis

    def get_model_info(self):
        return {
            "model_type": "K-Nearest Neighbors",
            "n_destinations": len(self.df),
            "features_used": self.features,
            "n_clusters": self.kmeans.n_clusters
        }