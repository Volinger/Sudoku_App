from rest_framework import serializers
from .models import Difficulty, Results
from django.contrib.auth.models import User


class ResultSerializer(serializers.ModelSerializer):
	Difficulty = serializers.SlugRelatedField(
		many=False,
		read_only=False,
		slug_field='Option',
		queryset=Difficulty.objects.all()
	)

	UserId = serializers.SlugRelatedField(
		many=False,
		read_only=False,
		slug_field='username',
		queryset=User.objects.all(),
		required=False
	)

	Time = serializers.DateTimeField(format='%d. %m. %Y %H: %M')

	class Meta:
		model = Results
		fields = '__all__'


class DifficultySerializer(serializers.ModelSerializer):

	class Meta:
		model = Difficulty
		fields = '__all__'
