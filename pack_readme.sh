B64=`rdiscount < README.md | base64`
FN='blogtrans/readme.py'

cat <<PYPY > "$FN"
import base64
html = base64.b64decode("$B64").decode("UTF-8")
PYPY
