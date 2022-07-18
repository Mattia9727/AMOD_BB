Antonangeli Mattia, Villani Federica 
Progetto del corso di Algoritmi e Modelli di Ottimizzazione Discreta.

ISTRUZIONI PER L'USO

main.py: usato per risolvere il problema 1|prec|sum(Ci) usando Gurobi e una tecnica di Branch & Bound, e stampando i risultati nel file results.csv
  1) Eseguire main.py con Python 3.10
  2) Scegliere la modalità di esecuzione:
    a) Premere "i" per eseguire le istanze generate su instances.txt. I risultati verranno scritti nel file results.csv.
    b) Premere "k" per inserire "a mano" i processing time e le precedenze per l'esecuzione di una singola istanza. I risultati verranno stampati su schermo.
    c) Premere "q" per uscire
    
generator.py: usato per generare il file "instances.txt" in cui vengono scritti i processing time e le precedenze generate.
  1) Eseguire generator.py con Python 3.10
  2) Inserire:
    a) N: numero istanze da generare
    b) n: numero di processing time da generare
    c) k: numero di precedenze da generare
    d) var: 1 se si vogliono generare processing time con variabilità alta (tempi da 40 a 60), 0 se si vogliono generare con variabilità bassa (tempi da 1 a 100)
    e) hold_on: se il file instances.txt esiste, si può decidere se mantenere il file e aggiungere le nuove istanze in fondo al file (hold_on=1) oppure se sovrascrivere il file (hold_on=0)
    
Nota: il limite di tempo massimo di esecuzione è impostato a 600 secondi. Il limite può essere cambiato nel file constants.py
    
