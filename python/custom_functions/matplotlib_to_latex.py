import os
import random
import matplotlib.pyplot as plt
import uuid


def plot_to_latex(file_name=None, caption=None, label=None, position='htbp', position_float='centering', width=''):
    # Eingabevalidierung
    if file_name is not None and not isinstance(file_name, str):
        raise TypeError("file_name muss str oder None sein")
    if caption is not None and not isinstance(caption, str):
        raise TypeError("caption muss str oder None sein")
    if label is not None and not isinstance(label, str):
        raise TypeError("label muss str oder None sein")
    if not isinstance(position, str) or not position:
        raise TypeError("position muss ein nicht-leerer str sein")
    if not set(position).issubset(set("htbp!H")):
        raise ValueError("position darf nur die Zeichen h, t, b, p, ! und H enthalten")
    if not isinstance(position_float, str):
        raise TypeError("position_float muss str sein")
    if position_float not in {"centering", "flushright", "flushleft", ""}:
        raise ValueError("position_float muss 'centering', 'flushleft', 'flushright' oder '' sein")

    # width validieren/normalisieren
    if width is None:
        width = ''
    elif isinstance(width, (int, float)):
        if not (0 < float(width) <= 1):
            raise ValueError("width muss im Intervall (0, 1] liegen")
        width = str(float(width))
    elif isinstance(width, str):
        if width.strip() == '':
            width = ''
        else:
            try:
                w = float(width)
            except ValueError:
                raise ValueError("width muss leer ('') oder numerisch sein, z.B. '0.8'")
            if not (0 < w <= 1):
                raise ValueError("width muss im Intervall (0, 1] liegen")
            width = str(w)
    else:
        raise TypeError("width muss str, Zahl oder '' sein")

    # Hilfsfunktion für Dateinamen prüfen
    def _is_safe_basename(name: str) -> bool:
        return all(sep not in name for sep in ('/', '\\'))

    # file name argument
    adjectives = [
        "aromatic", "aliphatic", "covalent", "ionic", "metallic",
        "polar", "nonpolar", "amphoteric", "acidic", "basic", "alkaline",
        "chiral", "achiral", "enantioselective", "diastereoselective",
        "nucleophilic", "electrophilic", "oxidative", "reductive",
        "radical", "photochemical", "thermochemical", "organometallic",
        "heterocyclic", "homocyclic", "anionic", "cationic", "zwitterionic",
        "aqueous", "aprotic", "protic", "hydrophobic", "hydrophilic",
        "paramagnetic", "diamagnetic", "exergonic", "endergonic",
        "endothermic", "exothermic", "stoichiometric", "catalytic",
        "superacidic", "superbasic", "quantum", "spectroscopic",
        "crystalline", "amorphous", "mesoporous", "microporous"
    ]
    nouns = [
        "molecule", "ligand", "catalyst", "polymer", "monomer",
        "ion", "radical", "complex", "acid", "base",
        "reagent", "solvent", "solute", "precipitate",
        "crystal", "lattice", "spectrum", "chromatogram", "reactor",
        "alkane", "alkene", "alkyne", "arene",
        "peptide", "protein", "enzyme", "nucleotide",
        "nucleophile", "electrophile", "carbocation", "carbanion",
        "carbene", "nitrene", "ketone", "aldehyde", "ester", "amide",
        "anhydride", "ether", "alcohol", "thiol", "phenol", "amine",
        "imide", "iminium", "borane", "silane", "phosphine",
        "perovskite", "zeolite", "nanotube", "nanoparticle",
        "quantumdot", "mof", "cof", "framework"
    ]

    root_dir = os.path.dirname(os.getcwd())

    if file_name is None:
        folder = os.path.join(root_dir, 'TeX', 'Tabellen')
        try:
            existing_files = set(os.listdir(folder))
        except FileNotFoundError:
            existing_files = set()
        # robust gegen Kollisionen
        for _ in range(1000):
            random_file_name = f'{random.choice(adjectives)}-{random.choice(nouns)}'
            if random_file_name not in existing_files:
                file_name = random_file_name
                break
        else:
            file_name = f'plot-{uuid.uuid4().hex[:8]}'
    else:
        if not _is_safe_basename(file_name):
            raise ValueError("file_name darf keine Pfadseparatoren enthalten")

    # caption name argument
    if caption is None:
        caption = f'{random.choice(adjectives)}-{random.choice(nouns)}'

    # label name argument (korrekt nutzen; fallback auf file_name)
    if label is None:
        label = file_name

    # Verzeichnisse vorbereiten
    pgf_dir = os.path.join(root_dir, 'TeX', 'Abbildungen', 'PGF')
    tex_dir = os.path.join(root_dir, 'TeX', 'Abbildungen')
    try:
        os.makedirs(pgf_dir, exist_ok=True)
        os.makedirs(tex_dir, exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Konnte benötigte Verzeichnisse nicht erstellen: {pgf_dir} / {tex_dir}") from e

    # save plot as pgf
    pgf_path = os.path.join(pgf_dir, f'{file_name}.pgf')
    try:
        plt.savefig(pgf_path, format='pgf', bbox_inches='tight')
    except Exception as e:
        raise RuntimeError(f"Fehler beim Speichern der PGF-Datei: {pgf_path}") from e

    # create latex file
    figure_string = [fr'\begin{{figure}}[{position}]']
    if position_float:
        figure_string.append(fr'    \{position_float}')
    figure_string += [
        fr'    \resizebox{{{width}\textwidth}}{{!}}{{\input{{Abbildungen/PGF/{file_name}.pgf}}}}',
        fr'    \caption{{{caption}}}',
        fr'    \label{{fig:{label}}}',
        r'\end{figure}'
    ]

    tex_path = os.path.join(tex_dir, f'{file_name}.tex')
    try:
        with open(tex_path, 'w') as file:
            file.write('\n'.join(figure_string))
        print(f"LaTeX-plot erfolgreich in {file_name} geschrieben")
        return pgf_path, tex_path
    except OSError as e:
        raise RuntimeError(f"Fehler beim Schreiben der LaTeX-Datei: {tex_path}") from e
    

# def subplot_to_latex(position, position_float, width, file_name, caption, label):

#     # create LaTeX file
#     figure_string = [fr'\begin{{figure}}[{position}]']
#     if position_float:
#         figure_string.append(fr'    \{position_float}')
#     figure_string += [
#         fr'    \begin{{subfigure}}{{0.45\textwidth}}',
#         fr'        \includegraphics[width]'
#         fr'    \caption{{{caption}}}',
#         fr'    \label{{fig:{label}}}',
#         r'\end{figure}'
#     ]

# \begin{figure}[htbp]
#     \centering
#     \begin{subfigure}{0.45\textwidth}
#         \includegraphics[width=\textwidth]{}
#         \caption{}
#         \label{fig:}
#     \end{subfigure}
#     \hfill
#     \begin{subfigure}{0.45\textwidth}
#         \includegraphics[width=\textwidth]{}
#         \caption{}
#         \label{fig:}
#     \end{subfigure}
#     \caption{}
#     \label{fig:}
# \end{figure}