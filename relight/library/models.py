from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils.text import slugify
import fitz
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class BookModel(models.Model):
    pdf_file = CloudinaryField('pdf', resource_type='raw')
    title = models.CharField(max_length=255, default="Untitled")
    author = models.CharField(max_length=100, default='Unknown')
    book_cover = CloudinaryField('image', resource_type='auto', blank=True, null=True)
    sypnosis = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)
    views = models.PositiveIntegerField(default=0)  # Tracks number of views
    likes = models.ManyToManyField(User, related_name="liked_books", blank=True)  # Tracks likes
    
    def save(self, *args, **kwargs):
        if not self.slug:
            count = 1
            base_slug = slugify(self.title)
            slug = base_slug
            while BookModel.objects.filter(slug=base_slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
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

class BookmarkModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = ArrayField(
        models.IntegerField(null=True, blank=True),
        null=True,
        blank=True,
        verbose_name='page'
    )    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "book", "page"], name="unique_bookmark")
        ]
        verbose_name = "bookmark"
        verbose_name_plural = "bookmarks"