from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from django.contrib.auth import logout as auth_logout
from .admin import CreateCustomerForm, BusForm
from collections import defaultdict
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from django.db.models import Subquery, OuterRef
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from datetime import datetime
from django.urls import reverse
from datetime import timedelta
import requests
import uuid
import hmac
import hashlib

# Create your views here.
logger = logging.getLogger('app')
def help(request):
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show" 
    else:
        user_not_login ="show"
        user_login = "hidden"
    is_driver = hasattr(request.user, 'driver')
    is_customer = hasattr(request.user, 'customer')
    is_admin = request.user.is_superuser
    context = {
        'is_driver':is_driver,
        'is_admin':is_admin,
        'is_customer':is_customer,
        'user_not_login': user_not_login,
        'user_login':user_login,}
    return render(request,"app/help.html",context)
def scheduleDriver(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        is_driver = hasattr(request.user, 'driver')
        if request.user.is_superuser:
            current_time = timezone.now()
            trips = Trip.objects.filter(departure_Time__gte=current_time)
            context={
                'trips':trips,
                'user_not_login':user_not_login,
                'user_login':user_login,
                'is_driver':is_driver,}
            return render(request, 'app/admin/scheduleDriver.html', context)
@login_required(login_url='/login/')
def statistics(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        is_driver = hasattr(request.user, 'driver')
        if request.user.is_superuser:
            month = request.GET.get('month')
            year = request.GET.get('year')    
            if month and year:
                try:
                    selected_month_start = timezone.datetime(int(year), int(month), 1)
                except ValueError:
                    return JsonResponse({'error': 'Invalid date'}, status=400)
            else:
                selected_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)            
            routes = Route.objects.all()
            data = []
            data1 = []
            for route in routes:
                current_month_bookings = Booking.objects.filter(
                    idTicket__idTrip__id_Route=route,
                    bookingDate__gte=selected_month_start,
                    bookingDate__lt=selected_month_start + relativedelta(months=1)
                ).count()
                current_month_revenue = Booking.objects.filter(
                    idTicket__idTrip__id_Route=route,
                    bookingDate__gte=selected_month_start,
                    bookingDate__lt=selected_month_start + relativedelta(months=1)
                ).aggregate(total_revenue=Sum('idTicket__idTrip__price'))['total_revenue'] or 0
                data.append({
                    'route': f"{route.startPoint} - {route.endPoint}",
                    'current_month_bookings': current_month_bookings,
                    'current_month_revenue': current_month_revenue,
                })
            current_month_total = Booking.objects.filter(
                bookingDate__gte=selected_month_start,
                bookingDate__lt=selected_month_start + relativedelta(months=1)
            ).aggregate(total_revenue=Sum('idTicket__idTrip__price'))['total_revenue'] or 0

            data1.append({
                'current_month_total': current_month_total,
            })

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'data': data,
                    'data1': data1
                }
                logger.info(f"Response Data: {response_data}")
                return JsonResponse(response_data)
            context = {
                'data': data,
                'data1': data1,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'is_driver': is_driver,
            }
            return render(request, "app/admin/statistics.html", context)
        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'You do not have access.'
            }, status=403)
    return render(request, 'app/errors.html', {
        'error_code': 403,
        'error_message': 'You must login before view.'
    }, status=403)

@login_required(login_url='/login/')
def feedbackAdmin(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        is_driver = hasattr(request.user, 'driver')
        if request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-idTicket__idTrip__departure_Time')
            booked_tickets = []
            seen_trips = set()
            current_date = None
            for booking in bookings:
                ticket = booking.idTicket
                trip = ticket.idTrip if ticket else None
                if trip and trip.id not in seen_trips:
                    if ticket and ticket.status:
                        departure_date = trip.departure_Time.date()
                        formatted_date = departure_date.strftime("%Y-%m-%d")
                        if formatted_date != current_date:
                            booked_tickets.append({
                                'is_date': True,
                                'date': formatted_date,
                            })
                            current_date = formatted_date
                        booked_tickets.append({
                            'ticket': ticket,
                            'booking': booking,
                            'is_date': False,
                        })
                        seen_trips.add(trip.id)
            context = {
                'user_not_login': user_not_login,
                'user_login': user_login,
                'booked_tickets': booked_tickets,
                'is_driver': is_driver,
            }
            return render(request, 'app/admin/feedback.html', context)                
        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'You do not have access.'
            }, status=403)
    return render(request, 'app/errors.html', {
        'error_code': 403,
        'error_message': 'You must login before feedback.'
    }, status=403)


@login_required(login_url='/login/')
def feedback(request, trip_id):
    if request.user.is_authenticated:
        if request.user.is_superuser or hasattr(request.user, 'customer'):
            is_driver = hasattr(request.user, 'driver')
            is_customer = hasattr(request.user, 'customer')
            user_not_login = "hidden"
            user_login = "show"        
            trip = get_object_or_404(Trip, pk=trip_id)            
            can_submit_feedback = False
            if is_customer:            
                can_submit_feedback = Booking.objects.filter(idCustomer=request.user.customer, idTicket__idTrip=trip).exists()
            if request.user.is_superuser:
                can_submit_feedback=True
            if request.method == 'POST' and can_submit_feedback:
                content = request.POST.get('content')
                if content:
                    Feedback.objects.create(
                        content=content,
                        idTrip=trip,
                        user=request.user
                    )
                    return redirect('feedback', trip_id=trip_id)            
            feedbacks = Feedback.objects.filter(idTrip=trip)            
            context = {
                'is_driver': is_driver,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'trip_id': trip_id,
                'feedbacks': feedbacks,
                'is_customer': is_customer,
                'can_submit_feedback': can_submit_feedback,  
            }            
            return render(request, 'app/customer/feedback.html', context)
        else:
            return render(request, 'app/errors.html', {
                            'error_code': 403,
                            'error_message': 'You do not have access.'
                        }, status=403)
    else:
        return render(request, 'app/errors.html', {
            'error_code': 403,
            'error_message': 'You must login before feedback.'
        }, status=403)

def overviewFeedback(request):
            is_driver = hasattr(request.user, 'driver')
            is_customer = hasattr(request.user, 'customer')
            if request.user.is_authenticated:
                user_not_login = "hidden"
                user_login = "show"
            else:
                user_not_login ="show"
                user_login = "hidden" 
            feedbacks = Feedback.objects.select_related('idTrip').all()
            context = {
                'is_driver': is_driver,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'feedbacks': feedbacks,
                'is_customer': is_customer,
            }            
            return render(request, 'app/customer/overviewFeedback.html', context)

@login_required(login_url='/login/')
def schedule(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        is_driver = hasattr(request.user, 'driver')
        if hasattr(request.user, 'driver'):
            buses = Bus.objects.filter(id_Driver=request.user)
            trips = Trip.objects.filter(id_Buses__in=buses, departure_Time__gt=timezone.now())
        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'Driver can see schedule.'
            }, status=403)    
    else:
        return render(request, 'app/errors.html', {
            'error_code': 403,
            'error_message': 'You must login to see schedule.'
        }, status=403)
    context = {
        'buses':buses,
        'is_driver':is_driver,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'trips': trips,
    }
    return render(request, 'app/driver/schedule.html', context)

@login_required(login_url='/login/')
def reportVehicle(request, bus_id, trip_id):
    if request.user.is_authenticated:
        is_driver = hasattr(request.user, 'driver')
        user_not_login = "hidden"
        user_login = "show"
        status="show"
        if hasattr(request.user, 'driver'):
            current_time = timezone.now()
            bus = get_object_or_404(Bus, id=bus_id)
            trip = get_object_or_404(Trip, id=trip_id)
            if current_time <= trip.arrival_Time: status="hidden"
            if request.method == 'POST':
                form = BusForm(request.POST, request.FILES, instance=bus)
                if form.is_valid():
                    form.save()
                    return redirect('reportVehicle', bus_id=bus_id)  
            form = BusForm(instance=bus)
            context = {
                'form': form,
                'status':status,
                'bus_id':bus_id,
                'is_driver':is_driver,
                'user_not_login': user_not_login,
                'user_login': user_login,
                }
            return render(request, 'app/driver/reportVehicle.html', context)
        else:
             return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'Driver can see report vehicle.'
            }, status=403)    
    else:
        return render(request, 'app/errors.html', {
            'error_code': 403,
            'error_message': 'You must login to see report vehicle.'
        }, status=403)


def confirm(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    context = {
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, "app/customer/confirm.html", context)

def search(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    context = {
        'user_not_login': user_not_login,
        'user_login': user_login,
        'routes': VIETNAM_PROVINCES, 
    }
    is_driver = hasattr(request.user, 'driver')
    if request.method == "POST":
        journeyType = request.POST.get('journeyType')
        start_point = request.POST.get('departure')
        end_point = request.POST.get('destination')
        departure_date = request.POST.get('departureDate')
        return_date = request.POST.get('returnDate', None)
        number_of_tickets = request.POST.get('numberOfTickets')

        if not (start_point and end_point and departure_date and number_of_tickets and journeyType):
            context['error_message'] = "Please complete all information!"
            return render(request, 'app/search.html', context)

        number_of_tickets = int(number_of_tickets)
        if journeyType == "true" and return_date:
            departure_date_dt = datetime.strptime(departure_date, '%Y-%m-%d')
            return_date_dt = datetime.strptime(return_date, '%Y-%m-%d')

            if departure_date_dt > return_date_dt:
                context['error_message'] = "Return date must be after the departure date!"
                return render(request, 'app/search.html', context)

        routes = Route.objects.filter(startPoint=start_point, endPoint=end_point)
        trips = Trip.objects.filter(
            id_Route__in=routes,
            departure_Time__date=departure_date,
            total_Seats__gte=number_of_tickets
        ).select_related('id_Buses', 'id_Route').prefetch_related('Tickets')

        if return_date:
            return_routes = Route.objects.filter(startPoint=end_point, endPoint=start_point)
            return_trips = Trip.objects.filter(
                id_Route__in=return_routes,
                departure_Time__date=return_date,
                total_Seats__gte=number_of_tickets
            ).select_related('id_Buses', 'id_Route').prefetch_related('Tickets')
        else:
            return_trips = []

        results = []
        for trip in trips:
            available_tickets = trip.total_Seats - trip.reserved_Seats
            if available_tickets >= number_of_tickets:
                results.append({
                    'trip': trip,
                    'available_tickets': available_tickets,
                    'tickets': trip.Tickets.all(),
                })

        return_results = []
        for return_trip in return_trips:
            available_tickets = return_trip.total_Seats - return_trip.reserved_Seats
            if available_tickets >= number_of_tickets:
                return_results.append({
                    'trip': return_trip,
                    'available_tickets': available_tickets,
                    'tickets': return_trip.Tickets.all(),
                })

        context.update({
            'is_driver': is_driver,
            'trips': results,
            'return_trips': return_results,
            'departure': start_point,
            'destination': end_point,
            'departure_date': departure_date,
            'return_date': return_date,
            'number_of_tickets': number_of_tickets,
            'journeyType': journeyType,
            # 'routes':VIETNAM_PROVINCES,

        })

    return render(request, 'app/search.html', context)

@login_required(login_url='/login/')
def download_customer_info(request, trip_id):
    if request.user.is_authenticated and hasattr(request.user, 'driver'):
        trip = get_object_or_404(Trip, id=trip_id)
        customer_info = Booking.objects.filter(idTicket__idTrip=trip)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="trip_{trip.id}_customer_info.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone Number', 'Ticket Name'])

        for customer in customer_info:
            writer.writerow([customer.name_Customer, customer.phone_Customer, customer.idTicket.name])

        return response
    else:
        return render(request, 'app/errors.html', {
            'error_code': 403,
            'error_message': 'Access denied.'
        }, status=403)

@login_required(login_url='/login/')
def passengerList(request, trip_id):
    if request.user.is_authenticated:
        is_driver = hasattr(request.user, 'driver')
        user_not_login = "hidden"
        user_login = "show"
        if hasattr(request.user, 'driver'):
            trip = get_object_or_404(Trip, id=trip_id)
            customer_info = Booking.objects.filter(idTicket__idTrip=trip)
            

        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'Driver can see passenger list.'
            }, status=403)    
    else:
        return render(request, 'app/errors.html', {
            'error_code': 403,
            'error_message': 'You must login to see passenger list.'
        }, status=403)
    
    
    context = {
        'customer_info':customer_info,
        'is_driver':is_driver,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'trip': trip,
    }
    return render(request, 'app/driver/passengerList.html', context)



@login_required(login_url='/login/')
def history(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        is_driver = hasattr(request.user, 'driver')
        message = None
        if hasattr(request.user, 'customer'):
            user = request.user
            bookings = Booking.objects.filter(idCustomer=user).order_by('-idTicket__idTrip__departure_Time')
            trips_grouped_by_date = []
            for booking in bookings:
                ticket = booking.idTicket
                if ticket and ticket.status:            
                    is_past_trip = timezone.now() > ticket.idTrip.arrival_Time                                            
                    trips_grouped_by_date.append({
                        'ticket': ticket,
                        'booking': booking,
                        'is_past_trip': is_past_trip,  
                    })
            if request.method=='POST':
                ticket_id = request.POST.get('ticket_id')
                try:
                    ticket = Ticket.objects.get(id=ticket_id)
                    if ticket:
                        booking = Booking.objects.filter(idTicket=ticket).first()
                        if booking:
                            if ticket.idTrip.departure_Time - timezone.now() >= timedelta(days=3):                                
                                booking.delete()
                                customer=Customer.objects.get(id=request.user.id)
                                customer.point-=10  
                                customer.save()                                
                                ticket.update_status()                                
                                return redirect(reverse('history') + '?message=Ticket Cancellation Successful')
                            else:
                                return redirect(reverse('history') + '?message=You can only cancel tickets at least 3 days before departure.')

                except Ticket.DoesNotExist:
                    
                    return redirect(f'{reverse("history")}?message=Ticket does not exist.')
            context = {
                'user_not_login': user_not_login,
                'user_login': user_login,
                'trips_grouped_by_date': trips_grouped_by_date,
                'is_driver': is_driver,
            }
            return render(request, 'app/customer/history.html', context)    
        elif is_driver:
            buses = Bus.objects.filter(id_Driver=request.user)
            trips = Trip.objects.filter(id_Buses__in=buses, departure_Time__lt=timezone.now())
            context = {
                'trips': trips,
                'buses': buses,
                'is_driver': is_driver,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'history':True,
            }
            return render(request, 'app/driver/schedule.html', context)        
        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'You do not have access.'
            }, status=403)
    return render(request, 'app/errors.html', {
        'error_code': 403,
        'error_message': 'You must login before view history.'
    }, status=403)

@login_required(login_url='/login/')
def profile(request):
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show" 
        is_driver = hasattr(request.user, 'driver')
        is_customer = hasattr(request.user, 'customer')
    user = request.user
    if is_customer:
        customer = Customer.objects.filter(pk=user.pk).first()
        if customer:
            point = customer.point
    if is_driver:
        driver = Driver.objects.filter(pk=user.pk).first()
        if driver:
            salary = driver.totalSalary
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        if (len(phone_number)!=10): messages.info(request, 'Phone number must be exactly 10 digits!')
        else:
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.first_name = first_name
            user.last_name = last_name
            user.username = user_name
            user.phone_Number = phone_number 
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    context = {
        'is_driver':is_driver,
        'full_name': user.first_name,
        'user_name': user.username,
        'phone': user.phone_Number,
        'email': user.email,
        'user_not_login': user_not_login,
        'user_login':user_login,
        'is_customer':is_customer,
        'point':point if is_customer else 0,
        'salary': salary if is_driver else 0,

    }
    return render(request, 'app/profile.html', context)


def logoutPage(request):
    auth_logout(request)
    request.session.flush()  # Xóa toàn bộ session data
    request.session.clear_expired()  # Xóa session đã hết hạn

    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')


def send_email_booking(request,name,mobie,booked_tickets,user_email):
        subject = 'Successfull Booking'
        message = f'You have booking ticket with {name}, {mobie}, and {booked_tickets}!'
        recipient_list = [user_email]
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            messages.success(request, 'Send email for booking complete!')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'Failed to send email. Error: {str(e)}')
            return JsonResponse({'success': False, 'error': str(e)})

def send_otp_email(request):
        if request.user.is_authenticated:
            user = request.user
            otp = generate_otp()
            request.session['otp'] = otp
            subject = 'OTP for Password Change Request'
            message = f'Your OTP for password change request is: {otp}'
            recipient_list = [user.email]
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
                messages.success(request, 'OTP has been sent to your email.')
                return JsonResponse({'success': True})
            except Exception as e:
                messages.error(request, f'Failed to send OTP. Error: {str(e)}')
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            otp = generate_otp()
            fill_email = request.POST.get('email')
            request.session['otp'] = otp
            request.session['email'] = fill_email
            subject = 'OTP for Password Change Request'
            message = f'Your OTP for password change request is: {otp}'
            recipient_list = [fill_email]
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
                messages.success(request, 'OTP has been sent to your email.')
                return redirect('change_password')
            except Exception as e:
                messages.error(request, f'Failed to send OTP. Error: {str(e)}')
                return redirect('change_password')
            
def formEmail(request):
    return render(request, 'app/formEmail.html')
def generate_otp():
    return str(random.randint(100000, 999999))

def change_password(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        form = PasswordChangeForm(request.user)  # Form dành cho người dùng đã đăng nhập
    else:
        user_not_login = "show"
        user_login = "hidden"
        form = SetPasswordForm(None)  # Form đặt lại mật khẩu cho người dùng chưa đăng nhập

    # Khởi tạo context để truyền vào template
    context = {
        'user_not_login': user_not_login,
        'user_login': user_login,
        'form': form,  # Thêm form vào context
    }

    if request.method == 'POST':
        otp_from_user = request.POST.get('otp', '')
        if otp_from_user:
            if 'otp' in request.session and request.session['otp'] == otp_from_user:
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')

                if new_password1 == new_password2:
                    email = request.session.get('email')
                    if request.user.is_authenticated:
                        user = request.user
                    else:
                        try:
                            user = User.objects.get(email=email)
                        except User.DoesNotExist:
                            messages.error(request, 'No user is associated with this email.')
                            return redirect('forget_password')

                    # Đặt lại mật khẩu cho người dùng
                    user.set_password(new_password1)
                    user.save()

                    # Nếu người dùng đã đăng nhập, xác thực lại
                    if request.user.is_authenticated:
                        updated_user = authenticate(username=user.username, password=new_password1)
                        if updated_user is not None:
                            login(request, updated_user)
                    else:                    
                        messages.success(request, 'You have changed your password successfully!')
                        return redirect('login')

                    # Thông báo thành công và điều hướng
                    messages.success(request, 'You have changed your password successfully!')
                    return redirect('profile')
                else:
                    messages.error(request, 'Passwords do not match.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')

    # Trả về trang `change_password.html` với context
    return render(request, 'app/change_password.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index') 
        elif hasattr(request.user, 'driver'):
            return redirect('schedule')
        return redirect('home') 
       
    user_not_login ="show"
    user_login = "hidden" 
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')    
            elif hasattr(request.user, 'driver'):
                return redirect('schedule')
            else:
                return redirect('home')
        else: messages.info(request, 'User or password is not correct!')
    context = {'user_not_login':user_not_login, 'user_login':user_login}
    return render(request,'app/login.html',context)

def aboutUs(request):
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show" 
    else:
        user_not_login ="show"
        user_login = "hidden" 
    is_driver = hasattr(request.user, 'driver')
    context = {
        'is_driver':is_driver,
        'user_not_login': user_not_login,
        'user_login':user_login,
    }
    return render(request, 'app/aboutUs.html',context)

def register(request):
    form = CreateCustomerForm()
    if request.method == "POST":
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Register successful!")
            return redirect('login')
    user_not_login = "show" 
    user_login = "hidden" 
    return render(request, 'app/register.html', {'form': form,'user_not_login': user_not_login, 'user_login': user_login})

VIETNAM_PROVINCES = [
    ('Hà Nội', 'Hà Nội'),
    ('Hà Giang', 'Hà Giang'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Lào Cai', 'Lào Cai'),
    ('Điện Biên', 'Điện Biên'),
    ('Lai Châu', 'Lai Châu'),
    ('Sơn La', 'Sơn La'),
    ('Yên Bái', 'Yên Bái'),
    ('Hoà Bình', 'Hoà Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Thái Bình', 'Thái Bình'),
    ('Hà Nam', 'Hà Nam'),
    ('Nam Định', 'Nam Định'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Nghệ An', 'Nghệ An'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Bình Định', 'Bình Định'),
    ('Phú Yên', 'Phú Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Kon Tum', 'Kon Tum'),
    ('Gia Lai', 'Gia Lai'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Đà Lạt', 'Đà Lạt'),
    ('Bình Phước', 'Bình Phước'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Bình Dương', 'Bình Dương'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Thành phố Hồ Chí Minh', 'Thành phố Hồ Chí Minh'),
    ('Long An', 'Long An'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Bến Tre', 'Bến Tre'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('An Giang', 'An Giang'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Cà Mau', 'Cà Mau'),
    ]
def index(request):
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show"
    else:
        user_not_login ="show"
        user_login = "hidden"   
    try:        
            all_buses = Bus.objects.all()        
            all_trips = Trip.objects.filter(
                departure_Time__gte=timezone.now(),
                departure_Time__lte= timezone.now() + timedelta(days=3),
            ).order_by('departure_Time')[:8]                   
            hcm = Trip.objects.filter(id_Route__startPoint='Thành phố Hồ Chí Minh', departure_Time__gt=timezone.now())
            dl = Trip.objects.filter(id_Route__startPoint='Đà Lạt', departure_Time__gt=timezone.now())                        
            vt = Trip.objects.filter(
                id_Route__startPoint='Bà Rịa - Vũng Tàu',
                departure_Time__gt=timezone.now()
            ).order_by('id_Route__endPoint', 'departure_Time')
            unique_endpoints = set()
            filtered_vt_trips = []
            for trip in vt:
                if trip.id_Route.endPoint not in unique_endpoints:
                    unique_endpoints.add(trip.id_Route.endPoint)
                    filtered_vt_trips.append(trip)
                if len(filtered_vt_trips) >= 2:
                    break        
            dl = Trip.objects.filter(
                id_Route__startPoint='Đà Lạt',
                departure_Time__gt=timezone.now()
            ).order_by('id_Route__endPoint', 'departure_Time')            
            unique_endpoints = set()
            filtered_dl_trips = []
            for trip in dl:
                if trip.id_Route.endPoint not in unique_endpoints:
                    unique_endpoints.add(trip.id_Route.endPoint)
                    filtered_dl_trips.append(trip)
                if len(filtered_dl_trips) >= 3:
                    break                
            hcm = Trip.objects.filter(
                id_Route__startPoint='Thành phố Hồ Chí Minh',
                departure_Time__gt=timezone.now()
            ).order_by('id_Route__endPoint', 'departure_Time')
            unique_endpoints = set()
            filtered_hcm_trips = []
            for trip in hcm:
                if trip.id_Route.endPoint not in unique_endpoints:
                    unique_endpoints.add(trip.id_Route.endPoint)
                    filtered_hcm_trips.append(trip)
                if len(filtered_hcm_trips) >= 3:
                    break
            user_data = request.session.get('user_data')
            response = request.session.get('response')
            is_driver = hasattr(request.user, 'driver')
            context = {
                'is_driver':is_driver,
                'hcm_trips':filtered_hcm_trips,
                'dl_trips':filtered_dl_trips,
                'vt_trips':filtered_vt_trips,
                'routes':VIETNAM_PROVINCES,
                'all_buses':all_buses,
                'all_trips':all_trips,
                'user_not_login':user_not_login,
                'user_login': user_login,
                'user_data':user_data,
                'response':response,
            }            
            return render(request, 'app/home.html', context)
    except Exception as e:
        return render(request, 'app/home.html', {'error': 'An error occurred'})

def booking(request, trip_id):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        if hasattr(request.user, 'customer'):
            try:
                customer = Customer.objects.get(id=request.user.id)
            except Customer.DoesNotExist:
                customer = None
        else:
            return render(request, 'app/errors.html', {
                'error_code': 403,
                'error_message': 'Customer can booking.'
            }, status=403)        
    else:
        customer = None
        user_not_login = "show"
        user_login = "hidden"
    trip = Trip.objects.get(id=trip_id)
    tickets = Ticket.objects.filter(idTrip=trip)
    error_message = ""
    if request.method == "POST":
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile', '')
        selected_tickets = request.POST.get('selected_tickets')
        payment_method = request.POST.get('payment_method')
        total_price = float(request.POST.get('total_price_input', '0'))*25000
        try:
            selected_tickets = json.loads(selected_tickets)
        except json.JSONDecodeError:
            selected_tickets = []        
        if name and mobile and selected_tickets:
            booked_tickets = []
            for ticket_id in selected_tickets:
                ticket = Ticket.objects.get(id=ticket_id)
                if Booking.objects.filter(idTicket=ticket).exists():
                    error_message = f"Ticket {ticket.idSeatNumber} is already booked."
                    context = {
                        'user_not_login': user_not_login,
                        'user_login': user_login,
                        'trip': trip,
                        'tickets': tickets,
                        'error_message': error_message,
                    }
                    return render(request, 'app/customer/booking.html', context)
                booked_tickets.append(ticket)
            for ticket in booked_tickets:
                if customer:                    
                    customer.point += 10
                    if customer.point>=100:
                        customer.point -= 100
                    customer.save()
                Booking.objects.create(
                    name_Customer=name,
                    phone_Customer=mobile,
                    idTicket=ticket,
                    idCustomer=customer                
                )
            user_email = request.user.email if request.user.is_authenticated else None
            if user_email:
                send_email_booking(name, mobile, selected_tickets, user_email)
            point = customer.point if customer else 0
            if payment_method == "online_payment":
                return redirect(generate_momo_payment_url( total_price))  
            context = {
                'name': name,
                'phone': mobile,
                'booked_tickets': booked_tickets,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'discount_price': point,
            }
            return render(request, "app/customer/confirm.html", context)
        else:
            error_message = "Name and mobile number are required."
            point = customer.point if customer else 0

            context = {
                'discount_price': point,
                'user_not_login': user_not_login,
                'user_login': user_login,
                'trip': trip,
                'tickets': tickets,
                'selected_tickets': selected_tickets,
                'error_message': error_message,
            }
            return render(request, 'app/customer/booking.html', context)        
    point = customer.point if customer else 0
    context = {
        'user_not_login': user_not_login,
        'user_login': user_login,
        'trip': trip,
        'tickets': tickets,
        'error_message': error_message,
        'discount_price': point,

    }
    return render(request, 'app/customer/booking.html', context)

def momo_return(request):
    return redirect('home')


def send_email_booking(name, mobile, booked_tickets, user_email):
    subject = 'Successful Booking'
    message = f'You have booked tickets with the following details:\n\nName: {name}\nMobile: {mobile}\nTickets: {booked_tickets}'
    recipient_list = [user_email]
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return True
    except Exception as e:
        return False
    
def generate_momo_payment_url( amount):
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    partnerCode = "MOMO"
    redirectUrl = "https://smartbus-4b8558a1299d.herokuapp.com/momo_return/"
    ipnUrl = "https://your-ipn-url.com"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    extraData = ""
    amount = int(amount) 
    partnerName = "MoMo Payment"
    requestType = "payWithMethod"
    storeId = "Test Store"
    orderGroupId = ""
    autoCapture = True
    lang = "en"

    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    data = {
        'partnerCode': partnerCode,
        'orderId': orderId,
        'partnerName': partnerName,
        'storeId': storeId,
        'ipnUrl': ipnUrl,
        'amount': amount,
        'lang': lang,
        'requestType': requestType,
        'redirectUrl': redirectUrl,
        'autoCapture': autoCapture,
        'orderInfo': orderInfo,
        'requestId': requestId,
        'extraData': extraData,
        'signature': signature,
        'orderGroupId': orderGroupId
    }

    response = requests.post(endpoint, json=data, headers={'Content-Type': 'application/json'})
    result = response.json()

    if 'payUrl' in result:
        return result['payUrl']
    else:
        raise Exception(f"MoMo payment error: {result.get('message', 'Unknown error')}")


# NGUYEN VAN A
# 9704 0000 0000 0018
# 03/07
# OTP