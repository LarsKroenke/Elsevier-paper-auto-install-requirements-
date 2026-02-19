import os
import random
import re
import pandas as pd


class column_format_shortage(Exception):
    pass


def main():
    ...


def df_to_tex(df, 
              column_format=None, 
              columns=None,                 # which columns to take from dataframe
              position='htbp',              # 
              position_float='centering', 
              hrules=True, 
              caption=None, 
              label=None, 
              siunitx=True, 
              file_name=None, 
              adjustbox=None, 
              na_rep='{–}', 
              show_table=False, 
              multicol_align=None,
              DINunit=True,
              precision=[], 
              exponents=[]
            ):    
    
    # df = df.pint.dequantify()

    # na_rep argument
    if na_rep != '{–}':
        df = df.fillna('{'+na_rep+'}')
    else:
        df = df.fillna(na_rep)

    # file name argument
    adjectives = [
        "sleepy", "curious", "fluffy", "musical", 'fierce', 'hilarious', 'hysterical', 'enchanted', 'astonishing', 'blundering', 'bewildering', 'boisterous', 'clumsy', 'dumbfounded', 'discombobulated', 'enigmatic', 'exasperating', 'fumbling', 'frivolous', 'gullible', 'gumptious', 'half-baked',
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

    # NEU: Datenzellen je Spalte auf gleiche Zeichenlänge auffüllen (Überschriften bleiben unverändert)
    # Maximalbreite pro Spalte aus Datenzeilen (ohne Header) bestimmen
    col_widths = {}
    for col in df_styler.columns:
        # in Strings wandeln und Länge messen
        lengths = df_styler[col].astype(str).map(len)
        col_widths[col] = lengths.max() if len(lengths) > 0 else 0
    # Padding anwenden: nur Datenzellen, nicht die Header
    for col in df_styler.columns:
        width = col_widths[col]
        if width and width > 0:
            df_styler[col] = df_styler[col].astype(str).str.ljust(width)

    # column format default center
    if column_format == None:
        column_format = ''
        for i in range(len(columns)):
            column_format += 'c'

    # throw error in case of too few arguments
    if len(columns) != len(column_format):
        raise column_format_shortage('Too few letters in column_format')

    # siunitx column format auto adjustments
    column_format = column_format.replace('S', f'S[fixed-exponent=0, round-mode=places, round-precision=3]')
    
    if exponents != []:
        def set_exponent(text, exponents):
            it = iter(exponents)

            def repl(match):
                content = match.group(1)
                exp = next(it)

                content = re.sub(
                    r'fixed-exponent\s*=\s*[+-]?\d+',
                    f'fixed-exponent={exp}',
                    content
                )

                return f'S[{content}]'

            return re.sub(r'S\[(.*?)\]', repl, text)
    
        column_format = set_exponent(column_format, exponents)

    # prcision default 3, unless list given as argument
    if precision != []:
        def set_precision(text, precision):
            it = iter(precision)

            def repl(match):
                content = match.group(1)
                n = next(it)

                content = re.sub(
                    r'round-precision\s*=\s*[+-]?\d+',
                    f'round-precision={n}',
                    content
                )

                return f'S[{content}]'

            return re.sub(r'S\[(.*?)\]', repl, text)
        
        column_format = set_precision(column_format, precision)


    # generating the latex table with Styler to_latex() function
    latex_table = df_styler.style.hide(axis='index').to_latex(
        column_format=column_format,
        position=position,
        position_float=position_float,
        hrules=hrules,
        label=label,
        caption=caption,
        siunitx=siunitx,
        convert_css=True,
        multicol_align=multicol_align,
    )

    # verwendete 10er Potenzen vor die Einheit setzen 
    if exponents != []:
        latex_table = latex_table.splitlines()
        # Replace only braces with surrounding spaces to avoid over-replacement
        latex_table[7] = re.sub(r"^\{", r"{$10^{0}\,$", latex_table[7])
        latex_table[7] = re.sub(r"\s\{", r"{$10^{0}\,$", latex_table[7])
        latex_table = '\n'.join(latex_table)
        def replace_exponents(text, exponents):
            it = iter(exponents)

            def repl(match):
                return f'10^{{{next(it)}}}'
            
            return re.sub(r'10\^\{0\}', repl, text)
        
        latex_table = replace_exponents(latex_table, exponents)
        latex_table = latex_table.replace(r'$10^{0}\,$', '')

    # DIN unit presentation
    if DINunit:
        latex_table = latex_table.splitlines()
        # Replace only braces with surrounding spaces to avoid over-replacement
        latex_table[7] = latex_table[7].replace('&', '&  ')
        latex_table[7] = re.sub(r"\}\s", ")} ", latex_table[7])
        latex_table[7] = re.sub(r"^\{", r"{(", latex_table[7])
        latex_table[7] = re.sub(r"\s\{", r"{(", latex_table[7])
        latex_table = '\n'.join(latex_table)
    else:
        latex_table = latex_table.splitlines()
        latex_table[7] = latex_table[7].replace('&', '& ')
        latex_table = '\n'.join(latex_table)

    # adjustbox argument
    if adjustbox:
        latex_table = latex_table.splitlines()
        latex_table.insert(4, fr'\begin{{adjustbox}}{{width={adjustbox}\textwidth}}')
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
    
    # writing to_latex output string to a file
    try:
        file_path_table = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Tabellen', file_name)
        os.makedirs(os.path.dirname(file_path_table), exist_ok=True)
        with open(file_path_table, 'w') as file:
            file.write(indented_table)
            # print(f"LaTeX-Tabelle erfolgreich in {file_name} geschrieben")
    except FileNotFoundError:
        print(f"Fehler beim Schreiben der LaTeX-Tabelle")


if __name__ == "__main__":
    main()