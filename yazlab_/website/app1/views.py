from re import search, split
from django.db.models.fields import FilePathField
from django.shortcuts import render
from django.shortcuts import redirect,redirect
from django.contrib.auth.models import User
from .models import anahtar_kelime, content, danışman, juri, kullanıcı, yazar
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import File
from .forms import FileForm
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os.path
from unipath import Path
import codecs
username=0
user=[]
context={} 
event_list=[]
dosyalar=[]
url=str
url_list=[]
url_listesi_tutucu=[]
varint=0
super_user=""
kullanıcı_listesi=[]
kullanıcı_parola_listesi=[]
kullanıcı_type=[]
dosya_isimleri=[]
dosya_isimleri2=[]
dosya_isimleri3=[]
dosya_yolu=[]
dosya_adı=""
içerik=""
ad=""
soyad=""
ders_adı=""
özet=""
özet2=""
teslim_tarihi=""
teslim_tarihi2=""
teslim_tarihi_yılı=""
proje_başlığı=""
anahtar_kelimeler=""
anahtar_kelimeler_dizi=[]
anahtar_kelimeler2=""
ad_dizi=[]
soyad_dizi=[]
numara_dizi=[]
ad_soyad_dizi=[]
ogretim_tur_dizi=[]
danisman_ad_dizi=[]
danisman_soyad_dizi=[]
danisman_unvan_dizi=[]
jüri_ad_dizi=[]
jüri_soyad_dizi=[]
jüri_unvan_dizi=[]
dönem_aralık=""
file_id=0
seçilen_dönem=""
sorgu2_dosyası=""
sorgu2_dosya_yolu=[]
sorgu2_dosya_yolu_listesi=[]
sorgu2_isimler=[]
sorgu2_isimler_kopya=[]
sorgu2_ciddi_isimler=[]
sorgu2_ciddi_isimler_kopya=[]
sorgu2_isimler_yeni=[]
login_kullanıcı=0
def buyukHarfCevir(sStr):
    str      = sStr
    aranan   = ''
    HARFDIZI = [
                ('i','İ'), ('ğ','Ğ'),('ü','Ü'), ('ş','Ş'), ('ö','Ö'),('ç','Ç'),
                ('ı','I')
               ]
    for aranan, harf in HARFDIZI:
        str  = str.replace(aranan, harf)
    str      = str.upper()
    return str

def login(request):
    global username,user,super_user
    username=request.POST.get('username',False)
    #print(request.POST.get('username',False))
    password=request.POST.get('password',False)
    #print(request.POST.get('password',False))
    
    if(kullanıcı.objects.filter(username=username,password=password)):
        super_user=kullanıcı.objects.filter(username=username,password=password)[0].super_user
    
    user = kullanıcı.objects.filter(username=username , password=password)  
    if username!=False and password!=False and username!="" and password!="" and super_user=="False":
        request.session['id'] = user[0].id
        return redirect('dashboard')
    else:
        return render(request,'login.html')
def dashboardView(request):
    
    global event_list
    print("Ana Sayfadasınız")
    print(username)
    current_user = request.user
    print (user[0].id)
    event_list=File.objects.filter(user_id=user[0].id).values_list('name')
    url_list=File.objects.filter(user_id=user[0].id).values_list('filepath')
    url_list=list(url_list)
    
    return render(request,'dashboard.html',{'un':username ,'event_list':event_list,'url':url,'filepath':url_list})

def yonetici_giris(request):
    global super_user
    username=request.POST.get('username',False)
    password=request.POST.get('password',False)
    
    
    if(kullanıcı.objects.filter(username=username,password=password)):
        super_user=kullanıcı.objects.filter(username=username,password=password)[0].super_user    
        user = kullanıcı.objects.filter(username=username , password=password)
        
    if username!=False and password!=False and super_user=="True":
        print("TUNAY BEN BURDAYIM")
        request.session['id'] = user[0].id
        return redirect('yonetici')
    else:
        return render(request,'yonetici_giris.html')
        

class kullanıcı_bilgileri:
    def __init__(self,username,password,user_type):
        self.username=username
        self.password=password
        self.usertype=user_type
        
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager(caching=True)
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text   



def yonetici(request):
    global dosyalar,dosya_isimleri,dosya_isimleri2,dosya_yolu
    dosyalar=File.objects.filter().values_list('filepath')
    dosya_isimleri=File.objects.filter().values_list('name')
    
    kullanıcı_listesi=kullanıcı.objects.values_list('username')
    kullanıcı_listesi_kopya=[]
    kullanıcı_parola_listesi=kullanıcı.objects.values_list('password')
    kullanıcı_type=kullanıcı.objects.values_list('super_user')
    öğrenciler=kullanıcı_bilgileri(kullanıcı_listesi,kullanıcı_parola_listesi,kullanıcı_type)
    index=0
    for i in dosyalar:
        for j in i:
            dosya_isimleri2.append(j)
    print(dosya_isimleri2)

    for i in dosya_isimleri:
        for j in i:
            dosya_isimleri3.append(j)
    print(dosya_isimleri3)
     
    for i in kullanıcı_listesi:

        kullanıcı_listesi_kopya.append([])

    for i in kullanıcı_listesi:
        for j in i:
            kullanıcı_listesi_kopya[index].append(j)
            index+=1
    index=0    
    for i in kullanıcı_parola_listesi:
        for j in i:
            kullanıcı_listesi_kopya[index].append(j)
            index+=1
    index=0
    for i in kullanıcı_type:
        for j in i:
            kullanıcı_listesi_kopya[index].append(j)
            index+=1
    index=0
    print(kullanıcı_listesi_kopya)


   
    


    if request.method=='POST':
        k_adı = request.POST.get('username', False)
        sifre = request.POST.get('password', False)
        user_type=request.POST.get('super_user',False)
        print("Daha ife girmedim")
           
        if(k_adı!="" and sifre!="" and user_type!=""):
            print("BİZ")
            print(k_adı,sifre,user_type)         
            kullanıcı.objects.create(username=k_adı,password=sifre,super_user=user_type)
        k_adı = ""
        sifre = ""
        user_type=""    
    return render(request,'yonetici.html',{'dosyalar':dosyalar ,'kullanıcılar':kullanıcı_listesi_kopya,'şifreler':kullanıcı_parola_listesi,'type':kullanıcı_type})
        
    redirect('yonetici')

    

    
def upload(request):
    global context,url,dosya_yolu,dosya_adı,içerik,ad,soyad,özet,özet2,teslim_tarihi,teslim_tarihi2,teslim_tarihi_yılı,anahtar_kelimeler,proje_başlığı,anahtar_kelimeler_dizi,anahtar_kelimeler2,ad_dizi,soyad_dizi,ad_soyad_dizi,numara_dizi,ogretim_tur_dizi
    global danisman_ad_dizi,danisman_soyad_dizi,danisman_unvan_dizi,jüri_ad_dizi,jüri_soyad_dizi,jüri_unvan_dizi,dönem_aralık,file_id
    url=""
    if request.method=='POST':
        uploaded_file=request.FILES['document']
        fs=FileSystemStorage()
        url=fs.url(uploaded_file)
        print(type(fs.url(uploaded_file)))
        dosya=File.objects.create(filepath=url,name=uploaded_file.name,user_id=request.session['id'])
        file_id=dosya.id
        print("BEN DOSYA ID'siyim",file_id)
        print(uploaded_file.name)
        print(uploaded_file.size)
        dosya_adı=uploaded_file.name
        file_name=fs.save(uploaded_file.name,uploaded_file)
        context['url']=fs.url(uploaded_file)
        print(type(context))

        dosya_yolu=Path(dosya_adı).absolute()
        print(dosya_yolu)
        dosya_yolu=dosya_yolu.replace("\\","/")
        dosya_yolu = dosya_yolu[:53] + "media/" + dosya_yolu[53:]
        print(dosya_yolu)    
        a=convert_pdf_to_txt(dosya_yolu)
        file = codecs.open("içerik.txt", "w", "utf-8")
        file.write(a)
        file.close()  

        file = codecs.open("içerik.txt", "r", "utf-8")
        içerik=file.read()
        yeni=içerik.split("\n")
        file.close()
        #print(içerik)
        yeni2=[]

        for i in range(len(yeni)):
            yeni[i]=yeni[i].strip()
            if(yeni[i]!=''):
                yeni2.append(yeni[i])


        
        
        
        index=[]
        
        ders_sayac=0
        ders_target_araştırma="ARAŞTIRMA PROBLEMLERİ"
        ders_target_bitirme="BİTİRME PROJESİ"
        for i in range(len(yeni2)):
            if(yeni2[i].__contains__(ders_target_araştırma)):
                ders_sayac=i
                break
            if(yeni2[i].__contains__(ders_target_bitirme)):
                ders_sayac=i
                break
           

        ders_adı=yeni2[ders_sayac]
        ders_adı=ders_adı.strip()


        başlangıç=0
        bitiş=0
        
        target="Anahtar"
        target2="kelimeler:"
        for i in range(len(yeni2)):
            if(yeni2[i]=="ÖZET"):
                başlangıç=i
            if yeni2[i].__contains__(target) and yeni2[i].__contains__(target2):
                bitiş=i
        print("başlangıç : ",başlangıç ,"bitiş : ",bitiş)
        özet=yeni2[başlangıç:bitiş]
        for i in özet:
            özet2+=i
            özet2+=" "
        
        tarih_index=0
        for i in range(len(yeni2)):
            if(search("Tezin Savunulduğu Tarih:",yeni2[i])):
                tarih_index=i
        
        teslim_tarihi=yeni2[tarih_index][::-1]

        for i in teslim_tarihi:
            if i==" ":
                break
            else:
                teslim_tarihi2+=i

        teslim_tarihi=teslim_tarihi2[::-1]
        for i in teslim_tarihi2:
            if i==".":
                break
            else:
                teslim_tarihi_yılı+=i
        teslim_tarihi_yılı=teslim_tarihi_yılı[::-1]       
        print("YILIMIZ",teslim_tarihi_yılı)

        ad_target="Adı Soyadı:"
        numara_target="Öğrenci No:"
        ad_soyad=""
        numara=""
        ogretim_tur=""
        ad_tutucu=""
        ad_indexler=[]
        numara_tutucu=""
        numara_indexler=[]
        sayaç=0
        for i in range(len(yeni2)):
            if(yeni2[i].__contains__(ad_target)):
                ad_indexler.append(i)
                
                
        for i in range(len(yeni2)):
            if(yeni2[i].__contains__(numara_target)):
                numara_indexler.append(i)
               

        for i in numara_indexler:
            numara_tutucu=yeni2[i]
            numara_tutucu=numara_tutucu[::-1]
            sayaç=0
            for i in numara_tutucu:
                if i!=":":
                    numara+=i
                if i==":":
                    break
            numara=numara[::-1]
            numara=numara.strip()
            numara_dizi.append(numara)
        
            if numara[5]=="2":
                ogretim_tur="İkinci Öğretim"
            if numara[5]=="1":
                ogretim_tur="Birinci Öğretim"
        
            ogretim_tur_dizi.append(ogretim_tur)
            numara=""

        


        for i in ad_indexler:
            ad_tutucu=yeni2[i]
            ad_tutucu=ad_tutucu[::-1]
            sayaç=0
            for i in ad_tutucu:
                if i!=":":
                    ad_soyad+=i
                if i==":":
                    break

            for i in ad_soyad:
                if sayaç==0 and i==" ":
                    sayaç+=1
                elif sayaç==0 and i!=" ":
                    soyad+=i

                elif(sayaç>0):
                    ad+=i

            ad=ad[::-1]
            soyad=soyad[::-1]
            ad_soyad=ad_soyad[::-1]
            ad_soyad=ad_soyad.strip()
            ad=ad.strip()
            soyad=soyad.strip()
            ad_dizi.append(ad)
            soyad_dizi.append(soyad)
            ad_soyad_dizi.append(ad_soyad)
            ad=""
            soyad=""
            ad_soyad=""

        

        proje_başlığı_başlangıç=0
        proje_başlığı_bitiş=0
        proje_başlığı_sayacı=0
        ad_soyad_buyuk=buyukHarfCevir(ad_soyad_dizi[0])
        ders_adı_buyuk=buyukHarfCevir(ders_adı)
       
        yeni2_buyuk=""
        for i in range(len(yeni2)):
            yeni2_buyuk=buyukHarfCevir(yeni2[i])
            if(yeni2_buyuk.__contains__(ders_adı_buyuk)):
                proje_başlığı_başlangıç=i+1
            if(proje_başlığı_başlangıç!=0):
                if(yeni2_buyuk.__contains__(ad_soyad_buyuk)):
                    proje_başlığı_bitiş=i
                    break
            

        print("proje başlangıç ",proje_başlığı_başlangıç,"proje bitişimiz  ",proje_başlığı_bitiş)

        for i in range(proje_başlığı_başlangıç,proje_başlığı_bitiş):
            proje_başlığı+=yeni2[i]
            proje_başlığı+=" "



        anahtar_kelimeler_başlangıç=0
        anahtar_kelimeler_bitiş=0

        for i in range(len(yeni2)):
            if(search(target,yeni2[i])):
                bitiş=i

        for i in range(len(yeni2)):
            if(search(target,yeni2[i])):
                anahtar_kelimeler_başlangıç=i
                anahtar_kelimeler_bitiş=i
        
        for i in range(anahtar_kelimeler_başlangıç,len(yeni2)):
            if(yeni2[i].__contains__(".")):
                anahtar_kelimeler_bitiş+=1 
                break
            else:
                anahtar_kelimeler_bitiş+=1

        
        for i in range(anahtar_kelimeler_başlangıç,anahtar_kelimeler_bitiş):
            anahtar_kelimeler+=yeni2[i]
        

        
        anahtar_kelimeler=anahtar_kelimeler[::-1]
        for i in anahtar_kelimeler:
            if i!=":":
                anahtar_kelimeler2+=i
            if i==":":
                break
        
        anahtar_kelimeler=anahtar_kelimeler2[::-1]
        anahtar_kelime_sayacı=0
        anahtar_kelime_tutucu=""
        for i in anahtar_kelimeler:
            if i!="," and i!=".":
                anahtar_kelime_tutucu+=i
                
            else:
                anahtar_kelimeler_dizi.append(anahtar_kelime_tutucu)
                anahtar_kelime_tutucu=""
                anahtar_kelime_sayacı+=1
            

        for i in range(len(anahtar_kelimeler_dizi)):
            anahtar_kelimeler_dizi[i]=anahtar_kelimeler_dizi[i].strip()



        target_danisman="Danışman"
        target_jüri="Jüri"
        jüri_tutucu=""
        danışman_tutucu=""
        tutucu_index=""
        tutucu_index2=""
        danisman_ad=""
        danisman_soyadı=""
        danisman_unvan=""
        danisman_toplu=""
        danisman_ad_soyad=""
        jüri_ad=""
        jüri_soyadı=""
        jüri_unvan=""
        jüri_toplu=""
        jüri_ad_soyad=""
        
        for i in range(len(yeni2)):
            if (yeni2[i].__contains__(target_danisman)):
                for j in yeni2[i]:
                    danışman_tutucu+=j
                    if(danışman_tutucu=="Danışman"):
                        tutucu_index=i-1
                        danisman_toplu=yeni2[tutucu_index]
                        danisman_toplu=danisman_toplu[::-1]
                        sayaç=0
                        for i in danisman_toplu:
                            if(i!="." and sayaç==0):
                                danisman_ad_soyad+=i
                            else:
                                sayaç+=1
                            if(sayaç>0):
                                danisman_unvan+=i

                        sayaç=0
                        for i in danisman_ad_soyad:
                            if sayaç==0 and i==" ":
                                sayaç+=1
                            elif sayaç==0 and i!=" ":
                                danisman_soyadı+=i

                            elif(sayaç>0):
                                danisman_ad+=i
                        danisman_ad=danisman_ad[::-1]
                        danisman_soyadı=danisman_soyadı[::-1]
                        danisman_ad=danisman_ad.strip()
                        danisman_soyadı=danisman_soyadı.strip()
                        danisman_unvan=danisman_unvan[::-1]
                        danisman_unvan=danisman_unvan.strip()
                        danisman_ad_dizi.append(danisman_ad)
                        danisman_soyad_dizi.append(danisman_soyadı)
                        danisman_unvan_dizi.append(danisman_unvan)

                        geçici_index=0
                        
                        for j in range(len(danisman_ad_dizi)):
                                if(danisman_ad_dizi[j].__contains__("Üyesi")):
                                    danisman_ad_dizi[j]=danisman_ad_dizi[j].replace("Üyesi"," ")
                                    geçici_index=j
                                    danisman_unvan_dizi[j]+=" Üyesi"

                        
                        danisman_ad_dizi[geçici_index]=danisman_ad_dizi[geçici_index].strip()

                        danisman_ad=""
                        danisman_soyadı=""
                        danisman_unvan=""
                        danisman_ad_soyad=""
                        
                        

                    
                danışman_tutucu=""
                        

        for i in range(len(yeni2)):            
            if (yeni2[i].__contains__(target_jüri)):
                for j in yeni2[i]:
                    jüri_tutucu+=j
                    if(jüri_tutucu=="Jüri"):
                        print("girdim laa")
                        tutucu_index2=i-1
                        jüri_toplu=yeni2[tutucu_index2]
                        jüri_toplu=jüri_toplu[::-1]
                        sayaç=0
                        for i in jüri_toplu:
                            if(i!="." and sayaç==0):
                                jüri_ad_soyad+=i
                            else:
                                sayaç+=1
                            if(sayaç>0):
                                jüri_unvan+=i

                        sayaç=0
                        for i in jüri_ad_soyad:
                            if sayaç==0 and i==" ":
                                sayaç+=1
                            elif sayaç==0 and i!=" ":
                                jüri_soyadı+=i

                            elif(sayaç>0):
                                jüri_ad+=i
                        jüri_ad=jüri_ad[::-1]
                        jüri_soyadı=jüri_soyadı[::-1]
                        jüri_unvan=jüri_unvan[::-1]
                        jüri_ad=jüri_ad.strip()
                        jüri_soyadı=jüri_soyadı.strip()
                        jüri_unvan=jüri_unvan.strip()
                        jüri_ad_dizi.append(jüri_ad)
                        jüri_soyad_dizi.append(jüri_soyadı)
                        jüri_unvan_dizi.append(jüri_unvan)
                        
                        geçici_index=0
                        
                        for j in range(len(jüri_ad_dizi)):
                                if(jüri_ad_dizi[j].__contains__("Üyesi")):
                                    jüri_ad_dizi[j]=jüri_ad_dizi[j].replace("Üyesi"," ")
                                    geçici_index=j
                                    jüri_unvan_dizi[j]+=" Üyesi"

                        
                        jüri_ad_dizi[geçici_index]=jüri_ad_dizi[geçici_index].strip()

                        jüri_ad=""
                        jüri_soyadı=""
                        jüri_unvan=""
                        jüri_toplu=""
                        jüri_ad_soyad=""

                        


                        
                        

                   
                jüri_tutucu=""


        dönem=teslim_tarihi[3:5]
        dönem_sayı=0
        onlar_basmağı=int(dönem[0])
        birler_basmağı=int(dönem[1])
        dönem_sayı=onlar_basmağı*10+birler_basmağı
        print(dönem_sayı)
        if(dönem_sayı>1 and dönem_sayı<9):
            dönem_sözel="Bahar"
            dönem_aralık=str(int(teslim_tarihi_yılı)-1)+"-"+teslim_tarihi_yılı+" Bahar"
        elif(dönem_sayı==1):
            dönem_sözel="Güz"
            dönem_aralık=str(int(teslim_tarihi_yılı)-1)+"-"+teslim_tarihi_yılı+" Güz"
        else:
            dönem_sözel="Güz"
            dönem_aralık=teslim_tarihi_yılı+"-"+str(int(teslim_tarihi_yılı)+1)+" Güz"
           
        print("DÖNEM AY:",dönem,"SÖZEL OLARAK DÖNEM:",dönem_sözel)   
        print("DÖNEM ARALIĞI:",dönem_aralık)

             
                




        print("ANAHTAR KELİMELER")  
        print(anahtar_kelimeler_dizi[0:len(anahtar_kelimeler_dizi)])
        print("PROJE BAŞLIĞIMIZ")
        print(proje_başlığı)
        for i in range(len(ad_dizi)):
            print("ad[{}] = {}".format(i,ad_dizi[i]))
        for i in range(len(soyad_dizi)):
            print("soyad[{}] = {}".format(i,soyad_dizi[i]))
        for i in range(len(numara_dizi)):
            print("numara[{}] = {}".format(i,numara_dizi[i]))
        for i in range(len(ogretim_tur_dizi)):
            print("ogretim tur[{}] = {}".format(i,ogretim_tur_dizi[i]))
        print("Ders Adı:",ders_adı)
        for i in range(len(danisman_ad_dizi)):
            print("danisman ad[{}] = {}".format(i,danisman_ad_dizi[i]))
        for i in range(len( danisman_soyad_dizi)):
            print("danisman soyad[{}] = {}".format(i, danisman_soyad_dizi[i]))
        for i in range(len(danisman_unvan_dizi)):
            print("danisman unvan[{}] = {}".format(i,danisman_unvan_dizi[i]))
        for i in range(len(jüri_ad_dizi)):
            print("jüri ad[{}] = {}".format(i,jüri_ad_dizi[i]))
        for i in range(len(jüri_soyad_dizi)):
            print("jüri soyad[{}] = {}".format(i, jüri_soyad_dizi[i]))
        for i in range(len(jüri_unvan_dizi)):
            print("jüri unvan[{}] = {}".format(i,jüri_unvan_dizi[i]))    

        print(özet2)
        print(teslim_tarihi)
        content.objects.create(yazar_adı=ad_dizi,yazar_soyadı=soyad_dizi,ogrenci_numarası=numara_dizi,ogretim_turu=ogretim_tur_dizi,ders_adı=ders_adı,proje_özeti=özet2,teslim_tarihi=dönem_aralık,proje_başlığı=proje_başlığı,danışman_adı=danisman_ad_dizi,danışman_soyadı=danisman_soyad_dizi,danışman_ünvan=danisman_unvan_dizi,jüri_ad=jüri_ad_dizi,jüri_soyad=jüri_soyad_dizi ,jüri_ünvan=jüri_unvan_dizi,file_id=file_id,user_id=request.session['id'],filepath=url)

        for i in range(len(ad_dizi)):
            yazar.objects.create(yazar_ad=ad_dizi[i],yazar_soyad=soyad_dizi[i],öğrenci_numarası=numara_dizi[i],öğretim_türü=ogretim_tur_dizi[i],filepath=url,file_id=file_id,kullanıcı_id=request.session['id'],yazar_ad_soyad=ad_soyad_dizi[i])

        for i in range(len(anahtar_kelimeler_dizi)):
            anahtar_kelime.objects.create(anahtar_kelime=anahtar_kelimeler_dizi[i],filepath=url,file_id=file_id,kullanıcı_id=request.session['id'])

        for i in range(len(jüri_ad_dizi)):
            juri.objects.create(jüri_ad=jüri_ad_dizi[i],jüri_soyad=jüri_soyad_dizi[i],jüri_ünvan=jüri_unvan_dizi[i],filepath=url,file_id=file_id,kullanıcı_id=request.session['id'])
        
        for i in range(len(danisman_ad_dizi)):
            danışman.objects.create(danışman_ad=danisman_ad_dizi[i],danışman_soyad=danisman_soyad_dizi[i],danışman_ünvan=danisman_unvan_dizi[i],filepath=url,file_id=file_id,kullanıcı_id=request.session['id'])
        
        ad_dizi=[]
        soyad_dizi=[]
        ad_soyad_dizi=[]
        numara_dizi=[]
        ogretim_tur_dizi=[]
        danisman_ad_dizi=[]
        danisman_soyad_dizi=[]
        danisman_unvan_dizi=[]
        jüri_ad_dizi=[]
        jüri_soyad_dizi=[]
        jüri_unvan_dizi=[]
        anahtar_kelimeler_dizi=[]
        anahtar_kelimeler2=""
        proje_başlığı=""
        teslim_tarihi_yılı=""
        özet2=""
        teslim_tarihi=""
        teslim_tarihi2=""
        yeni2_buyuk=""
        ad_soyad_buyuk=""
        proje_başlığı_başlangıç=0
        proje_başlığı_bitiş=0
        proje_başlığı_sayacı=0
        ders_adı_buyuk=""
        ders_adı=""
        dönem_aralık=""
        file_id=0









    return render(request,'upload.html',{'event_list':event_list,'url':url})   


def admin_sorgu(request):
    global seçilen_dönem,sorgu2_dosya_yolu,sorgu2_dosya_yolu_listesi,sorgu2_isimler_kopya,sorgu2_ciddi_isimler,sorgu2_ciddi_isimler_kopya,sorgu2_isimler_yeni
    sorgu2_dosya_yolu_listesi=[]
    sorgu2_isimler_yeni=[]
    sorgu2_isimler_kopya=[]
    sorgu2_isimler=[]
    if request.method=='POST':
        seçilen_dönem=request.POST.get('dönem',False)
        print("SEÇİLEN DÖNEM",seçilen_dönem)
        
        print(dosya_isimleri2)
        sorgu2_dosya_yolu=content.objects.filter(teslim_tarihi=seçilen_dönem).values_list('filepath')
        
        sorgu2_isimler=content.objects.filter(teslim_tarihi=seçilen_dönem).values_list('user_id')


        for i in sorgu2_dosya_yolu:
            for j in i:
                sorgu2_dosya_yolu_listesi.append(j)
                print(j)

        for i in sorgu2_isimler:
            for j in i:
                sorgu2_isimler_kopya.append(j)
                print(j)
        
        for i in sorgu2_isimler_kopya:
            sorgu2_isimler_ciddi=kullanıcı.objects.filter(id=i).values_list('username')
            
            for i in sorgu2_isimler_ciddi:
                for j in i:
                    sorgu2_isimler_yeni.append(j) 

        print("onetap ",sorgu2_ciddi_isimler_kopya)
         


        
        

    return render(request,'sorgu.html',{'dosyalar':sorgu2_dosya_yolu_listesi,'isimler':sorgu2_isimler_yeni})

def sorgu1(request):
    global seçilen_dönem,proje_başlığı
    sorgu2_dosya_yolu_listesi=[]
    proje_başlıkları=[]
    proje_başlıkları_son=[]
    sorgu1_proje_dosya_yolu_listesi=[]
    ders_adı1=""
    sorgu1_ders_adı=[]
    sorgu1_ders_adı_listesi=[]
    yazar_ad_soyad=[]
    yazar_ad_soyad_son=[]
    sorgu1_yazar_ad_soyad_dosya_yolu=[]
    sorgu1_yazar_ad_soyad_listesi=[]
    proje_başlıkları=content.objects.filter().values_list('proje_başlığı')
    yazar_ad_soyad=yazar.objects.filter().values_list('yazar_ad_soyad')
    anahtar_kelimeler=anahtar_kelime.objects.filter().values_list('anahtar_kelime')
    anahtar_kelimeler_son=[]
    sorgu1_anahtar_kelimeler_dosya_yolu=[]
    sorgu1_anahtar_kelimeler_dosya_yolu_listesi=[]
    for i in yazar_ad_soyad:
        for j in i:
            if j not in yazar_ad_soyad_son:
                yazar_ad_soyad_son.append(j)
    for i in anahtar_kelimeler:
        for j in i:
            if j not in anahtar_kelimeler_son:
                anahtar_kelimeler_son.append(j)


    for i in proje_başlıkları:
        for j in i:
            if j not in proje_başlıkları_son:
                proje_başlıkları_son.append(j)
                
    print("PROJE BAŞLIKLARIMIZ",proje_başlıkları_son)
    if request.method== "POST":
       seçilen_dönem=request.POST.get('dönem',False)
       proje_adı=request.POST.get('proje_adı',False)
       ders_adı1=request.POST.get('ders',False)
       yazar_ad_soyad1=request.POST.get('yazar',False)
       anahtar_kelimeler1=request.POST.get('anahtar_kelime',False)
       print("SEÇİLEN DÖNEM",seçilen_dönem)
       print("PROJE ADI",proje_adı) 
       print("DERSİMİZ",ders_adı1)
       print("SEÇİLEN ANAHTAR KELİME",anahtar_kelimeler1)
       print(dosya_isimleri2)
       sorgu2_dosya_yolu=content.objects.filter(teslim_tarihi=seçilen_dönem).values_list('filepath')
       sorgu1_proje_dosya_yolu=content.objects.filter(proje_başlığı=proje_adı).values_list('filepath')
       sorgu1_ders_adı=content.objects.filter(ders_adı =ders_adı1).values_list('filepath')
       sorgu1_yazar_ad_soyad_dosya_yolu=yazar.objects.filter(yazar_ad_soyad=yazar_ad_soyad1).values_list('filepath')
       sorgu1_anahtar_kelimeler_dosya_yolu=anahtar_kelime.objects.filter(anahtar_kelime=anahtar_kelimeler1).values_list('filepath')
       print("DERS DOSYA YOLU",sorgu1_ders_adı)
       for i in sorgu1_proje_dosya_yolu:
           for j in i:
               sorgu1_proje_dosya_yolu_listesi.append(j)
               print(j)

       for i in sorgu2_dosya_yolu:
           for j in i:
               sorgu2_dosya_yolu_listesi.append(j)
               print(j)
        
       for i in sorgu1_ders_adı:
           for j in i:
               sorgu1_ders_adı_listesi.append(j)
               print(j)
    
       for i in sorgu1_yazar_ad_soyad_dosya_yolu:
           for j in i:
               sorgu1_yazar_ad_soyad_listesi.append(j)
               print(j)

       for i in sorgu1_anahtar_kelimeler_dosya_yolu:
           for j in i:
               sorgu1_anahtar_kelimeler_dosya_yolu_listesi.append(j)
               print(j)

       print("GELEN DOSYA YOLLARI YAZARA GÖRE",sorgu1_yazar_ad_soyad_listesi)
       print("ANAHTAR KELİMELERE GÖRE GELEN DOSYA",sorgu1_anahtar_kelimeler_dosya_yolu_listesi)

    return render(request,'sorgu1.html',{'dosyalar':sorgu2_dosya_yolu_listesi,'proje_başlıkları':proje_başlıkları_son,'proje_başlığı':sorgu1_proje_dosya_yolu_listesi,'ders_adı':sorgu1_ders_adı_listesi,'yazarlar':yazar_ad_soyad_son,'yazar_dosya_listesi':sorgu1_yazar_ad_soyad_listesi,'anahtar_kelimeler':anahtar_kelimeler_son,'anahtar_kelimeler_dosya':sorgu1_anahtar_kelimeler_dosya_yolu_listesi})


def kullanıcı_sorgu(request):
    global seçilen_dönem,sorgu2_dosya_yolu,sorgu2_dosya_yolu_listesi,sorgu2_isimler_kopya,sorgu2_ciddi_isimler,sorgu2_ciddi_isimler_kopya,sorgu2_isimler_yeni
    sorgu2_dosya_yolu_listesi=[]
    sorgu2_isimler_yeni=[]
    sorgu2_isimler_kopya=[]
    sorgu2_isimler=[]
    if request.method=='POST':
        seçilen_dönem=request.POST.get('dönem2',False)
        print("SEÇİLEN DÖNEM",seçilen_dönem)
        
        print(dosya_isimleri2)
        sorgu2_dosya_yolu=content.objects.filter(teslim_tarihi=seçilen_dönem,user_id=request.session['id']).values_list('filepath')
        
        sorgu2_isimler=content.objects.filter(teslim_tarihi=seçilen_dönem,user_id=request.session['id']).values_list('user_id')


        for i in sorgu2_dosya_yolu:
            for j in i:
                sorgu2_dosya_yolu_listesi.append(j)
                print(j)

       

        

    return render(request,'kullanıcı_sorgu.html',{'dosyalar':sorgu2_dosya_yolu_listesi})     
   
def kullanıcı_sorgu1(request):
    global seçilen_dönem,proje_başlığı
    sorgu2_dosya_yolu_listesi=[]
    proje_başlıkları=[]
    proje_başlıkları_son=[]
    sorgu1_proje_dosya_yolu_listesi=[]
    ders_adı1=""
    sorgu1_ders_adı=[]
    sorgu1_ders_adı_listesi=[]
    yazar_ad_soyad=[]
    yazar_ad_soyad_son=[]
    sorgu1_yazar_ad_soyad_dosya_yolu=[]
    sorgu1_yazar_ad_soyad_listesi=[]
    proje_başlıkları=content.objects.filter(user_id=request.session['id']).values_list('proje_başlığı')
    yazar_ad_soyad=yazar.objects.filter(kullanıcı_id=request.session['id']).values_list('yazar_ad_soyad')
    anahtar_kelimeler=anahtar_kelime.objects.filter(kullanıcı_id=request.session['id']).values_list('anahtar_kelime')
    anahtar_kelimeler_son=[]
    sorgu1_anahtar_kelimeler_dosya_yolu=[]
    sorgu1_anahtar_kelimeler_dosya_yolu_listesi=[]
    for i in yazar_ad_soyad:
        for j in i:
            if j not in yazar_ad_soyad_son:
                yazar_ad_soyad_son.append(j)
    for i in anahtar_kelimeler:
        for j in i:
            if j not in anahtar_kelimeler_son:
                anahtar_kelimeler_son.append(j)


    for i in proje_başlıkları:
        for j in i:
            if j not in proje_başlıkları_son:
                proje_başlıkları_son.append(j)
                
    print("PROJE BAŞLIKLARIMIZ",proje_başlıkları_son)
    if request.method== "POST":
       seçilen_dönem=request.POST.get('dönem',False)
       proje_adı=request.POST.get('proje_adı',False)
       ders_adı1=request.POST.get('ders',False)
       yazar_ad_soyad1=request.POST.get('yazar',False)
       anahtar_kelimeler1=request.POST.get('anahtar_kelime',False)
       print("SEÇİLEN DÖNEM",seçilen_dönem)
       print("PROJE ADI",proje_adı) 
       print("DERSİMİZ",ders_adı1)
       print("SEÇİLEN ANAHTAR KELİME",anahtar_kelimeler1)
       print(dosya_isimleri2)
       sorgu2_dosya_yolu=content.objects.filter(teslim_tarihi=seçilen_dönem,user_id=request.session['id']).values_list('filepath')
       sorgu1_proje_dosya_yolu=content.objects.filter(proje_başlığı=proje_adı,user_id=request.session['id']).values_list('filepath')
       sorgu1_ders_adı=content.objects.filter(ders_adı =ders_adı1,user_id=request.session['id']).values_list('filepath')
       sorgu1_yazar_ad_soyad_dosya_yolu=yazar.objects.filter(yazar_ad_soyad=yazar_ad_soyad1,kullanıcı_id=request.session['id']).values_list('filepath')
       sorgu1_anahtar_kelimeler_dosya_yolu=anahtar_kelime.objects.filter(anahtar_kelime=anahtar_kelimeler1,kullanıcı_id=request.session['id']).values_list('filepath')
       print("DERS DOSYA YOLU",sorgu1_ders_adı)
       for i in sorgu1_proje_dosya_yolu:
           for j in i:
               sorgu1_proje_dosya_yolu_listesi.append(j)
               print(j)

       for i in sorgu2_dosya_yolu:
           for j in i:
               sorgu2_dosya_yolu_listesi.append(j)
               print(j)
        
       for i in sorgu1_ders_adı:
           for j in i:
               sorgu1_ders_adı_listesi.append(j)
               print(j)
    
       for i in sorgu1_yazar_ad_soyad_dosya_yolu:
           for j in i:
               sorgu1_yazar_ad_soyad_listesi.append(j)
               print(j)

       for i in sorgu1_anahtar_kelimeler_dosya_yolu:
           for j in i:
               sorgu1_anahtar_kelimeler_dosya_yolu_listesi.append(j)
               print(j)

       print("GELEN DOSYA YOLLARI YAZARA GÖRE",sorgu1_yazar_ad_soyad_listesi)
       print("ANAHTAR KELİMELERE GÖRE GELEN DOSYA",sorgu1_anahtar_kelimeler_dosya_yolu_listesi)
    return render(request,'kullanıcı_sorgu1.html',{'dosyalar':sorgu2_dosya_yolu_listesi,'proje_başlıkları':proje_başlıkları_son,'proje_başlığı':sorgu1_proje_dosya_yolu_listesi,'ders_adı':sorgu1_ders_adı_listesi,'yazarlar':yazar_ad_soyad_son,'yazar_dosya_listesi':sorgu1_yazar_ad_soyad_listesi,'anahtar_kelimeler':anahtar_kelimeler_son,'anahtar_kelimeler_dosya':sorgu1_anahtar_kelimeler_dosya_yolu_listesi})     



def showfile(request):

    lastfile= File.objects.last()

    filepath= lastfile.filepath

    filename= lastfile.name


    form= FileForm(request.POST or None, request.FILES or None)  
    form.save()

    
    context= {'filepath': filepath,
              'form': form,
              'filename': filename
              }
    
      
    return render(request, 'upload.html', context)




