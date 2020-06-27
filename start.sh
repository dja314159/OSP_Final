#!/bin/bash

cat << EOF > pyscript.py
#!/usr/bin/python3
import nltk
nltk.download('punkt')

EOF

chmod 755 pyscript.py
python3 ./pyscript.py
rm ./pyscript.py

flask run

