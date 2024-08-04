# Generated by Django 5.0.3 on 2024-07-31 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_trip_departure_station_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='departure_Station',
            field=models.CharField(choices=[('Gas Hà Nội,21.0285,105.8542', 'Gas Hà Nội'), ('Gas Hà Giang,22.3255,104.4660', 'Gas Hà Giang'), ('Gas Cao Bằng,22.6636,106.2874', 'Gas Cao Bằng'), ('Gas Bắc Kạn,22.1533,105.6126', 'Gas Bắc Kạn'), ('Gas Tuyên Quang,21.8122,105.2176', 'Gas Tuyên Quang'), ('Gas Lạng Sơn,21.8458,106.7610', 'Gas Lạng Sơn'), ('Gas Quảng Ninh,21.0467,107.0832', 'Gas Quảng Ninh'), ('Gas Bắc Giang,21.2726,106.2025', 'Gas Bắc Giang'), ('Gas Bắc Ninh,21.1857,106.0854', 'Gas Bắc Ninh'), ('Gas Hải Dương,20.9388,106.3216', 'Gas Hải Dương'), ('Gas Hải Phòng,20.8449,106.6881', 'Gas Hải Phòng'), ('Gas Hưng Yên,20.5882,106.0664', 'Gas Hưng Yên'), ('Gas Thái Bình,20.4477,106.3586', 'Gas Thái Bình'), ('Gas Hà Nam,20.5737,105.9898', 'Gas Hà Nam'), ('Gas Nam Định,20.4098,106.1630', 'Gas Nam Định'), ('Gas Ninh Bình,20.2530,105.9767', 'Gas Ninh Bình'), ('Gas Thanh Hóa,19.8076,105.7740', 'Gas Thanh Hóa'), ('Gas Nghệ An,19.2613,104.4558', 'Gas Nghệ An'), ('Gas Hà Tĩnh,18.3358,105.9112', 'Gas Hà Tĩnh'), ('Gas Quảng Bình,17.4620,106.1955', 'Gas Quảng Bình'), ('Gas Quảng Trị,16.7425,107.1276', 'Gas Quảng Trị'), ('Gas Thừa Thiên Huế,16.4637,107.5836', 'Gas Thừa Thiên Huế'), ('Gas Đà Nẵng,16.0544,108.2022', 'Gas Đà Nẵng'), ('Gas Quảng Nam,15.5850,108.0751', 'Gas Quảng Nam'), ('Gas Quảng Ngãi,15.1176,108.8404', 'Gas Quảng Ngãi'), ('Gas Bình Định,13.7824,109.2102', 'Gas Bình Định'), ('Gas Phú Yên,13.0900,109.2470', 'Gas Phú Yên'), ('Gas Khánh Hòa,12.2384,109.1967', 'Gas Khánh Hòa'), ('Gas Ninh Thuận,11.5802,108.9351', 'Gas Ninh Thuận'), ('Gas Bình Thuận,10.9284,108.4731', 'Gas Bình Thuận'), ('Gas Lâm Đồng,11.6684,108.5402', 'Gas Lâm Đồng'), ('Gas Đắk Lắk,12.6780,108.3434', 'Gas Đắk Lắk'), ('Gas Đắk Nông,12.1910,107.5921', 'Gas Đắk Nông'), ('Gas Gia Lai,13.9860,108.4451', 'Gas Gia Lai'), ('Gas Kon Tum,14.3506,108.0001', 'Gas Kon Tum'), ('Gas Hồ Chí Minh,10.8231,106.6297', 'Gas Hồ Chí Minh'), ('Gas Bình Dương,11.0072,106.6512', 'Gas Bình Dương'), ('Gas Bình Phước,11.5020,106.9498', 'Gas Bình Phước'), ('Gas Tây Ninh,11.3478,106.1034', 'Gas Tây Ninh'), ('Gas Long An,10.5580,106.3420', 'Gas Long An'), ('Gas Tiền Giang,10.3619,106.3481', 'Gas Tiền Giang'), ('Gas Bến Tre,10.2430,106.3570', 'Gas Bến Tre'), ('Gas Trà Vinh,9.9274,106.3294', 'Gas Trà Vinh'), ('Gas Vĩnh Long,10.2537,105.9562', 'Gas Vĩnh Long'), ('Gas Cần Thơ,10.0451,105.7460', 'Gas Cần Thơ'), ('Gas Hậu Giang,10.3130,105.3880', 'Gas Hậu Giang'), ('Gas Sóc Trăng,9.5960,105.9800', 'Gas Sóc Trăng'), ('Gas Bạc Liêu,9.2950,105.7117', 'Gas Bạc Liêu'), ('Gas Cà Mau,9.1750,105.1500', 'Gas Cà Mau')], default='Gas Đà Lạt', max_length=100),
        ),
        migrations.AlterField(
            model_name='trip',
            name='ending_Station',
            field=models.CharField(choices=[('Gas Hà Nội,21.0285,105.8542', 'Gas Hà Nội'), ('Gas Hà Giang,22.3255,104.4660', 'Gas Hà Giang'), ('Gas Cao Bằng,22.6636,106.2874', 'Gas Cao Bằng'), ('Gas Bắc Kạn,22.1533,105.6126', 'Gas Bắc Kạn'), ('Gas Tuyên Quang,21.8122,105.2176', 'Gas Tuyên Quang'), ('Gas Lạng Sơn,21.8458,106.7610', 'Gas Lạng Sơn'), ('Gas Quảng Ninh,21.0467,107.0832', 'Gas Quảng Ninh'), ('Gas Bắc Giang,21.2726,106.2025', 'Gas Bắc Giang'), ('Gas Bắc Ninh,21.1857,106.0854', 'Gas Bắc Ninh'), ('Gas Hải Dương,20.9388,106.3216', 'Gas Hải Dương'), ('Gas Hải Phòng,20.8449,106.6881', 'Gas Hải Phòng'), ('Gas Hưng Yên,20.5882,106.0664', 'Gas Hưng Yên'), ('Gas Thái Bình,20.4477,106.3586', 'Gas Thái Bình'), ('Gas Hà Nam,20.5737,105.9898', 'Gas Hà Nam'), ('Gas Nam Định,20.4098,106.1630', 'Gas Nam Định'), ('Gas Ninh Bình,20.2530,105.9767', 'Gas Ninh Bình'), ('Gas Thanh Hóa,19.8076,105.7740', 'Gas Thanh Hóa'), ('Gas Nghệ An,19.2613,104.4558', 'Gas Nghệ An'), ('Gas Hà Tĩnh,18.3358,105.9112', 'Gas Hà Tĩnh'), ('Gas Quảng Bình,17.4620,106.1955', 'Gas Quảng Bình'), ('Gas Quảng Trị,16.7425,107.1276', 'Gas Quảng Trị'), ('Gas Thừa Thiên Huế,16.4637,107.5836', 'Gas Thừa Thiên Huế'), ('Gas Đà Nẵng,16.0544,108.2022', 'Gas Đà Nẵng'), ('Gas Quảng Nam,15.5850,108.0751', 'Gas Quảng Nam'), ('Gas Quảng Ngãi,15.1176,108.8404', 'Gas Quảng Ngãi'), ('Gas Bình Định,13.7824,109.2102', 'Gas Bình Định'), ('Gas Phú Yên,13.0900,109.2470', 'Gas Phú Yên'), ('Gas Khánh Hòa,12.2384,109.1967', 'Gas Khánh Hòa'), ('Gas Ninh Thuận,11.5802,108.9351', 'Gas Ninh Thuận'), ('Gas Bình Thuận,10.9284,108.4731', 'Gas Bình Thuận'), ('Gas Lâm Đồng,11.6684,108.5402', 'Gas Lâm Đồng'), ('Gas Đắk Lắk,12.6780,108.3434', 'Gas Đắk Lắk'), ('Gas Đắk Nông,12.1910,107.5921', 'Gas Đắk Nông'), ('Gas Gia Lai,13.9860,108.4451', 'Gas Gia Lai'), ('Gas Kon Tum,14.3506,108.0001', 'Gas Kon Tum'), ('Gas Hồ Chí Minh,10.8231,106.6297', 'Gas Hồ Chí Minh'), ('Gas Bình Dương,11.0072,106.6512', 'Gas Bình Dương'), ('Gas Bình Phước,11.5020,106.9498', 'Gas Bình Phước'), ('Gas Tây Ninh,11.3478,106.1034', 'Gas Tây Ninh'), ('Gas Long An,10.5580,106.3420', 'Gas Long An'), ('Gas Tiền Giang,10.3619,106.3481', 'Gas Tiền Giang'), ('Gas Bến Tre,10.2430,106.3570', 'Gas Bến Tre'), ('Gas Trà Vinh,9.9274,106.3294', 'Gas Trà Vinh'), ('Gas Vĩnh Long,10.2537,105.9562', 'Gas Vĩnh Long'), ('Gas Cần Thơ,10.0451,105.7460', 'Gas Cần Thơ'), ('Gas Hậu Giang,10.3130,105.3880', 'Gas Hậu Giang'), ('Gas Sóc Trăng,9.5960,105.9800', 'Gas Sóc Trăng'), ('Gas Bạc Liêu,9.2950,105.7117', 'Gas Bạc Liêu'), ('Gas Cà Mau,9.1750,105.1500', 'Gas Cà Mau')], default='Gas Cần Thơ', max_length=100),
        ),
    ]
