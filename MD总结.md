gmx pdb2gmx -f cas_dP.pdb -o cas_dP.gro -ignh -missing

gmx editconf -f cas_dP.gro -o cas_dP_new.gro -bt dodecahedron -d 4.0

gmx solvate -cp cas_dP_new.gro -cs spc216.gro -p topol.top cas_dP_solv.gro

../zl/gmx_step1.sh cascade_dna

../zl/gmx_step2.sh cascade_dna_rmP

../zl/gmx_step3.sh cascade_dna_rmP

gmx make_ndx -f $pdb'cascade_dna_rmP_solv_ions.gro' -o index.ndx

#!/bin/bash
 ../zl/gmx_step4.sh cascade_dna_rmP
 ../zl/gmx_step5.sh cascade_dna_rmP
 
