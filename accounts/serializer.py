# serializer.py
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Force username = email
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(username=email, email=email, password=password)
        return user