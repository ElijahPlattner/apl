from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password, get_default_password_validators
from django.core.exceptions import ValidationError as DjangoValidationError
from api.models import Analyzation

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="This email address is already registered. Try logging in instead."
        )]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="That username is already taken. Please choose another one."
        )]
    )

    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    password2 = serializers.CharField(
        write_only=True, required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate_email(self, value):
        """Extra layer for format issues."""
        if not value or "@" not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value

    def validate_password(self, value):
        """Wrap Django’s password validation for clearer messages."""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            # Join all built-in password rule messages into one string
            raise serializers.ValidationError({
                "password": "Your password didn't meet security requirements.",
                "details": list(e.messages)
            })
        return value

    def validate(self, attrs):
        """Cross-field validation (e.g., password confirmation)."""
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({
                "password_mismatch": "Passwords do not match. Please re-enter both fields."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AnalyzationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyzation
        # You can use "__all__" to include every field, or list them explicitly
        fields = "__all__"