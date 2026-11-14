import flet as ft

def main(page):
    page.title = "Ejercicio2"
    page.padding = 20

    
    nombre = ft.TextField(value="Ingresa tu nombre: ", error="Escribe tu nombre")
    nombrebien = nombre.value.strip()
    vacio = ""
    boton = ft.Button(content="Hola, " + nombre.value, on_click=pulsar)

    def pulsar(e):
        if nombrebien == vacio:
            nombre.error = "El nombre está vacio"
            return
        else:
            nombre.error = None
                
    
    
    page.add(nombre, boton, pulsar)

    

ft.run(main)
    


