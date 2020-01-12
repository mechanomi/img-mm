# Source this file using `. activate.sh` instead of executing it

VENV=.venv
BIN=$VENV/bin

python3.7 -m venv $VENV
. $BIN/activate

$BIN/python -m pip install --upgrade pip
$BIN/python -m pip install --upgrade -r requirements.txt
