from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from profiles.models import Profiles, User


class ProfilesOwnerSerializer(
    serializers.ModelSerializer):
    admins = serializers.ListField(
        child=serializers.IntegerField()
    )
    members = serializers.ListField(
        child=serializers.IntegerField()
    )

    class Meta:
        model = Profiles
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )
        return super().create(validated_data)

    class Meta:
        model = User
        fields = '__all__'


