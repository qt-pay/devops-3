from rest_framework import serializers
from opers.models import Oper
#


class OperSerializer(serializers.ModelSerializer):
    oper_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="提交时间", label="提交时间")

    class Meta:
        model = Oper
        fields = "__all__"
        read_only_fields = ('deploy_status', 'oper_status', 'online_version')

    def create(self, validated_data):
        oper = Oper(**validated_data)
        oper.online_version = oper.site.online_version
        oper.save()
        return oper

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['online_version'] = instance.online_version.version[:8] if ret.get('online_version') else None
        ret['oper_version'] = instance.oper_version.version[:8]
        return ret



