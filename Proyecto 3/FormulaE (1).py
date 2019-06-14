"""
José Fabián Mendoza Mata
Fátima Leiva Chinchila
"""

from tkinter import *
from tkinter import messagebox
import os, sys
import operator
import time
import threading
import mttkinter
import random
from WiFiClient import NodeMCU

# Segundo intento

win = Tk()
win.geometry("1000x700")
win.title("Fórmula TEC")

myCar = NodeMCU()
myCar.start()

pil = open("Pilotos/Nombres_Pilotos.txt", "r")      # Abro un archivo que contiene los nombres de los archivos de los pilotos 
pilotos = pil.readline()
pilotos = pilotos.split(",")        # Convierto el string en una lista con cada dato del piloto
pilotos = pilotos[0:-1]
pil.close()

""" Función para destruir el canvas actual
    E: recibe el canvas que se desea eliminar(pantalla) y el canvas que se abre(destino)
    S: el canvas destino
    R: que se ingresen canvas que estén creados
"""
def changeWin(canvas, destiny):
    canvas.destroy()
    destiny()

"""Función showMainwin
    E: esta función no contiene entradas debido a que todo se crea dentro de la funcion
    S: crea el canvas(ventana) que pertenece a la pantalla de inicio
    R: como no tiene entradas, no contiene restricciones
    """
# ------------------ Se cargan imágenes ------------------------------- #

img = PhotoImage(file = r"Imagenes Test Drive/fondo_dia.png")

flechar = PhotoImage(file = "Imagenes Test Drive/flecha_derecha.png")
flechar = flechar.subsample(x=4, y=4)

flechau = PhotoImage(file = r"Imagenes Test Drive/flecha_arriba.png")
flechau = flechau.subsample(x = 4, y = 4)

flechad = PhotoImage(file = r"Imagenes Test Drive/flecha_abajo.png")
flechad = flechad.subsample(x = 4, y = 4)

flechal = PhotoImage(file = r"Imagenes Test Drive/flecha_izquierda.png")
flechal = flechal.subsample(x = 4, y = 4)

fondo_pilotos = PhotoImage(file = r"Imagenes Pilotos/fondo_pilotos.png")
fondo_tabla = PhotoImage(file = r"Imagenes Pilotos/fondo_tabla.png")

fondo1= PhotoImage(file= 'fondo.png')
fondo2= PhotoImage(file= 'carr.png')

fond= PhotoImage(file='wall.png')

fondoAutos = PhotoImage(file = "carros.png")

def showMainwin():

    data = getDataDefault()

    nombre = StringVar()
    nombre.set(data[0])

    logo = StringVar()
    logo.set(data[1])

    ubicacion = StringVar()
    ubicacion.set(data[2])

    patrocinadores = StringVar()
    patrocinadores.set(data[3])

    opc = StringVar()
    opc.set("Elija un piloto")
    
    #Canvas y rectángulos en la pantalla de inicio
    canvas = Canvas(win, height = 700, width = 1000) #Crea el canvas
    canvas.place(x = 0, y = 0)
    fondo= canvas.create_image(0, 0, image= fond, anchor= NW) #fondo
    rectangulo= canvas.create_rectangle(0, 40, 1000, 90, fill= "#191D58")
    rectan= canvas.create_rectangle(750, 140, 950, 570, fill= "#191D58")


    escLabel = Label(canvas, text = "Escudería:", font= ('BankGothic Lt Bt', 18), bg="#191D58", fg= 'white')
    escLabel.place(x = 320, y = 53)

    escEntry = Entry(canvas, font= ('courier', 15))
    escEntry.place(x = 470, y = 55)

    #Texto que cambia al cambiar la escudería en el canvas de Inicio

    nombreLabel = Label(canvas, text = "Nombre de la escudería:", bg= 'black', fg='white', font= ('courier', 13))
    nombreLabel.place(x = 150, y = 240)

    varnombreLabel = Label(canvas, textvariable = nombre, bg= 'black', fg= 'white', font= ('courier', 13))
    varnombreLabel.place(x = 590, y = 240)

    logoLabel = Label(canvas, text = "Logo: ",  bg= 'black', fg='white', font= ('courier', 13))
    logoLabel.place(x = 150, y = 300)

    varlogoLabel = Label(canvas, textvariable = logo, bg= 'black', fg= 'white', font= ('courier', 13))
    varlogoLabel.place(x = 590, y = 300)

    ubiLabel = Label(canvas, text = "Ubicación Geográfica: ",  bg= 'black', fg='white', font= ('courier', 13))
    ubiLabel.place(x = 150, y = 360)

    varubiLabel = Label(canvas, textvariable = ubicacion, bg= 'black', fg= 'white', font= ('courier', 13))
    varubiLabel.place(x = 590, y = 360)

    sponsorLabel = Label(canvas, text = "Patrocinadores: ",  bg= 'black', fg='white', font= ('courier', 13))
    sponsorLabel.place(x = 150, y = 420)

    varsponsorLabel = Label(canvas, textvariable = patrocinadores, bg= 'black', fg= 'white', font= ('courier', 13))
    varsponsorLabel.place(x = 590, y = 420)

    disponibleLabel = Label(canvas, text= 'Pilotos disponibles: ', bg= 'black', fg='white', font= ('courier', 13))
    disponibleLabel.place(x= 150, y = 480)

    #Opcion para el cambio de escudería

    changeEscBut = Button(canvas,font= ('Harlow Solid Italic', 11), text = "Cambiar escudería", command = lambda:getDataEsc(escEntry.get(), nombre, logo, ubicacion, patrocinadores), relief="raised", borderwidth=8, bg= "#101669", fg= 'white')
    changeEscBut.place(x = 140, y = 43)

    # Menú de opciones

    opciones = getNombresPilotos()

    opcMenu = OptionMenu(canvas, opc, *opciones)
    opcMenu.place(x = 400, y = 480)

    #Opciones para ir a diferentes ventanas

    newEscBut = Button(canvas,font= ('Harlow Solid Italic', 11), text = "Nueva Escudería", command = lambda:changeWin(canvas, showNewEscWin), relief="groove", borderwidth=8, bg= '#101669', fg= 'white')
    newEscBut.place(x = 800, y = 180)

    aboutBut= Button(canvas, text = 'Sobre nosotros...',font= ('Harlow Solid Italic', 11), command= lambda: changeWin(canvas, showAbout), relief="groove", borderwidth=8, bg= '#101669', fg= 'white')
    aboutBut.place(x=800, y= 470)

    showBut= Button(canvas, text= 'Ver carrocería',font= ('Harlow Solid Italic', 11), command= lambda: changeWin(canvas, AutosShow), bg= '#101669', relief="groove", fg='white', borderwidth=8)
    showBut.place(x=800, y= 250)

    testBut= Button(canvas, text= 'Test Drive',font= ('Harlow Solid Italic', 11), command= lambda: changeWin(canvas, testWin), bg= '#101669', relief="groove", fg='white', borderwidth=8)
    testBut.place(x=800, y= 400)

    pilotoBoton= Button(canvas, text= 'Mostrar pilotos',font= ('Harlow Solid Italic', 11), command= lambda: showTablePilots(), bg= '#101669', relief="groove", fg='white', borderwidth=8)
    pilotoBoton.place(x=800, y= 330)
    


"""Función para cambiar las escuderías
    E: las entradas el name de la escudería a la que se quiere cambiar
    S: cambio de escudería en la interfaz
    R: debe ser un nombre de escudería válido o ya existente
"""
def getDataEsc(name, nombre, logo, ubicacion, patrocinadores):

    try:
        file = open("Escuderias/" + name + ".txt","r")
        data = file.readline()
        file.close()
        data = data.split(",")
        nombre.set(data[0])
        logo.set(data[1])
        ubicacion.set(data[2])
        patrocinadores.set(data[3])
    except:
        messagebox.showerror("Error", "La escudería especificada no existe")

#Tiene la misma funcionalidad que la anterior solo que esta obtiene la escudería por default que va a aparecer en la ventana al ingresar
def getDataDefault():

    file = open("Escuderias/TEC.txt", "r")
    data = file.readline()
    file.close()
    data = data.split(",")
    return data


""" Función para crear escuderías por medio de los archivos de texto
    E: entran los parametros (name, nombre, logo, ubicación, patrocinadores) de la escudería a crear
    S: creación de la escudería
    R: deben ser nombres válidos con una dirección de imagen válida
"""
def createNewEsc(nombre, logo, ubicacion, sponsors, entrys):

    archivo_esc = open("Escuderias/" + nombre + ".txt","w")     # Crear un archivo
    archivo_esc.write(nombre + "," +  logo + "," +  ubicacion + ","  +  sponsors)
    for x in entrys:            # Para reiniciar los entrys de la ventana
        x.delete(0, END)

    messagebox.showinfo("Guardar escudería","Se ha guardado la escudería satisfactoriamente")


""" Función para la ventana de creación de escuderías
    E: no tiene entradas pues todo se crea en el canvas
    S: aparece el canvas, y dentro de este se guardan las nuevas escuderías
    R: no presenta
"""

def showNewEscWin():

    #creación de canvas y rectángulos en la interfaz de escuderías
    canvas = Canvas(win, height = 700, width = 1000)
    canvas.place(x = 0, y = 0)
    fondo= canvas.create_image(0, 0, image= fondo1, anchor= NW) #fondo
    cuadro1= canvas.create_rectangle(100, 0, 900, 700, fill= 'brown4')
    cuadro2= canvas.create_rectangle(100,50,900, 650, fill= 'black')

    escLabel = Label(canvas, text = "Nombre escudería:", bg= 'black', fg= 'white', font= ('courier', 15))
    escLabel.place(x = 200, y = 120)

    escEntry = Entry(canvas, font= ('courier', 15))
    escEntry.place(x = 550, y = 120)

    logoLabel = Label(canvas, text = "Logo:", bg= 'black', fg= 'white', font= ('courier', 15))
    logoLabel.place(x = 200, y = 220)

    logoEntry = Entry(canvas, font= ('courier', 15))
    logoEntry.place(x = 550, y = 220)

    ubiLabel = Label(canvas, text = "Ubicación Geográfica:", bg= 'black', fg= 'white', font= ('courier', 15))
    ubiLabel.place(x = 200, y = 320)

    ubiEntry = Entry(canvas,font= ('courier', 15))
    ubiEntry.place(x = 550, y = 320)

    sponsorLabel = Label(canvas, text = "Patrocinadores:", bg= 'black', fg= 'white', font= ('courier', 15))
    sponsorLabel.place(x = 200, y = 420)

    sponsorEntry = Entry(canvas, font= ('courier', 15))
    sponsorEntry.place(x = 550, y = 420)

    pilLabel = Label(canvas, text = "Pilotos Disponibles:", bg= 'black', fg= 'white', font= ('courier', 15))
    pilLabel.place(x = 200, y = 520)

    ubiEntry = Entry(canvas, font= ('courier', 15))
    ubiEntry.place(x = 550, y = 520)

    iniBut = Button(canvas, text = "Regresar al menú principal", command = lambda:changeWin(canvas, showMainwin), relief="sunken", borderwidth=5, bg= 'brown4', fg= 'white')
    iniBut.place(x = 690, y = 600)

    createBut = Button(canvas, text = "Crear Escudería", command = lambda: createNewEsc(escEntry.get(), logoEntry.get(), ubiEntry.get(), sponsorEntry.get(),[escEntry,logoEntry,ubiEntry,sponsorEntry]), relief="raised", borderwidth=5, bg= 'brown4', fg= 'white')
    createBut.place(x = 350, y = 600)


"""Esta función es la encargada de la creación de la ventana de About, que muestra la información de los creadores de la interfaz
    E: sin entradas porque todo se creaa dentro del canvas al llamarla
    S: la creación de la ventana de About
    R: no presenta
"""
imgTEC= PhotoImage(file= 'tec.png')
Fabifoto= PhotoImage(file= 'fabi.png')
Fatifoto= PhotoImage(file= 'fati.png')
def showAbout():
    #canvas y rectángulos en la ventana
    canvas= Canvas(win, height=700, width= 1000, bg= 'DodgerBlue4')
    canvas.place(x=0, y=0)
    fondo= canvas.create_image(0,0, image= fondo1, anchor= NW)
    rect= canvas.create_rectangle(100,0,900,700, fill= 'white')
    rectangulo1= canvas.create_rectangle(200,180,400,210, fill='brown4')
    rectangulo2= canvas.create_rectangle(200,260,400,290, fill='brown4')
    rectangulo3= canvas.create_rectangle(200,340,400,370, fill='brown4')
    rectangulo4= canvas.create_rectangle(200,420,400,450, fill='brown4')
    rectangulo5= canvas.create_rectangle(200,500,400,530, fill='brown4')
    rectangulo6= canvas.create_rectangle(200,580,400,610, fill='brown4')
    rectangulo7= canvas.create_rectangle(500,190,850,480, fill='brown4')
    rectangulo8= canvas.create_rectangle(500,550,850,630, fill='brown4')

    tec= canvas.create_image(300,40, image= imgTEC, anchor= NW) #Logo isntitución

    fati= canvas.create_image(530, 230, image= Fatifoto, anchor= NW)
    fabi= canvas.create_image(530, 355, image= Fabifoto, anchor= NW)

    #Datos que van dentro de los cuadros en la info

    DatosLabel= Label(canvas, text= 'Datos de los autores', font= ('courier',12), bg= 'brown4', fg='white') ########
    DatosLabel.place(x= 550, y= 200)

    carrLabel= Label(canvas, text= 'Carrera', font= ('courier',9), bg= 'brown4', fg='white')
    carrLabel.place(x=215, y=185)
    carreraLabel= Label(canvas, text= 'Ingeniería en Computadores',  font= ('courier',9, 'bold'), fg= 'brown4', bg='white')
    carreraLabel.place(x=230, y=215)

    cursLabel= Label(canvas, text= 'Curso', font= ('courier',9), bg= 'brown4', fg='white')
    cursLabel.place(x=215, y=265)
    cursoLabel= Label(canvas, text= 'Taller a la programación', font= ('courier',9, 'bold'), fg= 'brown4', bg='white')
    cursoLabel.place(x=230, y=295)

    annoLabel= Label(canvas, text= 'Año', font= ('courier',9), bg= 'brown4', fg='white')
    annoLabel.place(x=215, y=345)
    anLabel= Label(canvas, text= 'Generación 2019', font= ('courier',9, 'bold'), fg= 'brown4', bg='white')
    anLabel.place(x=230, y= 375)

    profLabel= Label(canvas, text= 'Profesor: ', font= ('courier',9), bg= 'brown4', fg='white')
    profLabel.place(x=215, y=425)
    jefLabel= Label(canvas, text= 'Jeff Schmidth Peralta', font= ('courier',9, 'bold'), fg= 'brown4', bg='white')
    jefLabel.place(x=230, y=455)

    paisLabel= Label(canvas, text= 'Desarrollado en Costa Rica', font= ('courier',9), bg= 'brown4', fg='white')
    paisLabel.place(x= 210, y= 505)

    versLabel= Label(canvas, text= 'Versión', font= ('courier',9), bg= 'brown4', fg='white')
    versLabel.place(x= 215, y= 585)

    versLabel= Label(canvas, text= 'Python 3.7', font= ('courier',9,'bold'), bg= 'white', fg='brown4')
    versLabel.place(x= 232, y= 615)

    nombreFat= Label(canvas, text= 'Fátima Leiva Chinchilla', font= ('courier',9), bg= 'brown4', fg='white')
    nombreFat.place(x= 650, y= 235)

    carnetFat= Label(canvas, text= '2019 153 089', font= ('courier',9), bg= 'brown4', fg='white')
    carnetFat.place(x= 650, y= 265)

    nombreFab= Label(canvas, text= 'Fabián Mendoza Mata', font= ('courier',9), bg= 'brown4', fg='white')
    nombreFab.place(x= 650, y= 365)

    carnetFab= Label(canvas, text= '2018 319 699', font= ('courier',9), bg= 'brown4', fg='white')
    carnetFab.place(x= 650, y= 395)

    masinfoLabel= Label(canvas, text='El trabajo fue realizado con los módulos \n mttkinter y Tkinter.', font= ('courier',9), bg= 'brown4', fg='white')
    masinfoLabel.place(x=530, y=560)

    #Boton de retorno a inicio
    init= Button(canvas, command= lambda: changeWin(canvas, showMainwin), text= 'Volver a inicio', relief="raised", borderwidth=5, bg= 'brown4', fg= 'white')
    init.place(x=630, y= 597)
    

"""Esta función es la encargada de crear la ventana donde se muestran los automóviles
    E: sin entradas pues todo se crea dentro del canvas
    S: creación de la ventana de automóviles
    R: no presenta
"""
def AutosShow():
    canvas= Canvas(win, height= 700, width= 1000) #ventana

    presButton= Button(canvas, text= 'RGP')
    presButton.place(x=100, y=20)




def CrearAuto(marca,modelo, paisfabricacion, foto, anno, baterias, pilas, niveltension, estado, consumomotores, sensores, peso, eficiencia):
    archivo_esc = open("Autos/" + marca + ".txt","w")     # Crear un archivo
    archivo_esc.write(nombre + "," +  logo + "," +  ubicacion + ","  +  sponsors)
    for x in eficiencia:            # Para reiniciar los entrys de la ventana
        x.delete(0, END)



#======================================Función para crear un nuevo auto y guardarlo en archivos de texto===========================#

def AutosCreate():

    canvas= Canvas(win, height= 700, width= 1000, bg= '#060D5E') #ventana
    canvas.place(x=0, y=0)

    text1= Label(canvas, text= 'Marca del carro:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text1.place(x=150, y=70)
    marca= Entry(canvas)
    marca.place(x=150, y= 100)

    text2= Label(canvas, text= 'Modelo del carro:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text2.place(x=150, y=150)
    modelo= Entry(canvas)
    modelo.place(x=150, y= 180)

    text3= Label(canvas, text= 'País de fabricación:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text3.place(x=150, y=230)
    paisfabricacion= Entry(canvas)
    paisfabricacion.place(x= 150, y= 260)

    text4= Label(canvas, text= 'Foto:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text4.place(x=150, y=310)
    foto= Entry(canvas)
    foto.place(x=150, y= 340)

    text5= Label(canvas, text= 'Año de temporada:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text5.place(x=150, y=390)
    anno= Entry(canvas)
    anno.place(x=150, y= 420)

    text6= Label(canvas, text= 'Cantidad de baterías:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text6.place(x=150, y=470)
    baterias= Entry(canvas)
    baterias.place(x=150, y=500)

    text7= Label(canvas, text= 'Cantidad de pilas:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text7.place(x=150, y=550)
    pilas= Entry(canvas)
    pilas.place(x=150, y=580)

    text8= Label(canvas, text= 'Nivel de tensión:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text8.place(x=150, y=630)
    tension= Entry(canvas)
    tension.place(x=150, y= 660)

    text9= Label(canvas, text= 'Estado:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text9.place(x=500, y=70)
    estado= Entry(canvas)
    estado.place(x=500, y= 100)

    text10= Label(canvas, text= 'Consumo de motores:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text10.place(x=500, y=160)
    consumo= Entry(canvas)
    consumo.place(x= 500, y= 190)

    text11= Label(canvas, text= 'Sensores:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text11.place(x=500, y=240)
    sensor= Entry(canvas)
    sensor.place(x=500, y=270)

    text12= Label(canvas, text= 'Peso del carro/ kg:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text12.place(x=500, y=320)
    peso=Entry(canvas)
    peso.place(x=500, y=350)

    text13= Label(canvas, text= 'Eficiencia:', bg= '#060D5E', fg='white' , font= ('Chiller', 16))
    text13.place(x=500, y=400)
    eficiencia=Entry(canvas)
    eficiencia.place(x=500, y=430)

    crearButon= Button(canvas, bg='#070B39', font= 'Forte', fg='white', relief='groove', borderwidth=6, text= 'Crear Auto', command= lambda: CrearAuto(marca.get(), modelo.get(), paisfabricacion.get(), foto.get(), anno.get(), baterias.get(), pilas.get(), tension.get(), estado.get(), consumo.get(), sensor.get(), peso.get(), eficiencia.get(), [marca, modelo, paisfabricacion, foto, anno, baterias, pilas, tension, estado, consumo, sensor, peso, eficiencia])) 
    crearButon.place(x=520, y= 520)

    cerrarButon= Button(canvas, bg='#070B39', font= 'Forte', fg='white', relief='groove', borderwidth=6, text= 'Cerrar', command= lambda: changeWin(canvas, AutosShow))
    cerrarButon.place(x=800, y= 650)


#====================================Función para obtener el data de cada carro en un archivo de texto======================#
def getDataCar(name):

    file = open("Autos/" + name,"r")
    data = file.readline()
    file.close()
    data = data.split(",")
    return data



"""============================================================================================
________________Función para crear un auto e ingresarlo a un archivo de texto
E: todos los parámetros de un auto
S: creación del carro
R: deben ser los parámetros específicos de la función
"""

def CrearAuto(marca,modelo, paisfabricacion, foto, anno, baterias, pilas, tension, estado, consumo, sensor, peso, eficiencia, entrys):
    archivo_esc = open("Autos/" + marca + ".txt","w")     # Crear un archivo
    archivo_esc.write(marca + "," + modelo + "," + paisfabricacion + "," +  foto + ","  +  anno + ","  + baterias + ","  + pilas + ","  + tension + ","  + estado + ","  + consumo + ","  + sensor + ","  + peso + ","  + eficiencia)
    for x in entrys:            # Para reiniciar los entrys de la ventana
        x.delete(0, END)
    messagebox.showinfo('Auto nuevo', 'auto agregado con exito')



"""=================================================================================================
_________________Función para editar los datos de un archivo de texto
E: el carro que se desea editar, la posicion a cambiar, el canvas 
S:
R:
"""
def editar(car, posicion, canvas, i):
    edit= Canvas(canvas, width= 200, height= 200)
    edit.place(x=200, y=30)
    j=0
    var= 0 + j
    editarLabel= Label(edit, text= 'Ingrese elemento')
    editarLabel.place(x=30, y=5)
    if var != 0:
        edit.destroy() #destruir la ventana del canvas
    editEntry= Entry(edit)
    editEntry.place(x=15, y= 30)
    Boton=Button(edit, text= 'Actualizar', command= lambda: editar(car, posicion, canvas, 1))
    Boton.place(x=30, y= 50)
    if i > 0:
        if int(posicion) > 0 and int(posicion) < 14:
            car[int(posicion)]= str(editEntry.get())
            edit.destroy()
            messagebox.showinfo('Actualizado', 'La información ha sido actualizada')
            var= 1
            j= 1
                
        else:
            messagebox.showerror('Error', 'Error con la posicion igresada')
            edit.destroy()
        edit.destroy()
    else:
        i=0
    i = 0

#=====================================Función para editar los datos 2.0


def AutosShow():
    canvas= Canvas(win, width= 1000, height= 700)
    canvas.place(x=0, y=0)

    fondo= canvas.create_image(0,0, image= fondoAutos, anchor= NW)
    cuadrado= canvas.create_rectangle(0,20,1000,70, fill= '#13483b')

    carg= PhotoImage(file= "AutosFotos/" + 'Audi' + ".png")
    canvas.create_image(0,0, image= carg, anchor= NW)

    importante= os.listdir( 'Autos')
    carros= []
    posicion= 1
    while posicion < len(importante):
        carros.append(getDataCar(importante[posicion]))
        posicion += 1
                

    
    """=====================================================================================================
    Función de algoritmo de ordenamiento merge sort
    Esta función ordena los datos de los carros de forma ascendente o descendente de acuerdo a su eficiencia
    E: el modo ya sea ascendente, descendente o ninguno
    S: datos ordenados
    R: __ no contiene restricciones, no importa lo que se ingrese podría ir al else que acepta todo caso y solo retorna los datos sin alterarlos
    """

    def Ordenar(modo):
        cont=0
        i= 0 #es la posicion dentro de la lista, es cada carro dentro de la lista
        if modo== 'ascendente':
            while i < len(carros): 
                j = 1 + cont
                var= ''
                while j < len(carros):
                    if int(carros[i][12]) > int(carros[j][12]): #en caso de que la eficiencia del carro i sea mayor que la eficiencia del carro j
                        var= carros[i] #asigna una variable con el carro i
                        carros[i]= carros[j] #la posicion del carro i se intercambia con el carro j
                        carros[j]= var #la posicion en la que estaba el carro j ahora va a ser el carro i
                        j += 1
                    else:
                        j += 1 #en caso de que la eficiencia del carro i sea menor que la del carro j
                cont += 1
                i += 1
        elif modo == 'descendente':
            while i < len(carros):
                j = 1 + cont
                var= ''
                while j < len(carros):
                    if int(carros[i][12]) < int(carros[j][12]):
                        var= carros[i]
                        carros[i]= carros[j]
                        carros[j]= var
                        j += 1
                    else:
                        j += 1
                cont += 1
                i += 1 #para analizar el siguiente carro en la lista
                
        else: #en caso de que el modo no sea ascendente ni descendente, ejemplo 'mostrar', solo acomoda los datos a como se presenten
            carros #la lista se quede tal y como está


        #=================Esta parte de la función pinta los elementos en la ventana==============
            
        m= 100  #posicion en x
        n= 120  #posicion en y
        for x in carros:
            fonLabel= Label(canvas, bg= '#13483b', width= 50, height= 2)
            fonLabel.place(x= m-4, y=n-4)

            marcacar1= Label(canvas, text= str(x[0]), bg= '#13483b', fg='#2dff34',  font= ('Harlow Solid Italic', 16))
            marcacar1.place(x= m, y= n)
            
            modelocar1= Label(canvas, text= str(x[1]), bg= '#13483b',fg= '#03ffaf', font= ('Harlow Solid Italic', 16))
            modelocar1.place(x= m + 120, y=n)

            eficar1= Label(canvas, text= str(x[12]), bg= '#13483b', fg= '#01fdf8', font= ('Harlow Solid Italic', 16))
            eficar1.place(x=m + 240, y=n)
            

            n += 60
            
                
    ShowBoton= Button(canvas, text= 'Mostrar carrocería', font=('Lobster', 12), relief= 'raised',borderwidth=5,  bg= '#13483b', fg= 'white', command= lambda: Ordenar('mostrar'))
    ShowBoton.place(x=150, y=27)
    
    ascenBoton= Button(canvas, text= 'Ordenar ascendentemente',font=('Lobster', 12), relief= 'raised', borderwidth=5, bg= '#13483b', fg= 'white', command= lambda: Ordenar('ascendente'))
    ascenBoton.place(x=400, y= 27)
    
    descenBoton= Button(canvas, text= 'Ordenar descendentemente',font=('Lobster', 12), relief= 'raised', borderwidth=5, bg= '#13483b', fg= 'white', command= lambda: Ordenar('descendente'))
    descenBoton.place(x=700, y= 27)

    cuadroinfo= canvas.create_rectangle(690, 300, 1000, 580, fill= '#0c2d24')

    infoLabel= Label(canvas, text= 'Si desea más información de los autos \n ingrese el nombre del auto que le interesa',
                     bg= '#13483b', fg='white', font= ('courier', 9))
    infoLabel.place(x=691, y= 310)

    infoEntry= Entry(canvas)
    infoEntry.place(x=730, y = 380)

    infoBoton= Button(canvas, text= 'Mostrar', bg= '#13483b', fg='white', relief= 'groove',borderwidth=5, command= lambda: infocar(infoEntry.get()))
    infoBoton.place(x=900, y=380)

    crearBoton= Button(canvas, text= 'Crear nuevo carro',bg= '#13483b', relief= 'groove',borderwidth=5, fg= 'white',  command= lambda: changeWin(canvas, AutosCreate))
    crearBoton.place(x=800, y= 450)

    salirBoton= Button(canvas, text= 'Salir', bg= '#13483b', fg='white', relief= 'groove',borderwidth=5, command= lambda: changeWin(canvas, showMainwin))
    salirBoton.place(x= 800, y= 540)

    #_____Función que crea el canvas para mostrar la información completa de un carro específico____
    
    def infocar(car):
        data= getDataCar(car + '.txt')
        info= Canvas(canvas, width=400, height=550)
        info.place(x=50, y=10)

        fondo= info.create_image(0,0, image= fondo1, anchor= NW)
        cuadra= info.create_rectangle(15, 15, 385, 535, fill= '#12164f')

        text1= Label(info, text= '1. Marca del carro:', fg='white', bg= '#12164f', font=('Forte', 12))
        text1.place(x=20, y=20)
        marcaLabel= Label(info, text=str(data[0]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        marcaLabel.place(x=200, y=20)

        text2= Label(info, text= '2. Modelo del carro:', fg='white', bg= '#12164f', font=('Forte', 12))
        text2.place(x=20, y=50)
        modeloLabel= Label(info, text= str(data[1]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        modeloLabel.place(x=200, y=50)

        text3= Label(info, text= '3. País de fabricación:',fg='white', bg= '#12164f', font=('Forte', 12))
        text3.place(x=20, y=80)
        paisLabel= Label(info, text= str(data[2]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        paisLabel.place(x=200, y= 80)

        text4= Label(info, text= '4. Foto:',fg='white', bg= '#12164f', font=('Forte', 12))
        text4.place(x=20, y=110)
        #labelfoto= Label(info, image= img)
        #labelfoto.place(x= 200, y=110)

        try:
            img = PhotoImage(file = "AutosFotos/" + car + ".png")
            labelfoto= Label(info, image= img)
            labelfoto.place(x= 270, y=110)
        except:
            label= Label(info, text= 'Error al cargar la imagen', bg= '#12164f', fg= 'red')
            label.place(x=200, y= 110)

        text5= Label(info, text= '5. Año de temporada:', fg='white', bg= '#12164f', font=('Forte', 12))
        text5.place(x=20, y=140)
        tempLabel= Label(info, text= str(data[4]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        tempLabel.place(x=200, y= 140)

        text6= Label(info, text= '6. Cantidad de baterías:', fg='white', bg= '#12164f', font=('Forte', 12))
        text6.place(x=20, y=170)
        bateLabel= Label(info, text= str(data[5]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        bateLabel.place(x=200, y= 170)

        text7= Label(info, text= '7. Cantidad de pilas:', fg='white', bg= '#12164f', font=('Forte', 12))
        text7.place(x=20, y=200)
        pilaLabel= Label(info, text= str(data[6]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        pilaLabel.place(x=200, y= 200)

        text8= Label(info, text= '8. Nivel de tensión:', fg='white', bg= '#12164f', font=('Forte', 12))
        text8.place(x=20, y=230)
        levelLabel= Label(info, text= str(data[7]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        levelLabel.place(x=200, y= 230)

        text9= Label(info, text= '9. Estado:',fg='white', bg= '#12164f', font=('Forte', 12))
        text9.place(x=20, y=260)
        estaLabel= Label(info, text= str(data[8]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        estaLabel.place(x=200, y= 260)

        text10= Label(info, text= '10. Consumo de motores:',fg='white', bg= '#12164f', font=('Forte', 12))
        text10.place(x=20, y=290)
        motoLabel= Label(info, text= str(data[9]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        motoLabel.place(x=200, y= 290)

        text11= Label(info, text= '11. Sensores:',fg='white', bg= '#12164f', font=('Forte', 12))
        text11.place(x=20, y=320)
        sensLabel= Label(info, text= str(data[10]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        sensLabel.place(x=200, y= 320)

        text12= Label(info, text= '12. Peso del carro/ kg:',fg='white', bg= '#12164f', font=('Forte', 12))
        text12.place(x=20, y=350)
        pesoLabel= Label(info, text= str(data[11]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        pesoLabel.place(x=200, y= 350)

        text13= Label(info, text= '13. Eficiencia:',fg='white', bg= '#12164f', font=('Forte', 12))
        text13.place(x=20, y=380)
        eficLabel= Label(info, text= str(data[12]),fg='white', bg= '#12164f', font=('Segoe UI', 12))
        eficLabel.place(x=200, y= 380)

        cerrarBoton= Button(info,bg='white', fg='#12164f',relief='groove',borderwidth=5, text='Cerrar', command= lambda: info.destroy())
        cerrarBoton.place(x=350, y= 520)
        
        EditarLabel= Label(info,fg='white', bg= '#12164f', font=('Segoe UI', 12), text= 'Para editar algún elemento \n ingrese el número que desea editar')
        EditarLabel.place(x=70, y=430)
        EditarEntry= Entry(info, font=('Segoe UI', 12))
        EditarEntry.place(x=50, y=490)
        editarBoton= Button(info,fg='white',borderwidth= 5, relief='raised', bg= '#12164f', font=('Forte', 10), text= 'Editar Valores', command= lambda: editar(data, EditarEntry.get(), info))
        editarBoton.place(x=250, y=490)

def editar_Archivo(carro, posicion, dato):

    archivo = open("Autos/" + carro[0] + ".txt", "r")
    info = archivo.readline()
    info = info.split(",")
    archivo.close()
    info[int(posicion) - 1] = dato
    archivo = open("Autos/" + carro[0] + ".txt", "w")
    for elem in info:
        
        archivo.write(elem)

        if elem == info[-1]:
            break
        archivo.write(",")

    archivo.close()
    

"""=================================================================================================
_________________Función para editar los datos de un archivo de texto
E: el carro que se desea editar, la posicion a cambiar, el canvas 
S:
R:
"""
def editar(car, posicion, canvas):
    edit= Canvas(canvas, width= 200, height= 100, bg= '#1F2C73')
    edit.place(x=100, y=30)
    j=0
    var= 0 + j
    editarLabel= Label(edit, text= 'Ingrese elemento', font= ('Forte', 12), fg= 'white', bg= '#1F2C73')
    editarLabel.place(x=30, y=10)
    editEntry= Entry(edit)
    editEntry.place(x=15, y= 40)
    Boton=Button(edit, text= 'Actualizar', command= lambda: editar_Archivo(car, posicion, editEntry.get()), fg= 'white', bg= '#1F2C73', relief= 'groove', borderwidth= 5)
    Boton.place(x=30, y= 60)
  

def getandsortRGP(canvas, opc_ord, opc_R):        # Ordena los pilotos por RGP, si opc es 0 lo ordena de forma ascendente, sino forma descendente

    rgp = {}            # Diccionario necesario para ordenar los pilotos respecto a su RGP

    tablaFrame = Frame(canvas, width  = 550, height = 500, bg = "green")      # Tabla donde se mostrarán los datos de los pilotos
    tablaFrame.place(x = 70, y = 50)

    fondoLabel = Label(tablaFrame, image = fondo_tabla)
    fondoLabel.place(x = 0, y = 0)
    
    nameLabel = Label(tablaFrame, text = "Nombre")
    nameLabel.grid(row = 0, column = 1, padx = 25, pady = 10)

    yearsLabel = Label(tablaFrame, text = "Edad")
    yearsLabel.grid(row = 0, column = 2, padx = 25, pady = 10)

    nationLabel = Label(tablaFrame, text = "Nacionalidad")
    nationLabel.grid(row = 0, column = 3, padx = 25, pady = 10)

    tempLabel = Label(tablaFrame, text = "Temporada")
    tempLabel.grid(row = 0, column = 4, padx = 25, pady = 10)

    podLabel = Label(tablaFrame, text = "Podios")
    podLabel.grid(row = 0, column = 5, padx = 25, pady = 10)

    rgpLabel = Label(tablaFrame, text = "RGP")
    rgpLabel.grid(row = 0, column = 6, padx = 25, pady = 10)

    repLabel = Label(tablaFrame, text = "REP")
    repLabel.grid(row = 0, column = 7, padx = 25, pady = 10)
    
    for piloto in pilotos:          # En este for se recopila la información del piloto para calcular su RGP, además se añaden elementos al diccionario de la forma:   piloto: RGP , para luego ordenarlo
        archivo = open("Pilotos/" + piloto + ".txt", "r")
        info = archivo.readline()      # Obtiene la información del archivo
        info = info.split(",")              # Transforma la información a una lista
        archivo.close()
        nombre_piloto = info[0]
        V = int(info[-1])
        P = int(info[5])
        T = int(info[4])
        A = int(info[6])
        RGP = ((V+P)/(T-A))*100
        REP = (V/(T-A)) * 100
        if opc_R == "RGP":
            rgp[nombre_piloto] = [RGP, REP, piloto]             # Esto es para saber de qué piloto se está hablando: esta es la llave, el RGP respectivo y el nombre del archivo que contiene los datos de ése piloto se ponen en una lista
        else:
            rgp[nombre_piloto] = [REP, RGP, piloto]
            
    resultado = sorted(rgp.items(), key=operator.itemgetter(1))   # Ordena los elementos de menor a mayor
    
    if opc_ord != 0:        # Por si se quiere ordenar de forma descendente
        resultado.reverse()

    posrow = 1              # Esta será la posición de los labels dentro del Frame
    cont = 1
    
    for piloto in resultado:        # Esto es para acomodar los labels en el frame
        archivo_piloto = open("Pilotos/" + piloto[1][2] + ".txt", "r")       # Para obtener los datos del piloto
        info_piloto = archivo_piloto.readline()
        info_piloto = info_piloto.split(",")      # Convierte el string en lista
        archivo_piloto.close()

    #--------------------------------------- Obtiene los datos respectivos de cada piloto -------------------#
    
        nombre = info_piloto[0]         
        edad = info_piloto[1]
        nacionalidad = info_piloto[2]
        año_temp = info_piloto[3]
        participaciones = info_piloto[4]
        RGP = round(piloto[1][0],1)
        REP = round(piloto[1][1],1)

        editBut =Boton(tablaFrame, piloto[1][2])       # Botón que sirve para editar los datos de un piloto
        editBut.boton.grid(row = posrow, column = 0, padx = 25, pady = 10)

    #--------------------------------------- Labels de los datos respectivos de cada piloto -------------------#
        
        labelNombre = Label(tablaFrame, text = str(cont) + " - " + nombre)
        labelNombre.grid(row = posrow, column = 1, padx = 25, pady = 10)

        labelAnhos = Label(tablaFrame, text = edad)
        labelAnhos.grid(row = posrow, column = 2, padx = 25, pady = 10)

        labelNac = Label(tablaFrame, text = nacionalidad)
        labelNac.grid(row = posrow, column = 3, padx = 25, pady = 10)

        labelTemp = Label(tablaFrame, text = año_temp)
        labelTemp.grid(row = posrow, column = 4, padx = 25, pady = 10)

        labelPart = Label(tablaFrame, text = participaciones)
        labelPart.grid(row = posrow, column = 5, padx = 25, pady = 10)

        labelRGP = Label(tablaFrame, text = RGP)
        labelRGP.grid(row = posrow, column = 6, padx = 25, pady = 10)

        labelREP = Label(tablaFrame, text = REP)
        labelREP.grid(row = posrow, column = 7, padx = 25, pady = 10)

        posrow += 1              # Para ir acomodando los politos sobre el eje y
        cont += 1           # Va editando la posición del piloto

def showTablePilots():          # Función que muestra la tabla de los piltos

    canvas = Canvas(win, width = 1000, height = 700, bg = "red")
    canvas.place(x = 0, y = 0)

    fondo = canvas.create_image(0,0, image = fondo_pilotos, anchor = NW)

    sortAscRGPBut = Button(canvas, relief="ridge", borderwidth = 5 ,bg = "#02b4f2",text = "Ordenar de forma ascendente: RGP", command = lambda:getandsortRGP(canvas,0, "RGP"))
    sortAscRGPBut.place(x = 220, y = 660)

    sortDesRGPBut = Button(canvas, relief="ridge", borderwidth = 5,bg = "#02b4f2", text = "Ordenar de forma descendente: RGP", command = lambda:getandsortRGP(canvas,1, "RGP"))
    sortDesRGPBut.place(x = 450 , y = 660)

    sortAscREPBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2",text = "Ordenar de forma ascendente: REP", command = lambda:getandsortRGP(canvas,0, "REP"))
    sortAscREPBut.place(x = 220 , y = 620)

    sortDesREPBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2", text = "Ordenar de forma descendente: REP", command = lambda:getandsortRGP(canvas,1, "REP"))
    sortDesREPBut.place(x = 450 , y = 620)
    
    mainBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2", text = "Regresar al Inicio", command = lambda: changeWin(canvas, showMainwin))
    mainBut.place(x = 750 , y = 640)

def actPil(archivo, nombre, años, nacionalidad, temp, competencias, part_des, abandonos, victorias, ventana):

    file_pilot = open("Pilotos/" + archivo + ".txt", "w")
    file_pilot.write(nombre + ","  + años + "," + nacionalidad + "," + temp + "," + competencias + "," + part_des + "," + abandonos + "," + victorias)
    file_pilot.close()

    ventana.destroy()
    messagebox.showinfo("Actualizado", "La información del piloto ha sido actualizada")    

def editPilot(pilot):       # Ventana que sirve para editar los datos de un piloto
    ventana = Toplevel()
    ventana.geometry("400x300")

    canvas = Canvas(ventana, width = 90, height = 140, bg = "red")
    canvas.place(x = 285, y = 10)

    img = PhotoImage(file = "Pilotos/" + pilot + ".png")
    foto = canvas.create_image(0,0, image = img, anchor = NW)

    archive = open("Pilotos/" + pilot + ".txt", "r")
    info = archive.readline()
    info = info.split(",")
    archive.close()

    nombre = info[0]
    años = info[1]
    nacionalidad = info[2]
    temp = info[3]
    comp = info[4]
    part_dest = info[5]
    aband = info[6]
    vict = info[-1]

    labelNombre = Label(ventana, text = "Nombre: ")
    labelNombre.place(x = 30, y = 20)

    entryNombre = Entry(ventana)
    entryNombre.insert(0, nombre)
    entryNombre.place(x = 100, y = 20)

    labelAño = Label(ventana, text = "Años: ")
    labelAño.place(x = 30, y = 50)

    entryAño = Entry(ventana)
    entryAño.insert(0, años)
    entryAño.place(x = 80, y = 50)

    labelNac = Label(ventana, text = "Nacionalidad: ")
    labelNac.place(x = 30, y = 80)

    entryNac = Entry(ventana)
    entryNac.insert(0, nacionalidad)
    entryNac.place(x = 120, y = 80)

    labelTemp = Label(ventana, text = "Temporada: ")
    labelTemp.place(x = 30, y = 110)

    entryTemp = Entry(ventana)
    entryTemp.insert(0, temp)
    entryTemp.place(x = 100, y = 110)

    labelComp = Label(ventana, text = "Competencias: ")
    labelComp.place(x = 30, y = 140)

    entryComp = Entry(ventana)
    entryComp.insert(0, comp)
    entryComp.place(x = 120, y = 140)

    labelPartDes = Label(ventana, text = "Participaciones destacadas: ")
    labelPartDes.place(x = 30, y = 170)

    entryPartDes = Entry(ventana)
    entryPartDes.insert(0, part_dest)
    entryPartDes.place(x = 190, y = 170)

    labelAba = Label(ventana, text = "Abandonos: ")
    labelAba.place(x = 30, y = 200)

    entryAba = Entry(ventana)
    entryAba.insert(0, aband)
    entryAba.place(x = 130, y = 200)

    actBut = Button(ventana, text = "Actualizar Información", command = lambda: actPil(pilot, entryNombre.get(), entryAño.get(),entryNac.get(), entryTemp.get(),entryComp.get(),entryPartDes.get(), entryAba.get(), vict, ventana))
    actBut.place(x = 20, y = 250)

    cancelBut = Button(ventana, text = "Salir", command = lambda: ventana.destroy())
    cancelBut.place(x = 300, y = 250)

    ventana.mainloop()

def showTablePilots():          # Función que muestra la tabla de los piltos

    canvas = Canvas(win, width = 1000, height = 700, bg = "red")
    canvas.place(x = 0, y = 0)

    fondo = canvas.create_image(0,0, image = fondo_pilotos, anchor = NW)

    sortAscRGPBut = Button(canvas, relief="ridge", borderwidth = 5 ,bg = "#02b4f2",text = "Ordenar de forma ascendente: RGP", command = lambda:getandsortRGP(canvas,0, "RGP"))
    sortAscRGPBut.place(x = 220, y = 660)

    sortDesRGPBut = Button(canvas, relief="ridge", borderwidth = 5,bg = "#02b4f2", text = "Ordenar de forma descendente: RGP", command = lambda:getandsortRGP(canvas,1, "RGP"))
    sortDesRGPBut.place(x = 450 , y = 660)

    sortAscREPBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2",text = "Ordenar de forma ascendente: REP", command = lambda:getandsortRGP(canvas,0, "REP"))
    sortAscREPBut.place(x = 220 , y = 620)

    sortDesREPBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2", text = "Ordenar de forma descendente: REP", command = lambda:getandsortRGP(canvas,1, "REP"))
    sortDesREPBut.place(x = 450 , y = 620)
    
    mainBut = Button(canvas, relief="ridge", borderwidth = 5, bg = "#02b4f2", text = "Regresar al Inicio", command = lambda: changeWin(canvas, showMainwin))
    mainBut.place(x = 750 , y = 640)

def testWin():

    global canvas

    opc = StringVar()
    opc.set("Elija un piloto")

    canvas = Canvas(win, width = 1000, height = 800, bg = "blue")
    canvas.place(x = 0, y = 0)

    imagen_fondo = canvas.create_image(0,0, image = img, anchor = NW)

    # ------------------------ Se colocan las luces del auto ------------------------------------#

    luzDirDer = canvas.create_oval(750, 600, 800, 650, fill = "yellow4")
    luzDirIzq = canvas.create_oval(200, 600, 250, 650, fill = "yellow4")
    luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red")
    luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red")
    luzDel1 = canvas.create_oval(550, 400, 600, 450, fill = "gray")
    luzDel2 = canvas.create_oval(380, 400, 430, 450, fill = "gray")

    # ------------------------------- label del piloto ----------------------------------- #

    pilotoText= Label(canvas, text = "El piloto escogido es: ", font = ("Impact", 15), bg='#0E1E5A', fg= 'white' )
    pilotoText.place(x = 10, y = 320)

    pilotoText= Label(canvas, textvariable = opc, font = ("Impact", 15), bg='#0E1E5A', fg= 'white')
    pilotoText.place(x = 30, y = 350)

    # --------------- funcion que obtiene el nombre de las escuderías ------------------------------#

    escuderias= os.listdir('Escuderias')
    
    nombres= []
    posicion= 1

    while posicion < len(escuderias):
        file= open('Escuderias/' + escuderias[posicion], 'r')
        data = file.readline()
        file.close()
        data = data.split(",")
        nombres.append(data[0])
        posicion += 1
        
    var= StringVar(canvas)
    var.set("Elija un escudería")

    menu= OptionMenu(canvas, var, *nombres)
    menu.place(x=10, y=50)

    escuLabel= Label(canvas, text= 'La escudería elegida: ', bg= '#0E1E5A', fg='white',font = ("Impact", 15))
    escuLabel.place(x=10, y=400)

    varLabel= Label(canvas, textvariable= var, bg= '#0E1E5A', fg= 'white',font = ("Impact", 15))
    varLabel.place(x= 30, y= 430)

    canvas.create_rectangle(0,307, 228, 475, fill= '#0E1E5A')
    
    # ----------------------------------  Opciones de los pilotos disponibles --------------------------------#

    opciones = getNombresPilotos()

    opcMenu = OptionMenu(canvas, opc, *opciones)
    opcMenu.place(x = 10, y = 10)

    # -------------------------- Se colocan los botones con las imágenes --------------- #
    
    derBut = Button(canvas, image = flechar, command =lambda: lightOn("dd"))
    derBut.place(x = 550, y = 600)

    upBut = Button(canvas, image = flechau, command =lambda: lightOn("front"))
    upBut.place(x = 450, y = 500)

    downBut = Button(canvas, image = flechad, command =lambda: lightOn("tras"))
    downBut.place(x = 450, y = 600)

    izqBut = Button(canvas, image = flechal, command =lambda: lightOn("di"))
    izqBut.place(x = 350, y = 600)

    iniBut = Button(canvas, text = "Salir", command = lambda:changeWin(canvas, showMainwin),bg= '#0E1E5A', fg= 'white', relief= 'sunken', borderwidth=5, font= ('courier',9))
    iniBut.place(x = 945, y = 6)

    MovBut = Button(canvas, text = "Movimiento especial", command = lambda: initRandomMovement(), bg= '#0E1E5A', fg= 'white', relief= 'sunken', borderwidth=5, font= ('courier', 9))
    MovBut.place(x = 830, y = 630)

class Boton:

    def __init__(self, frame, archivo):
        self.boton = Button(frame, text = "Editar", command = lambda:editPilot(archivo))

def lightOn(luz):

    global dir_izq, dir_der, traseras, derechas, pwm, canvas
    
    if luz == "dd":     # Si la luz es la direccional derecha
        
        if dir_izq:     # Si estaba la luz direccional izquierda encendida, sabemos que debe ir hacia delante            
            
            luzDirIzq = canvas.create_oval(200, 600, 250, 650, fill = "yellow4")
            dir_izq = False
            myCar.send("ll:0;")
            myCar.send("dir:0;")

        else:       # Sino es que estaba recto, entonces dobla y enciende la direccional
            dir_der = True
            myCar.send("lr:1;")
            myCar.send("dir:-1;")
            thread1 = threading.Thread(target = parpadeo)
            thread1.start()
            
    elif luz == "di":
        
        if dir_der:
            
            luzDirDer = canvas.create_oval(750, 600, 800, 650, fill = "yellow4")
            dir_der = False
            myCar.send("lr:0;")
            myCar.send("dir:0;")
        else:
            dir_izq = True
            myCar.send("ll:1;")
            myCar.send("dir:1;")
            thread1 = threading.Thread(target = parpadeo)
            thread1.start()
            
    elif luz == "front":
        if pwm == 0:
            pwm += min_pwm
            luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red4")
            luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red4")
            myCar.send("lb:0;")
            myCar.send("lf:1;")
        elif 0 < pwm and pwm < 1000:
                pwm += 100
        elif pwm < 0:
            pwm = 0
                    
        myCar.send("pwm:" + str(pwm) + ";")
        luzDel1 = canvas.create_oval(550, 400, 600, 450, fill = "white")
        luzDel2 = canvas.create_oval(380, 400, 430, 450, fill = "white")
        
    elif luz == "tras":
        if pwm > min_pwm:
            pwm -= 100
            myCar.send("pwm:" + str(pwm) + ";")
            thread = threading.Thread(target = frenar, args = ())
            thread.start()
        elif pwm == min_pwm:
            pwm = 0
            myCar.send("pwm:0;")
            luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red")
            luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red")
            myCar.send("lb:1;")
            luzDel1 = canvas.create_oval(550, 400, 600, 450, fill = "gray")
            luzDel2 = canvas.create_oval(380, 400, 430, 450, fill = "gray")
            myCar.send("lf:0;")
        elif pwm == 0:
            pwm = min_pwm * - 1
            myCar.send("pwm:" + str(pwm) + ";")
            luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red")
            luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red")
        else:
            print("-1")
            
        
# ------------------------------------ Banderas para el manejo del auto --------------------------------------------- #

encDirDer = False
encIDirzq = False

dir_izq = False
dir_der = False
traseras = False
delanteras = False
pwm = 0
min_pwm = 800

def frenar():
     luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red")
     luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red")
     time.sleep(0.75)
     luzTrasDer = canvas.create_oval(270, 600, 320, 650, fill = "red4")
     luzTrasIzq = canvas.create_oval(680, 600, 730, 650, fill = "red4")
     
def parpadeo():

    while dir_izq:
        myCar.send("ll:1;")
        luzDirIzq = canvas.create_oval(200, 600, 250, 650, fill = "yellow")
        time.sleep(0.5)
        myCar.send("ll:0;")
        luzDirIzq = canvas.create_oval(200, 600, 250, 650, fill = "yellow4")
        time.sleep(0.5)

    while dir_der:
        myCar.send("lr:1;")
        luzDirDer = canvas.create_oval(750, 600, 800, 650, fill = "yellow")
        time.sleep(0.5)
        myCar.send("lr:0;")
        luzDirDer = canvas.create_oval(750, 600, 800, 650, fill = "yellow4")
        time.sleep(0.5)

def initRandomMovement():

    mover = threading.Thread(target = randomMovement, args = ())
    mover.start()

def randomMovement():

    opc = random.randint(0, 1)
    luces = random.randint(0, 1)

    if opc == 1:
        pwm = random.randint(900, 1000)
        direccion = random.randint(-1, 1)
    else:
        pwm = random.randint(-1000, -900)
        direccion = random.randint(-1, 1)

    if luces == 1:
        myCar.send("lr:1;")
        myCar.send("ll:1;")
        time.sleep(random.randint(1,3))
        myCar.send("lr:0;")
        myCar.send("ll:0;")

    myCar.send("pwm:" + str(pwm) + ";")
    myCar.send("dir:" + str(direccion) + ";")
    time.sleep(random.randint(3,5))
    
    pwm = 0
    myCar.send("pwm:" + str(pwm) + ";")

    dir_der = False
    dir_der = False

def getSense():
    
    res = myCar.readById("sense;")
    return res

def getNombresPilotos():

    nombres_pil =[]

    for piloto in pilotos:

        archivo = open("Pilotos/" + piloto + ".txt", "r")
        info = archivo.readline()
        info = info.split(",")
        archivo.close()
        
        nombres_pil.append(info[0])
        
    return nombres_pil

n_pil = getNombresPilotos()

showMainwin()
