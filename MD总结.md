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
 
## 2.师姐提供的MD步骤

```
#!/bin/bash
###Read the tips below and then start perform MD simulation!!!!
###step1--5 do not need GPU drive, you can perform them on 并行scb8190,or 胖节点 or GPU2,3,4
###step6 needs GPU drive ,youcanperform it on GPU2,3,4 or 并行scz4082, use 6 cpu is ok!!!
###step1:convet pdb to gro
#gmx pdb2gmx -f 7lys.new.pdb -o 7lys.gro -ignh -missing
###tips:choose The Amber14sb_parmbsc1 force field and the tip3p water model
###step2:edit box to solvate
#gmx editconf -f 7lys.gro -o 7lys_newbox.gro -bt dodecahedron -d 4.0
#gmx solvate -cp 7lys_newbox.gro -cs spc216.gro -p topol.top -o 7lys_solv.gro
###step3:generate the ions.tpr file 
#gmx grompp -f ../codes/em.mdp -c 7lys_solv.gro -r 7lys_solv.gro -p topol.top -o ions.tpr -maxwarn 2
#gmx genion -s ions.tpr -o 7lys_solv_ions.gro -p topol.top -pname NA -nname CL -np 22
###step4:minimize the energy
##make index file
#gmx make_ndx -f 7lys_solv_ions.gro -o index.ndx
##generate em.tpr file
#gmx grompp -f ../codes/em.mdp -c 7lys_solv_ions.gro -r 7lys_solv_ions.gro -p topol.top -n index.ndx -o 7lys_em.tpr -maxwarn 2
##run energy minimize
#gmx mdrun -v -deffnm 7lys_em -ntmpi 1 -ntomp 16
###** -v -deffnm em 默认读取输入文件为em.tpr,能量最小化后生成的文件名也都为em，即生成em.edr，em.trr，em.gro，em.log
###step5:NVT NPT 预平衡
#gmx grompp -f ../codes/nvt.mdp -c 7lys_em.gro -r 7lys_em.gro -p topol.top -n index.ndx -o 7lys_nvt.tpr -maxwarn 2
#wait
#gmx mdrun -deffnm 7lys_nvt -ntmpi 1 -ntomp 12
###When perform this step on 并行scb8190,please change thread number to 128
###NPT系综的体系平衡
#gmx grompp -f ../codes/npt.mdp -c 7lys_nvt.gro -r 7lys_nvt.gro -t 7lys_nvt.cpt -p topol.top -n index.ndx -o 7lys_npt.tpr -maxwarn 2
###NPT系综运行体系平衡
#gmx mdrun -deffnm 7lys_npt -ntmpi 1 -ntomp 10
###When perform this step on 并行scb8190,please change thread number to 128
###step6:run md simulation
#gmx grompp -f ../../codes/md.mdp -c 7lys_npt.gro -r 7lys_npt.gro -t 7lys_npt.cpt -p topol.top -n index.ndx  -o 7lys_md01.tpr -maxwarn 2
#wait
#gmx mdrun -s 7lys_md01.tpr -cpi 7lys_md01.cpt -deffnm 7lys_md01 -pme gpu -bonded gpu -dlb yes -pmefft gpu -ntmpi 1 -ntomp 6 -gpu_id 0

```

### 在并行和并行GPU服务器上下载文件的命令

```
papp_cloud scp scb8190@bscc-a6:/public1/home/scb8190/caojian/MD/cj-2 /HOME/scz4082/run/caojian/MD/cascade_tev1
```
[参考网页](https://papp-cloud.paratera.com/docs/papp3/)


## 3.MD结果的可视化


## 4.MD续跑

在可视化得到的结果不是很理想的时候，需要对已经结束的任务进行续跑，期望RMSD能够稳定
主要有以下两个命令：

```
gmx convert-tpr -s cj_md2.tpr -extend 2000 -o cj_md2.tpr
gmx mdrun -v -deffnm cj_md2 -cpi cj_md2.cpt
```

## 5.GPU44上运行aiphafold的相关代码

```
# sh文件内容
work_dir=/mnt/0b4c0b27-228c-4032-80d0-7a7ecca7bfe5/caojian/l1_orf2
bash run_alphafold.sh -d /mnt/111d8171-c050-4d8b-8bf9-291a43dc804f/like_444/alphafold2 -o $work_dir -m model_1 -f $work_dir/sequence.fasta -t 2021-11-01
```
程序路径

```
/mnt/111d8171-c050-4d8b-8bf9-291a43dc804f/like_444/alphafold2/alphafold
conda activate like_alphafold
TnpB_af2.sh
```
