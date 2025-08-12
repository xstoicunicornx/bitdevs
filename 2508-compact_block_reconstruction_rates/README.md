### command to check compact block reconstruction rate for last 1024 blocks

```
grep 'Successfully reconstructed' ./debug.log | cut -d' ' -f 23 | tail -n 1024 | awk '{if ($1==0){aa+=1}} END {print aa/NR*100}'
```

### command to get compact block reconstruction stats for last 50 blocks

```
pip install -r requirements.txt
python compact_block_debug_parser.py
```

### running python notebook

if running in virtual env or different python version than system default
```
pip install ipykernel
```

then
```
jupyter lab
```
or
```
jupyter notebook
```

