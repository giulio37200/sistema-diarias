#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Geração de Planilha Excel - Controle de Diárias
Gera planilha Excel completa com dados, gráficos e formatação profissional
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

class ExcelGenerator:
    def __init__(self):
        self.workbook = None
        self.data = []
        self.credit_data = {}
        
    def load_data_from_js(self):
        """Carrega dados do sistema JavaScript"""
        try:
            # Dados de exemplo (em produção, viria do localStorage ou API)
            self.data = [
                {
                    "data": "2025-01-02",
                    "diaSemana": "Quinta-feira",
                    "mes": "Janeiro",
                    "ano": 2025,
                    "valorUSD": 250,
                    "statusPagamento": "A Pagar",
                    "localProjeto": "Projeto Alpha"
                },
                {
                    "data": "2025-01-03",
                    "diaSemana": "Sexta-feira",
                    "mes": "Janeiro",
                    "ano": 2025,
                    "valorUSD": 250,
                    "statusPagamento": "Pago",
                    "localProjeto": "Projeto Alpha"
                },
                {
                    "data": "2025-01-08",
                    "diaSemana": "Quarta-feira",
                    "mes": "Janeiro",
                    "ano": 2025,
                    "valorUSD": 250,
                    "statusPagamento": "A Pagar",
                    "localProjeto": "Projeto Beta"
                }
            ]
            
            self.credit_data = {
                "deposits": [
                    {
                        "id": 1,
                        "date": "2025-01-01",
                        "amount": 5000,
                        "description": "Pagamento antecipado Janeiro"
                    }
                ],
                "totalDeposited": 5000,
                "totalUsed": 750,
                "currentBalance": 4250
            }
            
            print("✅ Dados carregados com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def create_workbook(self, filename="Controle_Diarias_Completo.xlsx"):
        """Cria o arquivo Excel com múltiplas abas"""
        try:
            self.workbook = xlsxwriter.Workbook(filename)
            
            # Definir formatos
            self.formats = {
                'header': self.workbook.add_format({
                    'bold': True,
                    'font_size': 12,
                    'bg_color': '#4299e1',
                    'font_color': 'white',
                    'align': 'center',
                    'valign': 'vcenter',
                    'border': 1
                }),
                'title': self.workbook.add_format({
                    'bold': True,
                    'font_size': 16,
                    'font_color': '#2d3748',
                    'align': 'center'
                }),
                'subtitle': self.workbook.add_format({
                    'font_size': 12,
                    'font_color': '#4a5568',
                    'align': 'center'
                }),
                'currency': self.workbook.add_format({
                    'num_format': '$#,##0',
                    'align': 'right'
                }),
                'date': self.workbook.add_format({
                    'num_format': 'dd/mm/yyyy',
                    'align': 'center'
                }),
                'center': self.workbook.add_format({
                    'align': 'center',
                    'valign': 'vcenter'
                }),
                'pago': self.workbook.add_format({
                    'bg_color': '#c6f6d5',
                    'font_color': '#22543d',
                    'align': 'center',
                    'bold': True
                }),
                'a_pagar': self.workbook.add_format({
                    'bg_color': '#fed7aa',
                    'font_color': '#9c4221',
                    'align': 'center',
                    'bold': True
                }),
                'kpi_value': self.workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'font_color': '#2d3748',
                    'align': 'center'
                }),
                'kpi_label': self.workbook.add_format({
                    'font_size': 10,
                    'font_color': '#4a5568',
                    'align': 'center'
                })
            }
            
            print("✅ Workbook criado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar workbook: {e}")
            return False
    
    def create_dashboard_sheet(self):
        """Cria aba do dashboard com KPIs e resumos"""
        try:
            worksheet = self.workbook.add_worksheet('Dashboard')
            
            # Configurar largura das colunas
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:F', 12)
            worksheet.set_column('G:G', 20)
            
            # Título principal
            worksheet.merge_range('A1:G1', '💰 DASHBOARD - CONTROLE DE DIÁRIAS', self.formats['title'])
            worksheet.merge_range('A2:G2', f'Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', self.formats['subtitle'])
            
            # Calcular KPIs
            total_dias = len(self.data)
            total_valor = total_dias * 250
            dias_pagos = len([d for d in self.data if d['statusPagamento'] == 'Pago'])
            valor_pago = dias_pagos * 250
            dias_a_pagar = total_dias - dias_pagos
            valor_a_pagar = dias_a_pagar * 250
            percentual_pago = (dias_pagos / total_dias * 100) if total_dias > 0 else 0
            
            # KPIs principais
            row = 4
            kpis = [
                ('Total de Dias', total_dias, ''),
                ('Valor Total', total_valor, '$'),
                ('Dias Pagos', dias_pagos, ''),
                ('Valor Pago', valor_pago, '$'),
                ('Dias A Pagar', dias_a_pagar, ''),
                ('Valor A Pagar', valor_a_pagar, '$'),
                ('% Pago', f'{percentual_pago:.1f}%', '')
            ]
            
            # Cabeçalho dos KPIs
            worksheet.write(row, 0, 'INDICADORES PRINCIPAIS', self.formats['header'])
            worksheet.write(row, 1, 'VALOR', self.formats['header'])
            row += 1
            
            for label, value, prefix in kpis:
                worksheet.write(row, 0, label, self.formats['kpi_label'])
                if prefix == '$':
                    worksheet.write(row, 1, value, self.formats['currency'])
                else:
                    worksheet.write(row, 1, value, self.formats['kpi_value'])
                row += 1
            
            # Sistema de Créditos
            row += 2
            worksheet.write(row, 0, 'SISTEMA DE CRÉDITOS', self.formats['header'])
            worksheet.write(row, 1, 'VALOR', self.formats['header'])
            row += 1
            
            credit_kpis = [
                ('Total Depositado', self.credit_data['totalDeposited'], '$'),
                ('Total Usado', self.credit_data['totalUsed'], '$'),
                ('Saldo Atual', self.credit_data['currentBalance'], '$'),
                ('Dias Restantes', int(self.credit_data['currentBalance'] / 250), '')
            ]
            
            for label, value, prefix in credit_kpis:
                worksheet.write(row, 0, label, self.formats['kpi_label'])
                if prefix == '$':
                    worksheet.write(row, 1, value, self.formats['currency'])
                else:
                    worksheet.write(row, 1, value, self.formats['kpi_value'])
                row += 1
            
            # Resumo por mês
            row += 2
            worksheet.write(row, 4, 'RESUMO MENSAL', self.formats['header'])
            worksheet.write(row, 5, 'DIAS', self.formats['header'])
            worksheet.write(row, 6, 'VALOR', self.formats['header'])
            row += 1
            
            # Agrupar por mês
            monthly_data = {}
            for item in self.data:
                month = item['mes']
                if month not in monthly_data:
                    monthly_data[month] = {'dias': 0, 'valor': 0}
                monthly_data[month]['dias'] += 1
                monthly_data[month]['valor'] += item['valorUSD']
            
            for month, data in monthly_data.items():
                worksheet.write(row, 4, month, self.formats['center'])
                worksheet.write(row, 5, data['dias'], self.formats['center'])
                worksheet.write(row, 6, data['valor'], self.formats['currency'])
                row += 1
            
            print("✅ Aba Dashboard criada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar aba Dashboard: {e}")
            return False
    
    def create_data_sheet(self):
        """Cria aba com dados detalhados"""
        try:
            worksheet = self.workbook.add_worksheet('Dados Detalhados')
            
            # Configurar largura das colunas
            worksheet.set_column('A:A', 12)  # Data
            worksheet.set_column('B:B', 15)  # Dia da Semana
            worksheet.set_column('C:C', 12)  # Mês
            worksheet.set_column('D:D', 8)   # Ano
            worksheet.set_column('E:E', 12)  # Valor
            worksheet.set_column('F:F', 15)  # Status
            worksheet.set_column('G:G', 20)  # Projeto
            
            # Título
            worksheet.merge_range('A1:G1', 'DADOS DETALHADOS DAS DIÁRIAS', self.formats['title'])
            
            # Cabeçalhos
            headers = ['Data', 'Dia da Semana', 'Mês', 'Ano', 'Valor (USD)', 'Status Pagamento', 'Projeto']
            for col, header in enumerate(headers):
                worksheet.write(2, col, header, self.formats['header'])
            
            # Dados
            for row, item in enumerate(self.data, start=3):
                # Converter data para formato Excel
                date_obj = datetime.strptime(item['data'], '%Y-%m-%d')
                
                worksheet.write_datetime(row, 0, date_obj, self.formats['date'])
                worksheet.write(row, 1, item['diaSemana'], self.formats['center'])
                worksheet.write(row, 2, item['mes'], self.formats['center'])
                worksheet.write(row, 3, item['ano'], self.formats['center'])
                worksheet.write(row, 4, item['valorUSD'], self.formats['currency'])
                
                # Status com formatação condicional
                status_format = self.formats['pago'] if item['statusPagamento'] == 'Pago' else self.formats['a_pagar']
                worksheet.write(row, 5, item['statusPagamento'], status_format)
                
                worksheet.write(row, 6, item['localProjeto'], self.formats['center'])
            
            # Adicionar totais
            last_row = len(self.data) + 3
            worksheet.write(last_row, 3, 'TOTAL:', self.formats['header'])
            worksheet.write_formula(last_row, 4, f'=SUM(E4:E{last_row-1})', self.formats['currency'])
            
            print("✅ Aba Dados Detalhados criada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar aba Dados Detalhados: {e}")
            return False
    
    def create_credits_sheet(self):
        """Cria aba do sistema de créditos"""
        try:
            worksheet = self.workbook.add_worksheet('Sistema de Créditos')
            
            # Configurar largura das colunas
            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 12)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 15)
            
            # Título
            worksheet.merge_range('A1:D1', '💰 SISTEMA DE CRÉDITOS ANTECIPADOS', self.formats['title'])
            
            # Resumo de créditos
            row = 3
            worksheet.write(row, 0, 'RESUMO GERAL', self.formats['header'])
            worksheet.write(row, 1, 'VALOR', self.formats['header'])
            row += 1
            
            credit_summary = [
                ('Total Depositado', self.credit_data['totalDeposited']),
                ('Total Usado', self.credit_data['totalUsed']),
                ('Saldo Atual', self.credit_data['currentBalance']),
                ('Dias Disponíveis', int(self.credit_data['currentBalance'] / 250))
            ]
            
            for label, value in credit_summary:
                worksheet.write(row, 0, label, self.formats['kpi_label'])
                if 'Dias' not in label:
                    worksheet.write(row, 1, value, self.formats['currency'])
                else:
                    worksheet.write(row, 1, value, self.formats['kpi_value'])
                row += 1
            
            # Histórico de depósitos
            row += 2
            worksheet.write(row, 0, 'HISTÓRICO DE DEPÓSITOS', self.formats['header'])
            worksheet.write(row, 1, 'DATA', self.formats['header'])
            worksheet.write(row, 2, 'DESCRIÇÃO', self.formats['header'])
            worksheet.write(row, 3, 'VALOR', self.formats['header'])
            row += 1
            
            for deposit in self.credit_data['deposits']:
                worksheet.write(row, 0, f"Depósito #{deposit['id']}", self.formats['center'])
                
                # Converter data
                date_obj = datetime.strptime(deposit['date'], '%Y-%m-%d')
                worksheet.write_datetime(row, 1, date_obj, self.formats['date'])
                
                worksheet.write(row, 2, deposit['description'], self.formats['center'])
                worksheet.write(row, 3, deposit['amount'], self.formats['currency'])
                row += 1
            
            # Total de depósitos
            if self.credit_data['deposits']:
                worksheet.write(row, 2, 'TOTAL DEPOSITADO:', self.formats['header'])
                worksheet.write_formula(row, 3, f'=SUM(D{row-len(self.credit_data["deposits"])}:D{row-1})', self.formats['currency'])
            
            print("✅ Aba Sistema de Créditos criada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar aba Sistema de Créditos: {e}")
            return False
    
    def create_charts_sheet(self):
        """Cria aba com gráficos"""
        try:
            worksheet = self.workbook.add_worksheet('Gráficos')
            
            # Título
            worksheet.merge_range('A1:H1', '📊 GRÁFICOS E ANÁLISES', self.formats['title'])
            
            # Preparar dados para gráficos
            # Gráfico de status (Pizza)
            status_data = {}
            for item in self.data:
                status = item['statusPagamento']
                if status not in status_data:
                    status_data[status] = 0
                status_data[status] += item['valorUSD']
            
            # Criar gráfico de pizza
            chart_pie = self.workbook.add_chart({'type': 'pie'})
            
            # Dados para o gráfico (criar tabela temporária)
            row = 3
            worksheet.write(row, 0, 'Status', self.formats['header'])
            worksheet.write(row, 1, 'Valor', self.formats['header'])
            row += 1
            
            start_row = row
            for status, valor in status_data.items():
                worksheet.write(row, 0, status)
                worksheet.write(row, 1, valor)
                row += 1
            end_row = row - 1
            
            # Configurar gráfico de pizza
            chart_pie.add_series({
                'categories': f'=Gráficos!$A${start_row+1}:$A${end_row+1}',
                'values': f'=Gráficos!$B${start_row+1}:$B${end_row+1}',
                'data_labels': {'percentage': True},
            })
            
            chart_pie.set_title({'name': 'Distribuição por Status de Pagamento'})
            chart_pie.set_style(10)
            
            # Inserir gráfico
            worksheet.insert_chart('D3', chart_pie, {'x_scale': 1.2, 'y_scale': 1.2})
            
            # Gráfico mensal (Coluna)
            monthly_data = {}
            for item in self.data:
                month = item['mes']
                if month not in monthly_data:
                    monthly_data[month] = 0
                monthly_data[month] += item['valorUSD']
            
            # Dados para gráfico mensal
            row += 3
            worksheet.write(row, 0, 'Mês', self.formats['header'])
            worksheet.write(row, 1, 'Valor Total', self.formats['header'])
            row += 1
            
            start_row_monthly = row
            for month, valor in monthly_data.items():
                worksheet.write(row, 0, month)
                worksheet.write(row, 1, valor)
                row += 1
            end_row_monthly = row - 1
            
            # Criar gráfico de colunas
            chart_column = self.workbook.add_chart({'type': 'column'})
            
            chart_column.add_series({
                'categories': f'=Gráficos!$A${start_row_monthly+1}:$A${end_row_monthly+1}',
                'values': f'=Gráficos!$B${start_row_monthly+1}:$B${end_row_monthly+1}',
                'name': 'Valor Mensal',
            })
            
            chart_column.set_title({'name': 'Valores por Mês'})
            chart_column.set_x_axis({'name': 'Mês'})
            chart_column.set_y_axis({'name': 'Valor (USD)', 'num_format': '$#,##0'})
            chart_column.set_style(11)
            
            # Inserir gráfico
            worksheet.insert_chart('D18', chart_column, {'x_scale': 1.2, 'y_scale': 1.2})
            
            print("✅ Aba Gráficos criada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar aba Gráficos: {e}")
            return False
    
    def generate_excel(self, filename="Controle_Diarias_Completo.xlsx"):
        """Gera o arquivo Excel completo"""
        try:
            print("🚀 Iniciando geração do Excel...")
            
            # Carregar dados
            if not self.load_data_from_js():
                return False
            
            # Criar workbook
            if not self.create_workbook(filename):
                return False
            
            # Criar abas
            self.create_dashboard_sheet()
            self.create_data_sheet()
            self.create_credits_sheet()
            self.create_charts_sheet()
            
            # Fechar workbook
            self.workbook.close()
            
            print(f"✅ Arquivo Excel gerado com sucesso: {filename}")
            print(f"📁 Localização: {os.path.abspath(filename)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar Excel: {e}")
            return False

def main():
    """Função principal"""
    generator = ExcelGenerator()
    
    # Gerar arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Controle_Diarias_{timestamp}.xlsx"
    
    success = generator.generate_excel(filename)
    
    if success:
        print("\n🎉 EXCEL GERADO COM SUCESSO!")
        print("📋 O arquivo contém:")
        print("  • Dashboard com KPIs principais")
        print("  • Dados detalhados das diárias")
        print("  • Sistema de créditos antecipados")
        print("  • Gráficos e análises visuais")
        print("  • Formatação profissional")
    else:
        print("\n❌ ERRO NA GERAÇÃO DO EXCEL")

if __name__ == "__main__":
    main()