import pandas as pd

files = {
    'septiembre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Setiembre.xlsx",
    'octubre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Octubre.xlsx",
    'noviembre': r"c:\Users\User\Downloads\Métricas Calmet\Meta Ads - Noviembre.xlsx"
}

for month, file_path in files.items():
    print(f"\n=== {month.upper()} ===")
    try:
        xls = pd.ExcelFile(file_path)
        print(f"Hojas disponibles:")
        for i, sheet in enumerate(xls.sheet_names, 1):
            print(f"  {i}. '{sheet}'")
    except Exception as e:
        print(f"Error: {e}")
