# Dimv

An extension of [gdown](https://pypi.org/project/gdown/) library, meant to simplify and extend the use of this incredible library

### Features:

+ retrieve list of files (or file) in drive directory
+ download files individually or multiple at the time
+ Automatic folder and file naming if downloading folders

+ `shared` feature still not in place

### Usage:

Install `Dimv` on your system with pip:

```
pip install Dimv
```

### Example:

```python
import Dimv as dimv

folder = 'https://drive.google.com/drive/folders/1e0GsZ6_RbG8su43MfiOx4pURIoOqEqaL'
id = '1mJ-jfHNbXjjhCWIzaIW3ZvRaXw9VohpL'

dimv.find_files(folder, quiet = True)

dimv.find_file(id, folder, quiet = False)

output = 'test/test.txt'
dimv.download(id, output, shared = True, quiet = False)

dimv.download_file(id, folder, output = 'test/test', quiet = False)

dimv.download_files(folder, output = '', shared = True, quiet = False)
```