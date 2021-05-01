from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import datetime


app = Flask(__name__)

def xml_to_jsonlist(dzikir_arab, dzikir_arti):
    dzikir_list = []
    for i in range(len(dzikir_arab)):
        arti = dzikir_arti[i].text
        judul = arti.split('|')[0]
        baca = arti.split('|')[1]
        arti_list = arti.split('|')[2:]
        arab = dzikir_arab[i].text.split('|')
        dzikir_list.append({'judul':judul, 'baca':baca, 'arab':arab, 'arti':arti_list})
    return dzikir_list

@app.route('/')
def home():
    mode = request.args.get('mode') or 'light'
    dzikir = request.args.get('dzikir')
    tree = ET.parse('dzikir.xml')
    root = tree.getroot()
    list_font_size_arab, list_font_size_terjemah ,dzikir_pagi, dzikir_pagi_arti, dzikir_sore, dzikir_sore_arti = root


    dzikir_pagi_list = xml_to_jsonlist(dzikir_pagi, dzikir_pagi_arti)
    dzikir_sore_list = xml_to_jsonlist(dzikir_sore, dzikir_sore_arti)

    if dzikir == None: dzikir = 'pagi' if datetime.datetime.now().hour < 12 else 'sore'

    dzikir_list = dzikir_pagi_list if dzikir == 'pagi' else dzikir_sore_list

    return render_template('dzikir.html',
                           dzikir_list=dzikir_list,
                           mode=mode,
                           dzikir=dzikir)


if __name__ == "__main__":
    app.run()    