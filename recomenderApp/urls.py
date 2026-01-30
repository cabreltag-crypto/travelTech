from django.urls import path
from .views import (
    GenerateRecommendationsView,
    SimilarDestinationsView,
    ClusterAnalysisView,
    UserTravelProfileView,
    UserPreferencesView,
)

urlpatterns = [
    path('users/preferences/', UserPreferencesView.as_view(), name='user_preferences'),
   
    # a. Générer des recommandations personnalisées (KNN)
    path('recommendations/generate/', GenerateRecommendationsView.as_view(), name='generate-recs'),

    # b. Destinations similaires à une autre (K-NN)
    path('destinations/similar/<int:id>/', SimilarDestinationsView.as_view(), name='similar-destinations'),

    # c. Grouper les destinations par profil (K-Means Clustering)
    path('destinations/cluster/', ClusterAnalysisView.as_view(), name='destination-clusters'),

    # d. Analyser le profil voyageur d’un utilisateur
    path('users/<int:id>/travel-profile/', UserTravelProfileView.as_view(), name='user-travel-profile'),
]