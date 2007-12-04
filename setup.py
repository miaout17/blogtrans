from distutils.core import setup
import py2exe

setup(
  console=["blogtrans.py"], 
  options = { "py2exe": {"includes" : ["_strptime"] } }
)
