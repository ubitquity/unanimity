from ubitquity.ubitquity.models import BillOfSale, ApplicationForRegistration, SecurityGuarantee, Document
from rest_framework import serializers


# Bill of Sale
class BillOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillOfSale
        fields = ('transferee_name', 'transferee_address', 'transferee_nationality',
                  'transferor_name', 'transferor_address', 'transferor_nationality',
                  'manufacturer_and_model', 'manufactured', 'last_maintenance',
                  'serial_number', 'registration_number', 'transfered', 'tx_hash', 'file_hash')
        read_only_fields = ('tx_hash', )


# Application for Registration
class ApplicationForRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForRegistration
        fields = ('registration_number', 'manufacturer_and_model', 'serial_number',
                  'applicant_name', 'applicant_telephone', 'applicant_address',
                  'registration_type', 'registered', 'tx_hash', 'file_hash')
        read_only_fields = ('tx_hash', )


# Security Guarantee
class SecurityGuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityGuarantee
        fields = ('debtor_name', 'debtor_address', 'assignor_name', 'assignor_address',
                  'assignee_name', 'assignor_address', 'date', 'tx_hash', 'file_hash')
        read_only_fields = ('tx_hash', )


# Document Serializer
class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file', 'original_name', 'uuid_name', 'created_at', 'file_hash')
