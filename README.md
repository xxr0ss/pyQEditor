# pyQEditor

## Build
### Requirements
* Python3.8 +
* PySide6

### Steps
* Install required python and PySide6

* Compile ui fiels

use `pyside6-uic`(a tool provided by pyside6) to compile `.ui` files to `.py` files, for example: 
```bash
pyside6-uic -o ui/ui_main.py ui/main.ui
```

or use devtools to compile
```bash
python tools.py uic -a
```
