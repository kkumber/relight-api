from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils.text import slugify
import fitz

# Create your models here.
class BookModel(models.Model):
    pdf_file = CloudinaryField('pdf', resource_type='raw')
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    book_cover = CloudinaryField('image', resource_type='auto', blank=True, null=True)
    sypnosis = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            super(BookModel, self).save(*args, **kwargs)
            self.slug = f"{slugify(self.title)}-{self.id}"
        super(BookModel, self).save(*args, **kwargs)
                
    def __str__(self):
        return self.title or "Untitled"
    
class UserCommentOnBookModel(models.Model):
    specific_book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    post_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()        

    def __str__(self):
        return self.owner