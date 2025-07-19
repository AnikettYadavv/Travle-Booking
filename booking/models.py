from django.db import models
from django.contrib.auth.models import User



class TravelOption(models.Model):
      TravelID = models.AutoField(primary_key=True)
      type = models.CharField(max_length=100,choices=(('Flight','Flight'),('Train','Train'),('Bus','Bus')))
      image = models.ImageField(upload_to='travel_images/', blank=True, null=True)
      source = models.CharField(max_length=100)
      destination = models.CharField(max_length=100)
      Date_and_Time = models.DateTimeField()
      price = models.IntegerField()
      available_seats = models.IntegerField()

      def __str__(self):
        return f"{self.type}: {self.source} to {self.destination}"

class Booking(models.Model):
      BookingID = models.AutoField(primary_key=True)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
      number_of_seats = models.IntegerField()
      total_price = models.DecimalField(max_digits=10, decimal_places=2)
      booking_date = models.DateTimeField(auto_now_add=True)
      status = models.CharField(max_length=20, choices=(('Confirmed', 'Confirmed'), ('cancelled','Cancelled')), default='Confirmed')

      def __str__(self):
        return f"Booking {self.BookingID} by {self.user.username}"