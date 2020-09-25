from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length = 30)
    age = models.IntegerField()
    
    def __str__(self):
        return self.name
        
class Blog(models.Model):
    name = models.CharField(max_length = 100)
    tagline = models.TextField()
    
    def __str__(self):
        return self.name
        
class Author(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField()
    qq = models.CharField(max_length = 10)
    addr = models.TextField()
    
    def __str__(self):
        return self.name
        
class Article(models.Model):
    title = models.CharField(max_length = 50)
    # 外键要加on_delete, 不然运行不过
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()  # 文章的打分
    tags = models.ManyToManyField('Tag')
 
    def my_property(self):
        return self.content + ' ' + str(self.score)
    my_property.short_description = '正文和得分'         # 别名
    
    content_and_score = property(my_property)           # 后台可以展示此 属性'正文和得分'
 
    def __str__(self):
        return self.title
        
class Tag(models.Model):
    name = models.CharField(max_length = 50)
 
    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    headline = models.CharField(max_length = 255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
    
    def __str__(self):
        return self.headline