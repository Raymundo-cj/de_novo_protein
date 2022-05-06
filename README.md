# de_novo_protein
This is a notebook about learning rosetta.

rosetta路径
```
/public3/home/pg3152/zzl/zzl_softwares
```

### 1.建立segment库

```
H 5 20, L 1 3, E 3 10, L 1 3, H 5 20
```

参数解释：

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
segment_file_generator.linuxgccrelease \
-ignore_unrecognized_res \
-pdb_list_file pdbs.txt \
-motif_file motifs.txt \
-strict_dssp_changes false
```
存在问题

* 并未找到strict_dssp_changes
* 不加strict_dssp_changes 程序也没有报错
执行命令后会得到一个segment文件
segment_file_generator.default.linuxgccrelease -database ~/public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/database/ -ignore_unrecognized_res -pdb_list_file pdbs.txt -motif_file motifs.txt

检查命令

```
edge_file_generator.default.linuxgccrelease -sewing:smotifs_H_5_20_L_1_3_E_3_10_L_1_3_H_5_20.segments tev1.edges
```

![image](https://user-images.githubusercontent.com/64938817/166854018-a1caa82c-cbbd-4629-9cb8-72525d4ca728.png)


正确的命令
```
edge_file_generator.linuxclangrelease -sewing:model_file_name tev1.segments --edge_file_name tev1.edges
```
原因是命令写错了┭┮﹏┭┮

基本格式：
* `-model_file_name` : Path to the segment file
* `-edge_file_name`: Path to save generated edge file

可选格式：
* `-max_clash_score` : Maximum number of clashed atoms to allow during alignment
* 冲撞阈值，超出该阈值后，认为两个segment文件之间的匹配度较差
* `-min_hash_score` : The minimum number of aligned atoms to determine whether two segments are structurally compatible
* 打分阈值，打分超出这个值后，认为是匹配良好的（推荐设置为20）
* `-boxes_per_dimension` : The number of bins to consider in the geometric hash. 3 and 5 are the only acceptable values
* 在几何散列中要考虑的箱子数，只能设置3或5
* `-hash_opposite_termini` : Hashing will occur between segments with opposite termini (N to C or C to N )
* 反向组装顺序，N->C端为默认顺序，设置后，从C->N端装配。可以产生更加多样化的Segments

example
```
edge_file_generator.default.xxx -model_file_name smotifs_H_1_100_L_1_100_H_1_100.segments -edge_file_name smotifs_H_1_100_L_1_100_H_1_100.edges -boxes_per_dimension 3
```
### 运行组装
1.先建立一个flag文件

```
-ignore_unrecognized_res
-detect_disulf false
-mh
    -score
        -use_ss1 true
        -use_ss2 true
        -use_aa1 false
        -use_aa2 false
    -path
        -motifs /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/database/additional_protocol_data/sewing/xsmax_bb_ss_AILV_resl0.8_msc0.3/xsmax_bb_ss_AILV_resl0.8_msc0.3.rpm.bin.gz
        -scores_BB_BB /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/database/additional_protocol_data/sewing/xsmax_bb_ss_AILV_resl0.8_msc0.3
        -gen_reverse_motifs_on_load false
```
flag文件建立好之后需要一个pdb文件，这里复制了一个1LN0.pdb文件在这里

关于为什么用pdb文件，官方网站的解释是：一定要有，但是执行的过程中是可以忽略的。
之后执行如下的命令，实现拼接
```
rosetta_scripts.linuxgccrelease -s 1LN0.pdb -parser:protocol RosettaScript.xml @flag -nstruct 4 -out:path:pdb output
```
但是执行之后出现了报错

![image](https://user-images.githubusercontent.com/64938817/166937654-50a91c1d-8db3-4679-b0e5-11046131a971.png)
选项文件中的注释必须以'#'开头，选项必须以'-'行开头 ？？？不是很懂
应该是flag文件出现了问题。进行了如下修改

```
-mh:ignore_unrecognized_res
-mh:detect_disulf false
-mh:score:use_ss1 true
-mh:score:use_ss2 true
-mh:score:use_aa1 false
-mh:score:use_aa2 false
-mh:path:motifs /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/database/additional_protocol_data/sewing/xsmax_bb_ss_AILV_resl0.8_msc0.3/xsmax_bb_ss_AILV_resl0.8_msc0.3.rpm.bin.gz
-mh:path:scores_BB_BB 
/public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/database/additional_protocol_data/sewing/xsmax_bb_ss_AILV_resl0.8_msc0.3
-mh:gen_reverse_motifs_on_load false
```
出现了下面的错误：

![image](https://user-images.githubusercontent.com/64938817/166940934-f5cc6cc9-00cc-4f68-9030-32b28800f782.png)
在说mh用法错误

修改之后可以运行

出现下面的报错：

![image](https://user-images.githubusercontent.com/64938817/166944438-721d7ce8-f9f1-486f-9040-967d2f91daeb.png)
![image](https://user-images.githubusercontent.com/64938817/166944511-b559760e-30b9-480c-9aad-f8f328343ebc.png)


记得将命令写成脚本，在后台执行
```
sbatch run_sewing.sh
```
命令运行后得到四个pdb文件：
在pymol中查看发现4个结构是一样的

![image](https://user-images.githubusercontent.com/64938817/167051399-c2983e1e-0c95-4aab-b7ec-ea25924c62bb.png)

不懂什么原因
