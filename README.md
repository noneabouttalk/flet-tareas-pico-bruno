# Mis tareas (Flet)

Lista de tareas hecha con [Flet](https://flet.dev) para la práctica de ampliación de la primera app (2.º ASIR).
Autor: Bruno Picó.

## Funcionalidades
- Añadir, marcar, borrar y contar tareas pendientes.
- No permite tareas vacías ni repetidas (sin distinguir mayúsculas).
- Contador en rojo si no hay tareas y en verde si hay alguna.
- Botón «Borrar completadas».
- Botón «Modificar» en cada tarea (diálogo).

## Ejecutar
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flet
flet run src/main.py
```

## Publicar
```bash
flet build web && flet serve      # web en http://localhost:8000
flet build apk                    # Android (build/apk)
flet build linux                  # desde Linux
flet build windows                # desde Windows
```
