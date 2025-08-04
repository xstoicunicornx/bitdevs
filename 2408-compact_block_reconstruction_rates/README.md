### command to check compact block reconstruction rate

```
grep 'Successfully reconstructed' ./debug.log | cut -d' ' -f 23 | tail -n 1024 | awk '{if ($1==0){aa+=1}} END {print aa/NR*100}'
```

### command to get compact block reconstruction stats

```
python compact_block_debug_parser.py
```

### running python notebook

```
pip install -r requirements.txt
jupyter lab  # or jupyter notebook
```

