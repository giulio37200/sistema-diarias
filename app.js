// Sistema Completo de Controle de Diárias - Aplicação Principal
// Interface integrada com calendário, créditos, dashboard e exportação

window.DiariasApp = {
    // Estado da aplicação
    currentDate: new Date(),
    selectedDates: new Set(),
    charts: {},
    
    // Inicializar aplicação
    init: function() {
        console.log('🚀 Inicializando Aplicação de Diárias...');
        
        // Inicializar sistema de dados
        window.DiariasSystem.init();
        
        // Carregar datas existentes
        this.loadExistingDates();
        
        // Criar interface
        this.createInterface();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Atualizar displays
        this.updateAllDisplays();
        
        console.log('✅ Aplicação inicializada com sucesso!');
    },
    
    // === INTERFACE ===
    
    createInterface: function() {
        const container = document.getElementById('app-container');
        if (!container) {
            console.error('❌ Container da aplicação não encontrado!');
            return;
        }
        
        container.innerHTML = `
            <div class="main-container">
                <!-- Header -->
                <header class="header">
                    <h1>💰 Controle de Diárias de Alimentação</h1>
                    <p>Sistema completo com créditos antecipados, calendário interativo e dashboard</p>
                </header>

                <!-- Main Grid -->
                <div class="main-grid">
                    <!-- Left Panel -->
                    <div class="left-panel">
                        <!-- KPI Cards -->
                        <section class="kpi-grid">
                            <div class="kpi-card">
                                <div class="kpi-value" id="total-dias">0</div>
                                <div class="kpi-label">Total de Dias</div>
                                <div class="kpi-subtitle">Trabalhados</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value" id="total-valor">$0</div>
                                <div class="kpi-label">Valor Total</div>
                                <div class="kpi-subtitle">Diárias</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value" id="credit-balance-kpi">$0</div>
                                <div class="kpi-label">Saldo de Crédito</div>
                                <div class="kpi-subtitle">Antecipado</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value" id="credit-days-kpi">0</div>
                                <div class="kpi-label">Dias de Crédito</div>
                                <div class="kpi-subtitle">Disponíveis</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value" id="dias-pagos">0</div>
                                <div class="kpi-label">Dias Pagos</div>
                                <div class="kpi-subtitle" id="valor-pago">$0</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-value" id="dias-a-pagar">0</div>
                                <div class="kpi-label">Dias A Pagar</div>
                                <div class="kpi-subtitle" id="valor-a-pagar">$0</div>
                            </div>
                        </section>

                        <!-- Charts -->
                        <section class="charts-grid">
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">📊 Valores Mensais</h3>
                                </div>
                                <div class="card-body">
                                    <div id="monthly-chart" class="chart"></div>
                                </div>
                            </div>
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">📈 Status dos Pagamentos</h3>
                                </div>
                                <div class="card-body">
                                    <div id="status-chart" class="chart"></div>
                                </div>
                            </div>
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">🏢 Valores por Projeto</h3>
                                </div>
                                <div class="card-body">
                                    <div id="project-chart" class="chart"></div>
                                </div>
                            </div>
                            <div class="card">
                                <div class="card-header">
                                    <h3 class="card-title">📅 Tendência Mensal</h3>
                                </div>
                                <div class="card-body">
                                    <div id="trend-chart" class="chart"></div>
                                </div>
                            </div>
                        </section>
                    </div>

                    <!-- Right Panel -->
                    <div class="right-panel">
                        <!-- Sistema de Créditos (DESTAQUE) -->
                        <div class="credit-section">
                            <h3>💰 Sistema de Créditos Antecipados</h3>
                            <div class="credit-info">
                                <div class="credit-item">
                                    <div class="credit-label">Saldo Atual</div>
                                    <div class="credit-value" id="credit-balance">$0</div>
                                </div>
                                <div class="credit-item">
                                    <div class="credit-label">Dias Restantes</div>
                                    <div class="credit-value" id="credit-days">0</div>
                                </div>
                            </div>
                            <div class="credit-actions">
                                <div class="deposit-form">
                                    <input type="number" id="deposit-amount" placeholder="Valor do depósito (ex: 2500)" step="0.01" min="0">
                                    <input type="text" id="deposit-description" placeholder="Descrição (ex: Pagamento Janeiro)">
                                    <button id="add-deposit" class="btn btn-light">
                                        💵 Adicionar Depósito
                                    </button>
                                </div>
                                <button id="view-deposits" class="btn btn-light">
                                    📋 Ver Histórico de Depósitos
                                </button>
                            </div>
                        </div>

                        <!-- Calendário -->
                        <div class="card calendar-container">
                            <div class="card-header">
                                <h3 class="card-title">📅 Calendário de Dias Trabalhados</h3>
                            </div>
                            <div class="card-body">
                                <div class="calendar-header">
                                    <button id="prev-month" class="calendar-nav-btn">‹</button>
                                    <div class="calendar-selectors">
                                        <select id="month-selector" class="calendar-select">
                                            <option value="0">Janeiro</option>
                                            <option value="1">Fevereiro</option>
                                            <option value="2">Março</option>
                                            <option value="3">Abril</option>
                                            <option value="4">Maio</option>
                                            <option value="5">Junho</option>
                                            <option value="6">Julho</option>
                                            <option value="7">Agosto</option>
                                            <option value="8">Setembro</option>
                                            <option value="9">Outubro</option>
                                            <option value="10">Novembro</option>
                                            <option value="11">Dezembro</option>
                                        </select>
                                        <select id="year-selector" class="calendar-select">
                                            <option value="2023">2023</option>
                                            <option value="2024">2024</option>
                                            <option value="2025" selected>2025</option>
                                            <option value="2026">2026</option>
                                            <option value="2027">2027</option>
                                        </select>
                                    </div>
                                    <button id="next-month" class="calendar-nav-btn">›</button>
                                </div>
                                
                                <div class="calendar-weekdays">
                                    <div class="weekday">Dom</div>
                                    <div class="weekday">Seg</div>
                                    <div class="weekday">Ter</div>
                                    <div class="weekday">Qua</div>
                                    <div class="weekday">Qui</div>
                                    <div class="weekday">Sex</div>
                                    <div class="weekday">Sáb</div>
                                </div>
                                
                                <div id="calendar-days" class="calendar-days"></div>
                                
                                <div class="calendar-controls">
                                    <div class="project-input-group">
                                        <label for="project-input">Projeto:</label>
                                        <input type="text" id="project-input" placeholder="Nome do projeto" value="Novo Projeto">
                                    </div>
                                    
                                    <div class="calendar-legend">
                                        <div class="legend-item">
                                            <span class="legend-color selected"></span>
                                            <span>Dia Trabalhado</span>
                                        </div>
                                        <div class="legend-item">
                                            <span class="legend-color paid"></span>
                                            <span>Pago</span>
                                        </div>
                                        <div class="legend-item">
                                            <span class="legend-color pending"></span>
                                            <span>A Pagar</span>
                                        </div>
                                    </div>
                                    
                                    <div class="delete-mode-toggle">
                                        <label>
                                            <input type="checkbox" id="delete-mode-toggle">
                                            <span>Modo Deletar</span>
                                        </label>
                                        <small>Ative para remover dias clicando neles</small>
                                    </div>
                                    
                                    <div class="calendar-buttons">
                                        <button id="export-csv" class="btn btn-primary">📄 Exportar CSV</button>
                                        <button id="export-excel" class="btn btn-success">📊 Gerar Excel</button>
                                        <button id="clear-month" class="btn btn-danger">🗑️ Limpar Mês</button>
                                        <button id="go-today" class="btn btn-info">📅 Ir para Hoje</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Data Table -->
                <div class="card data-table-container">
                    <div class="card-header">
                        <div class="table-header">
                            <h3 class="card-title">📋 Detalhamento das Diárias</h3>
                            <div class="filter-controls">
                                <select id="filter-mes" class="filter-select">
                                    <option value="">Todos os Meses</option>
                                </select>
                                <select id="filter-status" class="filter-select">
                                    <option value="">Todos os Status</option>
                                    <option value="Pago">Pago</option>
                                    <option value="A Pagar">A Pagar</option>
                                </select>
                                <select id="filter-projeto" class="filter-select">
                                    <option value="">Todos os Projetos</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Data</th>
                                    <th>Dia da Semana</th>
                                    <th>Mês</th>
                                    <th>Projeto</th>
                                    <th>Valor</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="data-table-body">
                                <!-- Dados serão inseridos via JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
        
        console.log('✅ Interface criada com sucesso!');
    },
    
    // === EVENT LISTENERS ===
    
    setupEventListeners: function() {
        // Navegação do calendário
        document.getElementById('prev-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });
        
        document.getElementById('next-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });
        
        // Seletores de mês e ano
        document.getElementById('month-selector').addEventListener('change', (e) => {
            this.currentDate.setMonth(parseInt(e.target.value));
            this.renderCalendar();
        });
        
        document.getElementById('year-selector').addEventListener('change', (e) => {
            this.currentDate.setFullYear(parseInt(e.target.value));
            this.renderCalendar();
        });
        
        // Clique nos dias do calendário
        document.getElementById('calendar-days').addEventListener('click', (e) => {
            if (e.target.classList.contains('calendar-day') && !e.target.classList.contains('empty')) {
                this.toggleWorkDay(e.target);
            }
        });
        
        // Sistema de créditos
        document.getElementById('add-deposit').addEventListener('click', () => {
            this.addDeposit();
        });
        
        document.getElementById('view-deposits').addEventListener('click', () => {
            this.showDepositsHistory();
        });
        
        // Enter no campo de depósito
        document.getElementById('deposit-amount').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addDeposit();
            }
        });
        
        // Botões de ação
        document.getElementById('export-csv').addEventListener('click', () => {
            this.exportCSV();
        });
        
        document.getElementById('export-excel').addEventListener('click', () => {
            this.generateExcel();
        });
        
        document.getElementById('clear-month').addEventListener('click', () => {
            this.clearMonth();
        });
        
        document.getElementById('go-today').addEventListener('click', () => {
            this.goToToday();
        });
        
        // Modo deletar
        document.getElementById('delete-mode-toggle').addEventListener('change', (e) => {
            this.toggleDeleteMode(e.target.checked);
        });
        
        // Filtros da tabela
        document.getElementById('filter-mes').addEventListener('change', () => {
            this.updateDataTable();
        });
        
        document.getElementById('filter-status').addEventListener('change', () => {
            this.updateDataTable();
        });
        
        document.getElementById('filter-projeto').addEventListener('change', () => {
            this.updateDataTable();
        });
        
        console.log('✅ Event listeners configurados!');
    },
    
    // === CALENDÁRIO ===
    
    loadExistingDates: function() {
        this.selectedDates.clear();
        window.DiariasSystem.workingData.forEach(item => {
            this.selectedDates.add(item.data);
        });
    },
    
    renderCalendar: function() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Atualizar seletores
        document.getElementById('month-selector').value = month;
        document.getElementById('year-selector').value = year;
        
        // Calcular primeiro dia do mês e número de dias
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        // Limpar container de dias
        const daysContainer = document.getElementById('calendar-days');
        daysContainer.innerHTML = '';
        
        // Adicionar dias vazios do início
        for (let i = 0; i < startingDayOfWeek; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            daysContainer.appendChild(emptyDay);
        }
        
        // Adicionar dias do mês
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            dayElement.dataset.date = this.formatDate(year, month, day);
            
            // Verificar se é dia trabalhado
            const dateString = this.formatDate(year, month, day);
            if (this.selectedDates.has(dateString)) {
                const workDay = window.DiariasSystem.workingData.find(item => item.data === dateString);
                if (workDay) {
                    dayElement.classList.add('selected');
                    if (workDay.statusPagamento === 'Pago') {
                        dayElement.classList.add('paid');
                    } else {
                        dayElement.classList.add('pending');
                    }
                    dayElement.title = `${workDay.localProjeto} - ${workDay.statusPagamento}`;
                }
            }
            
            // Destacar dia atual
            const today = new Date();
            if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
                dayElement.classList.add('today');
            }
            
            // Desabilitar fins de semana (opcional)
            const dayOfWeek = new Date(year, month, day).getDay();
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                dayElement.classList.add('weekend');
            }
            
            daysContainer.appendChild(dayElement);
        }
        
        // Aplicar modo deletar se ativo
        const deleteMode = document.getElementById('delete-mode-toggle');
        if (deleteMode && deleteMode.checked) {
            this.toggleDeleteMode(true);
        }
    },
    
    toggleWorkDay: function(dayElement) {
        const date = dayElement.dataset.date;
        const project = document.getElementById('project-input').value || 'Novo Projeto';
        const deleteMode = document.getElementById('delete-mode-toggle').checked;
        
        if (this.selectedDates.has(date)) {
            if (deleteMode) {
                // Modo deletar: sempre remover
                if (confirm(`Remover dia ${dayElement.textContent} (${date})?`)) {
                    window.DiariasSystem.removeWorkDay(date);
                    this.selectedDates.delete(date);
                    dayElement.classList.remove('selected', 'paid', 'pending');
                    dayElement.title = '';
                    this.updateAllDisplays();
                }
            } else {
                // Modo normal: alternar status de pagamento
                const workDay = window.DiariasSystem.workingData.find(item => item.data === date);
                if (workDay) {
                    const newStatus = workDay.statusPagamento === 'Pago' ? 'A Pagar' : 'Pago';
                    window.DiariasSystem.updatePaymentStatus(date, newStatus);
                    
                    // Atualizar visual
                    dayElement.classList.remove('paid', 'pending');
                    if (newStatus === 'Pago') {
                        dayElement.classList.add('paid');
                    } else {
                        dayElement.classList.add('pending');
                    }
                    dayElement.title = `${workDay.localProjeto} - ${newStatus}`;
                    this.updateAllDisplays();
                }
            }
        } else {
            if (!deleteMode) {
                // Adicionar novo dia (apenas se não estiver em modo deletar)
                const newEntry = window.DiariasSystem.addWorkDay(date, project);
                this.selectedDates.add(date);
                dayElement.classList.add('selected', 'pending');
                dayElement.title = `${newEntry.localProjeto} - ${newEntry.statusPagamento}`;
                this.updateAllDisplays();
            }
        }
    },
    
    formatDate: function(year, month, day) {
        return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    },
    
    goToToday: function() {
        this.currentDate = new Date();
        this.renderCalendar();
    },
    
    toggleDeleteMode: function(enabled) {
        const daysContainer = document.getElementById('calendar-days');
        const days = daysContainer.querySelectorAll('.calendar-day');
        
        days.forEach(day => {
            if (enabled) {
                day.classList.add('delete-mode');
            } else {
                day.classList.remove('delete-mode');
            }
        });
        
        // Atualizar texto do modo
        const modeText = document.querySelector('.delete-mode-toggle small');
        if (enabled) {
            modeText.textContent = 'Clique nos dias trabalhados para removê-los';
            modeText.style.color = '#f56565';
        } else {
            modeText.textContent = 'Ative para remover dias clicando neles';
            modeText.style.color = '#a0aec0';
        }
    },
    
    clearMonth: function() {
        if (confirm('Tem certeza que deseja remover todos os dias trabalhados deste mês?')) {
            const year = this.currentDate.getFullYear();
            const month = this.currentDate.getMonth();
            const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
            const monthName = monthNames[month];
            
            // Contar dias que serão removidos para devolver crédito
            const daysToRemove = window.DiariasSystem.workingData.filter(item => 
                item.mes === monthName && item.ano === year
            ).length;
            
            // Remover todos os dias do mês atual
            window.DiariasSystem.workingData = window.DiariasSystem.workingData.filter(item => {
                return item.mes !== monthName || item.ano !== year;
            });
            
            // Devolver crédito pelos dias removidos
            window.DiariasSystem.addToCredit(daysToRemove * 250);
            
            // Atualizar selectedDates
            this.loadExistingDates();
            
            // Re-renderizar calendário
            this.renderCalendar();
            
            // Atualizar displays
            this.updateAllDisplays();
            
            console.log(`✅ Mês ${monthName}/${year} limpo - ${daysToRemove} dias removidos`);
        }
    },
    
    // === SISTEMA DE CRÉDITOS ===
    
    addDeposit: function() {
        const amountInput = document.getElementById('deposit-amount');
        const descriptionInput = document.getElementById('deposit-description');
        
        const amount = parseFloat(amountInput.value);
        const description = descriptionInput.value.trim() || 'Depósito antecipado';
        
        if (isNaN(amount) || amount <= 0) {
            alert('Por favor, insira um valor válido para o depósito.');
            return;
        }
        
        // Adicionar depósito
        const deposit = window.DiariasSystem.addDeposit(amount, description);
        
        // Limpar campos
        amountInput.value = '';
        descriptionInput.value = '';
        
        // Atualizar displays
        this.updateAllDisplays();
        
        // Mostrar confirmação
        const creditInfo = window.DiariasSystem.getCreditInfo();
        alert(`✅ Depósito de $${amount.toLocaleString()} adicionado com sucesso!\n💰 Novo saldo: $${creditInfo.currentBalance.toLocaleString()}`);
    },
    
    showDepositsHistory: function() {
        const creditInfo = window.DiariasSystem.getCreditInfo();
        const deposits = creditInfo.deposits;
        
        if (deposits.length === 0) {
            alert('Nenhum depósito registrado ainda.');
            return;
        }
        
        // Criar modal com histórico
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>💰 Histórico de Depósitos</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <div style="background: rgba(66, 153, 225, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>Total Depositado:</span>
                            <span style="color: #48bb78; font-weight: bold;">$${creditInfo.totalDeposited.toLocaleString()}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>Total Usado:</span>
                            <span style="color: #f56565; font-weight: bold;">$${creditInfo.totalUsed.toLocaleString()}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem; font-weight: bold; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 10px;">
                            <span>Saldo Atual:</span>
                            <span style="color: ${creditInfo.isNegative ? '#f56565' : '#48bb78'};">$${creditInfo.currentBalance.toLocaleString()}</span>
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom: 15px;">📋 Lista de Depósitos:</h4>
                        ${deposits.map(deposit => `
                            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 8px;">
                                <div>
                                    <div style="font-weight: 600; color: #2d3748;">${deposit.description}</div>
                                    <div style="font-size: 0.9rem; color: #4a5568;">${new Date(deposit.date).toLocaleDateString('pt-BR')}</div>
                                </div>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <span style="font-weight: bold; color: #48bb78;">$${deposit.amount.toLocaleString()}</span>
                                    <button class="btn btn-danger" style="padding: 4px 8px; font-size: 0.8rem;" onclick="DiariasApp.removeDeposit(${deposit.id})">Remover</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listeners do modal
        modal.querySelector('.modal-close').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    },
    
    removeDeposit: function(depositId) {
        if (confirm('Tem certeza que deseja remover este depósito?')) {
            window.DiariasSystem.removeDeposit(depositId);
            this.updateAllDisplays();
            
            // Fechar modal atual e reabrir atualizado
            const modal = document.querySelector('.modal');
            if (modal) {
                document.body.removeChild(modal);
                this.showDepositsHistory();
            }
        }
    },
    
    // === ATUALIZAÇÕES DE DISPLAY ===
    
    updateAllDisplays: function() {
        this.updateKPIs();
        this.updateCreditDisplay();
        this.updateCharts();
        this.updateDataTable();
        this.updateFilters();
    },
    
    updateKPIs: function() {
        const kpis = window.DiariasSystem.getKPIs();
        const creditInfo = window.DiariasSystem.getCreditInfo();
        
        document.getElementById('total-dias').textContent = kpis.totalDias;
        document.getElementById('total-valor').textContent = `$${kpis.totalValor.toLocaleString()}`;
        document.getElementById('dias-pagos').textContent = kpis.diasPagos;
        document.getElementById('valor-pago').textContent = `$${kpis.valorPago.toLocaleString()}`;
        document.getElementById('dias-a-pagar').textContent = kpis.diasAPagar;
        document.getElementById('valor-a-pagar').textContent = `$${kpis.valorAPagar.toLocaleString()}`;
        
        // KPIs de crédito
        const creditBalanceKPI = document.getElementById('credit-balance-kpi');
        const creditDaysKPI = document.getElementById('credit-days-kpi');
        
        creditBalanceKPI.textContent = `$${creditInfo.currentBalance.toLocaleString()}`;
        creditBalanceKPI.className = `kpi-value ${creditInfo.isNegative ? 'negative' : 'positive'}`;
        
        creditDaysKPI.textContent = Math.abs(creditInfo.daysRemaining);
        creditDaysKPI.className = `kpi-value ${creditInfo.isNegative ? 'negative' : 'positive'}`;
    },
    
    updateCreditDisplay: function() {
        const creditInfo = window.DiariasSystem.getCreditInfo();
        
        const balanceElement = document.getElementById('credit-balance');
        const daysElement = document.getElementById('credit-days');
        
        if (balanceElement && daysElement) {
            // Atualizar saldo
            balanceElement.textContent = `$${creditInfo.currentBalance.toLocaleString()}`;
            balanceElement.className = `credit-value ${creditInfo.isNegative ? 'negative' : ''}`;
            
            // Atualizar dias restantes
            if (creditInfo.isNegative) {
                daysElement.textContent = `${Math.abs(creditInfo.daysRemaining)} dias em débito`;
                daysElement.className = 'credit-value negative';
            } else {
                daysElement.textContent = `${creditInfo.daysRemaining} dias`;
                daysElement.className = 'credit-value';
            }
        }
    },
    
    updateCharts: function() {
        this.createMonthlyChart();
        this.createStatusChart();
        this.createProjectChart();
        this.createTrendChart();
    },
    
    updateDataTable: function() {
        const filters = {
            mes: document.getElementById('filter-mes').value,
            status: document.getElementById('filter-status').value,
            projeto: document.getElementById('filter-projeto').value
        };
        
        const filteredData = window.DiariasSystem.getFilteredData(filters);
        const tbody = document.getElementById('data-table-body');
        
        tbody.innerHTML = filteredData.map(item => `
            <tr>
                <td>${new Date(item.data).toLocaleDateString('pt-BR')}</td>
                <td>${item.diaSemana}</td>
                <td>${item.mes}</td>
                <td>${item.localProjeto}</td>
                <td>$${item.valorUSD.toLocaleString()}</td>
                <td>
                    <span class="status-badge status-${item.statusPagamento.toLowerCase().replace(' ', '-')}" 
                          onclick="DiariasApp.toggleStatus('${item.data}')">
                        ${item.statusPagamento}
                    </span>
                </td>
            </tr>
        `).join('');
    },
    
    updateFilters: function() {
        // Atualizar filtros de mês
        const meses = window.DiariasSystem.getUniqueValues('mes');
        const filterMes = document.getElementById('filter-mes');
        const currentMes = filterMes.value;
        
        filterMes.innerHTML = '<option value="">Todos os Meses</option>' +
            meses.map(mes => `<option value="${mes}" ${mes === currentMes ? 'selected' : ''}>${mes}</option>`).join('');
        
        // Atualizar filtros de projeto
        const projetos = window.DiariasSystem.getUniqueValues('localProjeto');
        const filterProjeto = document.getElementById('filter-projeto');
        const currentProjeto = filterProjeto.value;
        
        filterProjeto.innerHTML = '<option value="">Todos os Projetos</option>' +
            projetos.map(projeto => `<option value="${projeto}" ${projeto === currentProjeto ? 'selected' : ''}>${projeto}</option>`).join('');
    },
    
    toggleStatus: function(date) {
        const workDay = window.DiariasSystem.workingData.find(item => item.data === date);
        if (workDay) {
            const newStatus = workDay.statusPagamento === 'Pago' ? 'A Pagar' : 'Pago';
            window.DiariasSystem.updatePaymentStatus(date, newStatus);
            this.updateAllDisplays();
            this.renderCalendar();
        }
    },
    
    // === GRÁFICOS ===
    
    createMonthlyChart: function() {
        const monthlyData = window.DiariasSystem.getMonthlyData();
        const months = Object.keys(monthlyData);
        const values = months.map(month => monthlyData[month].totalValor);
        
        if (this.charts.monthly) {
            this.charts.monthly.dispose();
        }
        
        const chartDom = document.getElementById('monthly-chart');
        this.charts.monthly = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    const data = monthlyData[params[0].name];
                    return `
                        <strong>${params[0].name}</strong><br/>
                        Total: $${data.totalValor.toLocaleString()}<br/>
                        Dias: ${data.totalDias}<br/>
                        Pagos: $${data.valorPago.toLocaleString()}<br/>
                        A Pagar: $${data.valorAPagar.toLocaleString()}
                    `;
                }
            },
            xAxis: {
                type: 'category',
                data: months,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '${value}'
                }
            },
            series: [{
                data: values,
                type: 'bar',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#4299e1' },
                        { offset: 1, color: '#38b2ac' }
                    ])
                }
            }]
        };
        
        this.charts.monthly.setOption(option);
    },
    
    createStatusChart: function() {
        const kpis = window.DiariasSystem.getKPIs();
        
        if (this.charts.status) {
            this.charts.status.dispose();
        }
        
        const chartDom = document.getElementById('status-chart');
        this.charts.status = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: ${c} ({d}%)'
            },
            series: [{
                name: 'Status',
                type: 'pie',
                radius: '70%',
                data: [
                    { value: kpis.valorPago, name: 'Pago', itemStyle: { color: '#48bb78' } },
                    { value: kpis.valorAPagar, name: 'A Pagar', itemStyle: { color: '#ed8936' } }
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        
        this.charts.status.setOption(option);
    },
    
    createProjectChart: function() {
        const projectData = window.DiariasSystem.getProjectData();
        const projects = Object.keys(projectData);
        const values = projects.map(project => projectData[project].totalValor);
        
        if (this.charts.project) {
            this.charts.project.dispose();
        }
        
        const chartDom = document.getElementById('project-chart');
        this.charts.project = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    const data = projectData[params[0].name];
                    return `
                        <strong>${params[0].name}</strong><br/>
                        Total: $${data.totalValor.toLocaleString()}<br/>
                        Dias: ${data.totalDias}<br/>
                        Pagos: $${data.valorPago.toLocaleString()}<br/>
                        A Pagar: $${data.valorAPagar.toLocaleString()}
                    `;
                }
            },
            xAxis: {
                type: 'category',
                data: projects,
                axisLabel: {
                    rotate: 45,
                    interval: 0
                }
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '${value}'
                }
            },
            series: [{
                data: values,
                type: 'bar',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#ed8936' },
                        { offset: 1, color: '#dd6b20' }
                    ])
                }
            }]
        };
        
        this.charts.project.setOption(option);
    },
    
    createTrendChart: function() {
        const monthlyData = window.DiariasSystem.getMonthlyData();
        const months = Object.keys(monthlyData);
        const pagos = months.map(month => monthlyData[month].valorPago);
        const aPagar = months.map(month => monthlyData[month].valorAPagar);
        
        if (this.charts.trend) {
            this.charts.trend.dispose();
        }
        
        const chartDom = document.getElementById('trend-chart');
        this.charts.trend = echarts.init(chartDom);
        
        const option = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Pago', 'A Pagar']
            },
            xAxis: {
                type: 'category',
                data: months
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '${value}'
                }
            },
            series: [
                {
                    name: 'Pago',
                    type: 'line',
                    data: pagos,
                    itemStyle: { color: '#48bb78' },
                    areaStyle: { opacity: 0.3 }
                },
                {
                    name: 'A Pagar',
                    type: 'line',
                    data: aPagar,
                    itemStyle: { color: '#ed8936' },
                    areaStyle: { opacity: 0.3 }
                }
            ]
        };
        
        this.charts.trend.setOption(option);
    },
    
    // === EXPORTAÇÃO ===
    
    exportCSV: function() {
        const csvContent = window.DiariasSystem.exportToCSV();
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `diarias_${new Date().toISOString().split('T')[0]}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        console.log('📄 CSV exportado com sucesso!');
    },
    
    generateExcel: function() {
        console.log('📊 Iniciando geração de Excel...');
        
        // Mostrar loading
        const btn = document.getElementById('export-excel');
        const originalText = btn.innerHTML;
        btn.innerHTML = '⏳ Gerando Excel...';
        btn.disabled = true;
        
        // Preparar dados para envio
        const exportData = {
            workingData: window.DiariasSystem.workingData,
            creditSystem: window.DiariasSystem.creditSystem,
            timestamp: new Date().toISOString()
        };
        
        // Simular geração (em produção, seria uma chamada para o backend)
        setTimeout(() => {
            // Criar arquivo CSV como fallback
            const csvContent = this.generateAdvancedCSV();
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            
            if (link.download !== undefined) {
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', `diarias_completo_${new Date().toISOString().split('T')[0]}.csv`);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
            
            // Restaurar botão
            btn.innerHTML = originalText;
            btn.disabled = false;
            
            // Mostrar informações
            alert(`✅ Arquivo CSV avançado gerado com sucesso!\n\n📋 Conteúdo:\n• Dados detalhados das diárias\n• Sistema de créditos\n• KPIs calculados\n• Resumos mensais\n\n💡 Para Excel completo com gráficos, execute:\npython generate_excel.py`);
            
            console.log('✅ CSV avançado gerado com sucesso!');
        }, 1500);
    },
    
    generateAdvancedCSV: function() {
        const kpis = window.DiariasSystem.getKPIs();
        const creditInfo = window.DiariasSystem.getCreditInfo();
        const monthlyData = window.DiariasSystem.getMonthlyData();
        const projectData = window.DiariasSystem.getProjectData();
        
        let csvContent = '';
        
        // Cabeçalho do relatório
        csvContent += `RELATÓRIO COMPLETO DE DIÁRIAS DE ALIMENTAÇÃO\n`;
        csvContent += `Gerado em: ${new Date().toLocaleString('pt-BR')}\n`;
        csvContent += `\n`;
        
        // KPIs principais
        csvContent += `INDICADORES PRINCIPAIS\n`;
        csvContent += `Indicador,Valor\n`;
        csvContent += `Total de Dias,${kpis.totalDias}\n`;
        csvContent += `Valor Total,$${kpis.totalValor.toLocaleString()}\n`;
        csvContent += `Dias Pagos,${kpis.diasPagos}\n`;
        csvContent += `Valor Pago,$${kpis.valorPago.toLocaleString()}\n`;
        csvContent += `Dias A Pagar,${kpis.diasAPagar}\n`;
        csvContent += `Valor A Pagar,$${kpis.valorAPagar.toLocaleString()}\n`;
        csvContent += `Percentual Pago,${kpis.percentualPago}%\n`;
        csvContent += `\n`;
        
        // Sistema de créditos
        csvContent += `SISTEMA DE CRÉDITOS\n`;
        csvContent += `Item,Valor\n`;
        csvContent += `Total Depositado,$${creditInfo.totalDeposited.toLocaleString()}\n`;
        csvContent += `Total Usado,$${creditInfo.totalUsed.toLocaleString()}\n`;
        csvContent += `Saldo Atual,$${creditInfo.currentBalance.toLocaleString()}\n`;
        csvContent += `Dias Restantes,${creditInfo.daysRemaining}\n`;
        csvContent += `\n`;
        
        // Histórico de depósitos
        csvContent += `HISTÓRICO DE DEPÓSITOS\n`;
        csvContent += `Data,Descrição,Valor\n`;
        creditInfo.deposits.forEach(deposit => {
            csvContent += `${new Date(deposit.date).toLocaleDateString('pt-BR')},${deposit.description},$${deposit.amount.toLocaleString()}\n`;
        });
        csvContent += `\n`;
        
        // Resumo mensal
        csvContent += `RESUMO MENSAL\n`;
        csvContent += `Mês,Total Dias,Valor Total,Dias Pagos,Valor Pago,Dias A Pagar,Valor A Pagar\n`;
        Object.entries(monthlyData).forEach(([month, data]) => {
            csvContent += `${month},${data.totalDias},$${data.totalValor.toLocaleString()},${data.diasPagos},$${data.valorPago.toLocaleString()},${data.diasAPagar},$${data.valorAPagar.toLocaleString()}\n`;
        });
        csvContent += `\n`;
        
        // Resumo por projeto
        csvContent += `RESUMO POR PROJETO\n`;
        csvContent += `Projeto,Total Dias,Valor Total,Dias Pagos,Valor Pago,Dias A Pagar,Valor A Pagar\n`;
        Object.entries(projectData).forEach(([project, data]) => {
            csvContent += `${project},${data.totalDias},$${data.totalValor.toLocaleString()},${data.diasPagos},$${data.valorPago.toLocaleString()},${data.diasAPagar},$${data.valorAPagar.toLocaleString()}\n`;
        });
        csvContent += `\n`;
        
        // Dados detalhados
        csvContent += `DADOS DETALHADOS\n`;
        csvContent += `Data,Dia da Semana,Mês,Ano,Valor USD,Status Pagamento,Projeto\n`;
        window.DiariasSystem.workingData.forEach(item => {
            csvContent += `${new Date(item.data).toLocaleDateString('pt-BR')},${item.diaSemana},${item.mes},${item.ano},$${item.valorUSD.toLocaleString()},${item.statusPagamento},${item.localProjeto}\n`;
        });
        
        return csvContent;
    }
};

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    window.DiariasApp.init();
});