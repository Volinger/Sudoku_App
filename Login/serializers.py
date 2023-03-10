from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'})

	class Meta:
		model = User
		fields = ["username", "password"]


class RegisterSerializer(serializers.ModelSerializer):
	username = serializers.CharField()
	password = serializers.CharField(label='Password', style={'input_type': 'password'})
	password2 = serializers.CharField(label='Confirm password', style={'input_type': 'password'})

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password2']

	def validate(self, data):
		if data['password'] != data['password2']:
			raise serializers.ValidationError("passwords do not match")
		usernames = [username['username'] for username in User.objects.values('username')]
		if data['username'] in usernames:
			raise serializers.ValidationError("user already exists")
		return data

	def create(self, validated_data):
		validated_data.pop('password2')
		return User.objects.create_user(**validated_data)
