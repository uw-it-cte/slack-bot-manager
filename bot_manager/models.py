from django.db import models

# Create your models here.

class Bot(models.Model):
    pid = models.SmallIntegerField(default=0)
    class_name = models.CharField(max_length=128)
    module_name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    changed_by = models.CharField(max_length=32,null=True)
    changed_date = models.DateTimeField(null=True)
    is_active = models.NullBooleanField()

    def json_data(self):
        return {
            'bot_id': self.pk,
            'name': self.class_name,
            'description': self.description,
            'changed_by': self.changed_by,
            'changed_date': localtime(self.changed_date).isoformat() if (
                self.changed_date is not None) else None,
            'is_active': self.is_active,
        }
