## 1.MD相关流程总结
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
 
2022年9月9日

记录需要解决的问题

蛋白结构设计需要完成的任务
1.用pymol尝试替换PDB文件中的RNA；
2.搞明白cascade如何切割DNA已经切割是DNA的状态；
3.将突变体的结构预测结束；
4.MD的结果跑完并对结果进行分析；（还有一个可能需要解决的问题，DNA的长度变化问题）

Ago蛋白需要解决的问题
按照步骤接着跑
解决bug(重中之重)

## 2.MD结果的可视化


