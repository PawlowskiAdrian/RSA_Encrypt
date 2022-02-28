# Issues with Crypto packages:
## FIX
The function time.clock() has been removed, after having been deprecated since Python 3.3: use time.perf_counter() or time.process_time() instead, depending on your requirements, to have well-defined behavior. (Contributed by Matthias Bussonnier in bpo-36895.)

## OR Instal another Package
```
pip3 uninstall PyCrypto
pip3 install -U PyCryptodome
```