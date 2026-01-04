import pandas as pd
import xlsxwriter
from datetime import datetime, timedelta
import os

def create_daily_allowance_excel():
    """Criar planilha Excel profissional para controle de diárias (versão simplificada)"""
    
    # Carregar dados simplificados
    df = pd.read_csv('diarias_data_simplified.csv')
    
    # Converter coluna de data
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Criar arquivo Excel
    filename = 'Controle_Diarias_Alimentacao_v2.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    
    # Definir formatos
    formats = create_formats(workbook)
    
    # Criar worksheets
    create_dashboard_sheet(workbook, df, formats)
    create_data_sheet(workbook, df, formats)
    create_monthly_summary_sheet(workbook, df, formats)
    create_project_summary_sheet(workbook, df, formats)
    create_payment_control_sheet(workbook, df, formats)
    create_calendar_template_sheet(workbook, formats)
    
    workbook.close()
    print(f"Planilha criada: {filename}")
    return filename

def create_formats(workbook):
    """Criar formatos para a planilha"""
    formats = {}
    
    # Formato do cabeçalho
    formats['header'] = workbook.add_format({
        'bold': True,
        'font_color': '#FFF6F0',
        'bg_color': '#692927',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 11
    })
    
    # Formato de título
    formats['title'] = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'font_color': '#411B38',
        'align': 'center',
        'valign': 'vcenter'
    })
    
    # Formato de subtítulo
    formats['subtitle'] = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'font_color': '#411B38',
        'align': 'left',
        'valign': 'vcenter'
    })
    
    # Formato de dados
    formats['data'] = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    
    # Formato de moeda
    formats['currency'] = workbook.add_format({
        'num_format': '$#,##0',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    
    # Formato de data
    formats['date'] = workbook.add_format({
        'num_format': 'dd/mm/yyyy',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    
    # Formato para status pago
    formats['status_pago'] = workbook.add_format({
        'bg_color': '#d4edda',
        'font_color': '#155724',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'bold': True
    })
    
    # Formato para status a pagar
    formats['status_a_pagar'] = workbook.add_format({
        'bg_color': '#fff3cd',
        'font_color': '#856404',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'bold': True
    })
    
    # Formato KPI
    formats['kpi_value'] = workbook.add_format({
        'bold': True,
        'font_size': 18,
        'font_color': '#692927',
        'align': 'center',
        'valign': 'vcenter'
    })
    
    formats['kpi_label'] = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'font_color': '#411B38',
        'align': 'center',
        'valign': 'vcenter'
    })
    
    # Formato para calendário
    formats['calendar_day'] = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10
    })
    
    formats['calendar_worked'] = workbook.add_format({
        'bg_color': '#fff3cd',
        'font_color': '#856404',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'bold': True
    })
    
    formats['calendar_paid'] = workbook.add_format({
        'bg_color': '#d4edda',
        'font_color': '#155724',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'bold': True
    })
    
    return formats

def create_dashboard_sheet(workbook, df, formats):
    """Criar aba Dashboard"""
    worksheet = workbook.add_worksheet('Dashboard')
    worksheet.set_column('A:H', 15)
    
    # Título
    worksheet.merge_range('A1:H1', 'CONTROLE DE DIÁRIAS DE ALIMENTAÇÃO', formats['title'])
    worksheet.merge_range('A2:H2', 'Dashboard Executivo - Versão Simplificada', formats['subtitle'])
    
    # KPIs principais
    row = 4
    
    # Calcular KPIs
    total_dias = len(df)
    total_valor = total_dias * 250
    dias_pagos = len(df[df['Status_Pagamento'] == 'Pago'])
    valor_pago = dias_pagos * 250
    dias_a_pagar = len(df[df['Status_Pagamento'] == 'A Pagar'])
    valor_a_pagar = dias_a_pagar * 250
    percentual_pago = (dias_pagos / total_dias * 100) if total_dias > 0 else 0
    
    # Escrever KPIs
    kpis = [
        ('Total de Dias', total_dias),
        ('Valor Total', f'${total_valor:,}'),
        ('Dias Pagos', dias_pagos),
        ('Valor Pago', f'${valor_pago:,}'),
        ('Dias A Pagar', dias_a_pagar),
        ('Valor A Pagar', f'${valor_a_pagar:,}'),
        ('% Pago', f'{percentual_pago:.1f}%'),
        ('Valor Diário', '$250')
    ]
    
    col = 0
    for label, value in kpis:
        worksheet.write(row, col, label, formats['kpi_label'])
        worksheet.write(row + 1, col, value, formats['kpi_value'])
        col += 1
    
    # Resumo mensal
    row = 8
    worksheet.write(row, 0, 'RESUMO MENSAL', formats['subtitle'])
    row += 1
    
    # Cabeçalhos
    headers = ['Mês', 'Total Dias', 'Valor Total', 'Dias Pagos', 'Valor Pago', 'Dias A Pagar', 'Valor A Pagar', '% Pago']
    for col, header in enumerate(headers):
        worksheet.write(row, col, header, formats['header'])
    
    # Dados mensais
    monthly_summary = df.groupby('Mes').agg({
        'Data': 'count',
        'Valor_USD': 'sum',
        'Status_Pagamento': lambda x: (x == 'Pago').sum()
    }).reset_index()
    
    monthly_summary.columns = ['Mes', 'Total_Dias', 'Valor_Total', 'Dias_Pagos']
    monthly_summary['Valor_Pago'] = monthly_summary['Dias_Pagos'] * 250
    monthly_summary['Dias_A_Pagar'] = monthly_summary['Total_Dias'] - monthly_summary['Dias_Pagos']
    monthly_summary['Valor_A_Pagar'] = monthly_summary['Dias_A_Pagar'] * 250
    monthly_summary['Percentual_Pago'] = (monthly_summary['Dias_Pagos'] / monthly_summary['Total_Dias'] * 100).round(1)
    
    row += 1
    for idx, month_data in monthly_summary.iterrows():
        worksheet.write(row, 0, month_data['Mes'], formats['data'])
        worksheet.write(row, 1, month_data['Total_Dias'], formats['data'])
        worksheet.write(row, 2, month_data['Valor_Total'], formats['currency'])
        worksheet.write(row, 3, month_data['Dias_Pagos'], formats['data'])
        worksheet.write(row, 4, month_data['Valor_Pago'], formats['currency'])
        worksheet.write(row, 5, month_data['Dias_A_Pagar'], formats['data'])
        worksheet.write(row, 6, month_data['Valor_A_Pagar'], formats['currency'])
        worksheet.write(row, 7, f"{month_data['Percentual_Pago']:.1f}%", formats['data'])
        row += 1
    
    # Criar gráfico de barras
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'name': 'Valor Pago',
        'categories': f'=Dashboard!$A${10}:$A${9+len(monthly_summary)}',
        'values': f'=Dashboard!$E${10}:$E${9+len(monthly_summary)}',
        'fill': {'color': '#692927'}
    })
    chart.add_series({
        'name': 'Valor A Pagar',
        'categories': f'=Dashboard!$A${10}:$A${9+len(monthly_summary)}',
        'values': f'=Dashboard!$G${10}:$G${9+len(monthly_summary)}',
        'fill': {'color': '#c3a788'}
    })
    chart.set_title({'name': 'Valores Mensais - Pago vs A Pagar'})
    chart.set_x_axis({'name': 'Mês'})
    chart.set_y_axis({'name': 'Valor (USD)'})
    chart.set_size({'width': 600, 'height': 400})
    worksheet.insert_chart('A16', chart)

def create_data_sheet(workbook, df, formats):
    """Criar aba com dados detalhados"""
    worksheet = workbook.add_worksheet('Dados Detalhados')
    
    # Configurar larguras das colunas
    worksheet.set_column('A:A', 12)  # Data
    worksheet.set_column('B:B', 15)  # Dia da Semana
    worksheet.set_column('C:C', 12)  # Mês
    worksheet.set_column('D:D', 8)   # Ano
    worksheet.set_column('E:E', 12)  # Valor
    worksheet.set_column('F:F', 15)  # Status
    worksheet.set_column('G:G', 20)  # Projeto
    
    # Título
    worksheet.merge_range('A1:G1', 'DADOS DETALHADOS DAS DIÁRIAS', formats['title'])
    
    # Cabeçalhos
    headers = ['Data', 'Dia da Semana', 'Mês', 'Ano', 'Valor (USD)', 'Status Pagamento', 'Local/Projeto']
    
    for col, header in enumerate(headers):
        worksheet.write(2, col, header, formats['header'])
    
    # Dados
    for row, (idx, data) in enumerate(df.iterrows(), start=3):
        worksheet.write_datetime(row, 0, data['Data'], formats['date'])
        worksheet.write(row, 1, data['Dia_Semana'], formats['data'])
        worksheet.write(row, 2, data['Mes'], formats['data'])
        worksheet.write(row, 3, data['Ano'], formats['data'])
        worksheet.write(row, 4, data['Valor_USD'], formats['currency'])
        
        # Status com formatação condicional
        status_format = formats['status_pago'] if data['Status_Pagamento'] == 'Pago' else formats['status_a_pagar']
        worksheet.write(row, 5, data['Status_Pagamento'], status_format)
        
        worksheet.write(row, 6, data['Local_Projeto'], formats['data'])
    
    # Adicionar filtros
    worksheet.autofilter(f'A2:G{len(df)+2}')

def create_monthly_summary_sheet(workbook, df, formats):
    """Criar aba de resumo mensal"""
    worksheet = workbook.add_worksheet('Resumo Mensal')
    worksheet.set_column('A:H', 15)
    
    # Título
    worksheet.merge_range('A1:H1', 'RESUMO MENSAL DETALHADO', formats['title'])
    
    # Agrupar por mês
    monthly_data = df.groupby(['Mes', 'Status_Pagamento']).agg({
        'Data': 'count',
        'Valor_USD': 'sum'
    }).reset_index()
    
    # Pivot para melhor visualização
    pivot_data = monthly_data.pivot_table(
        index='Mes', 
        columns='Status_Pagamento', 
        values=['Data', 'Valor_USD'], 
        fill_value=0
    )
    
    # Cabeçalhos
    row = 3
    headers = ['Mês', 'Dias A Pagar', 'Valor A Pagar', 'Dias Pagos', 'Valor Pago', 'Total Dias', 'Total Valor', '% Pago']
    for col, header in enumerate(headers):
        worksheet.write(row, col, header, formats['header'])
    
    # Dados
    row += 1
    for mes in pivot_data.index:
        dias_a_pagar = pivot_data.loc[mes, ('Data', 'A Pagar')] if ('Data', 'A Pagar') in pivot_data.columns else 0
        valor_a_pagar = pivot_data.loc[mes, ('Valor_USD', 'A Pagar')] if ('Valor_USD', 'A Pagar') in pivot_data.columns else 0
        dias_pagos = pivot_data.loc[mes, ('Data', 'Pago')] if ('Data', 'Pago') in pivot_data.columns else 0
        valor_pago = pivot_data.loc[mes, ('Valor_USD', 'Pago')] if ('Valor_USD', 'Pago') in pivot_data.columns else 0
        
        total_dias = dias_a_pagar + dias_pagos
        total_valor = valor_a_pagar + valor_pago
        percentual = (dias_pagos / total_dias * 100) if total_dias > 0 else 0
        
        worksheet.write(row, 0, mes, formats['data'])
        worksheet.write(row, 1, dias_a_pagar, formats['data'])
        worksheet.write(row, 2, valor_a_pagar, formats['currency'])
        worksheet.write(row, 3, dias_pagos, formats['data'])
        worksheet.write(row, 4, valor_pago, formats['currency'])
        worksheet.write(row, 5, total_dias, formats['data'])
        worksheet.write(row, 6, total_valor, formats['currency'])
        worksheet.write(row, 7, f'{percentual:.1f}%', formats['data'])
        row += 1

def create_project_summary_sheet(workbook, df, formats):
    """Criar aba de resumo por projeto"""
    worksheet = workbook.add_worksheet('Resumo por Projeto')
    worksheet.set_column('A:G', 18)
    
    # Título
    worksheet.merge_range('A1:G1', 'RESUMO POR PROJETO', formats['title'])
    
    # Cabeçalhos
    row = 3
    headers = ['Projeto', 'Dias Trabalhados', 'Valor Total', 'Dias Pagos', 'Valor Pago', 'Dias A Pagar', 'Valor A Pagar']
    for col, header in enumerate(headers):
        worksheet.write(row, col, header, formats['header'])
    
    # Processar dados por projeto
    projects = df['Local_Projeto'].unique()
    row += 1
    
    for project in sorted(projects):
        project_data = df[df['Local_Projeto'] == project]
        total_dias = len(project_data)
        total_valor = total_dias * 250
        dias_pagos = len(project_data[project_data['Status_Pagamento'] == 'Pago'])
        valor_pago = dias_pagos * 250
        dias_a_pagar = total_dias - dias_pagos
        valor_a_pagar = dias_a_pagar * 250
        
        worksheet.write(row, 0, project, formats['data'])
        worksheet.write(row, 1, total_dias, formats['data'])
        worksheet.write(row, 2, total_valor, formats['currency'])
        worksheet.write(row, 3, dias_pagos, formats['data'])
        worksheet.write(row, 4, valor_pago, formats['currency'])
        worksheet.write(row, 5, dias_a_pagar, formats['data'])
        worksheet.write(row, 6, valor_a_pagar, formats['currency'])
        row += 1

def create_payment_control_sheet(workbook, df, formats):
    """Criar aba de controle de pagamentos"""
    worksheet = workbook.add_worksheet('Controle de Pagamentos')
    worksheet.set_column('A:D', 18)
    
    # Título
    worksheet.merge_range('A1:D1', 'CONTROLE DE PAGAMENTOS', formats['title'])
    
    # Seção A Pagar
    worksheet.write(3, 0, 'PENDENTES DE PAGAMENTO', formats['subtitle'])
    
    # Cabeçalhos A Pagar
    headers_pending = ['Data', 'Projeto', 'Valor', 'Dia da Semana']
    for col, header in enumerate(headers_pending):
        worksheet.write(4, col, header, formats['header'])
    
    # Dados A Pagar
    pending_data = df[df['Status_Pagamento'] == 'A Pagar'].sort_values('Data')
    row = 5
    for idx, data in pending_data.iterrows():
        worksheet.write_datetime(row, 0, data['Data'], formats['date'])
        worksheet.write(row, 1, data['Local_Projeto'], formats['data'])
        worksheet.write(row, 2, data['Valor_USD'], formats['currency'])
        worksheet.write(row, 3, data['Dia_Semana'], formats['data'])
        row += 1
    
    # Seção Pagos
    row += 2
    worksheet.write(row, 0, 'PAGAMENTOS REALIZADOS', formats['subtitle'])
    row += 1
    
    # Cabeçalhos Pagos
    for col, header in enumerate(headers_pending):
        worksheet.write(row, col, header, formats['header'])
    
    # Dados Pagos
    paid_data = df[df['Status_Pagamento'] == 'Pago'].sort_values('Data', ascending=False)
    row += 1
    for idx, data in paid_data.iterrows():
        worksheet.write_datetime(row, 0, data['Data'], formats['date'])
        worksheet.write(row, 1, data['Local_Projeto'], formats['status_pago'])
        worksheet.write(row, 2, data['Valor_USD'], formats['currency'])
        worksheet.write(row, 3, data['Dia_Semana'], formats['data'])
        row += 1

def create_calendar_template_sheet(workbook, formats):
    """Criar aba com template de calendário para 2025"""
    worksheet = workbook.add_worksheet('Calendário 2025')
    worksheet.set_column('A:G', 12)
    
    # Título
    worksheet.merge_range('A1:G1', 'CALENDÁRIO 2025 - TEMPLATE PARA DIAS TRABALHADOS', formats['title'])
    
    # Instruções
    worksheet.merge_range('A3:G3', 'Instruções: Marque os dias trabalhados alterando a cor da célula', formats['subtitle'])
    worksheet.write(4, 0, 'Legenda:', formats['subtitle'])
    worksheet.write(4, 1, 'A Pagar', formats['status_a_pagar'])
    worksheet.write(4, 2, 'Pago', formats['status_pago'])
    
    # Criar calendário para cada mês
    months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
              'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    row_start = 6
    for month_idx, month_name in enumerate(months):
        row = row_start + (month_idx * 10)
        
        # Nome do mês
        worksheet.merge_range(f'A{row+1}:G{row+1}', month_name, formats['header'])
        
        # Dias da semana
        weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
        for col, day in enumerate(weekdays):
            worksheet.write(row + 1, col, day, formats['header'])
        
        # Calcular dias do mês
        import calendar
        cal = calendar.monthcalendar(2025, month_idx + 1)
        
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    worksheet.write(row + 2 + week_idx, day_idx, '', formats['calendar_day'])
                else:
                    worksheet.write(row + 2 + week_idx, day_idx, day, formats['calendar_day'])

if __name__ == "__main__":
    # Mudar para o diretório correto
    os.chdir('/workspace/excel_report')
    
    # Criar planilha
    filename = create_daily_allowance_excel()
    print(f"Planilha Excel criada com sucesso: {filename}")