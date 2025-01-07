from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from places.models import Place , Gallery , Comment 

class PlaceSerializer(ModelSerializer):

    likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","name","featured_image","place","likes","is_liked")
        model = Place

    def get_likes(self,instance):
        return instance.likes.count()
    
    def get_is_liked(self,instance):
        request = self.context.get("request")
        if instance.likes.filter(username = request.user.username).exists():
            return True
        else:
            return False
        

class GallerySerializer(ModelSerializer):
    class Meta:
        fields = ("id","image")
        model = Gallery


class PlaceDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ("id", "name", "featured_image", "description", "place", "category", "gallery","likes","is_liked")

    def get_category(self, instance):
        return instance.category.name

    def get_gallery(self, instance):
        request = self.context.get("request")
        images = Gallery.objects.filter(place=instance)
        serializer = GallerySerializer(images, many=True, context={"request": request})
        return serializer.data
    
    def get_likes(self,instance):
        return instance.likes.count()
    
    def get_is_liked(self,instance):
        request = self.context.get("request")
        if instance.likes.filter(username = request.user.username).exists():
            return True
        else:
            return False

    

class CommentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    replys = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ("id", "comment", "user", "date","replys")

    def get_user(self, instance):
        return instance.user.username

    def get_date(self, instance):
        return instance.date.strftime("%d %B %Y")

    def get_replys(self , instance):
        instances = Comment.objects.filter( parent_comment = instance)
        

        serializer = CommentSerializer(instances,many=True)
        return serializer.data