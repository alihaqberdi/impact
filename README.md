# Yozda Birga Kod Yozamiz:  Impact Loyihasi
Loyiha Django Rest Framework va Postgresql Malumotlar obmoridan foydalanilgan.
# Eslatma
 - Vaqt formati quyidagicha: ``2023-06-22 11:30:11`` booking qilishda ham shu   formatdan foydalanilgan
 - loyihani soat kechgi ``20:00 dan kechgi 00:01 gacha test qilinsa xatoliklar kelib chiqish ehtimoli bor.`` Sabab test funksiyalar real vaqtda ishlaydi.funksiyalarda 4 soatgacha vaqt qo'shib booking qilib test qilingan.
Quyidagi o'rnatish qo'llanmasi yordamida o'rnatish maqsadga muvofiq.

## O'rnatish
    git clone https://github.com/alihaqberdi/impact.git
## Postgresql psql

    CREATE DATABASE impact;

## impact/config/settings.py

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "impact",
            "USER": "your_postgres_user",
            "PASSWORD": "your_postgres_password",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

## Virtual Muhit
### ubuntu
  
    python -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt

## Migratsiya impact/


    python3 manage.py migrate

## Run Code

    python3 manage.py runserver

## Tests 

    python3 manage.py test
    
# Eslatma
 - Vaqt formati quyidagicha: ``2023-06-22 11:30:11`` booking qilishda ham shu   formatdan foydalanilgan
 - loyihani soat kechgi 20:00 dan kechgi 00:01 gacha test qilinsa xatoliklar kelib chiqish ehtimoli bor. Sabab test funksiyalar real vaqtda ishlaydi.funksiyalarda 4 soatgacha vaqt qo'shib booking qilib test qilingan.


# impact/room/tests/test_views_and_serializer.py  test jarayoni

## TestRoomAvailabilityView
Bu class Xonaning bo'sh vaqtlarini chiqaruvchi viewni test qiladi

### def setUp(self) -> None:
SetUp funksiyasi test qilishga kerak bo'ladigan vazifalarni bajaradi


### def test_free_time(self):
test_free_time funksiyasi booking bolmagan bugungi  kunning bo'sh vaqtini chiqaradi

`misol hozir: 2023-06-13 11:10:30`
#### `GET rooms/1/availability/`

```json
{
  "start": "2023-06-13 11:10:30",
  "end": "2023-06-13 23:59:59"
}
```


### def test_with_booking(self):
test_with_booking funksiyasi bugungi kunga 1 marta booking bo'lgan holat uchun
bo'sh vaqtni chiqarish datasini tekshiradi ``misol hozir 2023-06-13 11:30:00``

#### `POST /rooms/1/book`
```json
{
  "resident": {
    "name": "Ali"
  },
  "start": "2023-06-13 12:30:00",
  "end": "2023-06-13 13:30:00"
}
```
Xona bo'sh vaqtini ko'rish:
#### `GET rooms/1/availability/`
```json
[
  {
    "start": "2023-06-13 11:30:00",
    "end": "2023-06-13 12:30:00"
  },
  {
    "start": "2023-06-13 13:30:00",
    "end": "2023-06-13 23:59:59"
  }
]
```
