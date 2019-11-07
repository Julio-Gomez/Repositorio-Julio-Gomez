from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Producto, Categoria, Subcategoria
from django.contrib.auth.models import User

class ProductoSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Categoria
        fields = '__all__'

class SubCategoriaSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Subcategoria
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validate_data):
        user = User(
            email = validate_data['email'],
            username = validate_data['username']
        )
        user.set_password(validate_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user