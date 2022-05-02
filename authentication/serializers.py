from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'confirm_password']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError(detail='password does not match', code='password_match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        response = super().to_representation(instance)
        token = Token.objects.filter(user_id=instance.id).first()
        response['token'] = token.key
        return response