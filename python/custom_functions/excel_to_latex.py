import pandas as pd
import random
import os
import pyperclip as pc
import sys

# Kopiere Excel Tabelle in die Zwischenablage, passe die Funktionsargumente (Zeile 18 - 33) an und starte das Programm. Die oben stehenden Bibliotheken müssen installiert sein.
# WICHTIG: Die Excel Tabelle darf keine leeren Zellen enthalten, da sonst kein DataFrame erstellt werden kann da die Länge der Zeilen gleich viele Spalten enthalten muss (keine Lust das Error proof zu machen)

def main():
    # Generiert aus in die Zwischenablage kopierte Excel Tabelle einen pandas Data Frame
    data_frame = excel_to_DataFrame()

    # Diese Funktion generiert die LaTeX Tabelle und speichert sie als .tex Datei unter TeX/Tabellen
    df_to_tex(data_frame, 
              
            # Hier können die wichtigen default values überschrieben werden um die LaTeX Tabelle anzupassen

            file_name='tabelle',            # Name der Datei, muss in anführungszeichen stehen (string)
            column_format=None,             # standardmäßig None -> "c" für center, muss ansonsten ein string (zb. 'lccc') sein und der anzahl columns entsprechen
            caption=None,                   # Name der caption, wenn None wird sie zufällig generiert
            label=None,                     # Name des labels, wenn None wird es zufällig generiert
            position='htbp',                # Position im Dokument, ggf. auf H wenn mehr Kontrolle erwünscht
            adjustbox=False,                # Auf True setzen um adjustbox umgebung einzubinden um Textbreite nicht zu überschreiten


            # Eigentlich weniger wichtig aber dennoch anpassbar:

            position_float='centering',     # Position Links, mitte oder rechts
            hrules=True,                    # Horitontale Zeilen in der Tabelle
            siunitx=True,                   # Spalten headers stehen in geschweiften Klammern, wichtig wenn column_format='S'. Stört aber bei 'cccc' auch nicht
            na_rep='{–}',                   # ersetzt NaN für Not a Number durch halbgeviertstrich "–", in Excel am besten alle Errors wie #Div/0! durch "NaN" ersetzen
            show_table=True,                # zeigt Vorschau in der Terminalausgabe wenn True
            precision=None,                 # rundet auf angegebene Anzahl signifikanter stellen, funktioniert nur in englischer dezimalschreibweise (3.14). Bei 3,14 oder None effektlos
            )


def excel_to_DataFrame():
    # data = pc.paste()

    # rows = [line.strip().split('\t') for line in data.strip().split('\n')]
    rows = [['V luft', 'V EtOH', 'V ges', 'c', 'vol'], ['150', '0', '150', '0', '0'], ['150', '1', '151', '0,0159', '0,662251656'], ['150', '2', '152', '0,031560673', '1,315789474'], ['150', '2,5', '152,5', '0,039321494', '1,639344262'], ['150', '3,5', '153,5', 'NaN', '2,280130293'], ['150', '4', '154', '0,062301588', '2,597402597'], ['150', '5', '155', '0,077374553', '3,225806452']]

    # Excel Errors durch – ersetzen
    excel_errors = [
    "NaN",
    "#DIV/0!",   # Division durch 0
    "#VALUE!",   # Falscher Datentyp
    "#REF!",     # Ungültiger Zellbezug
    "#NAME?",    # Unbekannter Name
    "#N/A",      # Wert nicht verfügbar
    "#NUM!",     # Ungültige Zahl
    "#NULL!",    # Ungültiger Zellbereich
    "#SPILL!",   # Überlauf-Fehler (Array)
    "#CALC!",    # Berechnungsfehler (Array)
    "#GETTING_DATA",  # Daten werden geladen
    "#CONNECT!"  # Verbindungsfehler (selten)
]
    counter_1 = -1
    for i in rows:
        counter_1 += 1
        counter_2 = 0
        for j in i:
            if j in excel_errors:
               rows[counter_1][counter_2] = '{–}'
            counter_2 += 1
               
    rows_transposed = list(map(lambda *x: list(x), *rows))

    # Alle Zellen auf gleiche Länge für hübschere Tabelle
    col_widths = [
        max((len(str(c)) for c in col[1:]), default=0)
        for col in rows_transposed
    ]
    rows_transposed = [
        [col[0]] + [str(cell).ljust(col_widths[i]) for cell in col[1:]]
        for i, col in enumerate(rows_transposed)
    ]
    
    # DataFrame aus list erstellen
    data_frame = {}
    for i in range(len(rows_transposed)):
        data_frame[f'{rows_transposed[i][0]}'] = rows_transposed[i][1:]

    df = pd.DataFrame(data_frame)
    return df


def df_to_tex(df, column_format=None, columns=None, position='htbp', position_float='centering', hrules=True, caption=None, label=None, siunitx=True, file_name=None, adjustbox=False, na_rep='{–}', show_table=False, precision=None, multicol_align=None):

    # na_rep argument
    if na_rep != '{–}':
        df = df.fillna('{'+na_rep+'}')
    else:
        df = df.fillna(na_rep)

    # file name argument
    adjectives = [
        "sexy", "sleepy", "curious", "fluffy", "musical", 'fierce', 'hilarious', 'hysterical', 'enchanted', 'astonishing', 'blundering', 'bewildering', 'boisterous', 'clumsy', 'dumbfounded', 'discombobulated', 'enigmatic', 'exasperating', 'fumbling', 'frivolous', 'gullible', 'gumptious', 'half-baked',
        "outrageous", "silent", "fancy", "clever", "mighty", 'harebrained', 'idiosyncratic', 'ingenious', 'knuckleheaded', 'lighthearted', 
        "shiny", "naked", "swifty", "lazy", "wild"
    ]

    nouns = [
        "capybara", "panda", "otter", "dolphin", "falcon",
        "tiger", "lion", "koala", "penguin", "cat",
        "fox", "wolf", "rabbit", "eagle", "bear"
    ]

    if file_name == None:   
        folder = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Tabellen')
        existing_files = set(os.listdir(folder))
        while True:
            random_file_name = f'{random.choice(adjectives)}-{random.choice(nouns)}.tex'
            if random_file_name not in existing_files:
                file_name = random_file_name
                break
    else:
        if not file_name.endswith(".tex"):
            file_name += ".tex"
        
    # caption name argument
    if caption == None:
        caption = f'{random.choice(adjectives)}-{random.choice(nouns)}'

    # label argument
    if label == None:
        label = f'tab:{random.choice(adjectives)}-{random.choice(nouns)}'
    else:
        label = 'tab:' + label

    # which columns to take from datframe, might remove columns argument
    df_styler = pd.DataFrame()
    if columns == None:
        columns = list(df.columns)
    df_styler = df[columns].copy()

    # column format default center
    if column_format == None:
        column_format = ''
        for i in range(len(columns)):
            column_format += 'c'
    
    if len(column_format) != len(columns):
        sys.exit('WARNUNG: column_format stimmt nicht mit der Anzahl Spalten überein!')
        

    # generating the latex table with Styler to_latex() function
    latex_table = df_styler.style.hide(axis='index').format(precision=precision).to_latex(
        column_format=column_format,
        position=position,
        position_float=position_float,
        hrules=hrules,
        label=label,
        caption=caption,
        siunitx=siunitx,
        convert_css=True,
        multicol_align=multicol_align
    )

    # adjustbox argument
    if adjustbox == True:
        latex_table = latex_table.splitlines()
        latex_table.insert(4, r'\begin{adjustbox}{width=\textwidth}')
        latex_table.insert(len(latex_table)-1, r'\end{adjustbox}')
        latex_table = '\n'.join(latex_table)

    # indent table properly
    latex_table2 = latex_table.splitlines()
    indented_table = []
    tab = ''
    for line in latex_table2:
        if not line.startswith(r'\end'):
            indented_table.append(tab + line)
        if line.startswith(r'\begin'):
            tab += '    '
        elif line.startswith(r'\end'):
            tab = tab[:-4]
            indented_table.append(tab + line)
    indented_table = '\n'.join(indented_table)

    # show table argument
    if show_table != False:
        print(indented_table)
        print()
    
    # writing to_latex output string to a file
    try:
        file_path_table = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Tabellen', file_name)
        if not os.path.exists(file_path_table):
            os.makedirs(os.path.dirname(file_path_table), exist_ok=True)
            with open(file_path_table, 'w') as file:
                file.write(indented_table)
            print(f'Die Tabelle {file_name} wurde erfolgreich erstellt und unter TeX/Tabellen gespeichert')
        else:
            print(f'WARNUNG: {file_path_table} existiert bereits, möchtest du die Datei überschreiben? ', end='')
            while True:
                yes_no = input('(y/n) ')
                if yes_no == 'y':
                    os.makedirs(os.path.dirname(file_path_table), exist_ok=True)
                    with open(file_path_table, 'w') as file:
                        file.write(indented_table)
                        print(f'Die Tabelle {file_name} wurde erfolgreich erstellt und unter TeX/Tabellen gespeichert')
                    break
                elif yes_no == 'n':
                    print('Ändere die Variable "file_name" und starte das Programm erneut')
                    break
                else:
                    print('Gib y für Ja oder n für Nein ein')
                    continue
    except FileNotFoundError:
        print(f"Stelle sicher dass das directory TeX/Tabellen existiert")


if __name__ == "__main__":
    main()