from django.db import models

# Create your models here.

class LDAP(models.Model):
      baseDN = models.CharField(max_length=2048)
      host = models.CharField(max_length=2048)
      adminDN = models.CharField(max_length=2048)
      password = models.CharField(max_length=2048)

      def __unicode__(self):
          return "LDAP connections details for "+self.host

class service(models.Model):
      tag = models.CharField(max_length=256)
      description = models.CharField(max_length=256)
      groupdn = models.CharField(max_length=2048)


class request(models.Model):
      email = models.CharField(max_length=2048)
      name = models.CharField(max_length=2048)
      services = models.CharField(max_length=2048)
      message = models.CharField(max_length=2048)

      def __unicode__(self):
          return "Account request for %s to access %s" % (self.email, self.services)

class mail(models.Model):
      tag = models.CharField(max_length=8)
      rfc822 = models.CharField(max_length=32768)

class admins(models.Model):
      email = models.CharField(max_length=512)
