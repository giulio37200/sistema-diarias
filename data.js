// Sistema Completo de Controle de Diárias - Dados e Lógica
// Criado do zero com todas as funcionalidades integradas

// Dados iniciais de exemplo
const initialData = [
    {
        data: "2025-01-02",
        diaSemana: "Quinta-feira",
        mes: "Janeiro",
        ano: 2025,
        valorUSD: 250,
        statusPagamento: "A Pagar",
        localProjeto: "Projeto Alpha"
    },
    {
        data: "2025-01-03",
        diaSemana: "Sexta-feira",
        mes: "Janeiro",
        ano: 2025,
        valorUSD: 250,
        statusPagamento: "Pago",
        localProjeto: "Projeto Alpha"
    },
    {
        data: "2025-01-08",
        diaSemana: "Quarta-feira",
        mes: "Janeiro",
        ano: 2025,
        valorUSD: 250,
        statusPagamento: "A Pagar",
        localProjeto: "Projeto Beta"
    }
];

// Sistema principal de gerenciamento
window.DiariasSystem = {
    // Dados de trabalho
    workingData: [...initialData],
    
    // Sistema de créditos antecipados
    creditSystem: {
        deposits: [
            // Exemplo inicial
            {
                id: 1,
                date: "2025-01-01",
                amount: 5000,
                description: "Pagamento antecipado Janeiro",
                timestamp: Date.now()
            }
        ],
        totalDeposited: 5000,
        totalUsed: 750, // 3 dias * 250
        currentBalance: 4250
    },
    
    // Inicializar sistema
    init: function() {
        console.log('🚀 Inicializando Sistema de Diárias...');
        this.loadFromStorage();
        this.recalculateBalance();
        console.log('✅ Sistema inicializado com sucesso!');
    },
    
    // === GERENCIAMENTO DE DIAS TRABALHADOS ===
    
    addWorkDay: function(date, project = 'Novo Projeto') {
        const dateObj = new Date(date);
        const dayNames = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
        const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                           'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
        
        const newEntry = {
            data: date,
            diaSemana: dayNames[dateObj.getDay()],
            mes: monthNames[dateObj.getMonth()],
            ano: dateObj.getFullYear(),
            valorUSD: 250,
            statusPagamento: "A Pagar",
            localProjeto: project
        };
        
        this.workingData.push(newEntry);
        this.sortData();
        
        // Descontar automaticamente do crédito
        this.deductFromCredit(250);
        this.saveToStorage();
        
        console.log(`✅ Dia adicionado: ${date} - ${project}`);
        return newEntry;
    },
    
    removeWorkDay: function(date) {
        const index = this.workingData.findIndex(item => item.data === date);
        if (index !== -1) {
            this.workingData.splice(index, 1);
            
            // Devolver crédito
            this.addToCredit(250);
            this.saveToStorage();
            
            console.log(`✅ Dia removido: ${date}`);
            return true;
        }
        return false;
    },
    
    updatePaymentStatus: function(date, status) {
        const item = this.workingData.find(item => item.data === date);
        if (item) {
            item.statusPagamento = status;
            this.saveToStorage();
            console.log(`✅ Status atualizado: ${date} -> ${status}`);
            return true;
        }
        return false;
    },
    
    hasWorkDay: function(date) {
        return this.workingData.some(item => item.data === date);
    },
    
    sortData: function() {
        this.workingData.sort((a, b) => new Date(a.data) - new Date(b.data));
    },
    
    // === SISTEMA DE CRÉDITOS ===
    
    addDeposit: function(amount, description = 'Depósito antecipado') {
        const deposit = {
            id: Date.now(),
            date: new Date().toISOString().split('T')[0],
            amount: parseFloat(amount),
            description: description,
            timestamp: Date.now()
        };
        
        this.creditSystem.deposits.push(deposit);
        this.creditSystem.totalDeposited += deposit.amount;
        this.creditSystem.currentBalance += deposit.amount;
        
        this.saveToStorage();
        console.log(`💰 Depósito adicionado: $${amount} - ${description}`);
        return deposit;
    },
    
    removeDeposit: function(depositId) {
        const index = this.creditSystem.deposits.findIndex(d => d.id === depositId);
        if (index !== -1) {
            const deposit = this.creditSystem.deposits[index];
            this.creditSystem.deposits.splice(index, 1);
            this.creditSystem.totalDeposited -= deposit.amount;
            this.creditSystem.currentBalance -= deposit.amount;
            
            this.saveToStorage();
            console.log(`💰 Depósito removido: $${deposit.amount}`);
            return true;
        }
        return false;
    },
    
    deductFromCredit: function(amount) {
        this.creditSystem.totalUsed += amount;
        this.creditSystem.currentBalance -= amount;
        this.saveToStorage();
    },
    
    addToCredit: function(amount) {
        this.creditSystem.totalUsed -= amount;
        this.creditSystem.currentBalance += amount;
        this.saveToStorage();
    },
    
    getCreditInfo: function() {
        return {
            currentBalance: this.creditSystem.currentBalance,
            totalDeposited: this.creditSystem.totalDeposited,
            totalUsed: this.creditSystem.totalUsed,
            deposits: [...this.creditSystem.deposits],
            isNegative: this.creditSystem.currentBalance < 0,
            daysRemaining: Math.floor(this.creditSystem.currentBalance / 250),
            nextPaymentNeeded: this.creditSystem.currentBalance < 0 ? Math.abs(this.creditSystem.currentBalance) : 0
        };
    },
    
    recalculateBalance: function() {
        // Recalcular total usado baseado nos dias trabalhados
        const totalDays = this.workingData.length;
        this.creditSystem.totalUsed = totalDays * 250;
        this.creditSystem.currentBalance = this.creditSystem.totalDeposited - this.creditSystem.totalUsed;
        this.saveToStorage();
    },
    
    // === ANÁLISE DE DADOS ===
    
    getKPIs: function() {
        const totalDias = this.workingData.length;
        const totalValor = totalDias * 250;
        const diasPagos = this.workingData.filter(item => item.statusPagamento === "Pago").length;
        const valorPago = diasPagos * 250;
        const diasAPagar = this.workingData.filter(item => item.statusPagamento === "A Pagar").length;
        const valorAPagar = diasAPagar * 250;
        
        return {
            totalDias,
            totalValor,
            diasPagos,
            valorPago,
            diasAPagar,
            valorAPagar,
            percentualPago: totalDias > 0 ? ((diasPagos / totalDias) * 100).toFixed(1) : 0
        };
    },
    
    getMonthlyData: function() {
        const monthlyData = {};
        
        this.workingData.forEach(item => {
            const month = item.mes;
            if (!monthlyData[month]) {
                monthlyData[month] = {
                    totalDias: 0,
                    totalValor: 0,
                    diasPagos: 0,
                    valorPago: 0,
                    diasAPagar: 0,
                    valorAPagar: 0
                };
            }
            
            monthlyData[month].totalDias++;
            monthlyData[month].totalValor += item.valorUSD;
            
            if (item.statusPagamento === "Pago") {
                monthlyData[month].diasPagos++;
                monthlyData[month].valorPago += item.valorUSD;
            } else {
                monthlyData[month].diasAPagar++;
                monthlyData[month].valorAPagar += item.valorUSD;
            }
        });
        
        return monthlyData;
    },
    
    getProjectData: function() {
        const projectData = {};
        
        this.workingData.forEach(item => {
            const project = item.localProjeto;
            if (!projectData[project]) {
                projectData[project] = {
                    totalDias: 0,
                    totalValor: 0,
                    diasPagos: 0,
                    valorPago: 0,
                    diasAPagar: 0,
                    valorAPagar: 0
                };
            }
            
            projectData[project].totalDias++;
            projectData[project].totalValor += item.valorUSD;
            
            if (item.statusPagamento === "Pago") {
                projectData[project].diasPagos++;
                projectData[project].valorPago += item.valorUSD;
            } else {
                projectData[project].diasAPagar++;
                projectData[project].valorAPagar += item.valorUSD;
            }
        });
        
        return projectData;
    },
    
    // === FILTROS E BUSCA ===
    
    getFilteredData: function(filters = {}) {
        let filteredData = [...this.workingData];
        
        if (filters.mes) {
            filteredData = filteredData.filter(item => item.mes === filters.mes);
        }
        
        if (filters.status) {
            filteredData = filteredData.filter(item => item.statusPagamento === filters.status);
        }
        
        if (filters.projeto) {
            filteredData = filteredData.filter(item => item.localProjeto === filters.projeto);
        }
        
        return filteredData;
    },
    
    getUniqueValues: function(field) {
        return [...new Set(this.workingData.map(item => item[field]))].sort();
    },
    
    // === EXPORTAÇÃO ===
    
    exportToCSV: function() {
        const headers = ['Data', 'Dia_Semana', 'Mes', 'Ano', 'Valor_USD', 'Status_Pagamento', 'Local_Projeto'];
        const csvContent = [
            headers.join(','),
            ...this.workingData.map(item => [
                item.data,
                item.diaSemana,
                item.mes,
                item.ano,
                item.valorUSD,
                item.statusPagamento,
                item.localProjeto
            ].join(','))
        ].join('\n');
        
        return csvContent;
    },
    
    // === PERSISTÊNCIA ===
    
    saveToStorage: function() {
        try {
            localStorage.setItem('diarias_working_data', JSON.stringify(this.workingData));
            localStorage.setItem('diarias_credit_system', JSON.stringify(this.creditSystem));
            console.log('💾 Dados salvos no localStorage');
        } catch (e) {
            console.warn('⚠️ Erro ao salvar dados:', e);
        }
    },
    
    loadFromStorage: function() {
        try {
            const savedWorkingData = localStorage.getItem('diarias_working_data');
            const savedCreditSystem = localStorage.getItem('diarias_credit_system');
            
            if (savedWorkingData) {
                this.workingData = JSON.parse(savedWorkingData);
                console.log('📂 Dados de trabalho carregados do localStorage');
            }
            
            if (savedCreditSystem) {
                this.creditSystem = { ...this.creditSystem, ...JSON.parse(savedCreditSystem) };
                console.log('💰 Sistema de créditos carregado do localStorage');
            }
        } catch (e) {
            console.warn('⚠️ Erro ao carregar dados:', e);
        }
    },
    
    clearAllData: function() {
        if (confirm('⚠️ Tem certeza que deseja limpar TODOS os dados? Esta ação não pode ser desfeita.')) {
            this.workingData = [];
            this.creditSystem = {
                deposits: [],
                totalDeposited: 0,
                totalUsed: 0,
                currentBalance: 0
            };
            this.saveToStorage();
            console.log('🗑️ Todos os dados foram limpos');
            return true;
        }
        return false;
    }
};

// Expor globalmente
window.rawData = initialData;
console.log('📊 Sistema de Dados carregado com sucesso!');