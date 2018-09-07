import hashlib
import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class BillOfSale(models.Model):
    # Name, address, and nationality  of person title is being issued to
    transferee_name = models.CharField(max_length=50)
    transferee_address = models.CharField(max_length=100)
    transferee_nationality = models.CharField(max_length=30)

    # Name, address, and nationality of person transferring title (if applicable)
    transferor_name = models.CharField(max_length=50, null=True, blank=True)
    transferor_address = models.CharField(max_length=100, null=True, blank=True)
    transferor_nationality = models.CharField(max_length=30, null=True, blank=True)

    # Make and model of aircraft, date of aircraft manufacture,
    # Date of last aircraft maintenance, manufacturer serial number,
    # aircraft registration number
    manufacturer_and_model = models.CharField(max_length=100)
    manufactured = models.DateField()
    last_maintenance = models.DateField()
    serial_number = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=50)

    transfered = models.DateField()

    tx_hash = models.CharField(max_length=70)
    file_hash = models.CharField(max_length=64, null=True, blank=True)


class ApplicationForRegistration(models.Model):
    # AC-8050: Application for Aircraft Registration
    registration_number = models.CharField(max_length=50)
    manufacturer_and_model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50)
    
    applicant_name = models.CharField(max_length=50)
    applicant_telephone = PhoneNumberField()
    applicant_address = models.CharField(max_length=100)

    TYPE_CHOICES = (
        ('1', 'Individual'),
        ('2', 'Partnership'),
        ('3', 'Corporation'),
        ('4', 'Co-Owner'),
        ('5', 'Government'),
        ('8', 'Non-Citizen Corporation'),
        ('9', 'Non-Citizen Corporation Co-Owner'),
    )

    registration_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    registered = models.DateField()

    tx_hash = models.CharField(max_length=70)
    file_hash = models.CharField(max_length=64, null=True, blank=True)


class SecurityGuarantee(models.Model):
    # 8050-98: Aircraft Security Agreement 
    debtor_name = models.CharField(max_length=50)
    debtor_address = models.CharField(max_length=100)

    assignor_name = models.CharField(max_length=50)
    assignor_address = models.CharField(max_length=100)

    assignee_name = models.CharField(max_length=50)
    assignor_address = models.CharField(max_length=100)

    date = models.DateField()

    tx_hash = models.CharField(max_length=70)
    file_hash = models.CharField(max_length=64, null=True, blank=True)

    """ engines = models.CharField(max_length=100)
    propellers = models.CharField(max_length=100)
    spare_parts = models.CharField(max_length=100)

    engines_horsepower = models.IntegerField()
    propellers_capability = models.IntegerField() """


def get_upload_to(instance, filename):
    return instance.uuid_name


class Document(models.Model):
    # a model which stores the file information
    file = models.FileField(upload_to=get_upload_to)
    original_name = models.CharField(max_length=255)
    uuid_name = models.CharField(max_length=48, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.original_name = self.file.name
        self.uuid_name = "{}.{}".format(uuid.uuid4().hex, self.original_name.split('.')[-1])  # get the extension
        self.file_hash = self.get_hash()
        super(Document, self).save()

    def get_hash(self):
        return hashlib.sha256(self.file.read()).hexdigest()
