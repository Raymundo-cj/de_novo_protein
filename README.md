# de_novo_protein
This is a notebook about learning rosetta.

## 1.建立segment库

```
H 5 20, L 1 3, E 3 10, L 1 3, H 5 20
```

生成数据库
```
cd $top8000_chains_70
for i in $(ls $(pwd)); do python /public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/tools/fragment_tools/pdb2vall/pdb_scripts/clean_pdb.py $i; rm -rf $i; done

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

rosetta路径
```
/public3/home/pg3152/zzl/zzl_softwares
```

```

/public3/home/pg3152/zzl/zzl_softwares/rosetta_src_2021.16.61629_bundle/main/tools/fragment_tools/pdb2vall/pdb_scripts/clean_pdb.py

```



执行检查命令后的界面
![image](https://user-images.githubusercontent.com/64938817/166611529-1c041e6c-c7f0-43d4-9717-6e7bcd565ede.png)

