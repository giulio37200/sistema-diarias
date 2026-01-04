#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Diárias com Sincronização Automática
Aplica o framework de sincronização ao sistema atual de controle de diárias
Interface Python como principal + sincronização automática com Excel
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import webbrowser
import time
import threading
from typing import Dict, List, Optional, Any

# Importar framework de sincronização
from excel_sync_framework import create_sync_manager, auto_sync, sync_dataframe
from excel_templates import get_template

class DiariasSystem:
    """Sistema principal de controle de diárias com sincronização automática"""
    
    def __init__(self, auto_start_web=True, auto_sync_interval=30):
        """
        Inicializa o sistema de diárias
        
        Args:
            auto_start_web: Se deve abrir automaticamente a interface web
            auto_sync_interval: Intervalo de sincronização em segundos
        """
        self.data_dir = Path("excel_report")
        self.excel_file = "outputs/controle_diarias_sync.xlsx"
        
        # Criar gerenciador de sincronização
        self.sync_manager = create_sync_manager(
            self.excel_file, 
            "operations"  # Template operacional para controle de diárias
        )
        
        # Configurar sincronização automática
        self.auto_sync_interval = auto_sync_interval
        self.sync_manager.start_auto_sync()
        
        # Dados do sistema
        self.working_days = {}
        self.deposits = []
        self.daily_rate = 250.0
        self.credit_balance = 0.0
        
        # Carregar dados existentes
        self._load_existing_data()
        
        # Configurar monitoramento de mudanças
        self._setup_monitoring()
        
        # Interface web
        if auto_start_web:
            self._start_web_interface()
        
        print("🚀 Sistema de Diárias inicializado com sincronização automática")
        print(f"💰 Saldo atual de créditos: R$ {self.credit_balance:.2f}")
        print(f"🔄 Sincronização automática: a cada {auto_sync_interval}s")
        print(f"📊 Arquivo Excel: {self.excel_file}")
    
    def _load_existing_data(self):
        """Carrega dados existentes do sistema web"""
        try:
            # Tentar carregar dados do localStorage simulado (arquivo JSON)
            data_file = self.data_dir / "diarias_data.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.working_days = data.get('workingDays', {})
                self.deposits = data.get('deposits', [])
                self.credit_balance = data.get('creditBalance', 0.0)
                
                print(f"📂 Dados carregados: {len(self.working_days)} dias, {len(self.deposits)} depósitos")
            else:
                print("📂 Nenhum dado anterior encontrado, iniciando sistema limpo")
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar dados: {e}")
            self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Inicializa dados de exemplo para demonstração"""
        print("🎯 Inicializando dados de exemplo...")
        
        # Adicionar alguns depósitos de exemplo
        self.add_deposit(5000.0, "Depósito inicial")
        self.add_deposit(3000.0, "Depósito adicional")
        
        # Adicionar alguns dias trabalhados no mês atual
        today = datetime.now()
        for i in range(1, 15):  # Primeiros 14 dias do mês
            work_date = today.replace(day=i)
            if work_date.weekday() < 5:  # Segunda a sexta
                self.add_working_day(work_date.strftime('%Y-%m-%d'))
        
        print("✅ Dados de exemplo criados")
    
    def _setup_monitoring(self):
        """Configura monitoramento de mudanças para sincronização automática"""
        
        # Thread para monitorar mudanças no arquivo de dados web
        def monitor_web_data():
            data_file = self.data_dir / "diarias_data.json"
            last_modified = 0
            
            while True:
                try:
                    if data_file.exists():
                        current_modified = data_file.stat().st_mtime
                        if current_modified > last_modified:
                            last_modified = current_modified
                            self._sync_from_web_data()
                    
                    time.sleep(5)  # Verificar a cada 5 segundos
                    
                except Exception as e:
                    print(f"⚠️ Erro no monitoramento: {e}")
                    time.sleep(10)
        
        # Iniciar thread de monitoramento
        monitor_thread = threading.Thread(target=monitor_web_data, daemon=True)
        monitor_thread.start()
    
    def _sync_from_web_data(self):
        """Sincroniza dados da interface web para o sistema Python"""
        try:
            data_file = self.data_dir / "diarias_data.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    web_data = json.load(f)
                
                # Atualizar dados locais
                old_days_count = len(self.working_days)
                old_deposits_count = len(self.deposits)
                
                self.working_days = web_data.get('workingDays', {})
                self.deposits = web_data.get('deposits', [])
                self.credit_balance = web_data.get('creditBalance', 0.0)
                
                # Verificar se houve mudanças
                new_days_count = len(self.working_days)
                new_deposits_count = len(self.deposits)
                
                if new_days_count != old_days_count or new_deposits_count != old_deposits_count:
                    print(f"🔄 Dados sincronizados da web: {new_days_count} dias, {new_deposits_count} depósitos")
                    self._trigger_excel_sync()
                
        except Exception as e:
            print(f"⚠️ Erro na sincronização web: {e}")
    
    def _trigger_excel_sync(self):
        """Força sincronização com Excel"""
        try:
            # Preparar dados para Excel
            self._prepare_excel_data()
            
            # Sincronizar
            self.sync_manager.sync_to_excel()
            
            print(f"📊 Dados sincronizados com Excel: {self.excel_file}")
            
        except Exception as e:
            print(f"❌ Erro na sincronização Excel: {e}")
    
    def _start_web_interface(self):
        """Inicia a interface web em thread separada"""
        def open_browser():
            time.sleep(2)  # Aguardar um pouco
            web_file = self.data_dir / "index.html"
            if web_file.exists():
                webbrowser.open(f"file://{web_file.absolute()}")
                print("🌐 Interface web aberta no navegador")
        
        # Abrir navegador em thread separada
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
    
    def get_working_days_dataframe(self) -> pd.DataFrame:
        """Retorna DataFrame com dias trabalhados"""
        if not self.working_days:
            return pd.DataFrame(columns=['Data', 'Status', 'Valor', 'Observacoes'])
        
        data = []
        for date_str, info in self.working_days.items():
            data.append({
                'Data': pd.to_datetime(date_str),
                'Status': info.get('status', 'pending'),
                'Valor': self.daily_rate,
                'Observacoes': info.get('notes', '')
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values('Data')
        df['Mes'] = df['Data'].dt.strftime('%Y-%m')
        df['Dia_Semana'] = df['Data'].dt.day_name()
        df['Valor_Acumulado'] = df['Valor'].cumsum()
        
        return df
    
    def get_deposits_dataframe(self) -> pd.DataFrame:
        """Retorna DataFrame com depósitos"""
        if not self.deposits:
            return pd.DataFrame(columns=['Data', 'Valor', 'Descricao', 'Saldo_Apos'])
        
        data = []
        for deposit in self.deposits:
            data.append({
                'Data': pd.to_datetime(deposit['date']),
                'Valor': deposit['amount'],
                'Descricao': deposit.get('description', ''),
                'Saldo_Apos': deposit.get('balanceAfter', 0)
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values('Data')
        df['Valor_Acumulado'] = df['Valor'].cumsum()
        
        return df
    
    def get_kpis(self) -> Dict[str, Any]:
        """Calcula KPIs do sistema de diárias"""
        df_days = self.get_working_days_dataframe()
        df_deposits = self.get_deposits_dataframe()
        
        # KPIs básicos
        total_days = len(df_days)
        total_earned = total_days * self.daily_rate
        total_deposited = df_deposits['Valor'].sum() if not df_deposits.empty else 0
        current_balance = total_deposited - total_earned
        
        # KPIs por status
        paid_days = len(df_days[df_days['Status'] == 'paid']) if not df_days.empty else 0
        pending_days = len(df_days[df_days['Status'] == 'pending']) if not df_days.empty else 0
        
        # KPIs temporais
        today = datetime.now()
        current_month = today.strftime('%Y-%m')
        
        if not df_days.empty:
            current_month_days = len(df_days[df_days['Mes'] == current_month])
            current_month_earned = current_month_days * self.daily_rate
        else:
            current_month_days = 0
            current_month_earned = 0
        
        # Projeções
        avg_days_per_month = total_days / max(1, len(df_days['Mes'].unique())) if not df_days.empty else 0
        projected_monthly_cost = avg_days_per_month * self.daily_rate
        
        return {
            'total_dias_trabalhados': total_days,
            'total_ganho': total_earned,
            'total_depositado': total_deposited,
            'saldo_atual': current_balance,
            'dias_pagos': paid_days,
            'dias_pendentes': pending_days,
            'dias_mes_atual': current_month_days,
            'ganho_mes_atual': current_month_earned,
            'media_dias_mes': avg_days_per_month,
            'custo_mensal_projetado': projected_monthly_cost,
            'taxa_pagamento': (paid_days / max(1, total_days)) * 100,
            'ultima_atualizacao': datetime.now().isoformat(),
            'valor_diaria': self.daily_rate,
            'status_saldo': 'positivo' if current_balance >= 0 else 'negativo'
        }
    
    def get_monthly_analysis(self) -> pd.DataFrame:
        """Análise mensal detalhada"""
        df_days = self.get_working_days_dataframe()
        
        if df_days.empty:
            return pd.DataFrame(columns=['Mes', 'Dias_Trabalhados', 'Valor_Total', 'Dias_Pagos', 'Dias_Pendentes'])
        
        monthly = df_days.groupby('Mes').agg({
            'Data': 'count',
            'Valor': 'sum',
            'Status': lambda x: (x == 'paid').sum()
        }).rename(columns={
            'Data': 'Dias_Trabalhados',
            'Valor': 'Valor_Total',
            'Status': 'Dias_Pagos'
        })
        
        monthly['Dias_Pendentes'] = monthly['Dias_Trabalhados'] - monthly['Dias_Pagos']
        monthly['Taxa_Pagamento'] = (monthly['Dias_Pagos'] / monthly['Dias_Trabalhados']) * 100
        monthly['Media_Dias_Semana'] = monthly['Dias_Trabalhados'] / 4.33  # Aproximadamente 4.33 semanas por mês
        
        return monthly.round(2)
    
    def get_cash_flow(self) -> pd.DataFrame:
        """Análise de fluxo de caixa"""
        df_days = self.get_working_days_dataframe()
        df_deposits = self.get_deposits_dataframe()
        
        # Combinar entradas (depósitos) e saídas (dias trabalhados)
        cash_flow_data = []
        
        # Adicionar depósitos como entradas
        for _, deposit in df_deposits.iterrows():
            cash_flow_data.append({
                'Data': deposit['Data'],
                'Tipo': 'Entrada',
                'Valor': deposit['Valor'],
                'Descricao': f"Depósito: {deposit['Descricao']}",
                'Saldo_Impacto': deposit['Valor']
            })
        
        # Adicionar dias trabalhados como saídas
        for _, day in df_days.iterrows():
            cash_flow_data.append({
                'Data': day['Data'],
                'Tipo': 'Saída',
                'Valor': -day['Valor'],
                'Descricao': f"Diária trabalhada ({day['Status']})",
                'Saldo_Impacto': -day['Valor']
            })
        
        if not cash_flow_data:
            return pd.DataFrame(columns=['Data', 'Tipo', 'Valor', 'Descricao', 'Saldo_Impacto', 'Saldo_Acumulado'])
        
        df_flow = pd.DataFrame(cash_flow_data)
        df_flow = df_flow.sort_values('Data')
        df_flow['Saldo_Acumulado'] = df_flow['Saldo_Impacto'].cumsum()
        
        return df_flow
    
    def _prepare_excel_data(self):
        """Prepara todos os dados para sincronização com Excel"""
        # Registrar todos os DataFrames
        self.sync_manager.register_data('dias_trabalhados', self.get_working_days_dataframe())
        self.sync_manager.register_data('depositos', self.get_deposits_dataframe())
        self.sync_manager.register_data('analise_mensal', self.get_monthly_analysis())
        self.sync_manager.register_data('fluxo_caixa', self.get_cash_flow())
        
        # Registrar KPIs
        self.sync_manager.register_data('kpis_diarias', self.get_kpis())
        
        # Dados de configuração
        config_data = {
            'valor_diaria': self.daily_rate,
            'total_dias': len(self.working_days),
            'total_depositos': len(self.deposits),
            'saldo_atual': self.credit_balance,
            'ultima_sincronizacao': datetime.now().isoformat(),
            'versao_sistema': '2.0.0'
        }
        
        self.sync_manager.register_data('configuracao', config_data)
    
    # Métodos para manipulação de dados
    def add_working_day(self, date_str: str, status: str = 'pending', notes: str = '') -> bool:
        """Adiciona um dia trabalhado"""
        try:
            self.working_days[date_str] = {
                'status': status,
                'notes': notes,
                'added_at': datetime.now().isoformat()
            }
            
            # Atualizar saldo
            self.credit_balance -= self.daily_rate
            
            # Salvar dados
            self._save_data()
            
            print(f"✅ Dia adicionado: {date_str} (Status: {status})")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar dia: {e}")
            return False
    
    def remove_working_day(self, date_str: str) -> bool:
        """Remove um dia trabalhado"""
        try:
            if date_str in self.working_days:
                del self.working_days[date_str]
                
                # Atualizar saldo
                self.credit_balance += self.daily_rate
                
                # Salvar dados
                self._save_data()
                
                print(f"🗑️ Dia removido: {date_str}")
                return True
            else:
                print(f"⚠️ Dia não encontrado: {date_str}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao remover dia: {e}")
            return False
    
    def add_deposit(self, amount: float, description: str = '') -> bool:
        """Adiciona um depósito"""
        try:
            deposit = {
                'date': datetime.now().isoformat(),
                'amount': amount,
                'description': description,
                'balanceAfter': self.credit_balance + amount
            }
            
            self.deposits.append(deposit)
            self.credit_balance += amount
            
            # Salvar dados
            self._save_data()
            
            print(f"💰 Depósito adicionado: R$ {amount:.2f} - {description}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar depósito: {e}")
            return False
    
    def _save_data(self):
        """Salva dados no arquivo JSON para sincronização com web"""
        try:
            data = {
                'workingDays': self.working_days,
                'deposits': self.deposits,
                'creditBalance': self.credit_balance,
                'lastUpdate': datetime.now().isoformat()
            }
            
            data_file = self.data_dir / "diarias_data.json"
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Trigger sincronização Excel
            self._trigger_excel_sync()
            
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
    
    def generate_report(self, export_excel: bool = True) -> str:
        """Gera relatório completo"""
        print("📋 Gerando relatório completo...")
        
        # Preparar dados
        self._prepare_excel_data()
        
        # Sincronizar com Excel se solicitado
        if export_excel:
            self.sync_manager.sync_to_excel()
        
        # Gerar resumo textual
        kpis = self.get_kpis()
        
        report = f"""
📊 RELATÓRIO DE DIÁRIAS - {datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*60}

💰 RESUMO FINANCEIRO:
   • Saldo atual: R$ {kpis['saldo_atual']:.2f}
   • Total depositado: R$ {kpis['total_depositado']:.2f}
   • Total ganho: R$ {kpis['total_ganho']:.2f}
   • Status: {kpis['status_saldo'].upper()}

📅 DIAS TRABALHADOS:
   • Total de dias: {kpis['total_dias_trabalhados']}
   • Dias pagos: {kpis['dias_pagos']}
   • Dias pendentes: {kpis['dias_pendentes']}
   • Taxa de pagamento: {kpis['taxa_pagamento']:.1f}%

📈 ANÁLISE MENSAL:
   • Dias no mês atual: {kpis['dias_mes_atual']}
   • Ganho no mês: R$ {kpis['ganho_mes_atual']:.2f}
   • Média de dias/mês: {kpis['media_dias_mes']:.1f}
   • Custo mensal projetado: R$ {kpis['custo_mensal_projetado']:.2f}

⚙️ CONFIGURAÇÃO:
   • Valor da diária: R$ {kpis['valor_diaria']:.2f}
   • Última atualização: {kpis['ultima_atualizacao']}

📁 ARQUIVOS GERADOS:
   • Excel: {self.excel_file}
   • Interface Web: {self.data_dir}/index.html
"""
        
        print(report)
        
        if export_excel:
            print(f"✅ Relatório Excel gerado: {self.excel_file}")
        
        return report
    
    def show_status(self):
        """Mostra status atual do sistema"""
        kpis = self.get_kpis()
        
        print(f"\n🎯 STATUS DO SISTEMA DE DIÁRIAS")
        print(f"{'='*50}")
        print(f"💰 Saldo: R$ {kpis['saldo_atual']:.2f} ({kpis['status_saldo']})")
        print(f"📅 Dias trabalhados: {kpis['total_dias_trabalhados']}")
        print(f"💳 Depósitos: {len(self.deposits)}")
        print(f"🔄 Sincronização: Ativa (a cada {self.auto_sync_interval}s)")
        print(f"📊 Excel: {self.excel_file}")
        print(f"🌐 Web: {self.data_dir}/index.html")
    
    def __del__(self):
        """Cleanup ao finalizar"""
        if hasattr(self, 'sync_manager'):
            self.sync_manager.stop_auto_sync()
            print("🔄 Sincronização automática finalizada")

# Funções de conveniência para uso interativo
def criar_sistema_diarias(auto_sync_interval: int = 30) -> DiariasSystem:
    """Cria e retorna uma instância do sistema de diárias"""
    return DiariasSystem(auto_sync_interval=auto_sync_interval)

def exemplo_uso_completo():
    """Exemplo completo de uso do sistema"""
    print("🚀 Exemplo de uso completo do Sistema de Diárias")
    print("="*60)
    
    # Criar sistema
    sistema = DiariasSystem(auto_start_web=False, auto_sync_interval=10)
    
    # Mostrar status inicial
    sistema.show_status()
    
    # Adicionar alguns dados de exemplo
    print("\n📝 Adicionando dados de exemplo...")
    
    # Adicionar depósito
    sistema.add_deposit(2000.0, "Depósito de teste")
    
    # Adicionar dias trabalhados
    hoje = datetime.now()
    for i in range(5):
        data = (hoje - timedelta(days=i)).strftime('%Y-%m-%d')
        sistema.add_working_day(data, 'paid' if i < 3 else 'pending')
    
    # Gerar relatório
    print("\n📊 Gerando relatório...")
    sistema.generate_report()
    
    # Mostrar status final
    print("\n🎯 Status final:")
    sistema.show_status()
    
    return sistema

if __name__ == "__main__":
    # Executar exemplo se rodado diretamente
    sistema = exemplo_uso_completo()
    
    print("\n" + "="*60)
    print("🎉 Sistema de Diárias com Sincronização Automática Pronto!")
    print("="*60)
    print("\n💡 Comandos úteis:")
    print("  sistema.show_status()           # Ver status atual")
    print("  sistema.generate_report()       # Gerar relatório")
    print("  sistema.add_deposit(1000, 'desc')  # Adicionar depósito")
    print("  sistema.add_working_day('2024-01-15')  # Adicionar dia")
    print("\n🌐 Interface web disponível em: excel_report/index.html")
    print("📊 Arquivo Excel: outputs/controle_diarias_sync.xlsx")
    print("\n🔄 Sincronização automática ativa - dados são atualizados automaticamente!")