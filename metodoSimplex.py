import re
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from Tabla  import Tabla
from especiales import CEspeciales
from Matriz_sig import Matriz

class Main:
    def __init__(self):
        self.window = tk.Tk()
        self.ventana()
        self.numvariables = None
        self.numvarestricciones = None

    def userText(self,even):
        self.numvariables.delete(0, tk.END)
        self.numvariables.config()

    def userText1(self, even):
        self.numvarestricciones.delete(0, tk.END)
        self.numvarestricciones.config()

    def ventana(self):
        self.window.title("Método Simplex")
        self.window.resizable(0,0)  #No redimension
        self.window.iconbitmap("logo.ico")  # Logo
        inicio = tk.Frame() #el frame
        inicio.pack(fill="both", expand="true") #adaptarse
        inicio.config(width = "500", height = "500")

        #numero de variables
        tk.Label(inicio,text="Cantidad de variables: ", font = ("Times New Roman",18)).place(x=10, y = 10)
        self.numvariables = tk.Entry(inicio,font = ("Times New Roman",18), justify = tk.CENTER, width = 10, borderwidth=5)
        self.numvariables.place(x=300, y = 10)
        self.numvariables.insert(0,"Digite")
        self.numvariables.bind("<Button>",self.userText)

        #numero de restricciones
        tk.Label(inicio, text="Cantidad de restricciones: ", font=("Times New Roman", 18)).place(x=10, y=80)
        self.numvarestricciones = tk.Entry(inicio,font = ("Times New Roman",18),justify = tk.CENTER, width = 10, borderwidth=5)
        self.numvarestricciones.place(x=300, y=80)
        self.numvarestricciones.insert(0, "Digite")
        self.numvarestricciones.bind("<Button>",self.userText1)

        #Boton
        tk.Button(inicio,text="Continuar", font=("Times New Roman", 19), cursor = "hand2", command=self.validar).place(x=200,y=200)

        self.window.mainloop()

    def validar(self):
        estructuraentero = re.compile('^\d{1,2}$')
        if (re.search(estructuraentero, self.numvarestricciones.get()) is None) or (re.search(estructuraentero, self.numvariables.get()) is None):
            messagebox.showwarning("Cuidado", "Ingrese maximo 2 numeros entero")
        else:
            rest = self.numvariables.get()
            var = self.numvarestricciones.get()
            self.window.destroy()
            Pregunta(rest,var)

class Pregunta:
    def __init__(self,MaxVar,MaxRest):
        self.MaxVar = MaxVar
        self.MaxRest = MaxRest
        self.numvar = []
        self.numrest = []
        self.window = Tk()
        self.ventana()
        self.inicio = None

    def ventana(self):
        self.window.title("Método Simplex")
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.iconbitmap("logo.ico")  # Logo
        scrollbar = Scrollbar(self.window, orient="horizontal")
        scrollbar2 = Scrollbar(self.window)
        c = Canvas(self.window,xscrollcommand=scrollbar.set,yscrollcommand=scrollbar2.set, width = "1000", height = "768")
        scrollbar.config(command=c.xview)
        scrollbar2.config(command=c.yview)
        scrollbar2.pack(side=RIGHT,fill=Y)
        scrollbar.pack(side=BOTTOM, fill=X)
        self.inicio = Frame(c) #el frame
        self.inicio.columnconfigure(0, weight=1)
        self.inicio.rowconfigure(0, weight=1)
        c.pack(side="left", fill="both", expand=True)
        c.create_window(0, 0, window=self.inicio, anchor="nw")


        #Maximizar o min
        labelF = Label(self.inicio, text="Función:", font=("Times New Roman", 18))
        labelF.grid(row=0,column=0,pady=30)

        funcion = ttk.Combobox(self.inicio,state="readonly", width = 5, values=["Max z"],font = ("Times New Roman",18))
        funcion.set("Max z")
        funcion.grid(row=1, column=0)

        Label(self.inicio, text="=", font=("Times New Roman", 18)).grid(row=1, column=1)

        for i in range(int(self.MaxVar)):
            self.crearT(i)
            if i == 0: texto = "X"+str(i+1)
            else: texto += ",X"+str(i+1)
        Label(self.inicio, text=texto+"≥0", font=("Times New Roman", 18)).grid(row=int(self.MaxRest)+5,column=0,pady=30)

        Label(self.inicio, text="Restricciones:", font=("Times New Roman", 18)).grid(row=2,column=0,pady=30,padx=20)

        desig = []
        result = []
        for i in range(int(self.MaxRest)):
            for j in range(int(self.MaxVar)):
                self.crearR(i,j)
            desig.append(ttk.Combobox(self.inicio,state="readonly", width = 2, values=["≤"],font = ("Times New Roman",18)))
            desig[i].set("≤")
            desig[i].grid(row=3+i, column = int(self.MaxVar)*4,padx=20)
            result.append(Entry(self.inicio, font=("Times New Roman", 18),justify=CENTER, width=10, borderwidth=5))
            result[i].grid(row=3+i, column = int(self.MaxVar)*5,padx=20)

        self.window.update()
        c.config(scrollregion=c.bbox("all"))

        boton = Button(self.inicio, text="Continuar",font=("Times New Roman", 19),cursor="hand2", command= lambda : self.pasar(funcion.get(), desig, result))
        boton.grid(row=int(self.MaxRest) + 6, column=1)

        boton2 = Button(self.inicio, text="Inicio", font=("Times New Roman", 19),cursor="hand2", command=lambda: self.inicio1())
        boton2.grid(pady=30)

        self.window.mainloop()


    def inicio1(self):
        self.window.destroy()
        Main()

    def pasar(self,funcion,desig1,result):
        numvar = []
        numrest = []
        desig = []
        result1 = []
        for i in range(len(self.numvar)):
            numvar.append(self.numvar[i].get())

        for i in range(int(self.MaxRest)):
            numrest.append([])
            for j in range(int(self.MaxVar)):
                numrest[i].append(self.numrest[i][j].get())

        for i in range(len(desig1)):
            desig.append(desig1[i].get())

        for i in range(len(result)):
            result1.append(result[i].get())
        self.window.destroy()
        Resolver(funcion, numvar, numrest, desig, result1)
#---------------------------------------------
    def crearT(self,i):
        if(i==0):
            self.numvar.append(Entry(self.inicio, font=("Times New Roman", 18), justify=CENTER, width=10, borderwidth=5))
            self.numvar[i].grid(row=1, column=2)
            Label(self.inicio, text="X"+str(i+1), font=("Times New Roman", 18)).grid(row=1, column=3)
        else:
            Label(self.inicio, text="+", font=("Times New Roman", 18)).grid(row=1, column=i*3+1)
            self.numvar.append(Entry(self.inicio, font=("Times New Roman", 18),justify=CENTER, width=10, borderwidth=5))
            self.numvar[i].grid(row=1, column=i*3+2)
            Label(self.inicio, text="X" + str(i+1), font=("Times New Roman", 18)).grid(row=1, column=i*3+3)

    def crearR(self, i,j):
        self.numrest.append([])
        if(j==0):
            self.numrest[i].append(Entry(self.inicio, font=("Times New Roman", 18), justify=CENTER, width=10,borderwidth=5))
            self.numrest[i][j].grid(row=3+i, column=2, pady = 10)
            Label(self.inicio, text="X" + str(j + 1), font=("Times New Roman", 18)).grid(row=3+i, column=3)
        else:
            Label(self.inicio, text="+", font=("Times New Roman", 18)).grid(row=3+i, column=j*3+1)
            self.numrest[i].append(Entry(self.inicio, font=("Times New Roman", 18),justify=CENTER, width=10, borderwidth=5))
            self.numrest[i][j].grid(row=3+i,column=j*3+2)
            Label(self.inicio, text="X" + str(j + 1), font=("Times New Roman", 18)).grid(row=3+i, column=j*3+3)


class Resolver:
    def __init__(self,funcion,variables,restricciones,desig,result):
        self.funcion = funcion
        self.variables = variables
        self.restricciones = restricciones
        self.desig = desig
        self.result = result
        self.window = Tk()
        self.matriz = []
        self.degenerado = []
        self.bandera = False
        self.bandera1 = False
        self.count = 0
        self.empezar()
        self.ventana()
        self.boton = None
        self.inicio = None
        self.pivote = None

    def mostrar(self):
        print("Función: ",self.funcion,"\n\n")

        for i in range(len(self.variables)):
            print("X%d="%i+str(self.variables[i])+"\t\t",end="")

        print("\n")
        for i in range(len(self.restricciones)):
            print("Restricción %d" % (i+1))
            for j in range(len(self.restricciones[i])):
                print("X%d=" % (j) + str(self.restricciones[i][j])+"\t\t",end="")
            print("\n")

        for i in range(len(self.desig)):
            print("Desigualdad %d" % i+str(self.desig[i])+"\t",end="")
        print("\n")

        for i in range(len(self.result)):
            print("Resultado %d" % i+str(self.result[i])+"\t",end="")
        print("\n")

    def ventana(self):
        self.window.title("Método Simplex")
        self.window.iconbitmap("logo.ico")  # Logo
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        scrollbar = Scrollbar(self.window, orient="horizontal")
        scrollbar2 = Scrollbar(self.window)
        c = Canvas(self.window, xscrollcommand=scrollbar.set, yscrollcommand=scrollbar2.set, width="1000",height="768")
        scrollbar.config(command=c.xview)
        scrollbar2.config(command=c.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)
        scrollbar.pack(side=BOTTOM, fill=X)
        self.inicio = Frame(c) #el frame
        self.inicio.columnconfigure(0, weight=1)
        self.inicio.rowconfigure(0, weight=1)
        c.pack(side="left", fill="both", expand=True)
        c.create_window(0, 0, window=self.inicio, anchor="nw")



        Label(self.inicio, width="4", height="2",font=("Times New Roman", 19)).grid(row=0, column=0, pady=50,padx=50)

        self.crearMatriz()

        self.boton = Button(self.inicio, text="Continuar", font=("Times New Roman", 19), cursor="hand2", command=lambda: self.obtenerPivote())
        self.boton.grid()

        self.boton2 = Button(self.inicio, text="Inicio", font=("Times New Roman", 19),cursor="hand2", command=lambda: self.inicio1())
        self.boton2.grid(pady=30)

        self.window.update()
        c.config(scrollregion=c.bbox("all"))
        self.window.mainloop()
    def inicio1(self):
        self.window.destroy()
        Main()

    def empezar(self):
        matriz1 = Tabla(self.funcion, self.variables, self.restricciones, self.desig, self.result)
        self.matriz = matriz1.matrizlol()

    def crearMatriz(self):
        label = []
        for i in range(4 + len(self.result)):
            label.append([])
            for j in range(len(self.matriz[0])):
                if self.matriz[i][j] == "":
                    label[i].append(Label(self.inicio, width="6", height="2", font=("Times New Roman", 14),borderwidth=2, relief="solid"))
                    label[i][j].grid(row=i + 1, column=j + 1)
                else:
                    label[i].append(Label(self.inicio, text=self.matriz[i][j], width="6", height="2", font=("Times New Roman", 14), borderwidth=2, relief="solid"))
                    label[i][j].grid(row=i + 1, column=j + 1)

        pivote = CEspeciales(self.matriz, self.funcion)
        pivote.pivoteE()
        pivote.pivoteS()
        self.pivote = pivote.pivotefc
        if (pivote.nacotada):
            self.bandera1 = True
            self.boton.config(state='disabled')


        if pivote.degenerado:
            self.bandera = True


        if pivote.solucion:
            self.bandera = False
            self.boton.config(state = 'disabled')
            a = str(self.matriz[len(self.matriz)-2][2])
            mult = False
            si = False
            if(a.find("M")==-1):
                Label(self.inicio, text="Solución = "+str(self.matriz[len(self.matriz)-2][2]), font=("Times New Roman", 19)).grid(columnspan=3,row = 0 , column=1)
            else:
                messagebox.showwarning("Advertencia", "Problema no acotado hay variables artificiales en la solucion")
            for i in range(len(self.variables)):
                for j in range(2,len(self.matriz)-2):
                    if self.matriz[j][1].count("X"+str(i+1)) > 0:
                        Label(self.inicio, text="X%d = "%(i+1) + str(self.matriz[j][2]),font=("Times New Roman", 19)).grid(columnspan=3, row=0, column=3+i*2)
                        si = True
                        break
                if si == False:
                    Label(self.inicio, text="X%d = 0"%(i+1),font=("Times New Roman", 19)).grid(columnspan=3, row=0,column=3+i*2)
            for i in range(len(self.variables)):
                for j in range(2,len(self.matriz)-2):
                    if self.matriz[j][1].count("X"+str(i+1)) > 0:
                        mult = True
                if mult == False: break
            if(mult==False and self.bandera1 == False):
                messagebox.showwarning("Advertencia", "Es una solución optima multiple")

        if (pivote.abierto):
            self.boton.config(state='disabled')
        else:
            for i in range(len(self.matriz[0])):
                label[pivote.pivotefc[1]][i].config(bg="#ffff00")
            for i in range(len(self.matriz)):
                label[i][pivote.pivotefc[0]].config(bg="#ffff00")
            label[pivote.pivotefc[1]][pivote.pivotefc[0]].config(bg="#ffA500")

        if self.bandera:
            degenerado = []
            for i in range(len(self.matriz)):
                degenerado.append(str(self.matriz[i][2]))
            if(degenerado == self.degenerado):
                self.count += 1
                if(self.count == 3):
                    self.boton.config(state='disabled')
                    messagebox.showwarning("Advertencia", "Es un problema con ciclajes")
                    Label(self.inicio, text="Solución = " + str(self.matriz[len(self.matriz) - 2][2]),font=("Comic Sans MS", 19)).grid(columnspan=3, row=0, column=1)
            self.degenerado = degenerado

    def obtenerPivote(self):
        matriz = Matriz(self.matriz,self.pivote)
        self.matriz = matriz.convinar()
        self.crearMatriz()

if __name__ == '__main__':
    aplicacion = Main()