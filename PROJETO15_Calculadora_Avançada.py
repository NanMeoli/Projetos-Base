import flet as ft
import math

# 🎨 CORREÇÃO: O objeto de cores deve ser 'Colors' (com C maiúsculo)
# --- Constantes de Estilo CORRIGIDAS ---
BG_COLOR = ft.Colors.BLUE_GREY_900
BUTTON_COLOR = ft.Colors.BLUE_GREY_700
OPERATOR_COLOR = ft.Colors.AMBER_700
SCIENTIFIC_COLOR = ft.Colors.BLUE_GREY_600
CLEAR_COLOR = ft.Colors.RED_700
EQUAL_COLOR = ft.Colors.GREEN_700
TEXT_COLOR = ft.Colors.WHITE
DISPLAY_BG_COLOR = ft.Colors.BLUE_GREY_800

class Calculator(ft.Container):
    def __init__(self):
        super().__init__(
            width=400,
            padding=20,
            bgcolor=BG_COLOR, 
            border_radius=ft.border_radius.all(20),
        )
        self.result = "0"
        self.expression = ""
        self.is_new_number = True
        self.scientific_mode = False
        
        # --- Display de Resultado e Expressão ---
        self.display_result = ft.TextField(
            value=self.result,
            text_size=36,
            color=TEXT_COLOR,
            text_align=ft.TextAlign.RIGHT,
            read_only=True,
            border=ft.InputBorder.NONE,
            bgcolor=DISPLAY_BG_COLOR,
            content_padding=15,
            height=70
        )
        
        self.display_expression = ft.Text(
            value=self.expression,
            size=14,
            # CORREÇÃO: A cor WHITE70 também deve usar 'Colors'
            color=ft.Colors.WHITE70, 
            text_align=ft.TextAlign.RIGHT,
        )

        # --- Layout Principal ---
        self.content = ft.Column(
            controls=[
                self.display_expression,
                self.display_result,
                self._create_scientific_buttons(),
                self._create_basic_buttons(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        )
    
    def _create_button(self, text, color=BUTTON_COLOR, text_color=TEXT_COLOR, on_click=None, expand=1):
        """Cria um botão com estilo e função de clique."""
        return ft.ElevatedButton(
            text=text,
            expand=expand,
            on_click=on_click if on_click else self.button_click,
            bgcolor=color,
            color=text_color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.all(15),
            ),
        )

    def _create_scientific_buttons(self):
        """Cria a linha de botões científicos (oculta/visível)."""
        buttons = [
            self._create_button("sin", SCIENTIFIC_COLOR, on_click=self.scientific_operation),
            self._create_button("cos", SCIENTIFIC_COLOR, on_click=self.scientific_operation),
            self._create_button("tan", SCIENTIFIC_COLOR, on_click=self.scientific_operation),
            self._create_button("log", SCIENTIFIC_COLOR, on_click=self.scientific_operation),
            self._create_button("sqrt", SCIENTIFIC_COLOR, on_click=self.scientific_operation),
        ]
        self.scientific_row = ft.Row(buttons, spacing=10, visible=self.scientific_mode)
        return self.scientific_row

    def _create_basic_buttons(self):
        """Cria as linhas de botões básicos."""
        
        # Botões de controle e modo
        row0 = ft.Row(
            [
                self._create_button("AC", CLEAR_COLOR, on_click=lambda e: self.clear_all()),
                self._create_button("+/-", CLEAR_COLOR, on_click=lambda e: self.negate()),
                self._create_button("%", OPERATOR_COLOR, on_click=self.button_click),
                self._create_button("÷", OPERATOR_COLOR, on_click=self.button_click),
            ], spacing=10
        )

        # Botões numéricos e operacionais
        row1 = ft.Row([self._create_button("7"), self._create_button("8"), self._create_button("9"), self._create_button("x", OPERATOR_COLOR)], spacing=10)
        row2 = ft.Row([self._create_button("4"), self._create_button("5"), self._create_button("6"), self._create_button("-", OPERATOR_COLOR)], spacing=10)
        row3 = ft.Row([self._create_button("1"), self._create_button("2"), self._create_button("3"), self._create_button("+", OPERATOR_COLOR)], spacing=10)

        # Última linha
        row4 = ft.Row(
            [
                self._create_button("Sci" if not self.scientific_mode else "Basic", SCIENTIFIC_COLOR, on_click=lambda e: self.toggle_mode(), expand=2),
                self._create_button("0", expand=2),
                self._create_button("."),
                self._create_button("=", EQUAL_COLOR, on_click=lambda e: self.calculate()),
            ], spacing=10
        )
        
        return ft.Column([row0, row1, row2, row3, row4], spacing=10)
    
    # O restante dos métodos (update_display, button_click, scientific_operation, calculate, clear_all, negate, toggle_mode)
    # permanece inalterado, pois usam variáveis de cor (BG_COLOR, etc.) que já foram corrigidas.
    
    def update_display(self):
        self.display_result.value = self.result
        self.display_expression.value = self.expression
        self.update()

    def button_click(self, e):
        btn_text = e.control.text
        
        if btn_text.isdigit() or btn_text == '.':
            if self.is_new_number or self.result == "0" or self.result == "Error":
                if btn_text == '.':
                    self.result = "0."
                elif btn_text.isdigit():
                    self.result = btn_text
                self.is_new_number = False
                
            elif btn_text == '.' and '.' not in self.result:
                self.result += btn_text
            elif btn_text.isdigit():
                self.result += btn_text
            
            self.expression += btn_text
            
        elif btn_text in ["+", "-", "x", "÷", "%"]:
            if self.result == "Error":
                self.clear_all()
                return
            
            op_map = {"x": "*", "÷": "/", "%": "/100*"} 
            op_python = op_map.get(btn_text, btn_text)
            
            self.expression = f"{self.result}{btn_text}" 
            self.is_new_number = True
        
        self.update_display()
        
    def scientific_operation(self, e):
        op = e.control.text
        if self.result == "Error":
            self.clear_all()
            return
            
        try:
            value = float(self.result)
            new_result = ""
            
            if op == "sqrt":
                if value < 0:
                    new_result = "Error: Raiz Negativa"
                else:
                    new_result = str(math.sqrt(value))
            elif op == "sin":
                new_result = str(math.sin(math.radians(value)))
            elif op == "cos":
                new_result = str(math.cos(math.radians(value)))
            elif op == "tan":
                new_result = str(math.tan(math.radians(value)))
            elif op == "log":
                if value <= 0:
                    new_result = "Error: Log Negativo/Zero"
                else:
                    new_result = str(math.log10(value))

            self.result = new_result
            self.expression = f"{op}({value}) = {new_result}"
            self.is_new_number = True
            
        except Exception:
            self.result = "Error: Cálculo Científico"
        
        self.update_display()

    def calculate(self):
        if self.result == "Error":
            self.clear_all()
            return
            
        try:
            calc_expression = self.display_result.value.replace("x", "*").replace("÷", "/")
            
            full_expression = self.expression.replace("x", "*").replace("÷", "/")
            if not full_expression: return

            import re
            match = re.search(r"(\d+\.?\d*)([\+\-\*\/])(\d+\.?\d*)", full_expression)
            
            if match:
                expression_to_eval = match.group(0).replace("x", "*").replace("÷", "/")
            else:
                expression_to_eval = self.display_result.value
            
            final_result = str(eval(expression_to_eval))
            
            if final_result.endswith(".0"):
                final_result = final_result[:-2]

            self.expression = f"{full_expression}="
            self.result = final_result
            self.is_new_number = True
            
        except ZeroDivisionError:
            self.result = "Error: Divisão por Zero"
            self.expression = ""
        except Exception:
            self.result = "Error"
            self.expression = ""
            
        self.update_display()

    def clear_all(self):
        self.result = "0"
        self.expression = ""
        self.is_new_number = True
        self.update_display()
        
    def negate(self):
        if self.result == "0" or self.result == "Error":
            return
        
        try:
            if self.result.startswith("-"):
                self.result = self.result[1:]
            else:
                self.result = "-" + self.result
                
            self.expression = self.result
            self.is_new_number = False
            self.update_display()
        except Exception:
            self.result = "Error"
            self.update_display()
            
    def toggle_mode(self):
        self.scientific_mode = not self.scientific_mode
        self.content.controls[3].controls[4] = self._create_basic_buttons().controls[-1]
        self.scientific_row.visible = self.scientific_mode
        self.update()


def main(page: ft.Page):
    page.title = "Calculadora Flet Completa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # 📌 CORREÇÃO FINAL: Usando ft.Colors.BLUE_GREY_900
    page.bgcolor = ft.Colors.BLUE_GREY_900 
    page.window_width = 400
    page.window_height = 700
    
    calc = Calculator()
    
    page.add(calc)

if __name__ == "__main__":
    ft.app(target=main)