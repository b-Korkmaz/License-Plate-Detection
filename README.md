# Raspberryi-Pi-3-Plaka-Okuma-Sistemi

Bu çalışmada, Raspberry Pi 3B+ geliştirme kartı kullanılarak OpenCv ve Tesseract kütüphanelerinden yararlanılarak plaka okuma sistemi yapılmıştır. 
Tasarımda, görüntünün okunması için harici olarak USB Kamera kullanılmıştır. Kameradan okunan görüntü kayıt edilerek, OpenCv ve Tesseract kütüphanelerdeki 
görüntü işleme yöntemleri kullanılarak analiz edilmiştir. Analiz sonucunda bir veri tabanında karşılaştırma yapılmış ve bu sonuca göre çevre birimler aktif edilmiştir. Sistem bir ara yüz ile kontrol edilmektedir. 
Bu ara yüzden elde edilen sonuçlar bir “txt” dosyasına kaydedilebilmektedir. Aynı zamanda çevre birimler de kontrol edilmektedir.

Ortamda bulunan nesnelerin gerçek zamanlı tespit edilmesi, sınıflandırılması ve elde edilen sonuçlar sunulmaktadır.
Önerilen yönteme ait deneysel çalışmaların gerçekleştirilmesinde araç plakası kullanılmaktadır. Fotoğraflar alındıktan sonra görüntü işleme teknikleri kullanılarak işlenmektedir. Plakaların görüntü düzlemi üzerindeki harf ve sayıları gibi verileri hesaplanarak elde edilmektedir.

# IDE - Kütüphaneler ve Çevre Birimlerin Tanımlanması
Bu çalışmada kaynak kodun hazırlanmasında Thony IDE’ si kullanılmıştır. Bütün Raspberry Pi geliştirme kartlarında yükle olarak gelmektedir. Hem esnek olmasından dolayı hem de gerekli kütüphanelerin yüklenmesi açısından oldukça kolaylık sağlamaktadır.
İlk olarak gerekli kütüphane tanımlamaları yapılmıştır. Thony IDE’ sinin mevcut LCD kütüphanesi ile GPIO pinleri çakıştığı için Adafriut Kütüphaneleri kullanılmıştır. Bu tanımlamalardan sonra çevre birimler tek tek test edilerek çalıştığı gözlemlenmiştir. Sonrasında sistemin ara yüzü oluşturulmaya başlanmıştır. Ara yüz oluşturmak için Python dilinin Tkhinder kütüphanesi kullanılmıştır.

*Kütüphane Tanımlamalarının Yapıldığı Program Bölümü;*
```python
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pytesseract
import datetime
from time import sleep
import board
import digitalio
import pwmio
import pulseio
from adafruit_motor import servo
import adafruit_character_lcd.character_lcd as characterlcd
#import RPi.GPIO as GPIO

```

*Çevre Birimlerinin Tanımlanımlandığı Program Bölümü;*

```python
#Buzzer
buzzer =pulseio.PWMOut(board.D26, variable_frequency=True)

#Ledler
led_yesil=digitalio.DigitalInOut(board.D20)
led_kirmizi=digitalio.DigitalInOut(board.D21)


#Servo
pwm = pwmio.PWMOut(board.D16, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)


#16x2 LCD

lcd_columns =16
lcd_rows =2

lcd_rs=digitalio.DigitalInOut(board.D27)
lcd_en =digitalio.DigitalInOut(board.D22)
lcd_d4=digitalio.DigitalInOut(board.D25)
lcd_d5=digitalio.DigitalInOut(board.D24)
lcd_d6=digitalio.DigitalInOut(board.D23)
lcd_d7=digitalio.DigitalInOut(board.D18)


lcd = characterlcd.Character_LCD_Mono(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows)
led_yesil.direction = digitalio.Direction.OUTPUT
led_kirmizi.direction = digitalio.Direction.OUTPUT
lcd.clear()

```
*Çevre Birimlerin Bağlandıktan Sonraki Sistemin Devre Modeli;*

Kamera, Klavye, 16x2 LCD, Servo – Motor, Led ve Buzzer breadboard üzerinde kurulmuştur. Servo – Motor, Led, 16x2 LCD ve Buzzer raspberry pi 3 kartında belirlenen ve uygun olan pinlere, Kamera ve Klavye ise raspberry pi 3 kartında USB portlarına bağlanmıştır.

![image](https://user-images.githubusercontent.com/70108497/130410546-42fb2c13-9274-4bf8-a181-1eff7dde0251.png)

# Sistem Arayüzü
Plaka Tespitini gerçekleştirirken kameradan alınan verilerin kaydedilmesi, alınan verilerin görüntülenmesi ve ara yüzde bastırılması, servo – motor çalıştırılması, bariyer durumu, uyarıların kontrol edilmesi, elde edilen plaka değerinin kaydedilmesi, sistem saatinin ara yüzde bastırılması, okunan plakanın bastırılması ve plaka durumunun görüntülenmesi işlemleri aşağıda görüldüğü gibi Python da Tkhinder kütüphanesi ile tasarlanmıştır.

“Kamerayı Çalıştır” butonuna basıldığında Kamera modülü ile ara yüz Raspberry Pi USB Portu üzerinden seri haberleşme tabanlı yapılmaktadır. Okunan görüntüyü kaydetmek için klavyeden ” S” tuşuna basılması gerekmektedir.
“Görüntüyü Oku” butonunun aktif olmasıyla kaydedilen görüntü okunduktan sonra ara yüzde en son okunan plaka ve araç durumu şablonlarında okunan değer bastırılmaktadır. “Sisteme Kaydet” butonunun aktif edilmesiyle şablonlardan veriler çekilerek “txt” uzantılı dosyaya kaydedilebilmektedir. “Temizle” butonun aktif edilmesiyle ara yüzdeki bütün veriler ve paneller temizlenmektedir.
Sistemde bariyer kontrolü ise “Bariyeri Aç” ve “Bariyeri Kapat” butonlarının aktif edilmesiyle sağlanmaktadır ve bariyer durumu ara yüzde gösterilmektedir.

![image](https://user-images.githubusercontent.com/70108497/130411616-6d5d69b9-bfba-4992-817d-dfba68e7fca8.png)

# Görüntüyü Okuma Algoritması
Görüntüyü okuma fonksiyonun da ise ilk olarak kayıt edilen görüntü açılmıştır. Sonrasında Tesseract kütüphanesindeki imgage_to_boxes fonksiyonu kullanılmıştır. Devamında for döngüsü ile resim üzerinde harfler ve sayılar dikdörtgen içine alınmıştır. Okunan görüntü matris içinde tutulduğu için veri tabanında karşılaştırmak için  Split ve Join fonksiyonları ile istenilen değer elde edilerek "y" değişkenin de tutulmuştur. 

```python
def okuma():
   
    
    img = cv2.imread("/home/pi/bk_174209010_micpro/p3.png")
    cv2.imshow("Kayıt Edilen Görüntü", img)
    cv2.moveWindow("Kayıt Edilen Görüntü",620,80)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       
    hImg, wImg, _ = img.shape
    boxes = (pytesseract.image_to_boxes(img))

    plaka_o = []

    for b in boxes.splitlines():
        
        plaka_o.append(b[0])
        b = b.split(' ')
        
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 3)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
  
    y = ("".join(plaka_o))
    

```
Devamında ise dosya işlemleri ile Text dosyasından veri okuma ve veri kaydetme işlemleri gerçekleştirilmiştir.

*Okunan Görüntüyü Veri Tabanında Karşılaştırmak için ;*

```python
    dosya = open("aranan_plakalar.txt", "r",encoding="utf-8")
    
    liste_plk = dosya.read()
    
    if (y in liste_plk):
            
            lcd.message = (y+"\n"+"Gecemez")
            
            led_kirmizi.value =True
            sleep(5)
            
            lcd.clear()
            buzzer.duty_cycle=2**15           

    else:
                 
            lcd.message = (y+"\n"+"Gecebilir")
            
            led_yesil.value =True
            sleep(10)
            lcd.clear()
            led_yesil.value =False         
            
            
              
    dosya.close()

```
*Okunan Görüntüyü Text Dosyasına Kaydetmek için;*

```python
    an = datetime.datetime.now()
    st_an=datetime.datetime.strftime(an,'Giriş Zamanı:%d.%m.%Y Saat %H.%M.%S')
    
    dosya_2 = open("kayit_edilen_plakalar.txt", "a", encoding="utf-8")

    
    dosya_2.write(y2+"-->"+y3)
    dosya_2.write("\n")
    dosya_2.write(st_an)
    dosya_2.write("\n")
    dosya_2.write("--------------------------------")
    dosya_2.write("\n")
    
    
    dosya_2.close()
    messagebox.showinfo("Kayıt","PLAKA KAYIT EDİLDİ")


```

# Sistemin Gerçek Zamanlı Test Edilmesi
Plaka tespiti için gerekli olan görüntü USB Kameradan alınarak, klavyeden “S” tuşuna basılarak elde edilmiştir. Kaydedilen görüntü sonrasında görüntü okuma işlemi yapıldığında aşağıda görüldüğü gibi plaka tespit edilmiştir.

*İlk Görüntünün Alınması;*

![image](https://user-images.githubusercontent.com/70108497/130415080-a5cde865-b86f-4ad5-b32d-dee980638e17.png)

*Görüntünün Okunması;*

![image](https://user-images.githubusercontent.com/70108497/130415177-bc507c7b-90cb-403a-97c7-3795f00f92eb.png)

Görüntü değerlendirildikten sonra çevre birimlerin çalışması aşığıda görüldüğü gibi ; plakanın durumuna göre işlemekedir.

*V1*

![image](https://user-images.githubusercontent.com/70108497/130415455-9ba2382c-87a5-45f3-8a13-ed2283ddf4b2.png)


*V2*

![image](https://user-images.githubusercontent.com/70108497/130415488-c301a34b-b7d6-4c03-ad07-1c1dace5d2f9.png)


*Sonuçların Text Dosyasına Kaydedilmesi;*

![image](https://user-images.githubusercontent.com/70108497/130415265-41d23dd1-8c40-434e-819e-a1c3c6b85b3d.png)

# Sonuç
Raspberry Pi 3B+ geliştirme kartı ile görüntü işleme yöntemleri kullanılarak Plaka Okuma Sistemi başarı ile çalıştırılmıştır. Tasarımda Thony IDE yani Python derleyicisi kullanılarak kaynak kodu hazırlanmıştır. Gerçek zamanlı hazırlanan bu sistemin gerekli çevre birimleri montajları breadboard üzerine yapılarak sistem çalışır hale getirilmiştir. Bu çalışmada Raspberry Pi geliştirme kartı kullanılarak bir sistem tasarımı sunulmuştur.



