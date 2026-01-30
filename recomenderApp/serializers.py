from rest_framework import serializers
from .models import Destination, UserPreference, Recommendation, Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']

class DestinationSerializer(serializers.ModelSerializer):
    # Champ calculé pour la note moyenne (optionnel mais très utile)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return 4.0  # Note par défaut
        return sum(r.rating for r in reviews) / reviews.count()

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            'user',  # FK vers User, peut être read_only
            'budget_per_day_usd', 'avg_temperature',
            'beach', 'mountain', 'culture', 'adventure',
            'nightlife', 'shopping', 'nature', 'historical',
            'family_friendly', 'romantic', 'safety_score'
        ]
        read_only_fields = ['user']  # On ne laisse pas l'utilisateur changer l'user
        
class RecommendationSerializer(serializers.ModelSerializer):
    # On imbrique le serializer de destination pour avoir les noms des villes
    # plutôt que juste l'ID dans la réponse API
    destination_details = DestinationSerializer(source='destination', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'destination', 'destination_details', 
            'similarity_score', 'relevance_score', 'created_at'
        ]