from django import forms

from .content import MONTHS, TYPES, catalogue
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    regions = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)
    month = forms.ChoiceField(required=False)
    trip_type = forms.ChoiceField(required=False, widget=forms.RadioSelect)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "contact_pref", "trip_type", "regions", "package", "month", "days",
                  "adults", "children", "hotel_class", "budget", "from_city", "message", "source_page", "kind"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Dates, ages of children, places you must see, anything we should know"}),
            "source_page": forms.HiddenInput,
            "kind": forms.HiddenInput,
            "package": forms.HiddenInput,
            "contact_pref": forms.RadioSelect,
            "hotel_class": forms.Select(choices=[
                ("", "Any"), ("budget", "Budget / 2-star"), ("standard", "3-star"), ("premium", "4-star"),
                ("luxury", "5-star and boutique")]),
            "budget": forms.Select(choices=[
                ("", "Choose a range"), ("under-25k", "Under ₹25,000 per person"),
                ("25-50k", "₹25,000 – 50,000 per person"), ("50k-1l", "₹50,000 – 1,00,000 per person"),
                ("1-2l", "₹1,00,000 – 2,00,000 per person"), ("2l-plus", "Above ₹2,00,000 per person"),
                ("unsure", "Not sure yet")]),
        }
        labels = {"phone": "Phone or WhatsApp", "days": "Days (roughly)", "from_city": "Travelling from",
                  "message": "Anything else", "hotel_class": "Hotel class"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cat = catalogue()
        self.fields["regions"].choices = [(r["slug"], r["name"]) for r in cat.regions.values()]
        self.fields["month"].choices = [("", "Flexible")] + [(m, m) for m in MONTHS]
        self.fields["trip_type"].choices = [(k, v["label"]) for k, v in TYPES.items()]
        self.fields["kind"].required = False
        self.fields["contact_pref"].choices = Enquiry._meta.get_field("contact_pref").choices
        self.fields["contact_pref"].required = False
        self.fields["name"].widget.attrs.update({"autocomplete": "name"})
        self.fields["phone"].widget.attrs.update({"autocomplete": "tel", "inputmode": "tel"})
        self.fields["email"].widget.attrs.update({"autocomplete": "email"})

    def clean_kind(self):
        return self.cleaned_data.get("kind") or "full"

    def clean_regions(self):
        return ", ".join(self.cleaned_data.get("regions") or [])

    def clean(self):
        data = super().clean()
        if data.get("website"):
            raise forms.ValidationError("Spam detected.")
        if not data.get("phone") and not data.get("email"):
            raise forms.ValidationError("Leave a phone number or an email so we can send your quote.")
        return data


class SubscribeForm(forms.Form):
    email = forms.EmailField()
    source_page = forms.CharField(required=False, max_length=300)
    website = forms.CharField(required=False)  # honeypot
