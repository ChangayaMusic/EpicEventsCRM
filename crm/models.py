from django.db import models
from login.models import Staff

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="clients"
    )

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contracts"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="contracts"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    # False = Not Signed, True = Signed
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract {self.id} - {self.client.full_name}"


class Event(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="events"
    )
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="events"
    )
    location = models.CharField(max_length=200)
    attendees = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return f"Event {self.id} - {self.contract.client.full_name}"
