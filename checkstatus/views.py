import requests
from datetime import datetime
from pyquery import PyQuery as pq


from django.shortcuts import render


from applicants.models import Applicants


def get_all_applicants_to_check_procedure():
    ''' Find applications with active procedure for check procedure status '''
    for applicant in Applicants.objects.filter(active=True):
        check_procedure_extranjeria_chile(applicant)


def check_procedure_extranjeria_chile(applicant):
    ''' Check status of a request, send an alert via email if there are changes '''
    url_get_form = 'https://consultas.extranjeria.gob.cl/autoConsultaInicioB3K.action?option=nombre'
    url_post_form = 'http://consultas.extranjeria.gob.cl/autoConsultaPersona.action'
    url_open_procedure = 'http://consultas.extranjeria.gob.cl/autoConsultaSolicitud.action'
    form_data = {
        'option'      : applicant.option.lower(),
        'rut'        : applicant.rut if applicant.rut else '',
        'surname2'    : applicant.surname2,
        'fechaNas'    : applicant.fechaNas.strftime('%Y/%m/%d'),
        'names'       : applicant.names,
        'surname1'    : applicant.surname1,
        'apellido2'   : applicant.surname2,
        'fechaDia'    : applicant.fechaNas.day,
        'fechaMes'    : applicant.fechaNas.month,
        'fechaAnno'   : applicant.fechaNas.year,
        'idPaisOrigen': applicant.idPaisOrigen,
        'dniID'       : applicant.dniID,
    }

    session = requests.session()
    session.get(url=url_get_form)

    procedure = session.post(url=url_post_form, data=form_data)
    if 'No se encontró el registro' in procedure.text:
        return False
    else:
        inital_dom = pq(procedure.text)
        data = inital_dom('a.link')[0].attrib['href'].replace('javascript: SeleccionPersona(','')
        data = data.replace(')','').replace('"','').replace("'","").split(',')

        data_to_open = {
            'cod_ext' : data[0],
            'fec_ext' : data[1],
            'cod_doc' : data[2],
            'num_doc' : data[3],
            'fec_doc' : data[4],
            'cod_auto': data[5],
            'tipo'    : data[6],
        }

        final_response = session.post(url=url_open_procedure, data=data_to_open)
        if not 'Consulta del estado de Solicitudes' in final_response.text:
            pass
        final_dom = pq(final_response.text)
        data = []

for tr in final_dom('#idRegistros table > tbody > tr'):
    if len(tr.findall('table')) > 0:
        for tr in tr.findall('table > tbody > tr'):
            th, td = tr.find('th'), tr.find('td')
            print(th.text_content() if th is not None else '', td.text_content() if td is not None else '')
    else:
        th, td = tr.find('th'), tr.find('td')
        print(th.text_content() if th is not None else '', td.text_content() if td is not None else '')


for table in final_dom('#idRegistros table'):
    if table is not None:
        if table.findall('tr') is not None:
            for tr in table.findall('tr'):
                th, td = tr.find('th'), tr.find('td')
                print(th.text_content() if th is not None else '', td.text_content() if td is not None else '')
        
                

        # for status in final_dom('#solicitud .panel table'):
            

    return final_response
