from rest_framework import serializers
from .models import List
from .utils import initialize_list_data, resit_by_template, generate_templates

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name']

class ListDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'

class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['name', 'people', 'owner']
        read_only_fields = ['owner']

    def create(self, validated_data):
        obj = List(**validated_data)
        initialize_list_data(obj)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            if attr == 'people':
                initialize_list_data(instance)
        instance.save()
        return instance