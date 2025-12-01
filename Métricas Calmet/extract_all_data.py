import pandas as pd
import json
import os

# Rutas a los archivos Excel
files = {
    'septiembre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Setiembre.xlsx",
    'octubre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Octubre.xlsx",
    'noviembre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Noviembre.xlsx"
}

# Estructura de datos completa
data = {
    "months": {
        "septiembre": {"global": [], "ericka": [], "pablo": []},
        "octubre": {"global": [], "ericka": [], "pablo": []},
        "noviembre": {"global": [], "ericka": [], "pablo": []}
    },
    "evolution": {
        "labels": ["Septiembre", "Octubre", "Noviembre"],
        "inversion": [],
        "conversaciones": [],
        "cpa": []
    }
}

def clean_value(val):
    """Limpia y convierte valores a formatos apropiados"""
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val) if not pd.isna(val) else 0
    return str(val).strip()

def extract_sheet_data(file_path, sheet_name):
    """Extrae TODOS los datos de una hoja específica"""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Convertir TODAS las filas a diccionarios
        rows = []
        for idx, row in df.iterrows():
            row_data = {}
            for col in df.columns:
                row_data[col] = clean_value(row[col])
            rows.append(row_data)
        
        print(f"  [OK] {sheet_name}: {len(rows)} filas extraídas")
        return rows
    except Exception as e:
        print(f"  [ERROR] Error en {sheet_name}: {e}")
        return []

# Extraer datos de cada mes
for month_key, file_path in files.items():
    print(f"\n[*] Procesando {month_key.upper()}...")
    
    if not os.path.exists(file_path):
        print(f"  [ERROR] Archivo no encontrado: {file_path}")
        continue
    
    # Extraer las 3 hojas principales
    data["months"][month_key]["global"] = extract_sheet_data(file_path, "Ranking Global de Tratamientos")
    data["months"][month_key]["ericka"] = extract_sheet_data(file_path, "Ranking Ericka - Tratamientos")
    data["months"][month_key]["pablo"] = extract_sheet_data(file_path, "Ranking Pablo - Tratamientos")

# Calcular datos de evolución (totales por mes)
print("\n[+] Calculando datos de evolucion...")
for month_key in ['septiembre', 'octubre', 'noviembre']:
    global_data = data["months"][month_key]["global"]
    
    if global_data:
        # Buscar columnas de inversión y conversaciones (pueden tener nombres variados)
        total_inv = 0
        total_conv = 0
        
        # Intentar sumar valores numéricos relevantes
        for row in global_data:
            for key, val in row.items():
                key_lower = str(key).lower()
                if 'inversi' in key_lower or 'gasto' in key_lower or 'spend' in key_lower:
                    try:
                        total_inv += float(val) if val else 0
                    except:
                        pass
                elif 'conversacion' in key_lower or 'conversion' in key_lower:
                    try:
                        total_conv += float(val) if val else 0
                    except:
                        pass
        
        data["evolution"]["inversion"].append(round(total_inv, 2))
        data["evolution"]["conversaciones"].append(int(total_conv))
        
        # Calcular CPA
        cpa = round(total_inv / total_conv, 2) if total_conv > 0 else 0
        data["evolution"]["cpa"].append(cpa)
        
        print(f"  {month_key.capitalize()}: Inv={total_inv:.2f}, Conv={total_conv}, CPA={cpa:.2f}")

# Guardar a archivo JSON
output_file = r"c:\Users\User\Downloads\Métricas Calmet\meta_ads_data_complete.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n[SUCCESS] Datos completos guardados en: {output_file}")

# Mostrar resumen
print("\n=== RESUMEN DE EXTRACCION ===")
for month_key in ['septiembre', 'octubre', 'noviembre']:
    print(f"\n{month_key.upper()}:")
    print(f"  - Ranking Global: {len(data['months'][month_key]['global'])} filas")
    print(f"  - Ericka: {len(data['months'][month_key]['ericka'])} filas")
    print(f"  - Pablo: {len(data['months'][month_key]['pablo'])} filas")
    print(f"  - TOTAL: {len(data['months'][month_key]['global']) + len(data['months'][month_key]['ericka']) + len(data['months'][month_key]['pablo'])} filas")
