from rest_framework import serializers
from sites.models import Site
import re
#
regex = re.compile("^/([^/]+/?)+$")


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"
        read_only_fields = ('deploy_status', 'status', 'online_version', 'pre_version')

    def validate_dev_path(self, value):
        if not regex.match(value):
            raise serializers.ValidationError("Not the correct file path")
        return value

    validate_site_path = validate_dev_path

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.dev_path = validated_data.get('dev_path', instance.dev_path)
        instance.site_path = validated_data.get('site_path', instance.site_path)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['online_version'] = {
            'id': instance.online_version.id,
            'version': instance.online_version.version[:8]
        } if ret.get('online_version') else None
        ret['pre_version'] = {
            'id': instance.pre_version.id,
            'version': instance.pre_version.version[:8]
        } if ret.get('pre_version') else None
        ret['server_count'] = instance.webserver_set.count()
        return ret


class SiteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ("id", "name")
