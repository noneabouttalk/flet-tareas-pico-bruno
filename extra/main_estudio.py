#Lista de tareas Bruno Picó
#2X ASIR
#VERSIÓN EXTRA: la práctica (4 mejoras pedidas) + mejoras que he practicado para el examen
#
#Mejoras de la práctica:
#   1. No permite tareas repetidas (sin distinguir mayúsculas)
#   2. Contador en rojo si no hay tareas y en verde si las hay
#   3. Botón "Borrar completadas"
#   4. Botón "Modificar" (lápiz) en cada tarea
#
#Mejoras extra:
#   - Contador con total, pendientes y completadas (y naranja si quedan pendientes)
#   - No permite tareas de menos de 3 ni de más de 30 caracteres (al añadir y al editar)
#   - Pone la primera letra en mayúscula al añadir
#   - Botón "Marcar todas" / "Desmarcar todas" (el mismo botón alterna)
#   - Botón "Ordenar A-Z" / "Ordenar Z-A" (el mismo botón alterna, sin distinguir mayúsculas)
#   - Botón "Pendientes primero" (y dentro de cada grupo, de la A a la Z)
#   - Flecha en cada tarea para subirla una posición
#   - "Borrar completadas" y "Borrar todas" preguntan antes de borrar

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
    contador = ft.Text("Tareas pendientes: 0")      #Texto inicial del contador, se actualiza nada más arrancar
    tareas = ft.Column()                            # columna vacía; dentro: tareas.controls

    # ───── FUNCIONES ─────
    def actualizar_contador(e=None):                # e=None: la llama Flet (con e) o yo (sin e)
        pendientes = 0
        for fila in tareas.controls:                # recorro cada tarea (fila)
            casilla = fila.controls[0]              # [0] = el Checkbox
            if casilla.value == False:              # sin marcar = pendiente
                pendientes = pendientes + 1
        total = len(tareas.controls)
        contador.value = f"Tareas: {total} * Pendientes: {pendientes} * Completadas: {total - pendientes}"  #Completadas = total - pendientes (sin otro bucle)

        if total == 0:                              #Si NO hay ninguna tarea
            contador.color = ft.Colors.RED
        elif pendientes > 0:                        #Si quedan pendientes
            contador.color = ft.Colors.ORANGE
        else:                                       #Si hay tareas y todas están completadas
            contador.color = ft.Colors.GREEN

        page.update()                               # mando los cambios a la pantalla


    def eliminar_tarea(fila):                       #Función para eliminar las tareas, recibe la fila a borrar
        tareas.controls.remove(fila)                # quito esa fila
        actualizar_contador()                       #Actualiza el contador ya que se ha modificado la cantidad de tareas


    def comprobar_repetidas(text, excluir=None):    #Devuelve True si está repetida
        for fila in tareas.controls:                # Miro cada tarea
            if fila is excluir:                     #Si soy yo? (para el paso de editar)
                continue                            # Me la salto porque yo soy igual que yo
            if text.lower() == fila.controls[0].label.lower(): #Comparo en minusculas
                return True                         # Si encuentro coincidencia = True
        return False                                # Si no, False, no es repetida


    def comprobar_longitud(texto):                  #Devuelve el mensaje de error si la longitud no vale, o None si está bien
        if len(texto) < 3:
            return "Mínimo 3 caracteres"
        if len(texto) > 30:
            return "Máximo 30 caracteres"
        return None


    def editar_tarea(fila):                         #Abre un dialogo para modificar el texto de ESA fila, la que recibe la función.
        campo = ft.TextField(value=fila.controls[0].label) #① Contenido de la tarea

        def cancelar(e):                            #② Cerrar sin cambiar nada
            page.pop_dialog()

        def guardar(e):                             #③ Guardamos los cambios
            texto = campo.value.strip()
            if not texto:                           #Revisamos que NO esté vacio
                campo.error = 'Campo vacio'
                page.update()
                return
            if comprobar_longitud(texto):           #Revisamos que tenga entre 3 y 30 caracteres
                campo.error = comprobar_longitud(texto)
                page.update()
                return
            if comprobar_repetidas(texto, fila):    #Revisamos que NO esté repetida (sin contarse a si misma)
                campo.error = "Esta tarea ya existe"
                page.update()
                return
            fila.controls[0].label = texto          #Modificamos el contenido
            page.pop_dialog()                       # Cerramos
            page.update()

        dialogo = ft.AlertDialog(                   #④ El dialogo
            modal=True,                             # NO se cierra pinchando fuera
            title=ft.Text("Modificar Tarea"),
            content=campo,                          #Campo de texto que vemos con el contenido de la tarea
            actions=[                               #Acciones que se pueden realizar desde el dialogo
                ft.TextButton(content="Cancelar", on_click=cancelar), #Boton de cancelar
                ft.TextButton(content="Guardar", on_click=guardar),   #Boton de guardar
                ],
        )
        page.show_dialog(dialogo)                   #⑤ Abre el dialogo !!IMPORTANTE!!


    def subir_tarea(fila):                          #Sube ESA fila una posición
        posicion = tareas.controls.index(fila)      #1. ¿En qué posición está?
        if posicion == 0:                           #   Si ya es la primera no hago nada
            return
        tareas.controls.pop(posicion)               #2. La saco de la lista
        tareas.controls.insert(posicion - 1, fila)  #3. La meto una posición más arriba (insert empuja, no borra)
        page.update()


    def añadir_tarea(e):                            # Agrega una tarea, recibe un evento, que en este caso es presionar añadir tarea o darle al enter
        texto = nueva_tarea.value.strip()           # lo escrito, sin espacios en los lados

        if not texto:                               # vacío -> error y salgo
            nueva_tarea.error = "Escribe una tarea"
            page.update()
            return

        if comprobar_longitud(texto):               #Menos de 3 o más de 30 caracteres -> error y salgo
            nueva_tarea.error = comprobar_longitud(texto)
            page.update()
            return

        if comprobar_repetidas(texto):              #Si repetida --> error "Esta tarea ya existe" y salgo
            nueva_tarea.error = "Esta tarea ya existe"
            page.update()
            return

        nueva_tarea.error = None                    # quito el error
        texto = texto.capitalize()                  #Primera letra en mayúscula

        fila = ft.Row()                             # fila vacía primero (la usan las lambdas)
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
            ),
            ft.IconButton(                          # [3] flecha para subir
                icon=ft.Icons.ARROW_UPWARD,
                icon_color=ft.Colors.BLUE,
                on_click=lambda e: subir_tarea(fila)    #Cada flecha recuerda SU fila
            ),
        ]

        tareas.controls.append(fila)                # la añado al final
        nueva_tarea.value = ""                      # vacío el campo
        actualizar_contador()


    def borrar_completas(e):                        #Pregunta y borra todas las marcadas como completas
        def no(e):                                  #Cerrar sin borrar
            page.pop_dialog()

        def si(e):                                  #Borrar las completadas
            sin_completar = []                      #Lista vacía donde meteremos las que NO estan completadas
            for fila in tareas.controls:            #Recorremos todas las tareas.
                if fila.controls[0].value == False: #Si están sin completar
                    sin_completar.append(fila)      #Las agregamos a la lista
            tareas.controls = sin_completar         #Sobrepone la lista original con la lista de tareas sin completar.
            page.pop_dialog()
            actualizar_contador()                   #Ha hecho un cambio así que actualiza el contador.

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Borrar completadas"),
            content=ft.Text("¿Estas seguro de querer borrar las tareas completadas?"),
            actions=[
                ft.TextButton(content="Si", on_click=si),
                ft.TextButton(content="No", on_click=no),
            ],
        )
        page.show_dialog(dialogo)


    def borrar_todas(e):                            #Pregunta y borra TODAS las tareas
        def no(e):                                  #Cerrar sin borrar
            page.pop_dialog()

        def si(e):                                  #Borrar todas
            tareas.controls = []
            page.pop_dialog()
            actualizar_contador()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar Todas"),
            content=ft.Text("¿Estas seguro de querer borrar todas las tareas?"),
            actions=[
                ft.TextButton(content="Si", on_click=si),
                ft.TextButton(content="No", on_click=no),
            ],
        )
        page.show_dialog(dialogo)


    def marcar_desmarcar(e):                        #Marca todas o desmarca todas (el botón alterna)
        if boton_marcar.content == "Marcar todas":  #Miro el TEXTO del botón para saber qué toca
            for fila in tareas.controls:
                fila.controls[0].value = True
            boton_marcar.content = "Desmarcar todas" #Fuera del for: se cambia una sola vez
        else:
            for fila in tareas.controls:
                fila.controls[0].value = False
            boton_marcar.content = "Marcar todas"
        actualizar_contador()                       #Cambian las pendientes (y ya hace page.update)


    def ordenar_tareas(e):                          #Ordena A-Z o Z-A por el texto, sin distinguir mayúsculas (el botón alterna)
        if boton_ordenar.content == "Ordenar A-Z":
            tareas.controls.sort(key=lambda fila: fila.controls[0].label.lower())
            boton_ordenar.content = "Ordenar Z-A"
        else:
            tareas.controls.sort(key=lambda fila: fila.controls[0].label.lower(), reverse=True)
            boton_ordenar.content = "Ordenar A-Z"
        page.update()                               #Fuera del if/else: se hace en los dos casos


    def pendientes_primero(e):                      #Pendientes arriba y, dentro de cada grupo, de la A a la Z
        tareas.controls.sort(key=lambda fila: (fila.controls[0].value, fila.controls[0].label.lower())) #1º estado (False va antes que True), si empatan el texto
        page.update()


    # ───── MONTAJE ─────
    boton = ft.Button(content="Añadir", on_click=añadir_tarea)   # sin () = no se ejecuta ahora
    boton_borrar_completadas = ft.Button(content="Borrar completadas", on_click=borrar_completas) #Boton borrar_completas, llama a la función.
    boton_borrar_todas = ft.Button(content="Borrar todas", on_click=borrar_todas)
    boton_marcar = ft.Button(content="Marcar todas", on_click=marcar_desmarcar)
    boton_ordenar = ft.Button(content="Ordenar A-Z", on_click=ordenar_tareas)
    boton_pendientes = ft.Button(content="Pendientes primero", on_click=pendientes_primero)

    page.add(                                       #Agrego cada uno de los componentes a la página, en orden.
        titulo,
        ft.Row([nueva_tarea, boton]),
        contador,
        tareas,
        ft.Row([boton_borrar_completadas, boton_borrar_todas, boton_marcar]),   #Fila de botones de borrar y marcar
        ft.Row([boton_ordenar, boton_pendientes]),                               #Fila de botones de ordenar
    )
    actualizar_contador()                           #Actualiza el contador nada más comenzar


ft.run(main)                                        # arranca la app
