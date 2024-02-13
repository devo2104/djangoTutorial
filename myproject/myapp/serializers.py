# myapp/serializers.py
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # these fields are not the model fields, but the api(json from frontend) fields
    email_address = serializers.EmailField(source='email') # this email points to customUser email
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email_address', 'password']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user