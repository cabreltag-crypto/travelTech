from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from .models import Destination, UserPreference, Recommendation
from .serializers import (
    DestinationSerializer, 
    UserPreferenceSerializer, 
    RecommendationSerializer
)
from .utils import TravelRecommendationService

# Initialisation globale du service pour éviter de recharger le .pkl à chaque requête
recommendation_service = TravelRecommendationService()

feature_columns = [
    'budget_per_day_usd', 'avg_temperature',
    'beach', 'mountain', 'culture', 'adventure',
    'nightlife', 'shopping', 'nature', 'historical',
    'family_friendly', 'romantic', 'safety_score'
]


class GenerateRecommendationsView(APIView):
    """
    POST /api/recommendations/generate/
    Récupère les préférences de l'utilisateur et génère des recommandations via KNN.
    
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        #  Récupérer les préférences utilisateur
        try:
            prefs = user.preference  # OneToOneField UserPreference
        except UserPreference.DoesNotExist:
            return Response(
                {"error": "Préférences utilisateur non trouvées"},
                status=status.HTTP_404_NOT_FOUND
            )

        #  Construire le dictionnaire des préférences pour le service KNN
        user_data = {col: getattr(prefs, col, 0.5) for col in feature_columns}

        #  Appel du service KNN pour générer les recommandations
        results = recommendation_service.get_recommendations(user_data)

        #  Sauvegarder les nouvelles recommandations sans supprimer les anciennes
        created_recs = []
        for item in results:
            try:
                dest = Destination.objects.get(id=item['destination_id'])
                rec = Recommendation.objects.create(
                    user=user,
                    destination=dest,
                    similarity_score=item['similarity_score'],
                    relevance_score=item['relevance_score']
                )
                created_recs.append(rec)
            except Destination.DoesNotExist:
                continue  

        #  Sérialisation et retour
        serializer = RecommendationSerializer(created_recs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class SimilarDestinationsView(APIView):
    """
    GET /api/destinations/similar/{id}/
    Trouve des destinations similaires à une destination donnée.
    """
    def get(self, request, id):
        similar_data = recommendation_service.find_similar_destinations(destination_id=id)
        if not similar_data:
            return Response({"error": "Destination non trouvée ou aucune similarité"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(similar_data, status=status.HTTP_200_OK)

class ClusterAnalysisView(APIView):
    """
    POST /api/destinations/cluster/
    Expose les groupes (clusters) de destinations définis par K-Means.
    """
    def post(self, request):
        analysis = recommendation_service.get_cluster_analysis()
        return Response(analysis, status=status.HTTP_200_OK)






class UserTravelProfileView(APIView):
    """
    GET /api/users/<id>/travel-profile/
    Retourne le profil voyageur d'un utilisateur basé sur ses préférences

    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.id != id:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)

        try:
            prefs = request.user.preference
        except UserPreference.DoesNotExist:
            return Response({"error": "Préférences utilisateur non trouvées"}, status=status.HTTP_404_NOT_FOUND)

        #  Profil complet
        profile = {col: getattr(prefs, col, None) for col in feature_columns}

        #  Colonnes d'activités
        activity_fields = ['beach', 'mountain', 'culture', 'adventure',
                           'nightlife', 'shopping', 'nature', 'historical',
                           'family_friendly', 'romantic']
        activities = {field: getattr(prefs, field, 0) for field in activity_fields}

        #  Déterminer l'intérêt principal
        main_interest = max(activities, key=activities.get)

        # Catégorie de budget
        budget_category = (
            "Luxe" if getattr(prefs, 'budget_per_day_usd', 0) > 3000 else
            "Standard" if getattr(prefs, 'budget_per_day_usd', 0) > 1000 else
            "Économique"
        )

        
        preferred_temperature = getattr(prefs, 'avg_temperature', 20)
        preferred_climate = (
            "Chaud" if preferred_temperature > 22 else
            "Tempéré" if preferred_temperature > 15 else
            "Froid"
        )

        return Response({
            "user_id": id,
            "travel_profile": profile,
        })




class UserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Créer ou mettre à jour les préférences de l'utilisateur connecté.
        """
        user = request.user

        # Vérifier si l'utilisateur a déjà des préférences
        try:
            user_pref = UserPreference.objects.get(user=user)
            serializer = UserPreferenceSerializer(user_pref, data=request.data, partial=True)
        except UserPreference.DoesNotExist:
            serializer = UserPreferenceSerializer(data=request.data)

        if serializer.is_valid():
            # Sauvegarde et liaison avec user si création
            serializer.save(user=user)
            return Response({
                "message": "Préférences enregistrées",
                "preferences": serializer.data
            })
        else:
            return Response(serializer.errors, status=400)