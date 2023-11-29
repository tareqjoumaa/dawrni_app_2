from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _
from .models import Category, Company, Client, Notification, CompanyPhoto

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CompanyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPhoto
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    
    def to_representation(self, obj):
        request = self.context.get('request')
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')

        if language == 'ar':
            name = obj.name_ar
        else: 
            name = obj.name_en
        return {
            'id': obj.id,
            'user': obj.user.username,
            'name': name,
            'email': obj.email,
            'photo': obj.photo.url,
            }


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), _("A user with that Email already exists.")
                    )
                ],
            },
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(_("Password must be at least 8 characters long."))
        return value
    
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user
    

class CompanySerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Use the CategorySerializer to nest category details

    class Meta:
        model = Company
        fields = '__all__'
    
    def to_representation(self, obj):
        request = self.context.get('request')
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')

        if language == 'ar':
            name = obj.name_ar
            address = obj.address_ar
            about = obj.about_ar
        else:
            name = obj.name_en
            address = obj.address_en
            about = obj.about_en

        return {
            'id': obj.id,
            'user': obj.user.username,
            'category': CategorySerializer(obj.category).data,  # Serialize the category field
            'name': name,
            'address': address,
            'about': about,
        }

        
class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code_name = serializers.CharField() 