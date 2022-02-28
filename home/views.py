from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .models import *
import cv2
import pytesseract
import re
from shutil import move
from subprocess import call
from io import BytesIO
from django.template.loader import get_template
from datetime import date
import datetime
from xhtml2pdf import pisa
from django.http import HttpResponse
from os import path
import os
import stat
from deep_translator import GoogleTranslator

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

today = date.today()
# Create your views here.


def render_to_pdf(src, dict={}):
    template = get_template(src)
    html = template.render(dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def home(request):
    papers = Type_Command.objects.all()
    # d2 = today.strftime("%B %d, %Y")
    context = {
        'papers': papers,
    }
    return TemplateResponse(request, 'scan.html', context)


def Done(request):
    return TemplateResponse(request, 'done.html')


def ToPDF(request, type):
    Cn = Cityonne.objects.get(CIN=type)
    dtNow = str(date.today())
    Type = request.session['Type']
    data = {
        'smia': Cn.nom,
        'knia': Cn.prenom,
        'cin': type,
        'datenaissance': Cn.datenaissance,
        'adresse_now': Cn.adresse_now,
        'dtnow': dtNow
    }
    data_ar = {
        'smia': Cn.nom_ar,
        'knia': Cn.prenom_ar,
        'cin': type,
        'datenaissance': Cn.datenaissance,
        'adresse_now': Cn.adresse_now,
        'dtnow': dtNow
    }
    match Type:
        case 'Certificat de residences':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_residences.html', data)
        case 'Certificat de deplacement':
            # HADA LI 3AMR  pdf_Certificat_de_deplacement.html
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_deplacement.html', data)
        case 'Certificat de residences provisoires':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_residences_provisoires.html', data)
        case 'Certificat administrative de non imposition':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_administrative_de_non_imposition.html', data)
        case 'Certificat d’indigence':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_d’indigence.html', data)
        case 'Certificat de non pelerinage':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_non_pelerinage.html', data)
        case 'Certificat de selection au pelerinage':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certifica_de_selection_au_pelerinage.html', data)
        case 'Certificat de travail pour les journaliers':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_travail_pour_les_journaliers.html', data)
        case 'Certificat de naissance':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_de_naissance.html', data_ar)
        case 'Certificat administrative de RAMED':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_administrative_de_RAMED.html', data)
        case 'Certificat d’orientation à l’hôpital pour les malades mentales':
            pdf = render_to_pdf(
                'PDF_temp/pdf_Certificat_d’orientation_à_l’hôpital_pour_les_malades_mentales.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def scan(request, type):
    i = 0
    if "Scan" in request.POST:
        call('py home/rotate.py', shell=True)
        call('py home/autoscan.py', shell=True)
    style = "block"
    message = ""
    cc = "idfront"
    alert = ""
    if not os.path.exists('static/images/cardid/front.jpg'):
        message = "Entrez l'avant de votre CIN"
    else:
        style = "block"
        img = cv2.imread('static/images/cardid/front.jpg')
        img = cv2.resize(img, None, fx=1.1, fy=1,
                         interpolation=cv2.INTER_CUBIC)
        fl_txt = pytesseract.image_to_string(img, lang='fra',
                                             config='--psm 11')
        lst = fl_txt.split('\n')
        f = []
        s=[]
        fullname = re.compile("^[A-Z]{3,}$")
        Cin = re.compile("^[A-Z]+[0-9]+$")
        addresse_front = re.compile("^à\s([A-Z]+\s*){2,}$")
        date = re.compile("^[0-9]{2}\.[0-9]{2}\.[0-9]{2,}$")
        lookLikeDate = re.compile("^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$")

        x = 0
        for i in lst:
            if(fullname.match(i)):
                f.append(i)
                x = x+1
                if x == 2:
                    break
        for i in lst:
            if(Cin.match(i)):
                f.append(i)

        for i in lst:
            if(addresse_front.match(i)):
                f.append(i)
        for i in lst:
            if(date.match(i)):
                f.append(i)

        name = f[0]
        name_ar = GoogleTranslator(source='french', target='arabic').translate(f[0])
        lastname = f[1]
        lastname_ar = GoogleTranslator(source='french', target='arabic').translate(f[1])
        CIN = f[2]
        AdresseF = f[3]
        AdresseF_ar = GoogleTranslator(source='french', target='arabic').translate(f[3])
        a = f[4].replace(".", "-")
        if not lookLikeDate.match(a):
            datebirth='2022-01-01'
        else:
            dateb = datetime.datetime.strptime(a, "%d-%m-%Y").strftime('%Y-%m-%d')
            datebirth = dateb
            
        if(not Cityonne.objects.filter(CIN=CIN).exists()):
            style = "none"
            if(not os.path.exists('static/images/cardid/back.jpg')):
                message = "Entrez l'arriére de votre CIN pour assurer la sécurité"
                style = "block"
                cc = "back"
            if "Sub" in request.POST:
                num = request.POST.get("number")
                Numb = re.compile("(06|07)[0-9]{8}")
                if not Numb.match(num):
                    alert = "Le numéro de téléphone doit commencer par 06 ou 07 et doit contenir 10 chiffres"
                else:
                    img = cv2.imread('static/images/cardid/back.jpg')
                    img = cv2.resize(img, None, fx=1.2, fy=1,
                                     interpolation=cv2.INTER_CUBIC)

                    fltxt = pytesseract.image_to_string(img, lang='fra',
                                                        config='--psm 11')
                    lstt = fltxt.split('\n')
                    img = cv2.resize(img, None, fx=1, fy=1.2,
                                     interpolation=cv2.INTER_CUBIC)
                    fl_txt_ara= pytesseract.image_to_string(img, lang='ara',config='--oem 1 --psm 11')
                    lst_ar=fl_txt_ara.split('\n')
                    adresse_ar = re.compile("لعنوان\s([ء-ي]+\s*){2,}[0-9]+\s+([ء-ي]+\s*)*")
                    S_re = re.compile("^(F|M)$")
                    ar=[]
                    for i in lst:
                        if S_re.match(i):
                            s.append(i)

                    for i in lst_ar:
                       if adresse_ar.match(i):
                          ar.append(i)
                    b = []
                    ben = re.compile("[A-Z]+\sben\s[A-Z]+")
                    bent = re.compile("[a-z]*\s*[A-Z]+\sbent\s[A-Z]+")
                    etat = re.compile("^[0-9]+\/+[0-9]+$")
                    adresse = re.compile(
                        "Adresse(\s*[a-zA-Z]+\s+)+[0-9]+(\s*[a-zA-Z]+\s*)*")
                    for i in lstt:
                        if(ben.match(i)):
                            b.append(i)

                    for i in lstt:
                        if(bent.match(i)):
                            b.append(i)

                    for i in lstt:
                        if(etat.match(i)):
                            b.append(i)

                    for i in lstt:
                        if(adresse.match(i)):
                            b.append(i)
                    ben = b[0]
                    ben_ar = GoogleTranslator(source='french', target='arabic').translate(b[0])
                    bent = b[1]
                    bent=bent.replace("etde","")
                    bent_ar = GoogleTranslator(source='french', target='arabic').translate(bent)
                    etatcivil = b[2]
                    try:
                        adresseB = b[3]
                    except:
                        adresseB='NotScannedCorrectly'
                    try:
                        sexe= s[0]
                    except:
                        sexe='checkCardid'
                    adresse_b_ar=ar[0]
                    try:
                        adresse_b_ar=ar[0]
                    except:
                        adresseb_b_ar="لا يوجد"
                    Cityonne.objects.create(
                        CIN=CIN,
                        nom=name,
                        nom_ar=name_ar,
                        prenom=lastname,
                        prenom_ar=lastname_ar,
                        datenaissance=datebirth,
                        adresse_now=AdresseF,
                        adresse_now_ar=AdresseF_ar,
                        sexe=sexe,
                        etat_civil=etatcivil,
                        file_de=ben,
                        file_de_ar=ben_ar,
                        et_de=bent,
                        et_de_ar=bent_ar,
                        adresse_back=adresseB,
                        adresse_back_ar=adresse_b_ar,
                        phone=num
                    )
                    typeNoS = type.replace("-", " ")
                    TypeN = typeNoS.strip()
                    typec = Type_Command.objects.filter(
                        TypeCommand__contains=TypeN)[0]
                    Demande.objects.create(
                        CIN=Cityonne.objects.get(CIN=CIN),
                        Res=typec.Res,
                        TypeCommand=Type_Command.objects.filter(
                            TypeCommand__contains=TypeN)[0],
                        Done=False
                    )
                    os.rename('static/images/cardid/front.jpg','static/images/cardid/front-'+str(CIN)+'.jpg')
                    os.rename('static/images/cardid/back.jpg','static/images/cardid/back-'+str(CIN)+'.jpg')
                    move('static/images/cardid/front-'+str(CIN)+'.jpg', 'static/images/cardid_all/front-'+str(CIN)+'.jpg')
                    move('static/images/cardid/back-'+str(CIN)+'.jpg', 'static/images/cardid_all/back-'+str(CIN)+'.jpg')
                    return redirect('../../Done')
            else:
                context = {
                    'message': message,
                    'style': style,
                    'cc': cc,
                    'alert': alert
                }
                return TemplateResponse(request, 'num.html', context)
        else:
            typeNoS = type.replace("-", " ")
            TypeN = typeNoS.strip()
            typec = Type_Command.objects.filter(TypeCommand__contains=TypeN)[0]
            Demande.objects.create(
                CIN=Cityonne.objects.get(CIN=CIN),
                Res=typec.Res,
                TypeCommand=Type_Command.objects.filter(
                    TypeCommand__contains=TypeN)[0]
            )
            if os.path.exists('static/images/cardid/front.jpg'):
                os.remove('static/images/cardid/front.jpg')
            if os.path.exists('static/images/cardid/back.jpg'):
                os.remove('static/images/cardid/back.jpg')
            return redirect('../../Done')

    context = {
        'message': message,
        'style': style,
        'cc': cc,
        'alert': alert
    }
    return TemplateResponse(request, 'num.html', context)
