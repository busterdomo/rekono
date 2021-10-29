from findings.models import (OSINT, Credential, Endpoint, Enumeration, Exploit,
                             Host, Technology, Vulnerability)
from rest_framework import serializers


class OSINTSerializer(serializers.ModelSerializer):

    class Meta:
        model = OSINT
        fields = (
            'id', 'execution', 'data', 'data_type', 'source', 'reference',
            'creation', 'is_active'
        )
        ordering = ['-id']


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = (
            'id', 'execution', 'address', 'os', 'os_type', 'creation',
            'is_active', 'enumerations'
        )
        ordering = ['-id']


class EnumerationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enumeration
        fields = (
            'id', 'execution', 'host', 'port', 'port_status', 'protocol',
            'service', 'creation', 'is_active', 'endpoints', 'technologys'
        )
        ordering = ['-id']


class EndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Endpoint
        fields = (
            'id', 'execution', 'enumeration', 'endpoint', 'status',
            'creation', 'is_active'
        )
        ordering = ['-id']


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology
        fields = (
            'id', 'execution', 'enumeration', 'name', 'version', 'description',
            'reference', 'related_to', 'related_technologies', 'creation',
            'is_active', 'vulnerabilitys', 'exploits'
        )
        ordering = ['-id']


class VulnerabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Vulnerability
        fields = (
            'id', 'execution', 'technology', 'name', 'description', 'severity',
            'cve', 'cwe', 'reference', 'creation', 'is_active', 'exploits'
        )
        read_only_fields = (
            'id', 'execution', 'technology', 'cve', 'creation', 'is_active',
            'exploits'
        )
        ordering = ['-id']


class CredentialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credential
        fields = ('id', 'email', 'username', 'secret')
        ordering = ['-id']


class ExploitSerializer(serializers.ModelSerializer):
    technology = TechnologySerializer(read_only=True, many=False, required=False)

    class Meta:
        model = Exploit
        fields = (
            'id', 'execution', 'vulnerability', 'technology', 'name',
            'description', 'reference', 'checked', 'creation', 'is_active'
        )
        ordering = ['-id']
