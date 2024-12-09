from rest_framework import serializers
from .models import Book, BookRequest, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_librarian']
        extra_kwargs = {'password': {'write_only': True}}

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRequest
        fields = ['book', 'start_date', 'end_date','status'] 
        read_only_fields = ['status', 'user']  

    def create(self, validated_data):

        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)