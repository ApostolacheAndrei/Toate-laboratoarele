import PySimpleGUI as sg
import json

"""

LINII DIN COD                                          EXPLICATIE COD           
    ↓                                                         ↓     
    
 36--38  : Se definește o clasă pentru interfața utilizatorului CaloriiCalculatorUI, care conține constructorul __init__
 40      : Se Setează tema la "LightBrown11"
 42--43  : Se creează o secțiune pentru partea stângă a interfeței, care conține două imagini.
 45--92  : Se creează o secțiune pentru partea centrală a interfeței, care include etichete, slidere pentru greutate,
 45--92  : înălțime  și vârstă, radio butoane pentru selectarea sexului, un combo box pentru selectarea nivelului de
 45--92  : activitate, butoane  pentru calcul și ieșire, un text pentru afișarea rezultatului și o listă pentru afișarea
 45--92  : rezultatelor anterioare.
 94--107 : Se creează o secțiune pentru partea dreaptă a interfeței, care conține text cu valori nutriționale pentru
 94--107 : anumite alimente
 109--111: Se definește layout-ul final al interfeței, care combină cele trei secțiuni : stânga, centru, dreapta
 113     : Se creează o fereastră utilizând layout-ul și se setează dimensiunile ferestrei
 115--121: Se definește o clasă CaloriiCalculator, care conține factorii de activitate citiți dintr-un fișier JSON
 115--121: la inițializare
 123--135: Se definește o metodă calculeaza_calorii care primește datele utilizatorului și calculează necesarul
 123--135: de calorii în funcție de sex și nivelul de activitate.
 137--179: Se definește funcția main, care creează obiecte pentru interfața utilizatorului și calculator, apoi rulează
 137--179: o buclă infinită pentru a gestiona evenimentele ferestrei.
 137--179: Se verifică evenimentele și se actualizează interfața în funcție de acestea.
 137--179: Dacă evenimentul este închiderea ferestrei sau apăsarea butonului "Ieșire", bucla este întreruptă și
 137--179: fereastra se închide.
 137--179: Dacă evenimentul este schimbarea vârstei, greutății, înălțimii sau sexului, se recalculează necesarul de
 137--179: calorii și se actualizează afișarea.
 137--179: Dacă evenimentul este apăsarea butonului "Calculează", se realizează același calcul și rezultatul este
 137--179: adăugat la o listă, iar lista este afișată într-un listbox.
 
"""

class CaloriiCalculatorUI:

    def __init__(self):

        sg.theme('LightBrown11')

        self.stanga = [[sg.Image('pag1ia.png', expand_x=True, expand_y=True )],
            [sg.Image('pag2ia.png', expand_x=True, expand_y=True )]]

        self.centru = [[sg.Text('Calculator de Calorii', font=('Times New Roman', 20))],

            [sg.Text('Greutate (kg): ', font=('Times New Roman', 15)),
            sg.Slider(range=(30, 150),
            orientation='h',
            size=(20, 10),
            default_value=70,
            key='greutate',
            enable_events=True)],

            [sg.Text('Înălțime (cm):', font=('Times New Roman', 15)),
            sg.Slider(range=(100, 220),
            orientation='h',
            size=(20, 10),
            default_value=170,
            key='inaltime',
            enable_events=True)],

            [sg.Text('Vârsta:            ', font=('Times New Roman', 15)),
            sg.Slider(range=(1, 100),
            orientation='h',
            size=(20, 10),
            default_value=30,
            key='varsta',
            enable_events=True)],

            [sg.Text('Sex:', font=('Times New Roman', 15))],
            [sg.Radio('Feminin' , font=('Times New Roman', 15),
            group_id='sex',
            default=True,
            key='sex_feminin'), sg.Radio('Masculin',
            font=('Times New Roman', 15),
            enable_events=True,
            group_id='sex',
            key='sex_masculin')],

            [sg.Text('Nivelul de activitate:', font=('Times New Roman', 15)),
            sg.Combo(['Sedentar', 'Usor activ', 'Moderat activ','Foarte activ', 'Extrem de activ'],
            key='activitate',
            default_value='Usor activ')],

            [sg.Button('Calculează' , font=('Times New Roman', 15)),
            sg.Button('Ieșire', font=('Times New Roman', 15))],

            [sg.Text('', size=(30, 2), key='rezultat')],

            [sg.Listbox(values=[], size=(40, 5), key='calorii_list')]
                      ]

        self.dreapta = [[sg.Push(), sg.Text("Valori nutritionale (per 100g):\n\n"
                                            "Carofi Prajiti = 311,9 kcal\n"
                                            "Carne Pui = 239 kcal\n"
                                            "Caju = 553 kcal\n"
                                            "Pepene = 30,4 kcal\n"
                                            "Paine = 264,6 kcal\n"
                                            "Oua = 155,1 kcal\n"
                                            "McPuisor = 250 kcal\n"
                                            "Supa Instant Pui = 39 kcal\n"
                                            "Crispy Strips KFC = 170 kcal\n"
                                            "Pizza California Pizza Hut = 210 kcal\n"
                                            "Mici = 233 kcal\n"
                                            "Sarmale = 186 kcal",
                                             font=('Times New Roman', 18)), sg.Push()]]

        self.layout =   [
            [sg.Column(self.stanga), sg.Column(self.centru), sg.Column(self.dreapta, justification = 'right')]
                        ]

        self.window = sg.Window('Calculator de Calorii', self.layout, size=(1320,900))

class CaloriiCalculator:

    def __init__(self):

        with open('factor_activitate.json', 'r') as file:

            self.factori_activitate = json.load(file)

    def calculeaza_calorii(self, greutate, inaltime, sex, activitate, varsta):

        if sex == 'Feminin':

            calorii_necesare = int((655 + (9.6 * greutate) + (1.8 * inaltime) - (4.7 * varsta))
            * self.factori_activitate[activitate])

        else:

            calorii_necesare = int((66 + (13.7 * greutate) + (5 * inaltime) - (6.8 * varsta))
            * self.factori_activitate[activitate])

        return calorii_necesare

def main():

    ui = CaloriiCalculatorUI()
    calculator = CaloriiCalculator()

    listbox_elem = ui.window['calorii_list']
    cal_list = []

    while True:

        event, values = ui.window.read()

        if event == sg.WIN_CLOSED or event == 'Ieșire':

            break

        if event =='varsta' or event =='greutate' or event =='inaltime' or event =='sex':

            greutate = values['greutate']
            inaltime = values['inaltime']
            sex = 'Feminin' if values['sex_feminin'] else 'Masculin'
            varsta = values['varsta']
            activitate = values['activitate']

            calorii = calculator.calculeaza_calorii(greutate, inaltime, sex, activitate, varsta)
            ui.window['rezultat'].update(f'Calorii necesare: {calorii:.2f} kcal')
            cal_list.append(calorii)

        elif event == 'Calculează':

            greutate = values['greutate']
            inaltime = values['inaltime']
            sex = 'Feminin' if values['sex_feminin'] else 'Masculin'
            varsta = values['varsta']
            activitate = values['activitate']

            calorii = calculator.calculeaza_calorii(greutate, inaltime, sex, activitate, varsta)
            ui.window['rezultat'].update(f'Calorii necesare: {calorii:.2f} kcal')
            cal_list.append(calorii)
            # Se adaugă valoarea în listbox
            listbox_elem.update(values=[f'Calorii: {calorii:.2f} kcal'] + listbox_elem.Values)

    ui.window.close()

if __name__ == '__main__':
    main()