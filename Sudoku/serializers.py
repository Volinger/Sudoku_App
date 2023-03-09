from rest_framework import serializers
from .models import Difficulty, Results


class ResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = Results
		fields = '__all__'


class DifficultySerializer(serializers.ModelSerializer):

	class Meta:
		model = Difficulty
		fields = '__all__'
