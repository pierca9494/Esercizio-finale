import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# Generazione dei dati
np.random.seed(42)  # Per risultati riproducibili
days = 305
mean_visitors = 1200
std_dev_visitors = 900
trend = np.linspace(0, -300, days)  # Trend decrescente

# Numero di visitatori con trend
visitors = np.random.normal(mean_visitors, std_dev_visitors, days) + trend
visitors = np.maximum(visitors, 0).astype(int)  # Per evitare numeri negativi

# Date e patologie casuali
dates = pd.date_range(start='2024-01-01', periods=days)
pathologies = np.random.choice(['ossa', 'cuore', 'testa'], size=days)

# Creazione del DataFrame
data = pd.DataFrame({'Data': dates, 'Visitatori': visitors, 'Patologia': pathologies})
data.set_index('Data', inplace=True)

# Analisi dei dati
monthly_stats = data.resample('M').agg({'Visitatori': ['mean', 'std']})
pathology_counts = data['Patologia'].value_counts()

# Visualizzazione
plt.figure(figsize=(15, 5))

# Grafico 1: Numero di visitatori giornalieri con media mobile a 7 giorni
plt.subplot(1, 3, 1)
data['Media_mobile_7gg'] = data['Visitatori'].rolling(window=7).mean()
plt.plot(data.index, data['Visitatori'], label='Visitatori Giornalieri')
plt.plot(data.index, data['Media_mobile_7gg'], label='Media Mobile 7gg', linestyle='--')
plt.title('Visitatori Giornalieri')
plt.legend()

# Grafico 2: Media mensile dei visitatori
plt.subplot(1, 3, 2)
monthly_stats['Visitatori', 'mean'].plot(kind='bar', color='skyblue', title='Media Mensile Visitatori')
plt.ylabel('Media Visitatori')

# Grafico 3: Divisione delle patologie
plt.subplot(1, 3, 3)
pathology_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Divisione Patologie')
plt.ylabel('')

plt.tight_layout()
plt.show()
