from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    avg_temperature = models.FloatField()
    budget_per_day_usd = models.FloatField()
    safety_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    popularity_score = models.FloatField(default=5.0)
    
    # Scores de types d'activités (0.0 à 1.0)2
    beach = models.FloatField(default=0.5)
    mountain = models.FloatField(default=0.5)
    culture = models.FloatField(default=0.5)
    adventure = models.FloatField(default=0.5)
    nightlife = models.FloatField(default=0.5)
    shopping = models.FloatField(default=0.5)
    nature = models.FloatField(default=0.5)
    historical = models.FloatField(default=0.5)
    family_friendly = models.FloatField(default=0.5)
    romantic = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.city}"

 

class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preference'
    )

    # Champs correspondant à feature_columns
    budget_per_day_usd = models.FloatField(default=0)
    avg_temperature = models.FloatField(default=0)
    
    beach = models.FloatField(default=0)
    mountain = models.FloatField(default=0)
    culture = models.FloatField(default=0)
    adventure = models.FloatField(default=0)
    nightlife = models.FloatField(default=0)
    shopping = models.FloatField(default=0)
    nature = models.FloatField(default=0)
    historical = models.FloatField(default=0)
    family_friendly = models.FloatField(default=0)
    romantic = models.FloatField(default=0)
    
    safety_score = models.FloatField(default=5)  # 0 à 10

    created_at = models.DateTimeField( default=datetime.date.today())
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences de {self.user.username}"


class Recommendation(models.Model):
    """Suggestions générées avec score de pertinence"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    
    # Scores issus du moteur de recommandation
    similarity_score = models.FloatField() # Distance KNN
    relevance_score = models.FloatField()  
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-relevance_score']
    
    def __str__(self):
        return  f"Reco {self.destination.id} pour {self.user.username}"


class Review(models.Model):
    """Avis d'utilisateurs sur les destinations"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)