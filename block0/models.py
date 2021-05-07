from django.db import models

class BlockDetails(models.Model):
    block = models.TextField(max_length=20)
    nonce = models.IntegerField()
    merkleroot = models.TextField(max_length=64)
    previous_hash = models.TextField(max_length=64)
    finalhash = models.TextField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

class transaction(models.Model):
    block_no = models.TextField(max_length=20)
    r_pub = models.TextField(max_length=64)
    s_pub = models.TextField(max_length=64)
    amount = models.IntegerField()
    current_hash = models.TextField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    block_no = models.TextField(max_length=12)

class User(models.Model):
    
    pub = models.TextField(max_length=64)
    priv = models.TextField(max_length=128)
    balance = models.IntegerField()

# Create your models here.
