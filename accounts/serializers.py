from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'phone', 'address', 'gender', 'age'
                  , 'description', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
