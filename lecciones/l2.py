import flet as ft

def main(page):
    page.title = "Leccion 2"
    page.padding = 20

    saludo = ft.Text("Hola", size=30, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD)
    page.add(saludo)

    print("El texto vale: ", saludo.value)

    saludo.value = 'Adios'
    saludo.color = ft.Colors.RED
    page.update()


ft.run(main)