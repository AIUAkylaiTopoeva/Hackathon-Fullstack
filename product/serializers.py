from rest_framework.serializers import ModelSerializer, ValidationError
from .models import  Product, Order, OrderItem
from django.db.models import Avg

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if  price < 0:
            raise ValidationError(
                'price must be > 0'
            )
        return price
    
class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['author'] = self.context['request'].user
        order = super().create(validated_data)
        total_sum = 0
        order_items = []
        for item in items:
            order_items.append(OrderItem(order=order,
                                          product = item['product'],
                                          quantity = item['quantity']))
            total_sum += item['product'].price * item['quantity']

        OrderItem.objects.bulk_create(order_items)
        order.total_sum = total_sum
        order.save()
        return order