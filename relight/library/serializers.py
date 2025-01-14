from rest_framework import serializers
from .models import BookModel, UserCommentOnBookModel

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = BookModel
        fields = '__all__'
    
    def validate(self, data):
        data['title'] = data.get('title', '').strip() or 'Untitled'
        data['author'] = data.get('author', '').strip() or 'Unknown'
        return data
        
        
class UserCommentOnBookSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    post_date = serializers.ReadOnlyField()
    
    class Meta:
        model = UserCommentOnBookModel
        fields = ['content', 'owner', 'post_date']