from django.db import models
import uuid
from user_auth.models import rootUser


class contents(models.Model):
    CATEGORIES = (
        ('category1', 'category1'),
        ('category2', 'category2'),
        ('category3', 'category3'),
        ('category4', 'category4'),
        ('category5', 'category5')
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=30,null=False)
    body = models.CharField(max_length=300,null=False)
    summary = models.CharField(max_length=60,null=False)
    document = models.FileField(upload_to='content/document')
    categories = models.CharField(max_length=10, choices=CATEGORIES,null=True,blank=True)
    user = models.ForeignKey(rootUser,on_delete=models.CASCADE,null=True,blank=True)
    created_by = models.ForeignKey(rootUser,on_delete=models.CASCADE,null=True,blank=True,related_name='created_by_user')
    updated_by = models.ForeignKey(rootUser,on_delete=models.CASCADE,null=True,blank=True,related_name='updated_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.title
                
    class Meta:
        db_table = 'contents'