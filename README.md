# de_novo_protein
This is a notebook about learning rosetta.

rosetta路径
```
/public3/home/pg3152/zzl/zzl_softwares
```

## 1.建立segment库

```
H 5 20, L 1 3, E 3 10, L 1 3, H 5 20
```

生成数据库
```
# 清洗数据库
cd $top8000_chains_70
for i in $(ls $(pwd)); do python /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/tools/fragment_tools/pdb2vall/pdb_scripts/clean_pdb.py $i; rm -rf $i; done
# 执行此操作会将文件夹里面的所有文件清空！！！
```
出现的问题
![image](https://user-images.githubusercontent.com/64938817/166611864-5143b60b-68f0-4dfc-81aa-752e33dd721d.png)
查看源代码
```
cd /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/tools/fragment_tools/pdb2vall/pdb_scripts/
cat clean_pdb.py 
```
发现存在以下问题
![image](https://user-images.githubusercontent.com/64938817/166611991-109e549a-77fb-462d-abc8-652dfd51ac06.png)
但是问题不是很大

**所以这想操作要在建立文件夹之后或者还未导入PDB文件之前操作！！！**

```
# 生成当前目录下的pdb.list
for i in $(ls $(pwd)); do echo $(pwd)/$i >> pdbs.txt; done
cp pdbs.txt $work_dir && cd $work_dir
```
建立segment文件
```
# strict_dssp_changes这个不加会报错，据说是已知bug，一年了都没修复...
segment_file_generator.linuxclangrelease \
-ignore_unrecognized_res \
-pdb_list_file pdbs.txt \
-motif_file motifs.txt \
-strict_dssp_changes false
```
存在问题

* 并未找到strict_dssp_changes
* 不加strict_dssp_changes 程序也没有报错
执行命令后会得到一个segment文件


执行检查命令后的界面

```
mpirun -np 2 edge_file_generator.linuxclangrelease -sewing:model_file_name $*.segments -edge_file_name $*.edges

edge_file_generator.linuxclangrelease -sewing:smotifs_H_5_20_L_1_3_E_3_10_L_1_3_H_5_20.segments -test1.edges
edge_file_generator.linuxgccrelease -sewing:smotifs_H_5_20_L_1_3_E_3_10_L_1_3_H_5_20.segment $*.segments

edge_file_generator.linuxgccrelease -sewing:smotifs_H_5_20_L_1_3_E_3_10_L_1_3_H_5_20$.segments -test1$.edges
```

![image](https://user-images.githubusercontent.com/64938817/166611529-1c041e6c-c7f0-43d4-9717-6e7bcd565ede.png)


