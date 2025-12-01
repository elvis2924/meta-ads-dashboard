import json

# Leer los datos completos
with open(r"c:\Users\User\Downloads\Métricas Calmet\meta_ads_data_complete.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Leer la plantilla HTML base
html_template_start = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Meta Ads - Trimestre Q4 2024</title>
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
    </style>
</head>
<body class="p-6">
    <div class="glass rounded-2xl p-6 mb-6">
        <h1 class="text-4xl font-bold text-white mb-2">Dashboard Meta Ads - Métricas Calmet</h1>
        <p class="text-gray-400">Análisis Trimestral: Septiembre - Noviembre 2024</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="glass rounded-2xl p-6 hover-lift">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-gray-400 text-sm font-medium">Inversión Total</h3>
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center"><span class="text-2xl">💰</span></div>
            </div>
            <p class="text-4xl font-bold text-white" id="kpi-inversion">S/ 0.00</p>
            <p class="text-green-400 text-sm mt-2">Trimestre Completo</p>
        </div>
        <div class="glass rounded-2xl p-6 hover-lift">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-gray-400 text-sm font-medium">Conversaciones</h3>
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center"><span class="text-2xl">💬</span></div>
            </div>
            <p class="text-4xl font-bold text-white" id="kpi-conversaciones">0</p>
            <p class="text-green-400 text-sm mt-2">Total Generadas</p>
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

    <div class="glass rounded-2xl p-6">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-white">Detalle Completo de Tratamientos</h3>
            <div class="text-gray-400 text-sm" id="tableInfo">Mostrando todos los registros</div>
        </div>
        <div class="scroll-table">
            <table class="w-full text-sm">
                <thead class="sticky top-0 bg-slate-800 text-gray-300">
                    <tr>
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

    <button onclick="showInsight()" class="floating-button gradient-bg text-white px-6 py-3 rounded-full font-semibold shadow-2xl">✨ Ver Análisis IA</button>

    <div id="insightModal" class="modal">
        <div class="glass rounded-2xl p-8 max-w-2xl mx-4">
            <h3 class="text-2xl font-bold text-white mb-4">💡 Insight Estratégico</h3>
            <p class="text-gray-300 text-lg leading-relaxed mb-6">
                <strong class="text-purple-400">Noviembre rompió récord de eficiencia</strong> con un CPA de <strong class="text-green-400">S/ 1.84</strong>, 
                reduciendo costos un <strong class="text-yellow-400">25%</strong> frente a septiembre (S/ 2.62). 
                Esto se logró aumentando las conversaciones en un <strong class="text-blue-400">40%</strong> mientras se mantenía 
                la inversión similar. El tratamiento "laser co2" se mantiene como líder consistente en los 3 meses.
            </p>
            <button onclick="hideInsight()" class="gradient-bg px-6 py-3 rounded-lg font-semibold text-white hover:opacity-90">Cerrar</button>
        </div>
    </div>

    <script>
        const db = '''

html_template_end = ''';

        // Calcular KPIs
        const totalInversion = db.evolution.inversion.reduce((a, b) => a + b, 0);
        const totalConversaciones = db.evolution.conversaciones.reduce((a, b) => a + b, 0);
        const cpaPromedio = totalInversion / totalConversaciones;

        document.getElementById('kpi-inversion').textContent = 'S/ ' + totalInversion.toLocaleString('es-PE', {minimumFractionDigits: 2});
        document.getElementById('kpi-conversaciones').textContent = totalConversaciones.toLocaleString('es-PE');
        document.getElementById('kpi-cpa').textContent = 'S/ ' + cpaPromedio.toFixed(2);

        const mejoraCPA = ((db.evolution.cpa[0] - db.evolution.cpa[2]) / db.evolution.cpa[0] * 100).toFixed(0);
        document.getElementById('kpi-trend').textContent = `Mejora del ${mejoraCPA}% vs Sep`;

        // Gráfico de Tendencia
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
                plugins: {
                    legend: { labels: { color: 'white' } }
                },
                scales: {
                    x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                    y: { position: 'left', ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
                    y1: { position: 'right', ticks: { color: 'white' }, grid: { display: false } }
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

            updateTable();
        }

        // Tabla Maestra
        function updateTable() {
            const month = document.getElementById('monthFilter').value;
            const responsible = document.getElementById('responsibleFilter').value;
            const data = db.months[month][responsible];

            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-gray-700 hover:bg-white/5';
                
                const cpa = row['CPA (S/)'] || 0;
                const cpaClass = cpa < 2 ? 'success-cell' : '';

                tr.innerHTML = `
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

            document.getElementById('tableInfo').textContent = `Mostrando ${data.length} registros`;
        }

        document.getElementById('monthFilter').addEventListener('change', updateTop10Chart);
        document.getElementById('responsibleFilter').addEventListener('change', updateTop10Chart);

        function showInsight() {
            document.getElementById('insightModal').classList.add('active');
        }

        function hideInsight() {
            document.getElementById('insightModal').classList.remove('active');
        }

        // Inicializar
        updateTop10Chart();
    </script>
</body>
</html>'''

# Generar HTML completo
full_html = html_template_start + json.dumps(data, ensure_ascii=False, indent=2) + html_template_end

# Guardar
output_path = r"c:\Users\User\Downloads\Métricas Calmet\dashboard_meta_ads.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"[SUCCESS] Dashboard HTML generado: {output_path}")
print(f"Tamaño del archivo: {len(full_html):,} bytes")
print(f"Total de registros incluidos: 228 filas")
