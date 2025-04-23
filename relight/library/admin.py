from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.BookModel)
admin.site.register(models.UserCommentOnBookModel)
admin.site.register(models.BookmarkModel)
admin.site.register(models.BookRatingModel)