from spotprices.models import SpotPrices
from rest_framework import serializers


class SpotPriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpotPrices
        fields = [
            "region", "size", "time", "api_price","cli_price",
            "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
        ]