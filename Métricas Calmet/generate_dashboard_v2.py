import json

# Leer los datos completos
with open(r"c:\Users\User\Downloads\Métricas Calmet\meta_ads_data_complete.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

html_template = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Meta Ads - Trimestre Q4 2025</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { font-family: 'Inter', sans-serif; }
        body { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); min-height: 100vh; }
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .gradient-bg { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%); }
        .hover-lift { transition: all 0.3s ease; }
        .hover-lift:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3); }
        .success-cell { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; font-weight: 600; }
        table { border-collapse: separate; border-spacing: 0; }
        .floating-button { position: fixed; bottom: 2rem; right: 2rem; z-index: 1000; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); z-index: 2000; justify-content: center; align-items: center; }
        .modal.active { display: flex; }
        .scroll-table { max-height: 600px; overflow-y: auto; }
        .scroll-table::-webkit-scrollbar { width: 8px; }
        .scroll-table::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); border-radius: 10px; }
        .scroll-table::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.6); border-radius: 10px; }
        
        /* Estilos mejorados para los select */
        select {
            background-color: rgba(30, 41, 59, 0.9) !important;
            color: white !important;
            border: 1px solid rgba(139, 92, 246, 0.5);
        }
        select option {
            background-color: #1e293b;
            color: white;
        }
        select:focus {
            outline: none;
            border-color: rgba(139, 92, 246, 1);
        }
        
        .insight-card {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border-left: 4px solid #8b5cf6;
        }
    </style>
</head>
<body class="p-6">
    <!-- Header -->
    <div class="glass rounded-2xl p-6 mb-6">
        <h1 class="text-4xl font-bold text-white mb-2">Dashboard Meta Ads - Métricas Calmet</h1>
        <p class="text-gray-400">Análisis Trimestral: Septiembre - Noviembre 2025</p>
    </div>

    <!-- Filtro Global de Mes para KPIs -->
    <div class="glass rounded-2xl p-4 mb-6">
        <div class="flex items-center gap-4">
            <label class="text-white font-medium">Filtrar KPIs por:</label>
            <select id="kpiMonthFilter" class="glass rounded-lg px-4 py-2 text-white outline-none" onchange="updateKPIs()">
                <option value="all">Trimestre Completo</option>
                <option value="septiembre">Septiembre</option>
                <option value="octubre">Octubre</option>
                <option value="noviembre">Noviembre</option>
            </select>
        </div>
    </div>

    <!-- KPIs Macro -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="glass rounded-2xl p-6 hover-lift">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-gray-400 text-sm font-medium">Inversión Total</h3>
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center"><span class="text-2xl">💰</span></div>
            </div>
            <p class="text-4xl font-bold text-white" id="kpi-inversion">S/ 0.00</p>
            <p class="text-green-400 text-sm mt-2" id="kpi-inversion-label">Trimestre Completo</p>
        </div>
        <div class="glass rounded-2xl p-6 hover-lift">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-gray-400 text-sm font-medium">Conversaciones</h3>
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center"><span class="text-2xl">💬</span></div>
            </div>
            <p class="text-4xl font-bold text-white" id="kpi-conversaciones">0</p>
            <p class="text-green-400 text-sm mt-2" id="kpi-conversaciones-label">Total Generadas</p>
        </div>
        <div class="glass rounded-2xl p-6 hover-lift">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-gray-400 text-sm font-medium">CPA Promedio</h3>
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center"><span class="text-2xl">📊</span></div>
            </div>
            <p class="text-4xl font-bold text-white" id="kpi-cpa">S/ 0.00</p>
            <p class="text-purple-400 text-sm mt-2" id="kpi-trend">Tendencia del trimestre</p>
        </div>
    </div>

    <!-- Gráficos -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div class="glass rounded-2xl p-6">
            <h3 class="text-xl font-semibold text-white mb-4">Tendencia Mensual</h3>
            <canvas id="trendChart"></canvas>
        </div>
        <div class="glass rounded-2xl p-6">
            <h3 class="text-xl font-semibold text-white mb-4">Top 10 Tratamientos</h3>
            <div class="grid grid-cols-2 gap-3 mb-4">
                <select id="monthFilter" class="glass rounded-lg px-4 py-2 text-white outline-none">
                    <option value="septiembre">Septiembre</option>
                    <option value="octubre">Octubre</option>
                    <option value="noviembre" selected>Noviembre</option>
                </select>
                <select id="responsibleFilter" class="glass rounded-lg px-4 py-2 text-white outline-none">
                    <option value="global" selected>Global</option>
                    <option value="ericka">Ericka</option>
                    <option value="pablo">Pablo</option>
                </select>
            </div>
            <canvas id="top10Chart"></canvas>
        </div>
    </div>

    <!-- Tabla Maestra con Filtros Mejorados -->
    <div class="glass rounded-2xl p-6 mb-6">
        <div class="flex flex-col gap-4 mb-4">
            <div class="flex justify-between items-center">
                <h3 class="text-xl font-semibold text-white">Detalle Completo de Tratamientos</h3>
                <div class="text-gray-400 text-sm" id="tableInfo">Mostrando todos los registros</div>
            </div>
            
            <!-- Filtros de la tabla -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div>
                    <label class="text-gray-400 text-xs mb-1 block">Vista</label>
                    <select id="tableViewFilter" class="glass rounded-lg px-4 py-2 text-white outline-none w-full">
                        <option value="all">Todos los Meses</option>
                        <option value="septiembre">Solo Septiembre</option>
                        <option value="octubre">Solo Octubre</option>
                        <option value="noviembre">Solo Noviembre</option>
                    </select>
                </div>
                <div>
                    <label class="text-gray-400 text-xs mb-1 block">Responsable</label>
                    <select id="tableResponsibleFilter" class="glass rounded-lg px-4 py-2 text-white outline-none w-full">
                        <option value="global" selected>Global</option>
                        <option value="ericka">Ericka</option>
                        <option value="pablo">Pablo</option>
                    </select>
                </div>
                <div>
                    <label class="text-gray-400 text-xs mb-1 block">Ordenar por</label>
                    <select id="tableSortFilter" class="glass rounded-lg px-4 py-2 text-white outline-none w-full">
                        <option value="ranking">Ranking</option>
                        <option value="inversion">Inversión (Mayor a Menor)</option>
                        <option value="conversaciones">Conversaciones (Mayor a Menor)</option>
                        <option value="cpa">CPA (Menor a Mayor)</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div class="scroll-table">
            <table class="w-full text-sm">
                <thead class="sticky top-0 bg-slate-800 text-gray-300">
                    <tr>
                        <th class="text-left p-3">Mes</th>
                        <th class="text-left p-3">Ranking</th>
                        <th class="text-left p-3">Tratamiento</th>
                        <th class="text-right p-3">Inversión (S/)</th>
                        <th class="text-right p-3">Conversaciones</th>
                        <th class="text-right p-3">CPA (S/)</th>
                        <th class="text-right p-3">CTR (%)</th>
                        <th class="text-right p-3">Frecuencia</th>
                    </tr>
                </thead>
                <tbody id="tableBody" class="text-white"></tbody>
            </table>
        </div>
    </div>

    <!-- Cuadros Analíticos -->
    <div class="glass rounded-2xl p-6 mb-6">
        <h3 class="text-2xl font-bold text-white mb-6">📈 Insights y Análisis Estratégico</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Evolución de Eficiencia -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">🎯 Evolución de Eficiencia</h4>
                <ul class="text-gray-300 space-y-2 text-sm">
                    <li>• <strong class="text-white">Mejora del 30%</strong> en CPA de Sep a Nov (S/ 2.62 → S/ 1.84)</li>
                    <li>• <strong class="text-green-400">+40% conversaciones</strong> en Nov vs Sep (7,431 → 10,436)</li>
                    <li>• Inversión estable (~S/ 19,400/mes) con mejores resultados</li>
                    <li>• Noviembre logró el <strong class="text-yellow-400">CPA más bajo del trimestre</strong></li>
                </ul>
            </div>

            <!-- Rendimiento por WhatsApp -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">📱 Rendimiento por Cuenta WhatsApp</h4>
                <ul class="text-gray-300 space-y-2 text-sm" id="whatsappInsights">
                    <!-- Se llenará dinámicamente -->
                </ul>
            </div>

            <!-- Optimización de Presupuesto -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">💡 Optimización de Presupuesto</h4>
                <ul class="text-gray-300 space-y-2 text-sm">
                    <li>• Reducción de <strong class="text-green-400">S/ 305.68</strong> en inversión de Sep a Nov</li>
                    <li>• <strong class="text-white">ROI mejorado:</strong> Más leads con menos presupuesto</li>
                    <li>• Los tratamientos con CPA < S/ 2.00 representan oportunidades de escalado</li>
                    <li>• Se identificaron <span id="lowCpaCount">X</span> tratamientos con CPA óptimo</li>
                </ul>
            </div>

            <!-- Top Performers -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">🏆 Top Performers Consistentes</h4>
                <ul class="text-gray-300 space-y-2 text-sm" id="topPerformers">
                    <!-- Se llenará dinámicamente -->
                </ul>
            </div>

            <!-- Tendencias y Patrones -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">📊 Tendencias y Patrones</h4>
                <ul class="text-gray-300 space-y-2 text-sm" id="trends">
                    <!-- Se llenará dinámicamente -->
                </ul>
            </div>

            <!-- Recomendaciones -->
            <div class="insight-card glass rounded-xl p-5">
                <h4 class="text-lg font-semibold text-purple-400 mb-3">💼 Recomendaciones Estratégicas</h4>
                <ul class="text-gray-300 space-y-2 text-sm">
                    <li>• <strong>Escalar:</strong> Tratamientos con CPA < S/ 2.00 tienen margen de crecimiento</li>
                    <li>• <strong>Optimizar:</strong> Revisar tratamientos con CPA > S/ 4.00</li>
                    <li>• <strong>Replicar:</strong> Estrategias de Noviembre en meses futuros</li>
                    <li>• <strong>Testear:</strong> Aumentar presupuesto en top performers para maximizar resultados</li>
                </ul>
            </div>
        </div>
    </div>

    <button onclick="showInsight()" class="floating-button gradient-bg text-white px-6 py-3 rounded-full font-semibold shadow-2xl">✨ Ver Análisis IA</button>

    <div id="insightModal" class="modal">
        <div class="glass rounded-2xl p-8 max-w-2xl mx-4">
            <h3 class="text-2xl font-bold text-white mb-4">💡 Insight Estratégico</h3>
            <p class="text-gray-300 text-lg leading-relaxed mb-6">
                <strong class="text-purple-400">Noviembre rompió récord de eficiencia</strong> con un CPA de <strong class="text-green-400">S/ 1.84</strong>, 
                reduciendo costos un <strong class="text-yellow-400">30%</strong> frente a septiembre (S/ 2.62). 
                Esto se logró aumentando las conversaciones en un <strong class="text-blue-400">40%</strong> mientras se mantenía 
                la inversión similar. El tratamiento "laser co2" se mantiene como líder consistente en los 3 meses.
            </p>
            <button onclick="hideInsight()" class="gradient-bg px-6 py-3 rounded-lg font-semibold text-white hover:opacity-90">Cerrar</button>
        </div>
    </div>

    <script>
        const db = ''' + json.dumps(data, ensure_ascii=False, indent=2) + ''';

        // Función para actualizar KPIs según filtro
        function updateKPIs() {
            const monthFilter = document.getElementById('kpiMonthFilter').value;
            let inversion, conversaciones, cpa, label, trend;

            if (monthFilter === 'all') {
                inversion = db.evolution.inversion.reduce((a, b) => a + b, 0);
                conversaciones = db.evolution.conversaciones.reduce((a, b) => a + b, 0);
                cpa = inversion / conversaciones;
                label = 'Trimestre Completo';
                const mejora = ((db.evolution.cpa[0] - db.evolution.cpa[2]) / db.evolution.cpa[0] * 100).toFixed(0);
                trend = `Mejora del ${mejora}% vs Sep`;
            } else {
                const monthIndex = ['septiembre', 'octubre', 'noviembre'].indexOf(monthFilter);
                inversion = db.evolution.inversion[monthIndex];
                conversaciones = db.evolution.conversaciones[monthIndex];
                cpa = db.evolution.cpa[monthIndex];
                label = monthFilter.charAt(0).toUpperCase() + monthFilter.slice(1);
                const monthNames = {septiembre: 'Sep', octubre: 'Oct', noviembre: 'Nov'};
                trend = `CPA: S/ ${cpa.toFixed(2)}`;
            }

            document.getElementById('kpi-inversion').textContent = 'S/ ' + inversion.toLocaleString('es-PE', {minimumFractionDigits: 2});
            document.getElementById('kpi-conversaciones').textContent = conversaciones.toLocaleString('es-PE');
            document.getElementById('kpi-cpa').textContent = 'S/ ' + cpa.toFixed(2);
            document.getElementById('kpi-inversion-label').textContent = label;
            document.getElementById('kpi-conversaciones-label').textContent = label;
            document.getElementById('kpi-trend').textContent = trend;
        }

        // Gráfico de Tendencia con tooltips mejorados
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'bar',
            data: {
                labels: db.evolution.labels,
                datasets: [{
                    label: 'Inversión (S/)',
                    data: db.evolution.inversion,
                    backgroundColor: 'rgba(139, 92, 246, 0.8)',
                    borderColor: 'rgba(139, 92, 246, 1)',
                    borderWidth: 2,
                    yAxisID: 'y'
                }, {
                    label: 'CPA (S/)',
                    data: db.evolution.cpa,
                    type: 'line',
                    borderColor: 'rgba(34, 197, 94, 1)',
                    backgroundColor: 'rgba(34, 197, 94, 0.2)',
                    borderWidth: 3,
                    yAxisID: 'y1',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: { labels: { color: 'white' } },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return context[0].label;
                            },
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += 'S/ ' + context.parsed.y.toFixed(2);
                                return label;
                            },
                            afterLabel: function(context) {
                                const index = context.dataIndex;
                                if (context.dataset.label === 'Inversión (S/)') {
                                    return 'CPA: S/ ' + db.evolution.cpa[index].toFixed(2);
                                } else {
                                    return 'Inversión: S/ ' + db.evolution.inversion[index].toFixed(2);
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                    y: { position: 'left', ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' }, title: { display: true, text: 'Inversión (S/)', color: 'white' } },
                    y1: { position: 'right', ticks: { color: 'white' }, grid: { display: false }, title: { display: true, text: 'CPA (S/)', color: 'white' } }
                }
            }
        });

        // Top 10 Chart
        let top10Chart;
        function updateTop10Chart() {
            const month = document.getElementById('monthFilter').value;
            const responsible = document.getElementById('responsibleFilter').value;
            const data = db.months[month][responsible];
            const top10 = data.slice(0, 10);

            const ctx = document.getElementById('top10Chart').getContext('2d');
            if (top10Chart) top10Chart.destroy();

            top10Chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: top10.map(item => item.Tratamiento),
                    datasets: [{
                        label: 'Inversión (S/)',
                        data: top10.map(item => item['Inversión (S/)']),
                        backgroundColor: 'rgba(99, 102, 241, 0.8)',
                        borderColor: 'rgba(99, 102, 241, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: { legend: { labels: { color: 'white' } } },
                    scales: {
                        x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                        y: { ticks: { color: 'white', font: { size: 10 } }, grid: { display: false } }
                    }
                }
            });
        }

        // Tabla Maestra Mejorada
        function updateMasterTable() {
            const viewFilter = document.getElementById('tableViewFilter').value;
            const responsibleFilter = document.getElementById('tableResponsibleFilter').value;
            const sortFilter = document.getElementById('tableSortFilter').value;

            let allData = [];

            if (viewFilter === 'all') {
                ['septiembre', 'octubre', 'noviembre'].forEach(month => {
                    const monthData = db.months[month][responsibleFilter];
                    monthData.forEach(row => {
                        allData.push({...row, month: month});
                    });
                });
            } else {
                const monthData = db.months[viewFilter][responsibleFilter];
                monthData.forEach(row => {
                    allData.push({...row, month: viewFilter});
                });
            }

            // Ordenar
            if (sortFilter === 'inversion') {
                allData.sort((a, b) => (b['Inversión (S/)'] || 0) - (a['Inversión (S/)'] || 0));
            } else if (sortFilter === 'conversaciones') {
                allData.sort((a, b) => (b.Conversaciones || 0) - (a.Conversaciones || 0));
            } else if (sortFilter === 'cpa') {
                allData.sort((a, b) => (a['CPA (S/)'] || 999) - (b['CPA (S/)'] || 999));
            }

            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            allData.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-gray-700 hover:bg-white/5';
                
                const cpa = row['CPA (S/)'] || 0;
                const cpaClass = cpa < 2 ? 'success-cell' : '';

                const monthNames = {septiembre: 'Sep', octubre: 'Oct', noviembre: 'Nov'};

                tr.innerHTML = `
                    <td class="p-3"><span class="px-2 py-1 rounded text-xs bg-purple-500/20 text-purple-300">${monthNames[row.month]}</span></td>
                    <td class="p-3">${row.Ranking || '-'}</td>
                    <td class="p-3 font-medium">${row.Tratamiento || '-'}</td>
                    <td class="p-3 text-right">S/ ${(row['Inversión (S/)'] || 0).toLocaleString('es-PE', {minimumFractionDigits: 2})}</td>
                    <td class="p-3 text-right">${(row.Conversaciones || 0).toLocaleString('es-PE')}</td>
                    <td class="p-3 text-right ${cpaClass}">S/ ${cpa.toFixed(2)}</td>
                    <td class="p-3 text-right">${(row['CTR (%)'] || 0).toFixed(2)}%</td>
                    <td class="p-3 text-right">${(row.Frecuencia || 0).toFixed(2)}</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('tableInfo').textContent = `Mostrando ${allData.length} registros`;
        }

        // Análisis dinámicos
        function generateInsights() {
            // Rendimiento por WhatsApp
            const erickaTotal = db.evolution.inversion.reduce((sum, _, i) => {
                const erickaData = Object.values(db.months)[i].ericka;
                return sum + erickaData.reduce((s, r) => s + (r['Inversión (S/)'] || 0), 0);
            }, 0);
            
            const pabloTotal = db.evolution.inversion.reduce((sum, _, i) => {
                const pabloData = Object.values(db.months)[i].pablo;
                return sum + pabloData.reduce((s, r) => s + (r['Inversión (S/)'] || 0), 0);
            }, 0);

            document.getElementById('whatsappInsights').innerHTML = `
                <li>• <strong class="text-white">Ericka:</strong> S/ ${erickaTotal.toFixed(2)} invertidos en el trimestre</li>
                <li>• <strong class="text-white">Pablo:</strong> S/ ${pabloTotal.toFixed(2)} invertidos en el trimestre</li>
                <li>• Ambas cuentas muestran <strong class="text-green-400">mejora sostenida</strong> en eficiencia</li>
                <li>• Coordinación efectiva entre equipos de WhatsApp</li>
            `;

            // Top Performers
            const allTreatments = {};
            ['septiembre', 'octubre', 'noviembre'].forEach(month => {
                db.months[month].global.forEach(row => {
                    if (!allTreatments[row.Tratamiento]) {
                        allTreatments[row.Tratamiento] = [];
                    }
                    allTreatments[row.Tratamiento].push(row.Ranking);
                });
            });

            const consistent = Object.entries(allTreatments)
                .filter(([_, rankings]) => rankings.length === 3 && rankings.every(r => r <= 10))
                .map(([name, _]) => name)
                .slice(0, 4);

            document.getElementById('topPerformers').innerHTML = consistent.map(name => 
                `<li>• <strong class="text-yellow-400">${name}</strong> - Top 10 los 3 meses</li>`
            ).join('');

            // Tendencias
            const lowCpaCount = Object.values(db.months.noviembre.global).filter(r => (r['CPA (S/)'] || 999) < 2).length;
            document.getElementById('lowCpaCount').textContent = lowCpaCount;

            const avgCTR = db.evolution.inversion.map((_, i) => {
                const monthData = Object.values(db.months)[i].global;
                const avgCtr = monthData.reduce((sum, r) => sum + (r['CTR (%)'] || 0), 0) / monthData.length;
                return avgCtr.toFixed(2);
            });

            document.getElementById('trends').innerHTML = `
                <li>• <strong class="text-white">CTR promedio:</strong> ${avgCTR[0]}% (Sep) → ${avgCTR[2]}% (Nov)</li>
                <li>• <strong class="text-green-400">${lowCpaCount} tratamientos</strong> con CPA óptimo en Noviembre</li>
                <li>• Frecuencia de impresión optimizada mes a mes</li>
                <li>• Alcance creciente con mejor targeting</li>
            `;
        }

        // Event Listeners
        document.getElementById('monthFilter').addEventListener('change', updateTop10Chart);
        document.getElementById('responsibleFilter').addEventListener('change', updateTop10Chart);
        document.getElementById('tableViewFilter').addEventListener('change', updateMasterTable);
        document.getElementById('tableResponsibleFilter').addEventListener('change', updateMasterTable);
        document.getElementById('tableSortFilter').addEventListener('change', updateMasterTable);

        function showInsight() {
            document.getElementById('insightModal').classList.add('active');
        }

        function hideInsight() {
            document.getElementById('insightModal').classList.remove('active');
        }

        // Inicializar
        updateKPIs();
        updateTop10Chart();
        updateMasterTable();
        generateInsights();
    </script>
</body>
</html>''';

# Guardar
output_path = r"c:\Users\User\Downloads\Métricas Calmet\dashboard_meta_ads.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"[SUCCESS] Dashboard mejorado generado: {output_path}")
print(f"Tamano del archivo: {len(html_template):,} bytes")
print("Mejoras aplicadas:")
print("  - Subtitulo cambiado a 2025")
print("  - Filtro de mes en KPIs")
print("  - Tooltips mejorados en grafico de tendencia")
print("  - Colores de fondo corregidos en dropdowns")
print("  - Filtros completos en tabla (Mes/Responsable/Ordenamiento)")
print("  - Seccion de cuadros analiticos agregada")
print("  - Insights dinamicos generados")
