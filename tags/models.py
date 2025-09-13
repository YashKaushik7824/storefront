from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Custom Manager
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects\
            .select_related('tag')\
            .filter(
                content_type = content_type,
                object_id = obj_id
            )

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class TaggedItem(models.Model):

    objects = TaggedItemManager()

    #What tag applied to What object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product) # poor way -> need to import Prodct app from store.models -> causing dependecy on store app
    #generic way -> two peice of info reuired
    #Type(product, video, article)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)# for generic type relation django provide ContentType -> installed in InstalledApps in settings.py
    #ID
    object_id = models.PositiveIntegerField()#if in any table primary key/id is not integer then this way/solution will not work -> Limitation
    content_object = GenericForeignKey()