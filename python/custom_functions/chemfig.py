import sys
import os
import subprocess
import re
import pubchempy as pcp
from mol2chemfigPy3 import mol2chemfig


def main():
    ...


def chemfig(name, file_name=None, opt='-wf', extra=None, rotate=0, rendernr=None, cmp_label=None):
# cmd = ['mol2chemfig', '-f', '-w', '-i', 'direct', 'C1=CC=C(C=C1)S']

    if re.search(r'\d+', str(name)) and re.search(r'[a-zA-Z]', str(name)) == None:
        compound = pcp.Compound.from_cid(name)
        smiles = compound.smiles
        cid_to_name = compound.synonyms
        if file_name == None:
            file_name = cid_to_name[0]
        if cmp_label == None:
            cmp_label = cid_to_name[0]
    else:
        compound = pcp.get_compounds(name, 'name')
        idf = re.search(r'\d+', str(compound))
        compound = pcp.Compound.from_cid(int(idf[0]))
        smiles = compound.smiles
        if file_name == None:
            file_name = name
        if cmp_label == None:
            cmp_label = name


    a = f'-a -{str(rotate)}'

    if extra:
        opt += extra

    if rendernr:
        cmd = [
            'mol2chemfig', 
            opt,  
            a,
            f'-e {rendernr}',
            '-i', 
            'direct', 
            f'{smiles.strip()}'
            ]
    else:
        cmd = [
            'mol2chemfig', 
            opt,  
            a,
            '-i', 
            'direct', 
            f'{smiles.strip()}'
            ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    # print(result)

    mol_string = result.stdout.splitlines()
    closing1 = '}{'
    closing2 = '}'
    mol_string.insert(0, r'\chemname{')
    # german Umlaut insertion
    # regex = re.sub(r'a', 'ä', cmp_label)
    mol_string.insert(len(mol_string), closing1+cmp_label.replace('ae', 'ä')+closing2)
    mol_string = '\n'.join(mol_string)


    try:
        file_path = os.path.join(os.path.dirname(os.getcwd()), 'TeX', 'Moleküle', f'{file_name}.tex')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(mol_string)
            print(f"chemfig Molekül erfolgreich geschrieben")
    except FileNotFoundError:
        print(f"Fehler beim Schreiben der LaTeX-Tabelle")


if __name__ == "__main__":
    main()