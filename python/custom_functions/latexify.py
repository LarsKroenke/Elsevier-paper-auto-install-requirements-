"""
Modul zur Umwandlung mathematischer Ausdrücke in LaTeX-Formeln.

Dieses Modul bietet Funktionalität zum Erstellen von LaTeX align-Umgebungen
aus Python-Ausdrücken mit Variablensubstitution.
"""

import os
import re
import sys
import csv
from pathlib import Path
from typing import Dict, Optional, Union


class LatexifyError(Exception):
    """Benutzerdefinierte Exception für Latexify-Fehler."""
    pass


def latexify_expression(
    expression: str,
    result: Union[int, float, str] = None,
    variables: Optional[Dict[str, Union[int, float, str]]] = None,
    identifier: str = None,
    file_name: str = None,
    result_idf = None,

) -> None:
    """
    Wandelt einen mathematischen Ausdruck in eine LaTeX align-Umgebung um.

    Args:
        expression: Mathematischer Ausdruck mit '=' (z.B. 'a + b = c')
        result: Das Endergebnis der Berechnung
        variables: Dictionary mit Variablennamen und deren Werten für Substitution
        file_name: Name der Ausgabedatei (ohne .tex Endung)

    Returns:
        Nichts (None)

    Raises:
        LatexifyError: Wenn der Ausdruck kein '=' enthält oder andere Fehler auftreten
        ValueError: Wenn die Eingabeparameter ungültig sind

    Example:
        >>> latexify_expression('a + b = c', 42, {'a': 5, 'b': 37}, 'summe')
    """
    # if variables is None:
    #     variables = {}

    if result_idf:
        result = write_variables(result, result_idf)

    if file_name == None:
        sys.exit('Argument file_name cannot be of type None')

    # Validierung
    if not expression or '=' not in expression:
        raise ValueError("Der Ausdruck muss ein '=' enthalten")
    
    # custom formula name
    if identifier:
        f, x = expression.split('=')
        expression = f'{identifier} = {x}'

    # Bereite den Ausdruck für LaTeX vor
    latex_expr = re.sub(r'=', '&=', str(expression))  # Gleichheitszeichen ersetzen
    latex_expr = re.sub(r'\\cdot\s+1(?![0-9])', r'\\cdot', latex_expr)  # \cdot 1 ersetzen
    
    try:
        expr_right, expr_left = latex_expr.split('=', 1)
    except ValueError:
        raise LatexifyError(f"Fehler beim Parsen des Ausdrucks: {expression}")

    # Variablensubstitution
    if variables != None:
        substituted_expr = _substitute_variables(expr_left, variables)

    # LaTeX-Code generieren
    if variables == None:
        latex_code = _generate_latex_align(latex_expr, variables, result)
    else:
        latex_code = _generate_latex_align(latex_expr, substituted_expr, result)
    latex_code = latex_code.replace('[]', '[exponent-mode=threshold]')

    #subscript LaTeX style
    latex_code = underscore_to_subscript(latex_code)

    # Datei schreiben
    _write_latex_file(latex_code, file_name)



def _substitute_variables(
    expression: str,
    variables: Dict[str, Union[int, float, str]]
) -> str:
    """
    Ersetzt Variablen im Ausdruck durch ihre Werte.

    Args:
        expression: Der zu bearbeitende Ausdruck
        variables: Dictionary mit Variablennamen und Werten

    Returns:
        Ausdruck mit substituierten Variablen
    """
    result_expr = expression
    
    for key, value in variables.items():
        # Escape Backslashes für LaTeX
        try:
            value_siunitx = f'{value:Lx}'
        except ValueError:
            value_siunitx = f'{value}'

        value_str = value_siunitx.replace('\\', r'\\')
        
        # Ersetze nur ganze Wörter (keine Teilstrings)
        pattern = r'(?<![a-zA-Z])' + re.escape(key) + r'(?![a-zA-Z])'
        result_expr = re.sub(pattern, value_str, result_expr)
    
    return result_expr


def _generate_latex_align(
    original_expr: str,
    substituted_expr: str,
    result: Union[int, float, str]
) -> str:
    """
    Generiert LaTeX align-Umgebung aus den Ausdrücken.

    Args:
        original_expr: Originalausdruck mit LaTeX-Formatierung
        substituted_expr: Ausdruck mit substituierten Variablen
        result: Endergebnis

    Returns:
        Formatierter LaTeX-Code
    """
    if substituted_expr == None:
        try:
            lines = [
                r'\begin{align}',
                f'    {original_expr}',
                r'\end{align}'
            ]
        except ValueError:
            lines = [
                r'\begin{align}',
                f'    {original_expr}',
                r'\end{align}'
            ]
    else:
        try:
            lines = [
                r'\begin{align}',
                f'    {original_expr} \\\\',
                f'    &={substituted_expr} \\\\',
                f'    &={result:Lx}',
                r'\end{align}'
            ]
        except ValueError:
            lines = [
                r'\begin{align}',
                f'    {original_expr} \\\\',
                f'    &={substituted_expr} \\\\',
                f'    &={result}',
                r'\end{align}'
            ]
        
    return '\n'.join(lines)


def _write_latex_file(content: str, filename: str) -> None:
    """
    Schreibt LaTeX-Code in eine Datei.

    Args:
        content: Der zu schreibende LaTeX-Code
        filename: Name der Ausgabedatei (ohne .tex)

    Raises:
        LatexifyError: Wenn die Datei nicht geschrieben werden kann
    """
    try:
        # Verwende pathlib für besseres Path-Handling
        base_dir = Path.cwd().parent
        output_dir = base_dir / 'TeX' / 'Formeln'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f'{filename}.tex'
        output_file.write_text(content, encoding='utf-8')
        
    except (OSError, IOError) as e:
        raise LatexifyError(
            f"Fehler beim Schreiben der LaTeX-Datei '{filename}.tex': {e}"
        ) from e
    

def underscore_to_subscript(s):
    return re.sub(r'([a-zA-Z])\\_([a-zA-Z0-9]+)', r'\1_{\2}', s)


def write_variables(variable, identifier):

    variable = f'{variable:Lx}'

    if identifier:
        variable = variable.replace(']', f'round-mode=figures, round-precision={identifier[1]}]')

    dict_var = {}

    file_path = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Formeln/_variables.dat')

    try: 
        with open(file_path, newline="") as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                dict_var[row[0]] = row[1]
    except FileNotFoundError:
        pass
    
    dict_var[identifier[0]] = variable

    with open(file_path, 'w') as f:
        for key in dict_var.keys():
            f.write(f'{key};{dict_var[key]}\n')
    
    return variable


def main() -> None:
    """Hauptfunktion für direkten Aufruf des Moduls."""
    ...


if __name__ == "__main__":
    main()