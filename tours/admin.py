from django.contrib import admin

from .models import Enquiry, Subscriber


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("created", "name", "phone", "email", "contact_pref", "kind", "trip_type", "package", "month",
                    "adults", "handled")
    list_filter = ("handled", "kind", "trip_type", "contact_pref", "month", "hotel_class")
    search_fields = ("name", "email", "phone", "package", "regions", "message", "from_city")
    list_editable = ("handled",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("created", "email", "source_page")
    search_fields = ("email",)
