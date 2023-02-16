from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(
        Tax, null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=12,
                                      decimal_places=2, null=True, blank=True)

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              default='draft', max_length=20)

    def save_total_price(self, *args, **kwargs):
        total = sum(item.price for item in self.items.all())

        if self.discount:
            total -= total * self.discount.value / 100

        if self.tax:
            total += total * self.tax.value / 100

        self.total_price = total
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id} - {self.status}'
