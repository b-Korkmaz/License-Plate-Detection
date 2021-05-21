import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pytesseract
import datetime
#from gpiozero import CPUTemperature
from time import sleep
import board
import digitalio
import pwmio
import pulseio
from adafruit_motor import servo
import adafruit_character_lcd.character_lcd as characterlcd
#import RPi.GPIO as GPIO



#Buzzer
buzzer =pulseio.PWMOut(board.D26, variable_frequency=True)

#Ledler
led_yesil=digitalio.DigitalInOut(board.D20)
led_kirmizi=digitalio.DigitalInOut(board.D21)


#Servo#
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

###########################################

pencere = tk.Tk()


entry = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=27,font="bold")
entry.place(x=280, y=366)

entry2 = tk.Entry(state='disabled',bd=5,disabledbackground="white",disabledforeground="black",width=27,font="bold")
entry2.place(x=280, y=416)

###########################################


#Kamera
cap = cv2.VideoCapture(0)

#############################################
def kamera():
    
    
    while True:
                
        ret, frame = cap.read()
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray[180:420, 40:560]
        cv2.imshow("Sistem Kamerası", roi)
        cv2.moveWindow("Sistem Kamerası",620,80)
        #cv2.waitKey(1)
        tus = cv2.waitKey(1)
        
        if tus == ord("s"):
            
            cv2.imwrite("/home/pi/bk_174209010_micpro/p3.png",roi)
            
            b4['state']='normal'
            cv2.destroyAllWindows()
            break
            
        
            
       

#############################################
def okuma():
    b4['state']='disabled'
    #b6['state']='normal'
    b8['state']='normal'
    b9['state']='normal'
    
    img = cv2.imread("/home/pi/bk_174209010_micpro/p3.png")
    cv2.imshow("Kayıt Edilen Görüntü", img)
    cv2.moveWindow("Kayıt Edilen Görüntü",620,80)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       
    hImg, wImg, _ = img.shape
    boxes = (pytesseract.image_to_boxes(img))

    plaka_o = []

    for b in boxes.splitlines():
        # print(b)
        plaka_o.append(b[0])
        b = b.split(' ')
        # print(b)

        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 3)
        cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)   
   
    
  
    cv2.imshow("Okunan Görüntü", img)
    cv2.moveWindow("Okunan Görüntü",620,380)
    
    
    #print(plaka_o)
    y = ("".join(plaka_o))
    print(y)
    
        

    an = datetime.datetime.now()
    st_an=datetime.datetime.strftime(an,'%d.%m.%Y Saat %H.%M.%S')

    

    global s_saati
    s_saati = tk.Label(text=('Giriş Zamanı:', st_an), bg="white",font="Verdana 15 bold")
    s_saati.place(x=10, y=480)

    dosya = open("aranan_plakalar.txt", "r",encoding="utf-8")
    
    liste_plk = dosya.read()
    
    led_durum=False

    if (y in liste_plk):
            
            entry['state']='normal'
            entry.insert(0,y)
            entry['state']='disabled'
            
            entry2['state']='normal'
            entry2.insert(0,"Araç Geçemez!!")
            entry2['state']='disabled'
            
            b5['state']='normal'
            
            arac_stabil=tk.Label(text=('---'), bg="red",font="Verdana 15 bold")
            arac_stabil.place(x=200, y=420)
            
        
            lcd.message = (y+"\n"+"Gecemez")
            
            led_kirmizi.value =True
            sleep(5)
            
            lcd.clear()
            buzzer.duty_cycle=2**15
            
            

    else:
                 
            
            entry['state']='normal'
            entry.insert(0,y)
            entry['state']='disabled'
            
            entry2['state']='normal'
            entry2.insert(0,"Araç Geçebilir")
            entry2['state']='disabled'
            
            
            arac_stabil=tk.Label(text=('---'), bg="green",font="Verdana 15 bold")
            arac_stabil.place(x=200, y=420)
            
            
            lcd.message = (y+"\n"+"Gecebilir")
            
            led_yesil.value =True
            sleep(10)
            lcd.clear()
            led_yesil.value =False         
            
            
              
    dosya.close()
    
    cv2.waitKey(200)
    
    


#############################################
def sistemi_kapat():
    cevap=messagebox.askyesno("Çıkış","Programı Kapatmak İstediğinizden\n Eminmisiniz ?")
    if cevap==1:
        exit()
    else:
        pass

#############################################
def m_kaldir():
    global b_acik
    b2['state']='disabled'
    b3['state']='normal'
    b_acik = tk.Label(text=('BARİYER AÇIK'), bg="green",fg="#FFFFFF",font="Verdana 15 bold")
    b_acik.place(x=250, y=310)
    
    
    my_servo.angle = 70
    #time.sleep(0.05)
    b_kapali.destroy()
    
#############################################
def m_kapat():
    b2['state']='normal'
    b3['state']='disabled'
    #b_acik = tk.Label()
    b_acik.destroy()
    global b_kapali
    b_kapali = tk.Label(text=('BARİYER KAPALI'), bg="red",font="Verdana 15 bold")
    b_kapali.place(x=250, y=310)
    my_servo.angle = 180
    #time.sleep(0.05)
    
    
#############################################     
def uyari():
    led_kirmizi.value =False
    buzzer.duty_cycle=0


############################################# 
def ent_temizle():
    temizle_cevap=messagebox.askyesno("Temizleme","Bütün Verileri Temizlemek İstediğinizden\n Eminmisiniz ?")
    if temizle_cevap==1:
        entry['state']='normal'
        entry.delete(0,tk.END)
        entry['state']='disabled'
    
        entry2['state']='normal'
        entry2.delete(0,tk.END)
        entry2['state']='disabled'
    
    
        #b6['state']='disabled'
        b9['state']='disabled'
    
        arac_stabil=tk.Label(text=('---'), bg="white",font="Verdana 15 bold")
        arac_stabil.place(x=200, y=420)
    
        b8['state']='disabled'
    
        s_saati.destroy()
        cv2.destroyAllWindows()
    else:
        pass
############################################# 
def veri_kaydet():
    
    y2=entry.get()
    y3=entry2.get()
    
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
    
    
#############################################    
    
pencere.title("Plaka Okuma Sistemi -Anasayfa")
pencere.geometry("600x700+0+0")


baslik=tk.Label(text="PLAKA OKUMA SİSTEMİ",font="Verdana 22 bold",bg="white")
baslik.place(x=10,y=10)

b1 = tk.Button(text ="Kamerayı Çalıştır",bg="white",command=kamera)
b1.place(x=10,y=100)

kam_yazi=tk.Label(text="Görüntüyü Kaydetmek için\n Klavyeden 'S' Tuşuna Basınız",font="Verdana 10 bold",bg="white")
kam_yazi.place(x=165,y=100)

#kam_yazi2=tk.Label(text="ÇIKIŞ için Klavyeden 'E' Tuşuna Basınız",font="Verdana 10 bold",bg="white")
#kam_yazi2.place(x=165,y=130)


b2=tk.Button(text="Bariyeri Aç",bg="green",fg="#FFFFFF",font="bold",command = m_kaldir)
b2.place(x=10,y=225)

b3=tk.Button(text="Bariyeri Kapat",state='disabled' ,bg="red",font="bold",command=m_kapat)
b3.place(x=135,y=225)

b4=tk.Button(text="Görüntüyü Oku",state='disabled', bg="white",command=okuma)
b4.place(x=10,y=150)

b5=tk.Button(text="Uyarıları Kapat!",state='disabled', bg="white",font="bold",command=uyari)
b5.place(x=285,y=225)

#b6=tk.Button(text="Pencereleri Kapat",state='disabled',command=yeniden_baslat)
#b6.place(x=10,y=590)

b7=tk.Button(text="Programı Kapat", command =sistemi_kapat)
b7.place(x=430,y=635)

b8=tk.Button(text="Temizle", state='disabled',command =ent_temizle)
b8.place(x=330,y=590)

b9=tk.Button(text="Sisteme Kaydet", state='disabled',command =veri_kaydet)
b9.place(x=430,y=590)


b_durumu = tk.Label(text=('BARİYER DURUMU : '), font="Verdana 15 bold",bg="white")
b_durumu.place(x=10, y=310)

b_kapali = tk.Label(text=('BARİYER KAPALI'), bg="red",font="Verdana 15 bold")
b_kapali.place(x=250, y=310)

okunan_plaka = tk.Label(text=("En son okunan plaka"),bg="white" ,font="Verdana 15 bold")
okunan_plaka.place(x=10, y=370)

arac_durumu  = tk.Label(text=('ARAÇ DURUMU'), bg="white",font="Verdana 15 bold")
arac_durumu.place(x=10, y=420)

arac_stabil=tk.Label(text=('---'), bg="white",font="Verdana 15 bold")
arac_stabil.place(x=200, y=420)

numara_isim =tk.Label(text=('Burhan KORKMAZ--174209010'), bg="white",font="Verdana 10 bold")
numara_isim.place(x=10,y=645)


s2=datetime.datetime.now()
s3=datetime.datetime.strftime(s2,'%d.%m.%Y')
sistem_saati2=tk.Label(text=(s3), bg="white",font="Verdana 10 bold")
sistem_saati2.place(x=450,y=10)

pencere.mainloop()

cap.release()
cv2.destroyAllWindows()
