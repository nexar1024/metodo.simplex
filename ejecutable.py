from cx_Freeze import setup, Executable
import tkinter
import sympy
import fractions

setup( name = "Simplex",
           version = "1.0" ,
           options = {'build_exe': {'packages':['tkinter','sympy','fractions'],'include_files':['logo.ico','especiales.py','Matriz_sig.py','Tabla.py']}},
           description = "Resolver" ,
           executables = [Executable("metodoSimplex.py")] , )