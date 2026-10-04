from django.db import models


class Enquiry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField("Phone or WhatsApp", max_length=40, blank=True)
    trip_type = models.CharField(max_length=40, blank=True)
    regions = models.CharField(max_length=300, blank=True)
    package = models.CharField(max_length=200, blank=True)
    month = models.CharField(max_length=40, blank=True)
    days = models.PositiveSmallIntegerField(null=True, blank=True)
    adults = models.PositiveSmallIntegerField(null=True, blank=True)
    children = models.PositiveSmallIntegerField(null=True, blank=True)
    hotel_class = models.CharField(max_length=40, blank=True)
    budget = models.CharField(max_length=60, blank=True)
    from_city = models.CharField(max_length=80, blank=True)
    message = models.TextField(blank=True)
    contact_pref = models.CharField("Best way to reach you", max_length=20, blank=True,
                                    choices=[("whatsapp", "WhatsApp"), ("call", "Phone call"), ("email", "Email")])
    kind = models.CharField(max_length=20, default="full",
                            choices=[("full", "Trip planner"), ("quick", "Quick quote"), ("callback", "Call back"),
                                     ("book", "Package booking request")])
    source_page = models.CharField(max_length=300, blank=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} · {self.package or self.trip_type or 'Nepal trip'} · {self.created:%d %b %Y}"


class Subscriber(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    source_page = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.email
