from django.db import models

class task(models.Model):
    id = models.AutoField(primary_key=True)
    title= models.CharField(max_length=50,unique=True, null=False)
    description = models.TextField(null=False)
    status= models.TextField(choices=[('New','New'),('In Progress','In Progress'),('Done','Done')],null=False)
    
class related_tasks(models.Model):
    id= models.AutoField(primary_key=True)
    TaskOne = models.OneToOneField(task,on_delete=models.CASCADE,related_name='First_Task')
    TaskTwo = models.OneToOneField(task,on_delete=models.CASCADE,related_name='Second_Task')
