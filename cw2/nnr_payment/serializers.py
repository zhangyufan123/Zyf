from rest_framework import serializers
from .models import consumption_record, user


class comserializer(serializers.ModelSerializer):
    class Meta:
        model = consumption_record
        fields = (
            'id',
            'Time',
            'Recipient',
            'Amount',
            'Money',
            'secret_key',
            'UserId',
            'Airline_order',
            'State',
        )


class userializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = (
            'id',
            'username',
            'password',
            'balance',
            'name',
        )
