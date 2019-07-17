from rest_framework import serializers
from servers.models import Server, WebServer
#


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"
        extra_kwargs = {'deploy_pwd': {'write_only': True}}


class ServerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ("id", "hostname")


class WebServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebServer
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['server'] = {
            'id': instance.server.id,
            'hostname': instance.server.hostname
        }
        return ret


