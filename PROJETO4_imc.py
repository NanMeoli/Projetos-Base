import flet as ft
from flet import Colors as colors

def main(page: ft.Page):
    page.title = "Projeto IMC"
    page.theme_mode = "light" # dark
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.width = 400
    page.window.height = 500

    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        duration=4000
    )

    # Título
    titulo = ft.Text(
        "Calculadora de IMC",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    # Campos de entrada
    peso_input = ft.TextField(
        label="Peso (kg)",
        hint_text="Ex: 75.5",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        text_align=ft.TextAlign.CENTER
    )

    altura_input = ft.TextField(
        label="Altura (m)",
        hint_text="Ex: 1.75",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300,
        text_align=ft.TextAlign.CENTER
    )

    resultado_saida = ft.Text(
        value="Aguardando cálculo...",
        size=18,
        weight=ft.FontWeight.NORMAL,
        color=colors.BLUE_GREY_600
    )

    def calcular_imc(e):
        try:
            peso = float(peso_input.value.replace(',', '.'))
            altura = float(altura_input.value.replace(',', '.'))
        except (ValueError, TypeError):
            page.snack_bar.content = ft.Text("❌ Por favor, preencha Peso e Altura com números válidos.", color=colors.WHITE)
            page.snack_bar.bgcolor = colors.RED_600
            page.snack_bar.open = True
            page.update()
            return

        if peso <= 0 or altura <= 0:
            page.snack_bar.content = ft.Text("❌ Peso e Altura devem ser valores positivos.", color=colors.WHITE)
            page.snack_bar.bgcolor = colors.RED_600
            page.snack_bar.open = True
            page.update()
            return

        imc = peso / (altura * altura)
        classificacao = ""
        cor_fundo = colors.BLUE_GREY_500

        if imc < 18.5:
            classificacao = "Abaixo do peso"
            cor_fundo = colors.YELLOW_700
        elif imc < 24.9:
            classificacao = "Peso normal"
            cor_fundo = colors.GREEN_700
        elif imc < 29.9:
            classificacao = "Sobrepeso"
            cor_fundo = colors.ORANGE_700
        else:
            classificacao = "Obesidade"
            cor_fundo = colors.RED_700

        resultado_saida.value = f"IMC: {imc:.2f} | Categoria: {classificacao}"
        resultado_saida.color = cor_fundo # Usa a cor da categoria no texto

        snackbar_texto = f"Cálculo concluído! IMC: {imc:.2f} ({classificacao})"
        page.snack_bar.content = ft.Text(snackbar_texto, weight=ft.FontWeight.BOLD)
        page.snack_bar.bgcolor = cor_fundo
        page.snack_bar.open = True
        page.update()


    # Botão de ação
    botao = ft.ElevatedButton(
        text="Calcular IMC",
        on_click=calcular_imc,
        color=colors.WHITE,
        bgcolor=colors.BLUE_700,
        width=300,
        height=50
    )

    page.add(
        ft.Container(height=20),
        titulo,
        ft.Container(height=30),
        peso_input,
        altura_input,
        ft.Container(height=30),
        botao,
        ft.Container(height=30),
        resultado_saida
    )

if __name__ == "__main__":
    ft.app(target=main)