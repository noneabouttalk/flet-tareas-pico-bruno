#Lista de tareas Bruno Picó
#2X ASIR
#Lista de tareas con añadir, editar, borrar y con contador

import flet as ft                                   # flet con apodo ft


def main(page):                                     # Flet la llama al abrir y le pasa la ventana (page)

    # ───── PÁGINA ─────
    page.title = "Lista de Tareas de Bruno"         # título de la ventana
    page.padding = 20                               # margen interior

    # ───── CONTROLES ─────
    titulo = ft.Text("Mis Tareas", size=30, weight=ft.FontWeight.BOLD)
    nueva_tarea = ft.TextField(
        label="Nueva Tarea",
        expand=True,                                # ocupa el ancho libre
        on_submit=lambda e: añadir_tarea(e),        # Enter = añadir (lambda: aún no existe)
    )
    contador = ft.Text("Tareas pendientes: 0")      #Texto inicial del contador, comienza como texto fijo marcando 0 pero se actualiza nada más arrancar
    tareas = ft.Column()                            # columna vacía; dentro: tareas.controls

    # ───── FUNCIONES ─────
    def actualizar_contador(e=None):                # e=None: la llama Flet (con e) o yo (sin e)
        pendientes = 0
        for fila in tareas.controls:                # recorro cada tarea (fila)
            casilla = fila.controls[0]              # [0] = el Checkbox
            if casilla.value == False:              # sin marcar = pendiente
                pendientes = pendientes + 1
        contador.value = f"Tareas: {len(tareas.controls)} * Tareas pendientes: {pendientes}"

        if len(tareas.controls) == 0: #Si NO hay ninguna tarea
            contador.color = ft.Colors.RED
        else: # Si hay alguna (Aún que esté completada)
            contador.color = ft.Colors.GREEN

        page.update()                               # mando los cambios a la pantalla


    def eliminar_tarea(fila):                       #Función para eliminar las tareas, recibe la fila a borrar
        tareas.controls.remove(fila)                # quito esa fila
        actualizar_contador()                       #Actualiza el contador ya que se ha modificado la cantidad de tareas


    def comprobar_repetidas(text, excluir=None): #Devuelve True si está repetida
        for fila in tareas.controls: # Miro cada tarea
            if fila is excluir: #Si soy yo? (para el paso de editar)
                continue # Me la salto porque yo soy igual que yo
            if text.lower() == fila.controls[0].label.lower(): #Comparo en minusculas
                return True # Si encuentro coincidencia = True
        return False # Si no, False, no es repetida


    def editar_tarea(fila): #Abre un dialogo para modificar el texto de ESA fila, la que recibe la función.
        campo = ft.TextField(value=fila.controls[0].label) #Contenido de la tarea

        def cancelar(e): #Cerrar sin cambiar nada
            page.pop_dialog()

        def guardar(e): #Guardamos los cambios
            texto = campo.value.strip()
            if not texto: #Revisamos que NO esté vacio
                campo.error = 'Campo vacio'
                page.update()
                return
            if comprobar_repetidas(texto, fila): #Revisamos que NO esté repetida (sin contarse a si misma)
                campo.error = "Esta tarea ya existe"
                page.update()
                return
            fila.controls[0].label = texto #Modificamos el contenido
            page.pop_dialog() # Cerramos
            page.update()

        dialogo = ft.AlertDialog(
            modal=True, # NO se cierra pinchando fuera
            title=ft.Text("Modificar Tarea"),
            content=campo, #Campo de texto que vemos con el contenido de la tarea
            actions=[ #Acciones que se pueden realizar desde el dialogo
                ft.TextButton(content="Cancelar", on_click=cancelar), #Boton de cancelar
                ft.TextButton(content="Guardar", on_click=guardar), #Boton de guardar
                ],
        )
        page.show_dialog(dialogo) #Abre el dialogo !!IMPORTANTE!!
            
    def añadir_tarea(e):                            # Agrega una tarea, recibe un evento, que en este caso es presionar añadir tarea o darle al enter
        texto = nueva_tarea.value.strip()           # lo escrito, sin espacios en los lados

        if not texto:                               # vacío -> error y salgo
            nueva_tarea.error = "Escribe una tarea"
            page.update()
            return

        if comprobar_repetidas(texto): #Si repetida --> error "Esta tarea ya existe" y salgo
            nueva_tarea.error = "Esta tarea ya existe"
            page.update()
            return

        nueva_tarea.error = None                    # quito el error

        fila = ft.Row()                             # fila vacía primero (la usa la lambda)
        fila.controls = [
            ft.Checkbox(                            # [0] casilla con el texto
                label=texto,
                expand=True,
                on_change=actualizar_contador,      # marcar/desmarcar = recontar
            ),
            ft.IconButton(                          # [1] papelera
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                on_click=lambda e: eliminar_tarea(fila),   # cada papelera recuerda SU fila
            ),
            ft.IconButton(                          # [2] lapiz
                icon=ft.Icons.EDIT,                 # icono de editar
                icon_color=ft.Colors.BLUE,          # En azul que queda mas bonito
                on_click=lambda e: editar_tarea(fila)   #Si click llama a editar tarea y le manda SU fila.
            )
        ]

        tareas.controls.append(fila)                # la añado al final
        nueva_tarea.value = ""                      # vacío el campo
        actualizar_contador()

    def borrar_completas(e): #Borra todas las marcadas como completas
        sin_completar = [] #Lista vacía donde meteremos las que NO estan completaadas
        for fila in tareas.controls: #Recorremos todas las tareas.
            if fila.controls[0].value == False: #Si están sin completar
                sin_completar.append(fila) #Las agregamos a la lista
        tareas.controls = sin_completar #Sobrepone la lista original con la lista de tareas sin completar.
        actualizar_contador() #Ha hecho un cambio así que actualiza el contador.



    # ───── MONTAJE ─────
    boton = ft.Button(content="Añadir", on_click=añadir_tarea)   # sin () = no se ejecuta ahora
    boton_borrar_completadas = ft.Button(content="Borrar completadas", on_click=borrar_completas) #Boton borrar_completas, llama a la función.

    page.add(titulo, ft.Row([nueva_tarea, boton]), contador, tareas, boton_borrar_completadas) #Agrego cada uno de los componentes a la página, en orden.
    actualizar_contador()#Actualiza el contador nada más comenzar


ft.run(main)                                        # arranca la app
