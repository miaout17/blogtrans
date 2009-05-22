from distutils.core import setup
import py2exe

setup(
    data_files = ["LICENSE"],
    console=["blogtrans.py"], 
    options = { "py2exe": {"includes" : ["_strptime"] } }
)
