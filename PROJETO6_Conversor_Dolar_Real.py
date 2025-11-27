import flet as ft
from flet import Colors as colors
from flet import Icons as icons
import requests
from datetime import datetime
import json
import time

# 🌍 Endpoint da AwesomeAPI
URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

def obter_cotacao_e_data():
    """Consome a API e retorna a cotação (bid) e a data de atualização."""
    try:
        resposta = requests.get(URL_API)
        resposta.raise_for_status() 
        dados = resposta.json()

        dados_usdbrl = dados.get('USDBRL', {})
        cotacao = float(dados_usdbrl.get('bid', 0.0))
        
        timestamp = int(dados_usdbrl.get('timestamp', 0))
        data_atualizacao = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')

        return cotacao, data_atualizacao

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API: {e}")
        return None, None
    except (KeyError, ValueError, json.JSONDecodeError):
        print("Erro ao processar os dados da API.")
        return None, None

def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "Conversor Dólar ↔ Real"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # --- Variáveis Globais de Cotação ---
    COTAÇÃO_ATUAL, DATA_ATUALIZACAO = obter_cotacao_e_data()

    if COTAÇÃO_ATUAL is None or COTAÇÃO_ATUAL == 0.0:
        page.add(ft.Text("❌ Não foi possível obter a cotação. Verifique sua conexão.", size=18))
        page.update()
        return

    # --- Elementos da Interface ---

    txt_valor = ft.TextField(
        label="Valor para Conversão",
        hint_text="Ex: 50.00, R$ 100, $ 20",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=300
    )

    lbl_resultado = ft.Text("Aguardando valor...", size=18, weight=ft.FontWeight.BOLD)
    
    lbl_cotacao = ft.Text(
        f"1 USD = R$ {COTAÇÃO_ATUAL:.4f}",
        size=16,
        color=colors.BLUE_700,
        weight=ft.FontWeight.BOLD
    )
    lbl_data = ft.Text(
        f"Atualizado em: {DATA_ATUALIZACAO}",
        size=12,
        color=colors.BLACK54
    )
    
    # --- Funções de Conversão e Atualização ---

    def limpar_valor_entrada(valor_str):
        """Limpa a string de entrada, removendo símbolos de moeda e trocando vírgula por ponto."""
        # Note que a limpeza ocorre APÓS a detecção no bloco principal, o que é correto.
        return valor_str.replace('R$', '').replace('$', '').replace(',', '.').strip()

    def realizar_conversao(e, direcao=None):
        valor_str = txt_valor.value
        
        try:
            valor_limpo = limpar_valor_entrada(valor_str)
            valor = float(valor_limpo)
            
            resultado = 0.0
            conversao_feita = ""
            
            detection_msg = "" # Mensagem para mostrar o resultado da detecção (somente em modo automático)
            
            # Lógica de Conversão Automática
            if direcao is None:
                # Se a string original contiver "R" ou "r", assume BRL -> USD
                is_brl_input = "R" in valor_str.upper() or "R$" in valor_str.upper()
                
                if is_brl_input:
                    direcao = 2 # BRL -> USD
                    detection_msg = " (Detectado: Real)"
                else:
                    direcao = 1 # USD -> BRL (Padrão quando a moeda é ambígua/não especificada)
                    detection_msg = " (Detectado: Dólar - Padrão)" # Indica o padrão

            if direcao == 1: # USD -> BRL
                resultado = valor * COTAÇÃO_ATUAL
                conversao_feita = f"💵 ${valor:.2f} ↔ **R$ {resultado:.2f}** 💰{detection_msg}"
            
            elif direcao == 2: # BRL -> USD
                resultado = valor / COTAÇÃO_ATUAL
                conversao_feita = f"💰 R$ {valor:.2f} ↔ **${resultado:.2f}** 💵{detection_msg}"
                
            lbl_resultado.value = conversao_feita
            lbl_resultado.color = colors.GREEN_700

        except ValueError:
            lbl_resultado.value = "⚠️ Erro: Digite um valor numérico válido."
            lbl_resultado.color = colors.RED_700
        except Exception:
            lbl_resultado.value = "❌ Ocorreu um erro inesperado."
            lbl_resultado.color = colors.RED_700
            
        page.update()

    # --- Botões de Ação ---
    
    btn_auto = ft.ElevatedButton(
        text="Conversão Automática",
        icon=icons.AUTO_MODE_OUTLINED,
        on_click=lambda e: realizar_conversao(e, direcao=None),
        width=300
    )
    
    btn_usd_brl = ft.OutlinedButton(
        text="USD → BRL",
        icon=icons.ARROW_DOWNWARD_SHARP,
        on_click=lambda e: realizar_conversao(e, direcao=1),
    )
    
    btn_brl_usd = ft.OutlinedButton(
        text="BRL → USD",
        icon=icons.ARROW_UPWARD_SHARP,
        on_click=lambda e: realizar_conversao(e, direcao=2),
    )


    # --- Layout Final ---
    
    cabecalho = ft.Container(
        content=ft.Column(
            [
                ft.Text("Conversor de Câmbio", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=5, color=colors.BLUE_GREY_100),
                lbl_cotacao,
                lbl_data,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        margin=ft.margin.only(bottom=20),
        bgcolor=colors.BLUE_GREY_50,
        border_radius=10,
    )


    # Adicionar todos os componentes à página
    page.add(
        cabecalho,
        txt_valor,
        ft.Container(height=10),
        btn_auto,
        ft.Row(
            [btn_usd_brl, btn_brl_usd],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        ft.Container(height=30),
        ft.Text("Resultado:", size=14, color=colors.GREY),
        lbl_resultado,
    )

ft.app(target=main)