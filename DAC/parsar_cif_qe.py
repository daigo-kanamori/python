rom pymatgen.core.structure import Structure
import numpy as np

## input 

name = "(filename)"
import_file = "(cif file directory)"
usp_files_dir = "(UPS files directory)"
usp_files = "(UPF file names)"

## make in file
# import cif file

file_name = name + ".scf.in"

cif_crystal = Structure.from_file(import_file)

crystal_lattice = cif_crystal.lattice.matrix
crystal_atom_num = np.size(cif_crystal.atomic_numbers)
crystal_atom_posi = cif_crystal.cart_coords
crystal_atom_kind = cif_crystal.atomic_numbers

#control

control_txt = "&control\n"\
" calculation   = 'scf',\n"\
" pseudo_dir = " + str(usp_files_dir) + ",\n"\
"/\n"


# system

system_txt = "&system\n"\
" ibrav         = 0,\n"\
" ntyp          = " + str(len(set(crystal_atom_kind))) + ",\n"\
" nat           = " + str(crystal_atom_num) + ",\n"\
" ecutwfc       = 25.0,\n"\
" ecutrho       = 225.0,\n"\
" nspin         = 1,\n"\
"/\n"

#electrons

electrons_txt = "&electrons\n"\
" conv_thr            = 1d-8,\n"\
" mixing_beta         = 0.7,\n"\
"/\n"

#atomic_species

atomic_species_txt = "ATOMIC_SPECIES\n"\
"" + str(usp_files)+"\n"\
"\n"

#atomic positions

priodic_table = ["H", "He",
                 "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                 "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
                 "K", "Ca", "So", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
                 "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"]

atom_posi_txt = ""

for atom_posi in range(crystal_atom_num*3):
    if atom_posi % 3 == 0:
        atom_posi_txt = atom_posi_txt + priodic_table[crystal_atom_kind[atom_posi//3] - 1] + "   " + str("{:.9f}".format(crystal_atom_posi[atom_posi // 3][atom_posi % 3])) + "   "
    elif atom_posi % 3 == 1:
        atom_posi_txt = atom_posi_txt + str("{:.9f}".format(crystal_atom_posi[atom_posi // 3][atom_posi % 3])) + "   "    
    elif atom_posi % 3 == 2:
        atom_posi_txt = atom_posi_txt + str("{:.9f}".format(crystal_atom_posi[atom_posi // 3][atom_posi % 3])) + "   \n"
    else:
        pass

atom_posi_txt = "ATOMIC_POSITIONS angstrom\n" + atom_posi_txt

#k_points

k_point_txt = "K_POINTS {automatic}\n"\
"3 3 3 0 0 0\n"\
"\n"

#crystal_lattice

cryatal_lattice_txt = ""

for cell_parameta in range(9):
    if cell_parameta % 3 == 2:
        cryatal_lattice_txt = cryatal_lattice_txt + str("{:.9f}".format(crystal_lattice[cell_parameta // 3][cell_parameta % 3])) + "   \n "
    else:
        cryatal_lattice_txt = cryatal_lattice_txt + str("{:.9f}".format(crystal_lattice[cell_parameta // 3][cell_parameta % 3])) + "   "
    
cryatal_lattice_txt = "CELL_PARAMETERS angstrom\n " + cryatal_lattice_txt


txt = control_txt + system_txt + electrons_txt + atomic_species_txt + atom_posi_txt + "\n" + k_point_txt + cryatal_lattice_txt + "\n"


with open(file_name, 'wb') as a_file:
    a_file.write(txt.encode('ASCII'))

    
print("finish!")
