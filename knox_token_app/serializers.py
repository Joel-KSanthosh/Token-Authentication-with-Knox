from .models import User
from rest_framework import serializers
# from rest_framework.views import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username','role','password')
        extra_kwargs = {'password' : {'write_only' : True ,'min_length':5}}


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class AuthSerializer(serializers.Serializer):
    class Meta:
        email = serializers.EmailField()
        password = serializers.CharField(
            style = {'input_type':'password' },
            trim_whitespace = False
        )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password)
        
        if not User:
            raise serializers.ValidationError("Invalid email or password")
        attrs['user'] = user
        return user
    
class AuthToken(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    