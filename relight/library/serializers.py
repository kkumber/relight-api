from rest_framework import serializers
from .models import BookModel, UserCommentOnBookModel, BookmarkModel, BookRatingModel

class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = BookModel
        fields = [
            'id',
            'uploaded_by',
            'slug',
            'pdf_file',
            'title',
            'author',
            'book_cover',
            'sypnosis',
            'upload_date',
            'views',
            'likes',
            'average_rating', 
        ]
    
        
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


class BookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRatingModel
        fields = ['score']
