from rest_framework import serializers
from .models import Post, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
