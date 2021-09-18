from rest_framework import serializers

from .models import Benefactor, Charity, Task


class BenefactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefactor
        fields = ('experience', 'free_time_per_week')

    def create(self, validated_data):
        return Benefactor.objects.create(user=validated_data['user'],
                                         experience=validated_data['experience'],
                                         free_time_per_week=validated_data['free_time_per_week'])


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('name', 'reg_number')

    def create(self, validated_data):
        return Charity.objects.create(user=validated_data['user'],
                                      name=validated_data['name'],
                                      reg_number=validated_data['reg_number'])


class TaskSerializer(serializers.ModelSerializer):
    pass
