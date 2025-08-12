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

if using virtual env (otherwise skip)
```
python -m venv .venv && source .venv/bin/activate
pip install jupyterlab
pip install ipykernel
python -m ipykernel install --user --name=venv
```

then
```
jupyter lab
```

open the `compact_block_reconstructions.ipynb` jupyter notebook (if using virtual env make sure to select the `venv` kernel that was created with the commands above)
