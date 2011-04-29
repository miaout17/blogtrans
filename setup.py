from distutils.core import setup
import py2exe

import blogtrans

setup(
    data_files = ["README", "LICENSE"],
    console=["blogtrans.py"],
    options = {
        "py2exe": {
            "includes" : ["_strptime"],
            "dist_dir": "dist/blogtrans-" + blogtrans.VERSION
         },
    }
)
