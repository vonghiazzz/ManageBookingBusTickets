# Generated by Django 4.2.15 on 2024-08-29 07:38

import app.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_Number', models.CharField(blank=True, max_length=10, null=True, validators=[app.models.validate_phone_number])),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to='uploads/%Y/%m')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('email',)},
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('vehycle_number', models.CharField(max_length=8)),
                ('vehicle_Condition', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Buses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('startPoint', models.CharField(choices=[('Hà Nội', 'Hà Nội'), ('Hà Giang', 'Hà Giang'), ('Cao Bằng', 'Cao Bằng'), ('Bắc Kạn', 'Bắc Kạn'), ('Tuyên Quang', 'Tuyên Quang'), ('Lào Cai', 'Lào Cai'), ('Điện Biên', 'Điện Biên'), ('Lai Châu', 'Lai Châu'), ('Sơn La', 'Sơn La'), ('Yên Bái', 'Yên Bái'), ('Hoà Bình', 'Hoà Bình'), ('Thái Nguyên', 'Thái Nguyên'), ('Lạng Sơn', 'Lạng Sơn'), ('Quảng Ninh', 'Quảng Ninh'), ('Bắc Giang', 'Bắc Giang'), ('Phú Thọ', 'Phú Thọ'), ('Vĩnh Phúc', 'Vĩnh Phúc'), ('Bắc Ninh', 'Bắc Ninh'), ('Hải Dương', 'Hải Dương'), ('Hải Phòng', 'Hải Phòng'), ('Hưng Yên', 'Hưng Yên'), ('Thái Bình', 'Thái Bình'), ('Hà Nam', 'Hà Nam'), ('Nam Định', 'Nam Định'), ('Ninh Bình', 'Ninh Bình'), ('Thanh Hóa', 'Thanh Hóa'), ('Nghệ An', 'Nghệ An'), ('Hà Tĩnh', 'Hà Tĩnh'), ('Quảng Bình', 'Quảng Bình'), ('Quảng Trị', 'Quảng Trị'), ('Thừa Thiên Huế', 'Thừa Thiên Huế'), ('Đà Nẵng', 'Đà Nẵng'), ('Quảng Nam', 'Quảng Nam'), ('Quảng Ngãi', 'Quảng Ngãi'), ('Bình Định', 'Bình Định'), ('Phú Yên', 'Phú Yên'), ('Khánh Hòa', 'Khánh Hòa'), ('Ninh Thuận', 'Ninh Thuận'), ('Bình Thuận', 'Bình Thuận'), ('Kon Tum', 'Kon Tum'), ('Gia Lai', 'Gia Lai'), ('Đắk Lắk', 'Đắk Lắk'), ('Đắk Nông', 'Đắk Nông'), ('Đà Lạt', 'Đà Lạt'), ('Bình Phước', 'Bình Phước'), ('Tây Ninh', 'Tây Ninh'), ('Bình Dương', 'Bình Dương'), ('Đồng Nai', 'Đồng Nai'), ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'), ('Thành phố Hồ Chí Minh', 'Thành phố Hồ Chí Minh'), ('Long An', 'Long An'), ('Tiền Giang', 'Tiền Giang'), ('Bến Tre', 'Bến Tre'), ('Trà Vinh', 'Trà Vinh'), ('Vĩnh Long', 'Vĩnh Long'), ('Đồng Tháp', 'Đồng Tháp'), ('An Giang', 'An Giang'), ('Kiên Giang', 'Kiên Giang'), ('Cần Thơ', 'Cần Thơ'), ('Hậu Giang', 'Hậu Giang'), ('Sóc Trăng', 'Sóc Trăng'), ('Bạc Liêu', 'Bạc Liêu'), ('Cà Mau', 'Cà Mau')], max_length=50)),
                ('endPoint', models.CharField(choices=[('Hà Nội', 'Hà Nội'), ('Hà Giang', 'Hà Giang'), ('Cao Bằng', 'Cao Bằng'), ('Bắc Kạn', 'Bắc Kạn'), ('Tuyên Quang', 'Tuyên Quang'), ('Lào Cai', 'Lào Cai'), ('Điện Biên', 'Điện Biên'), ('Lai Châu', 'Lai Châu'), ('Sơn La', 'Sơn La'), ('Yên Bái', 'Yên Bái'), ('Hoà Bình', 'Hoà Bình'), ('Thái Nguyên', 'Thái Nguyên'), ('Lạng Sơn', 'Lạng Sơn'), ('Quảng Ninh', 'Quảng Ninh'), ('Bắc Giang', 'Bắc Giang'), ('Phú Thọ', 'Phú Thọ'), ('Vĩnh Phúc', 'Vĩnh Phúc'), ('Bắc Ninh', 'Bắc Ninh'), ('Hải Dương', 'Hải Dương'), ('Hải Phòng', 'Hải Phòng'), ('Hưng Yên', 'Hưng Yên'), ('Thái Bình', 'Thái Bình'), ('Hà Nam', 'Hà Nam'), ('Nam Định', 'Nam Định'), ('Ninh Bình', 'Ninh Bình'), ('Thanh Hóa', 'Thanh Hóa'), ('Nghệ An', 'Nghệ An'), ('Hà Tĩnh', 'Hà Tĩnh'), ('Quảng Bình', 'Quảng Bình'), ('Quảng Trị', 'Quảng Trị'), ('Thừa Thiên Huế', 'Thừa Thiên Huế'), ('Đà Nẵng', 'Đà Nẵng'), ('Quảng Nam', 'Quảng Nam'), ('Quảng Ngãi', 'Quảng Ngãi'), ('Bình Định', 'Bình Định'), ('Phú Yên', 'Phú Yên'), ('Khánh Hòa', 'Khánh Hòa'), ('Ninh Thuận', 'Ninh Thuận'), ('Bình Thuận', 'Bình Thuận'), ('Kon Tum', 'Kon Tum'), ('Gia Lai', 'Gia Lai'), ('Đắk Lắk', 'Đắk Lắk'), ('Đắk Nông', 'Đắk Nông'), ('Đà Lạt', 'Đà Lạt'), ('Bình Phước', 'Bình Phước'), ('Tây Ninh', 'Tây Ninh'), ('Bình Dương', 'Bình Dương'), ('Đồng Nai', 'Đồng Nai'), ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'), ('Thành phố Hồ Chí Minh', 'Thành phố Hồ Chí Minh'), ('Long An', 'Long An'), ('Tiền Giang', 'Tiền Giang'), ('Bến Tre', 'Bến Tre'), ('Trà Vinh', 'Trà Vinh'), ('Vĩnh Long', 'Vĩnh Long'), ('Đồng Tháp', 'Đồng Tháp'), ('An Giang', 'An Giang'), ('Kiên Giang', 'Kiên Giang'), ('Cần Thơ', 'Cần Thơ'), ('Hậu Giang', 'Hậu Giang'), ('Sóc Trăng', 'Sóc Trăng'), ('Bạc Liêu', 'Bạc Liêu'), ('Cà Mau', 'Cà Mau')], max_length=50)),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('startPoint', 'endPoint')},
            },
        ),
        migrations.CreateModel(
            name='SeatNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('idBus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seatNumber', to='app.bus')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('seat_number', 'idBus')},
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('point', models.FloatField(default=0, max_length=10)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('app.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('totalDrivingTime', models.FloatField(default=0, max_length=10)),
                ('totalSalary', models.FloatField(default=0, max_length=10)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=('app.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(200)])),
                ('distance', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3000)])),
                ('departure_Station', models.CharField(choices=[('Gas Hà Nội,21.0285,105.8542', 'Gas Hà Nội'), ('Gas Hà Giang,22.3255,104.4660', 'Gas Hà Giang'), ('Gas Cao Bằng,22.6636,106.2874', 'Gas Cao Bằng'), ('Gas Bắc Kạn,22.1533,105.6126', 'Gas Bắc Kạn'), ('Gas Tuyên Quang,21.8122,105.2176', 'Gas Tuyên Quang'), ('Gas Lạng Sơn,21.8458,106.7610', 'Gas Lạng Sơn'), ('Gas Quảng Ninh,21.0467,107.0832', 'Gas Quảng Ninh'), ('Gas Bắc Giang,21.2726,106.2025', 'Gas Bắc Giang'), ('Gas Bắc Ninh,21.1857,106.0854', 'Gas Bắc Ninh'), ('Gas Hải Dương,20.9388,106.3216', 'Gas Hải Dương'), ('Gas Hải Phòng,20.8449,106.6881', 'Gas Hải Phòng'), ('Gas Hưng Yên,20.5882,106.0664', 'Gas Hưng Yên'), ('Gas Thái Bình,20.4477,106.3586', 'Gas Thái Bình'), ('Gas Hà Nam,20.5737,105.9898', 'Gas Hà Nam'), ('Gas Nam Định,20.4098,106.1630', 'Gas Nam Định'), ('Gas Ninh Bình,20.2530,105.9767', 'Gas Ninh Bình'), ('Gas Thanh Hóa,19.8076,105.7740', 'Gas Thanh Hóa'), ('Gas Nghệ An,19.2613,104.4558', 'Gas Nghệ An'), ('Gas Hà Tĩnh,18.3358,105.9112', 'Gas Hà Tĩnh'), ('Gas Quảng Bình,17.4620,106.1955', 'Gas Quảng Bình'), ('Gas Quảng Trị,16.7425,107.1276', 'Gas Quảng Trị'), ('Gas Thừa Thiên Huế,16.4637,107.5836', 'Gas Thừa Thiên Huế'), ('Gas Đà Nẵng,16.0544,108.2022', 'Gas Đà Nẵng'), ('Gas Quảng Nam,15.5850,108.0751', 'Gas Quảng Nam'), ('Gas Quảng Ngãi,15.1176,108.8404', 'Gas Quảng Ngãi'), ('Gas Bình Định,13.7824,109.2102', 'Gas Bình Định'), ('Gas Phú Yên,13.0900,109.2470', 'Gas Phú Yên'), ('Gas Khánh Hòa,12.2384,109.1967', 'Gas Khánh Hòa'), ('Gas Ninh Thuận,11.5802,108.9351', 'Gas Ninh Thuận'), ('Gas Bình Thuận,10.9284,108.4731', 'Gas Bình Thuận'), ('Gas Đà Lạt,11.6684,108.5402', 'Gas Đà Lạt'), ('Gas Đắk Lắk,12.6780,108.3434', 'Gas Đắk Lắk'), ('Gas Đắk Nông,12.1910,107.5921', 'Gas Đắk Nông'), ('Gas Gia Lai,13.9860,108.4451', 'Gas Gia Lai'), ('Gas Kon Tum,14.3506,108.0001', 'Gas Kon Tum'), ('Gas Hồ Chí Minh,10.8231,106.6297', 'Gas Hồ Chí Minh'), ('Gas Bình Dương,11.0072,106.6512', 'Gas Bình Dương'), ('Gas Bình Phước,11.5020,106.9498', 'Gas Bình Phước'), ('Gas Tây Ninh,11.3478,106.1034', 'Gas Tây Ninh'), ('Gas Long An,10.5580,106.3420', 'Gas Long An'), ('Gas Tiền Giang,10.3619,106.3481', 'Gas Tiền Giang'), ('Gas Bến Tre,10.2430,106.3570', 'Gas Bến Tre'), ('Gas Trà Vinh,9.9274,106.3294', 'Gas Trà Vinh'), ('Gas Vĩnh Long,10.2537,105.9562', 'Gas Vĩnh Long'), ('Gas Cần Thơ,10.0451,105.7460', 'Gas Cần Thơ'), ('Gas Hậu Giang,10.3130,105.3880', 'Gas Hậu Giang'), ('Gas Sóc Trăng,9.5960,105.9800', 'Gas Sóc Trăng'), ('Gas Bạc Liêu,9.2950,105.7117', 'Gas Bạc Liêu'), ('Gas Cà Mau,9.1750,105.1500', 'Gas Cà Mau')], default='Gas Đà Lạt,11.6684,108.5402', max_length=100)),
                ('ending_Station', models.CharField(choices=[('Gas Hà Nội,21.0285,105.8542', 'Gas Hà Nội'), ('Gas Hà Giang,22.3255,104.4660', 'Gas Hà Giang'), ('Gas Cao Bằng,22.6636,106.2874', 'Gas Cao Bằng'), ('Gas Bắc Kạn,22.1533,105.6126', 'Gas Bắc Kạn'), ('Gas Tuyên Quang,21.8122,105.2176', 'Gas Tuyên Quang'), ('Gas Lạng Sơn,21.8458,106.7610', 'Gas Lạng Sơn'), ('Gas Quảng Ninh,21.0467,107.0832', 'Gas Quảng Ninh'), ('Gas Bắc Giang,21.2726,106.2025', 'Gas Bắc Giang'), ('Gas Bắc Ninh,21.1857,106.0854', 'Gas Bắc Ninh'), ('Gas Hải Dương,20.9388,106.3216', 'Gas Hải Dương'), ('Gas Hải Phòng,20.8449,106.6881', 'Gas Hải Phòng'), ('Gas Hưng Yên,20.5882,106.0664', 'Gas Hưng Yên'), ('Gas Thái Bình,20.4477,106.3586', 'Gas Thái Bình'), ('Gas Hà Nam,20.5737,105.9898', 'Gas Hà Nam'), ('Gas Nam Định,20.4098,106.1630', 'Gas Nam Định'), ('Gas Ninh Bình,20.2530,105.9767', 'Gas Ninh Bình'), ('Gas Thanh Hóa,19.8076,105.7740', 'Gas Thanh Hóa'), ('Gas Nghệ An,19.2613,104.4558', 'Gas Nghệ An'), ('Gas Hà Tĩnh,18.3358,105.9112', 'Gas Hà Tĩnh'), ('Gas Quảng Bình,17.4620,106.1955', 'Gas Quảng Bình'), ('Gas Quảng Trị,16.7425,107.1276', 'Gas Quảng Trị'), ('Gas Thừa Thiên Huế,16.4637,107.5836', 'Gas Thừa Thiên Huế'), ('Gas Đà Nẵng,16.0544,108.2022', 'Gas Đà Nẵng'), ('Gas Quảng Nam,15.5850,108.0751', 'Gas Quảng Nam'), ('Gas Quảng Ngãi,15.1176,108.8404', 'Gas Quảng Ngãi'), ('Gas Bình Định,13.7824,109.2102', 'Gas Bình Định'), ('Gas Phú Yên,13.0900,109.2470', 'Gas Phú Yên'), ('Gas Khánh Hòa,12.2384,109.1967', 'Gas Khánh Hòa'), ('Gas Ninh Thuận,11.5802,108.9351', 'Gas Ninh Thuận'), ('Gas Bình Thuận,10.9284,108.4731', 'Gas Bình Thuận'), ('Gas Đà Lạt,11.6684,108.5402', 'Gas Đà Lạt'), ('Gas Đắk Lắk,12.6780,108.3434', 'Gas Đắk Lắk'), ('Gas Đắk Nông,12.1910,107.5921', 'Gas Đắk Nông'), ('Gas Gia Lai,13.9860,108.4451', 'Gas Gia Lai'), ('Gas Kon Tum,14.3506,108.0001', 'Gas Kon Tum'), ('Gas Hồ Chí Minh,10.8231,106.6297', 'Gas Hồ Chí Minh'), ('Gas Bình Dương,11.0072,106.6512', 'Gas Bình Dương'), ('Gas Bình Phước,11.5020,106.9498', 'Gas Bình Phước'), ('Gas Tây Ninh,11.3478,106.1034', 'Gas Tây Ninh'), ('Gas Long An,10.5580,106.3420', 'Gas Long An'), ('Gas Tiền Giang,10.3619,106.3481', 'Gas Tiền Giang'), ('Gas Bến Tre,10.2430,106.3570', 'Gas Bến Tre'), ('Gas Trà Vinh,9.9274,106.3294', 'Gas Trà Vinh'), ('Gas Vĩnh Long,10.2537,105.9562', 'Gas Vĩnh Long'), ('Gas Cần Thơ,10.0451,105.7460', 'Gas Cần Thơ'), ('Gas Hậu Giang,10.3130,105.3880', 'Gas Hậu Giang'), ('Gas Sóc Trăng,9.5960,105.9800', 'Gas Sóc Trăng'), ('Gas Bạc Liêu,9.2950,105.7117', 'Gas Bạc Liêu'), ('Gas Cà Mau,9.1750,105.1500', 'Gas Cà Mau')], default='Gas Cần Thơ,10.0451,105.7460', max_length=100)),
                ('departure_Time', models.DateTimeField(default=django.utils.timezone.now)),
                ('arrival_Time', models.DateTimeField(default=django.utils.timezone.now)),
                ('hours', models.CharField(blank=True, max_length=20, null=True)),
                ('total_Seats', models.IntegerField(default=34)),
                ('reserved_Seats', models.IntegerField(default=0)),
                ('id_Buses', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip', to='app.bus')),
                ('id_Route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip', to='app.route')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('departure_Station', 'departure_Time', 'id_Buses')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='ticket/%Y/%m')),
                ('status', models.BooleanField(default=False)),
                ('idSeatNumber', models.ForeignKey(limit_choices_to={'seat_number__isnull': True}, on_delete=django.db.models.deletion.CASCADE, related_name='Tickets', to='app.seatnumber')),
                ('idTrip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Tickets', to='app.trip')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('feedback_date', models.DateTimeField(auto_now_add=True)),
                ('idTrip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='app.trip')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='idType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Buss', to='app.type'),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('totalDistance', models.FloatField(max_length=10)),
                ('idDriver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Salary', to='app.driver')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='id_Driver',
            field=models.ForeignKey(limit_choices_to={'bus__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.driver'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Customer', models.CharField(max_length=100)),
                ('phone_Customer', models.CharField(blank=True, max_length=10, null=True, validators=[app.models.validate_phone_number])),
                ('bookingDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('idTicket', models.ForeignKey(blank=True, limit_choices_to={'booking__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.ticket')),
                ('idCustomer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Booking', to='app.customer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='bus',
            unique_together={('vehycle_number',)},
        ),
    ]
