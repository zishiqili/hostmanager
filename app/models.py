from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class IDC(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact_person = models.CharField(max_length=50, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='idcs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Host(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    os = models.CharField(max_length=50)
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE, related_name='hosts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class PasswordChangeLog(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    old_password = models.CharField(max_length=100)
    new_password = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)

class HostStat(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    host_count = models.IntegerField()
    stat_date = models.DateField()
