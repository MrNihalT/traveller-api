from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="places/images")
    place =models.CharField(max_length=128)
    category = models.ForeignKey("places.Category",on_delete=models.CASCADE)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField("auth.User")
    class Meta:
        db_table = "places_place"

    def __str__(self):
        return self.name


class Category(models.Model):
    featured_image = models.ImageField(upload_to="categories/images/")
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "places_category"
        verbose_name_plural = "categories"
    def __str__(self):
        return self.name


class Gallery(models.Model):
    place = models.ForeignKey("places.Place",on_delete=models.CASCADE)
    image = models.ImageField(upload_to="places/images/")

    class Meta:
        db_table = "places_gallery"

    def __str__(self):
        return str(self.id)
    

class Comment(models.Model):
    parent_comment = models.ForeignKey("places.Comment",related_name="master_comment",blank=True,null=True,on_delete=models.CASCADE)
    place = models.ForeignKey("places.Place",on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.TextField()

    class Meta:
        db_table = "places_comment"
        verbose_name_plural = "comment"

    def __str__(self):
        return str(self.id)
    
