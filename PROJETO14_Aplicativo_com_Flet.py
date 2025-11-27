import flet as ft
from flet import Icons as icons

# --- Constantes de Estilo para um tema limpo e moderno ---
PRIMARY_COLOR = ft.Colors.BLUE_500
ACCENT_COLOR = ft.Colors.CYAN_400
BG_COLOR = ft.Colors.BLUE_GREY_900
CARD_BG_COLOR = ft.Colors.BLUE_GREY_800
TEXT_COLOR = ft.Colors.WHITE
SUBTEXT_COLOR = ft.Colors.WHITE70

class ReadingGoalTracker(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            bgcolor=BG_COLOR,
            padding=20,
        )
        
        self.goals = []
        self.page_controls = {}

        # --- Componentes da Interface ---
        self.title_input = ft.TextField(
            label="Título do Livro",
            hint_text="Ex: O Senhor dos Anéis",
            color=TEXT_COLOR,
            bgcolor=CARD_BG_COLOR,
            border_radius=10,
            border_color=PRIMARY_COLOR,
            cursor_color=ACCENT_COLOR,
            label_style=ft.TextStyle(color=SUBTEXT_COLOR),
            width=300,
        )

        self.pages_input = ft.TextField(
            label="Total de Páginas",
            hint_text="Ex: 500",
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_COLOR,
            bgcolor=CARD_BG_COLOR,
            border_radius=10,
            border_color=PRIMARY_COLOR,
            label_style=ft.TextStyle(color=SUBTEXT_COLOR),
            width=150,
        )

        self.add_button = ft.ElevatedButton(
            text="Adicionar Meta",
            icon=ft.Icons.ADD_ROUNDED,
            on_click=self.add_goal,
            bgcolor=PRIMARY_COLOR,
            color=TEXT_COLOR,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            expand=True
        )

        self.goals_list = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=15,
            expand=True
        )
        
        # Display de Resumo
        self.total_pages_read_display = ft.Text("Páginas Lidas: 0", size=16, color=TEXT_COLOR)
        self.goals_summary_display = ft.Text("Metas Ativas: 0", size=16, color=TEXT_COLOR)
        self.completed_goals_display = ft.Text("Concluídas: 0", size=16, color=ACCENT_COLOR)
        
        self.page_controls['total_read'] = self.total_pages_read_display
        self.page_controls['goals_summary'] = self.goals_summary_display
        self.page_controls['completed_goals'] = self.completed_goals_display
        
        # --- Componente NOVO: Diálogo de Celebração (Compatível) ---
        self.celebration_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=CARD_BG_COLOR,
            title=ft.Text("🎉 Parabéns! Livro Finalizado! 🎉", color=ACCENT_COLOR, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Ícone estático (sem as transformações que causavam erro)
                        ft.Icon(
                            ft.Icons.STAR_HALF_ROUNDED, 
                            size=150, 
                            color=ft.Colors.YELLOW_ACCENT_400,
                        ),
                        ft.Text("Você atingiu sua meta de leitura!", color=TEXT_COLOR, size=18)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                height=250,
                width=300
            ),
            actions=[
                ft.TextButton("Obrigado!", on_click=lambda e: self.close_celebration_dialog(e)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )


        # Estrutura do Layout
        self.content = ft.Column(
            controls=[
                # Título Principal
                ft.Text("📊 Controle de Leitura", size=32, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                
                # Resumo
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, 
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                [
                                    self.total_pages_read_display, 
                                    ft.VerticalDivider(color=SUBTEXT_COLOR, width=1),
                                    self.goals_summary_display,
                                    ft.VerticalDivider(color=SUBTEXT_COLOR, width=1), 
                                    self.completed_goals_display
                                ], 
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                                wrap=True
                            ),
                            padding=15,
                            bgcolor=CARD_BG_COLOR,
                            border_radius=15,
                            width=500
                        )
                    ]
                ),

                ft.Divider(color=SUBTEXT_COLOR),

                # Seção de Adicionar Nova Meta
                ft.Column(
                    controls=[
                        ft.Row([self.title_input, self.pages_input], spacing=10, wrap=True, alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self.add_button], alignment=ft.MainAxisAlignment.CENTER, width=500),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),

                ft.Divider(color=SUBTEXT_COLOR),

                # Lista de Metas (Expansível)
                ft.Text("Minhas Metas", size=24, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                self.goals_list,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
    def show_celebration_dialog(self):
        """Exibe o diálogo de celebração (Sem animação, para compatibilidade)."""
        if self.page:
            if self.celebration_dialog not in self.page.overlay:
                self.page.overlay.append(self.celebration_dialog)
            
            # --- CÓDIGO DE ANIMAÇÃO REMOVIDO PARA COMPATIBILIDADE ---
            
            self.celebration_dialog.open = True
            self.page.update()

    def close_celebration_dialog(self, e):
        """Fecha o diálogo de celebração."""
        if self.page:
            self.celebration_dialog.open = False
            self.page.update()

    def add_goal(self, e):
        """Adiciona uma nova meta de leitura à lista."""
        title = self.title_input.value
        pages_str = self.pages_input.value
        
        if not title or not pages_str:
            self.show_message("Por favor, preencha o título e o total de páginas.", ft.Colors.RED_ACCENT)
            return

        try:
            total_pages = int(pages_str)
            if total_pages <= 0:
                raise ValueError
        except ValueError:
            self.show_message("Total de Páginas deve ser um número inteiro positivo.", ft.Colors.RED_ACCENT)
            return

        # Cria o objeto GoalCard
        new_goal = GoalCard(
            title=title,
            total_pages=total_pages,
            remove_callback=self.remove_goal,
            update_summary_callback=self.update_summary,
            show_celebration_callback=self.show_celebration_dialog,
            bg_color=CARD_BG_COLOR,
            primary_color=PRIMARY_COLOR,
            text_color=TEXT_COLOR,
        )
        
        self.goals.append(new_goal)
        self.goals_list.controls.insert(0, new_goal)
        
        # Limpa os campos
        self.title_input.value = ""
        self.pages_input.value = ""
        
        self.update_summary()
        self.update()
        
    def remove_goal(self, goal_card):
        """Remove uma meta da lista."""
        self.goals.remove(goal_card)
        self.goals_list.controls.remove(goal_card)
        self.update_summary()
        self.update()

    def update_summary(self):
        """Atualiza os displays de resumo com os dados totais."""
        total_pages_read = 0
        active_goals = 0
        completed_goals = 0

        for goal in self.goals:
            total_pages_read += goal.read_pages
            if goal.is_completed:
                completed_goals += 1
            else:
                active_goals += 1
        
        self.total_pages_read_display.value = f"Páginas Lidas: {total_pages_read}"
        self.goals_summary_display.value = f"Metas Ativas: {active_goals}"
        self.completed_goals_display.value = f"Concluídas: {completed_goals}"
        
        if self.page: 
            self.page.update()

    def show_message(self, message, color):
        """Exibe uma mensagem temporária na parte inferior (snackbar)."""
        if self.page: 
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message, color=ft.Colors.WHITE),
                bgcolor=color,
                duration=3000,
            )
            self.page.snack_bar.open = True
            self.page.update()


class GoalCard(ft.Container):
    """Componente reutilizável para exibir e interagir com uma meta de leitura individual."""
    def __init__(self, title, total_pages, remove_callback, update_summary_callback, show_celebration_callback, bg_color, primary_color, text_color):
        super().__init__(
            padding=15,
            bgcolor=bg_color,
            border_radius=15,
            width=500
        )
        self.title = title
        self.total_pages = total_pages
        self.read_pages = 0
        self.is_completed = False
        self.remove_callback = remove_callback
        self.update_summary_callback = update_summary_callback
        self.show_celebration_callback = show_celebration_callback
        self.primary_color = primary_color
        self.text_color = text_color
        
        # --- Controles Visuais ---
        self.title_text = ft.Text(
            self.title, 
            size=18, 
            weight=ft.FontWeight.BOLD, 
            color=text_color, 
            overflow=ft.TextOverflow.ELLIPSIS,
            expand=True
        )
        
        self.progress_text = ft.Text(f"0 / {self.total_pages} páginas", size=14, color=SUBTEXT_COLOR)
        self.progress_bar = ft.ProgressBar(value=0, color=ACCENT_COLOR, bgcolor=ft.Colors.BLUE_GREY_700, height=10)
        
        self.add_progress_input = ft.TextField(
            hint_text="Páginas lidas",
            width=120,
            height=40,
            content_padding=5,
            text_size=12,
            keyboard_type=ft.KeyboardType.NUMBER,
            color=TEXT_COLOR,
            bgcolor=ft.Colors.BLUE_GREY_700,
            border_radius=5,
            border=ft.InputBorder.NONE
        )

        self.log_progress_button = ft.IconButton(
            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
            tooltip="Registrar Progresso",
            on_click=self.log_progress,
            icon_color=primary_color,
            data=self,
        )
        
        self.remove_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
            tooltip="Remover Meta",
            on_click=lambda e: self.remove_callback(self),
            icon_color=ft.Colors.RED_400
        )
        
        # --- Layout do Card ---
        self.content = ft.Column(
            controls=[
                # Linha 1: Título e Botão de Remover
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.BOOK, color=primary_color),
                        self.title_text,
                        self.remove_button,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                
                # Linha 2: Barra de Progresso e Texto
                ft.Column(
                    controls=[
                        self.progress_bar,
                        self.progress_text,
                    ],
                    spacing=5
                ),
                
                # Linha 3: Adicionar Progresso
                ft.Row(
                    controls=[
                        ft.Text("Registrar leitura:", size=14, color=text_color),
                        self.add_progress_input,
                        self.log_progress_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
            ],
            spacing=10
        )

    def log_progress(self, e):
        """
        Função para adicionar páginas lidas e chamar a celebração se concluído.
        """
        if not self.page: return

        try:
            pages_to_add = int(self.add_progress_input.value or 0)
            if pages_to_add <= 0:
                raise ValueError("Deve adicionar pelo menos 1 página.")
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Entrada inválida. Use um número inteiro positivo.", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_ACCENT,
                duration=3000,
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        new_total = self.read_pages + pages_to_add
        
        # Estado antes de atualizar
        was_not_completed = not self.is_completed
        
        if new_total >= self.total_pages:
            new_total = self.total_pages
            
            if was_not_completed:
                self.is_completed = True 
                
                # CHAMA A CELEBRAÇÃO (agora sem animação)
                self.show_celebration_callback()

        self.read_pages = new_total
        
        # Atualiza a UI do Card
        self.progress_text.value = f"{self.read_pages} / {self.total_pages} páginas"
        self.progress_bar.value = self.read_pages / self.total_pages
        
        # Limpa o input
        self.add_progress_input.value = ""
        
        # Desabilita se completo
        if self.read_pages == self.total_pages:
            self.log_progress_button.disabled = True
            self.add_progress_input.disabled = True
            self.add_progress_input.hint_text = "Completo!"
        
        # Atualiza o Card
        self.update()
        
        # Atualiza o Resumo Geral
        self.update_summary_callback()


def main(page: ft.Page):
    page.title = "Controle de Metas de Leitura"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = BG_COLOR
    page.window_min_width = 500
    page.window_min_height = 600
    page.theme_mode = ft.ThemeMode.DARK

    page_content = ft.Container(
        content=ReadingGoalTracker(),
        width=550,
        height=700,
        padding=0
    )
    
    page.add(
        ft.Row(
            [page_content],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)