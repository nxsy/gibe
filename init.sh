#!/bin/sh

set -e

cd `dirname $0`
if [ ! -d .env ]; then
    python scripts/virtualenv.py --no-site-packages .env
fi
if [ ! -e activate ]; then
    ln -s .env/bin/activate activate
fi

source activate

pip install -r packages.txt
