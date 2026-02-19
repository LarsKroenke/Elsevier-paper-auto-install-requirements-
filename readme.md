# Projektübersicht

Dieses Repository bündelt die Erstellung eines wissenschaftlichen Artikels (Elsevier/elsarticle-deutsch) mit einer LaTeX-Hauptdatei und einem Satz an Python-Hilfsfunktionen, die Tabellen, Formeln, Molekülzeichnungen und Abbildungen automatisiert in das LaTeX-Projekt schreiben. Die Datenquelle liegt in `data/`, die Notebooks und Python-Helfer in `python/`, und das LaTeX-Projekt in `TeX/`.

## Struktur

```
Elsevier-Artikel/
├── TeX/                          # Hauptverzeichnis für LaTeX-Dokumente
│   ├── main.tex                  # Hauptdokument (Einstiegspunkt)
│   ├── elsarticle-deutsch.cls    # Angepasste Elsevier-Dokumentklasse
│   ├── mypreamble.sty            # Benutzerdefinierte Präambel mit allen Paketen
│   ├── Literatur.bib             # BibLaTeX-Literaturdatenbank
│   ├── Hauptkapitel/             # Hauptkapitel des Dokuments
│   │   ├── titleAbstract.tex     # Titel und Abstract
│   │   ├── 01Einleitung.tex      # Einleitung
│   │   ├── 02Material und Methoden.tex
│   │   ├── 03Ergebnisse.tex
│   │   ├── 04Diskussion.tex
│   │   └── Anhang.tex
│   ├── Abbildungen/              # LaTeX-Abbildungen (TikZ, PGFPlots)
│   │   ├── chromatogramm.tex
│   │   └── example_plot.tex
│   ├── Moleküle/                 # Chemische Strukturformeln (ChemFig)
│   │   ├── molecule.tex
│   ├── Tabellen/                 # LaTeX-Tabellen
│   │   └── table.tex
│   └── Konfigurationsdateien/    # Glossare und Akronyme
│       ├── myacronyms.tex
│       └── myglossary.tex
└── python/                       # Python-Hilfsskripte
    ├── chemfig.py                # Generierung von ChemFig-Molekülen
    ├── matplotlib_to_pgf.py      # Export von Matplotlib-Plots zu LaTeX
    ├── data_frame_to_latex.py    # Konvertierung von DataFrames zu LaTeX-Tabellen
    ├── extotex.py                # Excel-zu-LaTeX-Konvertierung
    └── data.ipynb                # Jupyter Notebook für Datenanalyse
```

## Python-Hilfsfunktionen

Diese Module automatisieren die Erstellung von LaTeX-Dateien in den entsprechenden Unterordnern von `TeX/`.

**Tabellen**
- **data_frame_to_latex.py**: Konvertiert einen `pandas.DataFrame` in eine LaTeX-Tabelle und schreibt sie nach [TeX/Tabellen](TeX/Tabellen).
   - **Hauptfunktion**: `df_to_tex(df, column_format, columns, position, position_float, hrules, caption, label, siunitx, file_name, adjustbox, na_rep, show_table, multicol_align, DINunit, precision, exponents)`
   - **Highlights**: automatische `siunitx`-Spaltenformatierung (`S[...]`), optionale Zehnerpotenzen (`exponents`), DIN-konforme Einheitenzeile (`DINunit`), zufällige Dateinamen/Caption/Label, saubere Einrückung.
   - **Output**: legt eine `.tex`-Datei im Tabellen-Ordner ab.

- **excel_to_latex.py**: Erzeugt einen DataFrame aus einer aus Excel kopierten Tabelle und schreibt die formatierten LaTeX-Tabellen nach [TeX/Tabellen](TeX/Tabellen).
   - **Ablauf**: Inhalt aus Excel in die Zwischenablage kopieren, Parameter im `main()` anpassen, Skript ausführen.
   - **Robustheit**: ersetzt typische Excel-Fehlercodes (z. B. `#DIV/0!`) durch `–`, gleichmäßige Zellbreiten für bessere Optik.

**Formeln**
- **latexify.py**: Baut aus einem Ausdruck eine `align`‑Umgebung mit optionaler Variablensubstitution und Ergebniszeile; schreibt nach [TeX/Formeln](TeX/Formeln).
   - **Hauptfunktion**: `latexify_expression(expression, result=None, variables=None, identifier=None, file_name=None, result_idf=None)`
   - **Features**: Ersetzt `=` durch `&=`, optional Werte via `variables` einsetzt, unterstützt `pint`/`siunitx`-Formatierung (`{value:Lx}`), Subscript aus `a\_b` → `a_{b}`.
   - **Variablenpersistenz**: `write_variables(value, identifier)` legt/aktualisiert [TeX/Formeln/_variables.dat](TeX/Formeln/_variables.dat) zur konsistenten Darstellung.

**Moleküle**
- **chemfig.py**: Holt SMILES aus PubChem (via CID oder Name) und ruft den externen Konverter `mol2chemfig`, um eine `\chemfig`‑Struktur zu erzeugen; schreibt nach [TeX/Moleküle](TeX/Moleküle).
   - **Hauptfunktion**: `chemfig(name, file_name=None, opt='-wf', extra=None, rotate=0, rendernr=None, cmp_label=None)`
   - **Hinweis**: benötigt `pubchempy` und das ausführbare Tool `mol2chemfig` im `PATH`.

**Abbildungen**
- **matplotlib_to_latex.py**: Speichert aktuelle `matplotlib`‑Grafik als `.pgf` und erzeugt eine passende LaTeX‑`figure` mit `\input{...}`; schreibt nach [TeX/Abbildungen/PGF](TeX/Abbildungen/PGF) und [TeX/Abbildungen](TeX/Abbildungen).
   - **Hauptfunktion**: `plot_to_latex(file_name=None, caption=None, label=None, position='htbp', position_float='centering', width='')`
   - **Features**: valide Parameterprüfung, zufällige Dateinamen/Caption, `width` als Anteil der Textbreite (0–1], erzeugt `.pgf` und `.tex`.

**Umgebung/Setup**
- **python/config/setup.py**: Konfiguriert `pint`/`UnitRegistry`, aktiviert LaTeX‑Rendering in `matplotlib` (`text.usetex=True`, `pgf.texsystem=pdflatex`), importiert die oben genannten Helfer für Notebook‑Kontexte.

## Notebooks (Beispiele)

- **data.ipynb**: Einlesen/Exploration der CSV‑Daten; Tabellenexport nach LaTeX.
- **geraete_chemikalien.ipynb**: Verknüpft Geräte‑ und Chemikalieninformationen; exportiert zusammengefasste Tabellen.
- **kalibrierung.ipynb**: Darstellung/Anpassung von Kalibrationsmessungen und Kennlinien; generiert Abbildungen und Formeln.
- **joy.ipynb**: Experimentelles/sonstiges (Plot‑Tests, Workflow‑Skizzen, etc.).

## LaTeX-Projekt

- **Einstieg**: [TeX/main.tex](TeX/main.tex) nutzt `elsarticle-deutsch` (5p, zweispaltig) und bindet Kapitel sowie Glossar/Akronyme ein.
- **Kapitel**: liegen in [TeX/Hauptkapitel](TeX/Hauptkapitel) und werden via `\input{...}` eingebunden.
- **Assets**: Tabellen ([TeX/Tabellen](TeX/Tabellen)), Abbildungen ([TeX/Abbildungen](TeX/Abbildungen)), Formeln ([TeX/Formeln](TeX/Formeln)), Moleküle ([TeX/Moleküle](TeX/Moleküle)).
- **Build**: typischerweise mit `latexmk` bzw. `pdflatex`/`biber`, abhängig von `mypreamble.sty`/BibLaTeX‑Konfiguration.

### Installation LaTeX

```bash
sudo apt-get update && sudo apt-get install -y texlive texlive-science texlive-latex-extra texlive-bibtex-extra biber latexmk texlive-lang-german
```
#### Kompatibilität mit Matplotlib/PGF
```bash
sudo apt-get update
sudo apt-get install -y \
  texlive-latex-base texlive-latex-recommended texlive-fonts-recommended \
  dvipng cm-super texlive-pictures \
  texlive-latex-extra texlive-fonts-extra dvisvgm ghostscript \
  texlive-lang-german
```

## Codespaces Prebuild

- **Aktivierung**: Repository → Settings → Codespaces → Prebuilds → Enable. Branches wählen (z. B. `master`, `Artikel-Elsevier`).
- **Devcontainer**: `.devcontainer/devcontainer.json` liefert Python+LaTeX Features und VS Code Extensions.
- **Lifecycle**:
	- `onCreateCommand`: installiert Python‑Pakete (`pandas`, `numpy`, `matplotlib`, `pint`, `pint-pandas`, `latexify`, `scienceplots`).
	- `updateContentCommand`: baut `TeX/main.tex` mit `latexmk` vor und wärmt BibLaTeX/PGF‑Cache.
- **Ergebnis**: schnellerer Start; erste LaTeX‑Kompilierung ist deutlich flotter. Artefakte liegen in [TeX/~build](TeX/~build).

### Manuelles Testen (lokal/in Codespace)

```bash
# Prebuild‑Skripte manuell ausführen
bash .devcontainer/on-create.sh
bash .devcontainer/update-content.sh
```

### Hinweise

- Prebuilds müssen im Repo explizit aktiviert werden (Org/Repo‑Einstellungen).
- Für `mol2chemfig` ggf. separate Installation und `PATH` berücksichtigen.
- Das LaTeX‑Feature installiert TeX Live; bei exotischen Paketen kann `apt-get` ergänzt werden.

## Installation & Voraussetzungen

- **Python 3.10+** und folgende Pakete: `pandas`, `numpy`, `matplotlib`, `scienceplots`, `pint`, `pint-pandas`, `pubchempy`, `pyperclip`.
- **Externe Tools**: `mol2chemfig` (für Molekül‑Rendering), `pdflatex`/`latexmk` (LaTeX‑Build).

### Schnellstart (Python)

```bash
# Installation über die Devcontainer-Requirements
pip install -r .devcontainer/requirements.txt
```

## Beispiele

**Tabelle aus DataFrame**

```python
import pandas as pd
from custom_functions.data_frame_to_latex import df_to_tex

df = pd.DataFrame({
      'c': [1.23, 4.56, 7.89],
      'unit': ['mg/L', 'mg/L', 'mg/L']
})

df_to_tex(
      df,
      column_format='cS',
      caption='Messwerte',
      label='messwerte',
      file_name='messwerte',
      DINunit=True,
      precision=[2],
)
# Ergebnis: TeX/Tabellen/messwerte.tex
```

**Formel mit Variablen**

```python
from custom_functions.latexify import latexify_expression

latexify_expression(
      expression='c = m / V',
      variables={'m': 5, 'V': 2},
      result=2.5,
      file_name='kal_btex_std'
)
# Ergebnis: TeX/Formeln/kal_btex_std.tex
```

**Molekül via PubChem → chemfig**

```python
from custom_functions.chemfig import chemfig

chemfig('benzene', file_name='benzol', rotate=0)
# Ergebnis: TeX/Moleküle/benzol.tex
```

**Matplotlib → PGF + Figure**

```python
import matplotlib.pyplot as plt
from custom_functions.matplotlib_to_latex import plot_to_latex

plt.plot([0,1,2], [0,1,4])
plot_to_latex(file_name='example_plot', caption='Beispielplot', width=0.8)
# Ergebnis: TeX/Abbildungen/PGF/example_plot.pgf und TeX/Abbildungen/example_plot.tex
```

## Tipps & Hinweise

- **Pfade**: Alle Helfer schreiben relativ zu `TeX/` in die passenden Unterordner.
- **Labels**: `tab:...` bzw. `fig:...` werden automatisch gesetzt; manuell via Argument überschreibbar.
- **Fehlertoleranz**: Tabellen‑Helfer ersetzen `NaN`/Excel‑Fehler durch `–` für robustes LaTeX.
- **LaTeX‑Engine**: Für PGF‑Plots muss `pdflatex` verfügbar sein; `matplotlib` nutzt `text.usetex=True`.
- **mol2chemfig**: Bitte separat installieren und im `PATH` bereitstellen.

---

Fragen oder Wunsch nach Automatisierung (z. B. `requirements.txt`, Build‑Scripts, Makefile)? Ich richte das gern ein.

