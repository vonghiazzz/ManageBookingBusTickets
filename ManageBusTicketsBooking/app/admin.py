from django.contrib import admin
from .models import *
from django.contrib.admin.actions import delete_selected
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import mark_safe
from django.shortcuts import redirect
from datetime import timedelta
class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username','email','first_name','last_name','password1','password2','phone_Number']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this Email already exists!")
        return email

class BusForm(forms.ModelForm):
    class Meta:
        model= Bus 
        fields='__all__'
        labels = {
            'vehicle_Condition': 'Vehicle Condition', 
            'idType':'Type of Bus',
            'id_Driver':'ID Driver',
        }

class BusAdmin(admin.ModelAdmin):
    class Media: 
        css={
        }
        js={
        }
    form = BusForm
    list_display=["id","vehycle_number","created_date","id_Driver","active"] 
    search_fields= ["created_date","vehycle_number"] 
    list_filter = ["active"]
    fields = ['vehycle_number','active','id_Driver','idType', 'vehicle_Condition']

class CustomerAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img","point"] 
    search_fields= ["username","email"] 
    readonly_fields = ["last_login","date_joined","img", "point"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number','point')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}), 
    )
    def img(self,user):
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

class DriverAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img","totalDrivingTime","totalSalary"] 
    search_fields= ["username","email"] 
    readonly_fields = ["last_login","date_joined","img", "totalDrivingTime","totalSalary"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number','totalSalary','totalDrivingTime')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),   
    )
    def img(self,user):
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

class SalaryForm(forms.ModelForm):
    class Meta:
        model= Salary 
        fields='__all__'
        labels = {
            'totalDistance': 'Total Distance', 
            'idDriver':'ID Driver',
        } 

class SalaryAdmin(admin.ModelAdmin):
    form = SalaryForm
    list_display=["id","month","totalDistance","idDriver"] 
    search_fields= ["id","idDriver","month"] 

class UserAdmin(admin.ModelAdmin):
    list_display=["id","username","email","img"] 
    search_fields= ["username","email"] 
    readonly_fields = ["last_login","date_joined","img","password"]  
    fieldsets = (
        ('Account', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'img','avatar','phone_Number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )
    def img(self,user):
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' alt='{user.username}' width='120px'/>")
        return "(No image)"
    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

class FeedbackForm(forms.ModelForm):
    class Meta:
            model= Feedback 
            fields='__all__'
            labels = {
                'feedback_date': 'Date time',
                'idTrip':'ID Trip',
            }

class FeedbackAdmin(admin.ModelAdmin):
    class Media: 
        css={
        }
        js={
        }
    form = FeedbackForm
    list_display=["id","feedback_date","idTrip","user"] 
    readonly_fields=["feedback_date"]
    def add_view(self, request, form_url='', extra_context=None):
        return redirect('/feedback/')  


class TickForm(forms.ModelForm):
    class Meta:
            model= Ticket 
            fields='__all__'
            labels = {
                'img': 'Image', 
                'idSeatNumber':'Seat Number',
                'idBus':'ID Bus',
                'idTrip':'ID Trip',
            }

class TickAdmin(admin.ModelAdmin):
    form = TickForm
    list_display=["id","name","created_date","status","active"] 
    search_fields= ["created_date"] 
    list_filter = ["active","status"]
    readonly_fields=["avatar","idSeatNumber"]
    def avatar(self,ticket):
        if ticket.img:
            return mark_safe(f"<img src='{ticket.img.url}' alt='{ticket.name}' width='120px'/>")
        return "(No image)"
    
class BookForm(forms.ModelForm):
    class Meta:
            model= Booking
            fields='__all__'
            labels = {
                'idCustomer':'ID Customer',
                'idTicket':'ID Ticket',
            }
class BookAdmin(admin.ModelAdmin):
    form = BookForm
    actions = ['delete_selected']
    def delete_selected(self, request, queryset):
        for booking in queryset:
            if booking.id:
                old_ticket = booking.idTicket
                booking.delete()
                if old_ticket:
                    old_ticket.status = False
                    old_ticket.save()
                    if old_ticket.idTrip:
                        trip = old_ticket.idTrip
                        if trip:
                            trip.reserved_Seats = Ticket.objects.filter(idTrip=trip, status=True).count()
                            Trip.objects.filter(pk=trip.pk).update(reserved_Seats=trip.reserved_Seats)
                    else:
                        print(f"No idTrip found for old_ticket {old_ticket.id}")
    list_display=["id","idTicket","idTrip_info","bookingDate","idCustomer","status"] 
    search_fields= ["idTicket__name", "bookingDate"] 
    list_filter = ["status"]
    def idTrip_info(self, obj):
        if obj.idTicket and obj.idTicket.idTrip:
            trip_id = obj.idTicket.idTrip.id
            trip_name = obj.idTicket.idTrip
            return f"{trip_id} - {trip_name}"
        return "-"
    idTrip_info.short_description = 'Trip Info'

class SeatNumberAdminForm(forms.ModelForm):
    class Meta:
        model = SeatNumber
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        seat_number = cleaned_data.get('seat_number')
        idBus = cleaned_data.get('idBus')
        if seat_number and idBus:
            max_seat_number = idBus.totalSeats
            if seat_number > max_seat_number:
                raise forms.ValidationError(
                    f"The seat number must be less than or equal to {max_seat_number}"
                )

class SeatNumberAdmin(admin.ModelAdmin):
    form = SeatNumberAdminForm

class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'
        labels = {
                'startPoint':'Start Point',
                'endPoint':'End Point',
            }

class RouteAdmin(admin.ModelAdmin):
    form = RouteAdminForm
    list_display=["id","name"]  

class TripAdminForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        startPoint = cleaned_data.get('departure_Station')
        endPoint = cleaned_data.get('ending_Station')
        id_Buses = cleaned_data.get("idTrip_id_Buses")
        departure_Time = cleaned_data.get("departure_Time")
        arrival_Time = cleaned_data.get("arrival_Time")
        trip_name = f"{startPoint} - {endPoint} - {departure_Time}"

        if Ticket.objects.filter(name__startswith=trip_name).exists():
            raise ValidationError(f"Name of Ticket '{trip_name}' already exists.")
 
        if id_Buses:
            overlapping_trips = Trip.objects.filter(
                    id_Buses=id_Buses,
                    departure_Time__lte=arrival_Time + timedelta(hours=1),
                    arrival_Time__gte=departure_Time - timedelta(hours=1)
                ).exclude(pk=self.instance.pk)
            if overlapping_trips.exists():
                raise forms.ValidationError(f"Bus {id_Buses} is assigned to another trip during this period or within 1 hour after the trip.")

        if startPoint == endPoint:
            raise forms.ValidationError("Start point and end point must be different")
        if departure_Time==None and arrival_Time==None:
            raise ValidationError("Departure time and Arrival time cannot be None.")
        if departure_Time < timezone.now():
            raise ValidationError("Departure time cannot be in the past.")
        if departure_Time and arrival_Time <= departure_Time:
            raise ValidationError("Arrival time must be after the departure time.")
        return cleaned_data

class TripAdmin(admin.ModelAdmin):
    form = TripAdminForm
    list_display=["id","name","departure_Time","arrival_Time","created_date","reserved_Seats", "total_Seats","active"] 
    search_fields= ["created_date"] 
    list_filter = ["active"]
    readonly_fields=["hours","reserved_Seats", "total_Seats","distance"]
    
class AppAdminSite(admin.AdminSite):
    site_header = "Bus ticket Management"
    site_title = 'Admin Portal'
    index_title = 'Welcome to manage page'


admin_site = AppAdminSite('myapp')
admin_site.index_template = 'app/admin/custom_admin.html'
admin_site.register(Driver,DriverAdmin)
admin_site.register(Customer,CustomerAdmin)
admin_site.register(Bus,BusAdmin)
admin_site.register(SeatNumber, SeatNumberAdmin)
admin_site.register(Trip, TripAdmin)
admin_site.register(Type)
admin_site.register(Ticket, TickAdmin)
admin_site.register(Booking,BookAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Route, RouteAdmin)
admin_site.register(Feedback, FeedbackAdmin)
admin_site.register(Salary, SalaryAdmin)

    # admin_site.register(Group)
    # admin_site.register(Permission)

