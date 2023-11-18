# function takes graph(functional).out files, reads through it to find OPT END keyword - if it is found: 
# values to find: Energy, Geom OPT cycles, Fermi Energy, Lattice parameter A and B
import re
import os
import pandas as pd

def getvals(directory):    
    
    # Sorts file in directory alphanumerically 
    dirFiles = os.listdir(directory) 
    sorteddirf = sorted(dirFiles)
    
    # Patterns to find
    pattern = " * OPT END - CONVERGED *"
    fermi = " FERMI ENERGY"
    lattice = "        A              B              C           ALPHA      BETA       GAMMA"
    alpha = "ALPHA BAND GAP:"
    beta = "BETA BAND GAP:"
    

    # Empty lists to add energy and cycle values into
    File = []
    E_AU = []
    Cycles = []
    A = []
    B =[]
    FE_AU = []
    ALPH = []
    BET = []

    # Start search 
    for func in sorteddirf:
        # Condition: look for .out files
        if func.endswith('.out'):
            func_path = os.path.join(directory,func)
            File.append(func)
            # Checks if: OPT END; if tru: stores value for Energy and number of opt cycles
            # Final optimised geometry - lattice parameter values saved
            try:
                with open(func_path, 'r') as funcf:
                    #opens .out file - read and split into lines
                    funcx = funcf.read()
                    lines = funcx.split('\n')
                    for index, line in enumerate(lines):
                        match = re.findall(pattern, line)
                        if match:
                            E_AU += [float(line.strip().split()[7])]
                            Cycles += [int(line.strip().split()[9])]

                            # Indexes new lines to search in - after OPT END to get final geometry 
                            text = lines[index:]
                            for i, l in enumerate(text):
                                latticem = re.search(lattice, l)
                                if latticem:
                                    vals = text[i+1]
                                    A += [float(vals.strip().split()[0])]
                                    B += [float(vals.strip().split()[1])] 
            except NameError:
                    print('Not Converged')
            
            # Fermi energy values collected - if there is a Band Gap 'NaM' saved in 
            try:
                with open(func_path, 'r') as funcf:
                    #open .out file - read and split into lines
                    funcx = funcf.read()
                    lines = funcx.split('\n')
                    found_fermi = False
                    for line in lines:
                        fermim = re.findall(fermi, line)
                        if fermim:
                            FE_AU.append(float(line.strip().split()[2]))
                            found_fermi = True
                            break 
            except FileNotFoundError:
                        print('Error')
            else:
                if found_fermi != True:
                    FE_AU.append('NaN')
                    
            # Alpha and Beta band Gap 
            try:
                with open(func_path, 'r') as funcf:
                    #open .out file - read and split into lines
                    funcx = funcf.read()
                    lines = funcx.split('\n')
                    found_alph = False
                    found_beta = False
                    for line in lines:
                        alphap = re.findall(alpha, line)
                        if alphap:
                            ALPH.append(float(line.strip().split()[3]))
                            found_alph = True
                            break
                    for line in lines:
                        betap = re.findall(beta, line)
                        if betap:
                            BET.append(float(line.strip().split()[3]))
                            found_beta = True
                            break
            except FileNotFoundError:
                        print('Error')
            else:
                if found_alph != True:
                    ALPH.append('NaN')
                if found_beta != True:
                    BET.append('NaN')               
    vals = pd.DataFrame()
    vals['File Name'] = File
    vals['Energy in Ha AU'] = E_AU
    vals['OPT Cycles'] = Cycles
    vals['Lattice Parameter A'] = A
    vals['Lattice Parameter B'] = B
    vals['Fermi Energy in Ha AU'] = FE_AU
    vals['Alpha Band Gap in eV'] = ALPH
    vals['Beta Band Gap in eV'] = BET
    return vals