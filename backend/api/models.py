from django.db import models
from django.contrib.auth.models import User

class Lexicon(models.Model):
    rank = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=255)
    freq = models.IntegerField(null=True)
    num_texts = models.IntegerField(null=True)
    perc_caps = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    blog = models.IntegerField(null=True)
    web = models.IntegerField(null=True)
    tvm = models.IntegerField(null=True)
    spok = models.IntegerField(null=True)
    fic = models.IntegerField(null=True)
    mag = models.IntegerField(null=True)
    news = models.IntegerField(null=True)
    acad = models.IntegerField(null=True)
    blog_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    web_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    tvm_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    spok_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    fic_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    mag_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    news_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    acad_pm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    apl_class = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "lexicon"

    def __str__(self):
        return f"{self.rank}: {self.word}"

class LookedUpWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "looked_up_words"

    def __str__(self):
        return self.word

class SkipWords(models.Model):  
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "skip_words"

    def __str__(self):
        return self.word

class Analyzation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analyzations", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    caps_count = models.IntegerField()
    uncommon_count = models.IntegerField()
    unknown_count = models.IntegerField()
    looked_up_count = models.IntegerField()
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    payment_id = models.IntegerField()
    
    class Meta:
        db_table = "analyzation"

    def __str__(self):
        return f"{self.file_name} (user {self.user_id})"