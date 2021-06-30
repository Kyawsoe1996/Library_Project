from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from account.models import Account

#Validator Rest Framework, phone_number validate on Account Serializer
from rest_framework.validators import UniqueValidator
  


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}, }

    def create(self, validated_data):

        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        # user.set_password(password)
        # user.save()
        validated_data.pop('password2')
        return super(UserSerializer,self).create(validated_data)


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    #adding validator
    phone_number = serializers.IntegerField(validators=[UniqueValidator(queryset=Account.objects.all())])    

    class Meta:
        model = Account
        fields = ['user', 'phone_number', 'present_address']
        

    def create(self, validated_data):
       

        user_data = validated_data.pop('user')

        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        user.set_password(user.password)       
        user.save()
        account = Account.objects.get(user=user)
        account.phone_number = validated_data.get('phone_number')
        account.present_address = validated_data.get('present_address')
        account.save()

        return account


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField()
    present_address = serializers.CharField(max_length=300)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password',
                  'confirm_password', 'phone_number', 'present_address']
