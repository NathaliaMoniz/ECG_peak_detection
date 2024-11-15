import pandas as pd
import os

# Ruta del archivo de Excel y la base de datos ECG-ID
path_excel = 'ecg_databases.xlsx'
path_database_ecg_id = 'C:\\Users\\natha\\OneDrive\\Documentos\\GitHub\\Fabricacion-de-ECG-con-GAN\\BBDD\\ecg-id-database-1.0.0'

# Cargar el archivo de Excel existente
report_table = pd.read_excel(path_excel)

import wfdb

# Lista para almacenar las nuevas filas
new_rows = []

# Recorrer cada paciente en el dataset ECG-ID
for patient_id in os.listdir(path_database_ecg_id):
    patient_path = os.path.join(path_database_ecg_id, patient_id)
    
    # Verificar que sea un directorio (para evitar archivos sueltos)
    if os.path.isdir(patient_path):
        # Obtener todos los archivos .hea para cada paciente
        records = [f.split('.')[0] for f in os.listdir(patient_path) if f.endswith('.hea')]
        
        for record_id in records:
            # Leer la información del archivo .hea
            path_file = os.path.join(patient_path, record_id)
            record = wfdb.rdsamp(path_file)
            fs = record[1]['fs']  # Frecuencia de muestreo
            length = len(record[0])  # Longitud total del ECG
            num_channels = record[0].shape[1]  # Número de canales

            # Crear una fila por cada canal disponible
            for channel_num in range(num_channels):
                # Obtener el nombre del canal
                lead_name = record[1]['sig_name'][channel_num]

                # Crear una nueva fila con la información de este canal
                new_row = {
                    'Database': 'ECG-ID',
                    'Patient': patient_id,
                    'Select': 1 if channel_num == 0 else 0,  # Solo seleccionar el primer canal como "1"
                    'Lead': lead_name,
                    'Num': channel_num,
                    'Frequency': fs,
                    'Length': length
                }
                new_rows.append(new_row)

# Crear un DataFrame con las nuevas filas y añadirlas al DataFrame existente
new_data = pd.DataFrame(new_rows)
report_table = pd.concat([report_table, new_data], ignore_index=True)

# Guardar el archivo actualizado en Excel
report_table.to_excel(path_excel, index=False)


