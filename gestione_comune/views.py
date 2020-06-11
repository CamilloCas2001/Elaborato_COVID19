from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
import json

# Create your views here.
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'Username o password scorretti')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    url_ita_nuovi_pos = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    url_lomb_nuovi_pos = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    url_co_nuovi_pos = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json"

    raw_data_ita = requests.request("GET", url_ita_nuovi_pos).json()
    raw_data_lomb = requests.request("GET", url_lomb_nuovi_pos).json()
    raw_data_como = requests.request("GET", url_co_nuovi_pos).json()

    # dati storici italia
    num = 0
    data_ita_historical = []
    for i in raw_data_ita:
        dict = {
            "data": raw_data_ita[num]['data'],
            "stato": raw_data_ita[num]['stato'],
            "ricoverati_con_sintomi": raw_data_ita[num]['ricoverati_con_sintomi'],
            "terapia_intensiva": raw_data_ita[num]['terapia_intensiva'],
            "totale_ospedalizzati": raw_data_ita[num]['totale_ospedalizzati'],
            "isolamento_domiciliare": raw_data_ita[num]['isolamento_domiciliare'],
            "totale_positivi": raw_data_ita[num]['totale_positivi'],
            "variazione_totale_positivi": raw_data_ita[num]['variazione_totale_positivi'],
            "nuovi_positivi": raw_data_ita[num]['nuovi_positivi'],
            "dimessi_guariti": raw_data_ita[num]['dimessi_guariti'],
            "deceduti": raw_data_ita[num]['deceduti'],
            "totale_casi": raw_data_ita[num]['totale_casi'],
            "tamponi": raw_data_ita[num]['tamponi'],
            "casi_testati": raw_data_ita[num]['casi_testati'],
            "note_it": raw_data_ita[num]['note_it'],
            "note_en": raw_data_ita[num]['note_en'],
        }
        data_ita_historical.append(dict)
        num += 1

    # Dati cumulativi sull'Italia
    data_ita_cumulativi = data_ita_historical[-1]

    #dati storici regione Lombardia
    num = 0
    data_lomb_historical = []
    for b in raw_data_lomb:
        dict1 = {
            "data": raw_data_lomb[num]['data'],
            "stato": raw_data_lomb[num]['stato'],
            "codice_regione": raw_data_lomb[num]['codice_regione'],
            "denominazione_regione": raw_data_lomb[num]['denominazione_regione'],
            "lat": raw_data_lomb[num]['lat'],
            "long": raw_data_lomb[num]['long'],
            "ricoverati_con_sintomi": raw_data_lomb[num]['ricoverati_con_sintomi'],
            "terapia_intensiva": raw_data_lomb[num]['terapia_intensiva'],
            "totale_ospedalizzati": raw_data_lomb[num]['totale_ospedalizzati'],
            "isolamento_domiciliare": raw_data_lomb[num]['isolamento_domiciliare'],
            "totale_positivi": raw_data_lomb[num]['totale_positivi'],
            "variazione_totale_positivi": raw_data_lomb[num]['variazione_totale_positivi'],
            "nuovi_positivi": raw_data_lomb[num]['nuovi_positivi'],
            "dimessi_guariti": raw_data_lomb[num]['dimessi_guariti'],
            "deceduti": raw_data_lomb[num]['deceduti'],
            "totale_casi": raw_data_lomb[num]['totale_casi'],
            "tamponi": raw_data_lomb[num]['tamponi'],
            "casi_testati": raw_data_lomb[num]['casi_testati'],
            "note_it": raw_data_lomb[num]['note_it'],
            "note_en": raw_data_lomb[num]['note_en'],
        }
        if dict1['denominazione_regione'] == 'Lombardia':
            data_lomb_historical.append(dict1)
        num += 1

    #dati storici provincia di Como
    num = 0
    data_como_historical = []
    for c in raw_data_como:
        dict2 = {
            "data": raw_data_como[num]['data'],
            "stato": raw_data_como[num]['stato'],
            "codice_regione": raw_data_como[num]['codice_regione'],
            "denominazione_regione": raw_data_como[num]['denominazione_regione'],
            "codice_provincia": raw_data_como[num]['codice_provincia'],
            "denominazione_provincia": raw_data_como[num]['denominazione_provincia'],
            "sigla_provincia": raw_data_como[num]['sigla_provincia'],
            "lat": raw_data_como[num]['lat'],
            "long": raw_data_como[num]['long'],
            "totale_casi": raw_data_como[num]['totale_casi'],
            "note_it": raw_data_como[num]['note_it'],
            "note_en": raw_data_como[num]['note_en'],
        }
        if dict2["sigla_provincia"] == "CO":
            data_como_historical.append(dict2)
        num += 1
    dati_lista = {
        "italia":data_ita_historical,
        "lombardia":data_lomb_historical,
        "como": data_como_historical,
    }
    return render(request, 'accounts/dashboard.html', data_ita_cumulativi)


