from rest_framework import serializers
from .models import BookModel, UserCommentOnBookModel, BookmarkModel

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = BookModel
        fields = '__all__'
    
        
class UserCommentOnBookSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    post_date = serializers.ReadOnlyField()
    
    class Meta:
        model = UserCommentOnBookModel
        fields = ['content', 'owner', 'post_date']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkModel
        fields = ['book', 'page', 'user', 'id']
        read_only_fields = ['book', 'user']