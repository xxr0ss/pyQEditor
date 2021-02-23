# PyQEditor

A Code Editor based on PySide6

## Build
### Requirements
* Python3.9+
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

* Compile qrc files
    use `pyside6-rcc`
    ```bash
    pyside6-rcc -o QEditor/rc_icons.py QEditor/icons.qrc
    ```

    or you can find devtools too in tools.py

* Run PyQEditor
    ```bash
    cd src # working directory is the src
    python main.py
    ```
