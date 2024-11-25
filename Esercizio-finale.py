import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class SimulatoreDatiOspedale:
    def __init__(self, giorni, media_visitatori, deviazione_std_visitatori, trend_decrescente):
        self.giorni = giorni
        self.media_visitatori = media_visitatori
        self.deviazione_std_visitatori = deviazione_std_visitatori
        self.trend_decrescente = trend_decrescente
        self.dati = None

    def genera_dati(self):
        np.random.seed(42)  
        trend = np.linspace(0, self.trend_decrescente, self.giorni)
        visitatori = np.random.normal(self.media_visitatori, self.deviazione_std_visitatori, self.giorni) + trend
        visitatori = np.maximum(visitatori, 0).astype(int)
        print(visitatori)
        date = pd.date_range(start='2024-01-01', periods=self.giorni)
        patologie = np.random.choice(['ossa', 'cuore', 'testa'], size=self.giorni)
        
        self.dati = pd.DataFrame({'Data': date, 'Visitatori': visitatori, 'Patologia': patologie})
        self.dati.set_index('Data', inplace=True)

    def ottieni_dati(self):
        if self.dati is None:
            raise ValueError("I dati non sono stati generati. Usa il metodo `genera_dati`.")
        return self.dati


class AnalizzatoreDatiOspedale:
    def __init__(self, dati):
        self.dati = dati

    def statistiche_mensili(self):
        return self.dati.resample('M').agg({'Visitatori': ['mean', 'std']})

    def distribuzione_patologie(self):
        return self.dati['Patologia'].value_counts()

    def aggiungi_media_mobile(self, finestra=7):
        self.dati['Media_mobile_7gg'] = self.dati['Visitatori'].rolling(window=finestra).mean()


class VisualizzatoreDatiOspedale:
    def __init__(self, dati, analizzatore):
        self.dati = dati
        self.analizzatore = analizzatore

    def grafico_visitatori_giornalieri(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.dati.index, self.dati['Visitatori'], label='Visitatori Giornalieri')
        plt.plot(self.dati.index, self.dati['Media_mobile_7gg'], label='Media Mobile 7gg', linestyle='--')
        plt.title('Visitatori Giornalieri')
        plt.legend()
        plt.show()

    def grafico_media_mensile(self):
        statistiche_mensili = self.analizzatore.statistiche_mensili()
        media_mensile = statistiche_mensili['Visitatori', 'mean']  # Seleziona solo la media
        media_mensile.index = media_mensile.index.strftime('%Y-%m')  # Formatta le date come "AAAA-MM"
    
        media_mensile.plot(kind='bar', color='skyblue', figsize=(10, 5), title='Media Mensile Visitatori')
        plt.xlabel('Mesi')
        plt.ylabel('Media Visitatori')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    def grafico_distribuzione_patologie(self):
        distribuzione_patologie = self.analizzatore.distribuzione_patologie()
        distribuzione_patologie.plot(kind='pie', autopct='%1.1f%%', startangle=90, title='Distribuzione Patologie', figsize=(7, 7))
        plt.ylabel('')
        plt.show()


# Main
if __name__ == "__main__":
    # Generazione dei dati
    simulatore = SimulatoreDatiOspedale(giorni=305, media_visitatori=1200, deviazione_std_visitatori=900, trend_decrescente=-300)
    simulatore.genera_dati()
    dati = simulatore.ottieni_dati()
    
    

    # Analisi dei dati
    analizzatore = AnalizzatoreDatiOspedale(dati)
    analizzatore.aggiungi_media_mobile()

    # Visualizzazione
    visualizzatore = VisualizzatoreDatiOspedale(dati, analizzatore)
    visualizzatore.grafico_visitatori_giornalieri()
    visualizzatore.grafico_media_mensile()
    visualizzatore.grafico_distribuzione_patologie()
