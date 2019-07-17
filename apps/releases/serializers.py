from rest_framework import serializers
from releases.models import Release
#


class ReleaseSerializer(serializers.ModelSerializer):
    committed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text="操作时间", label="操作时间")

    class Meta:
        model = Release
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['version'] = instance.version[:8]
        return ret
