from rest_framework import serializers
from .models import Difficulty, Results


class ResultSerializer(serializers.ModelSerializer):
	Difficulty = serializers.SlugRelatedField(
		many=False,
		read_only=False,
		slug_field='Option',
		queryset=Difficulty.objects.all()
	)
	class Meta:
		model = Results
		fields = '__all__'


class DifficultySerializer(serializers.ModelSerializer):

	class Meta:
		model = Difficulty
		fields = '__all__'
