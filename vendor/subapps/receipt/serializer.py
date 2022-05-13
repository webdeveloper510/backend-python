from rest_framework import serializers

from .models import Receipt


class ReceptSerializer(serializers.ModelSerializer):
    activity_title = serializers.CharField(source='activity.title')
    activity_code = serializers.CharField(source='activity.code')
    user_id = serializers.CharField(source='user.userdetails.code')
    full_name = serializers.SerializerMethodField()
    recept_date_time = serializers.SerializerMethodField()
    recept_no = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    vat = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    booking_reference = serializers.SerializerMethodField()
    transaction_id = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = ['id', 'activity_title', 'activity_code', 'full_name', 'user_id', 'recept_date_time',
                  'recept_no', 'amount', 'vat', 'total', 'booking_reference', 'transaction_id']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_recept_date_time(self, obj):
        return obj.created_at

    def get_recept_no(self, obj):
        return 'reccept no coming soon'

    def get_amount(self, obj):
        return 'coming soon'

    def get_vat(self, obj):
        return 'coming soon'

    def get_total(self, obj):
        return 'coming soon'

    def get_booking_reference(self, obj):
        return 'coming soon'

    def get_transaction_id(self, obj):
        return 'coming soon'
