# frontend/src/main.py
import flet as ft
import requests

BASE_URL = "http://localhost:8000"  # URL del backend
TOKEN = None  # Variable global para almacenar el token

def main(page: ft.Page):
    page.title = "Ecommerce App"
    page.padding = 20

    # Campos de login
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    login_status = ft.Text()

    # Función para manejar el login
    def login(e):
        global TOKEN
        try:
            response = requests.post(
                f"{BASE_URL}/auth/token",
                data={"username": email_field.value, "password": password_field.value}
            )
            response.raise_for_status()
            data = response.json()
            TOKEN = data["access_token"]
            login_status.value = "Login exitoso!"
            show_products_page()
        except requests.RequestException as err:
            login_status.value = f"Error: {str(err)}"
        page.update()

    # Botón de login
    login_button = ft.ElevatedButton("Login", on_click=login)

    # Pantalla de productos
    def show_products_page():
        page.controls.clear()
        products_list = ft.Column()

        try:
            response = requests.get(
                f"{BASE_URL}/products/",
                headers={"Authorization": f"Bearer {TOKEN}"}
            )
            response.raise_for_status()
            products = response.json()
            for product in products:
                products_list.controls.append(
                    ft.Text(f"{product['name']} - ${product['price']}")
                )
        except requests.RequestException as err:
            products_list.controls.append(ft.Text(f"Error al cargar productos: {str(err)}"))

        page.add(products_list)
        page.update()

    # Layout inicial (login)
    page.add(
        ft.Column([
            ft.Text("Iniciar Sesión", size=20, weight="bold"),
            email_field,
            password_field,
            login_button,
            login_status
        ])
    )

if __name__ == "__main__":
    # ft.app(target=main, port=8001)
    ft.app(target=main, port=8001, view=ft.AppView.WEB_BROWSER)