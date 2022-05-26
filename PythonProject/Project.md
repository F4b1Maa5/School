# Anforderungen

Es soll eine Software entwickelt werden, welche einen grafischen zugriff auf eine Datenbank zulässt. Hierbei sollen die wichtigsten Datenbankfunktionen abgedeckt werden. Das ganze Projekt soll in der Skriptsprache Python realisiert werden.

# 1 Beschreibung

Für dieses Projekt haben wir uns das Thema Lagerverwaltungssoftware gewählt. Hierbei handelt es sich lediglich um die Lagerverwaltung, sprich die erstellen der zu verbuchenden Belege uä ist nicht integriert. Hierbei haben wir folgende Funktionen implementiert

# 2 Hauptfunktionen

## 2.1 Laden der Belege

Die Belege werden im Wareneingang, Warenausgang und zur Inventur ähnlich vorbereitet. Im Anschluss folgt das Beispiel für den Wareneingang.

```python
def Wareneingang():
    mainfenster.title("Easy Log | Wareneingang") # Titel des Hauptfensters ändern
    mdBelege = []
    listbox.delete(0,"end")               # alle alten Einträge in der Liste löschen
    mdBelege = ReadDatafromDB('mdbelege') # alle nuene Belege Laden
    for row in mdBelege:        
        if row[1] != 'WE':                # schauen das nur Wareneingänge in der Liste bleiben
            mdBelege.remove(row)
    for beleg in mdBelege:
        if beleg.__len__() > 0:
            listbox.insert("end",beleg)   # Belege der listbox anfügen 
```

Dies ist die Vorbereitungsmethode um alle Wareneingangsbelege aus der Datenbank zu landen und in der Optionsliste anzuzeigen. Hierzu wird die Hilfsmethode [ReadDatafromDB(tabellenname)]() benutzt. Nun werden alle Belege welche nicht ‚WE‘ sind aus dieser Liste entfernt und die restlichen werden in die Auswahlliste hinzugefügt.

## 2.1 Listenauswahl

Hierbei wird auf das „OnDoubleClick“-Event der Listbox reagiert. Und dann entsprechend die Methode OpenNewWindowBeleg() aufgerufen. Dabei wird als Parameter der selektierte Beleg übergeben.

```python
listbox.bind('<Double-1>',lambda x : OpenNewWindowBeleg(listbox.selection_get().split())) 
```

**Information zum Vorgehen**: Durch den Lambda-ausdruck wird auf das entwspecehende Event die selbstdefenierte Methode gebunden/ zugeordnet.

### 2.1.1 OpenNewWindowBeleg

In dieser Methode wird nun anhand des übergebenen Belegs die entsprechenden Belegpositionen geladen. Nun wird anhand des übergebenen Beleg ein neues Fenster erstellt, sollte der Beleg nun ein Wareneingang („WE“) sein so wird das Fenster für einen Wareneingang erstellt. Dies muss so umgesetzt werden, da unterschieden werden muss welche Funktionen die Entsprechenden Buttons auf dem Fenster haben. Dies muss beim erstellen der Fensters schon defeniert werden, dahher wird hier entsrpechend der Belegart das Fenster erzeugt.

```python
def OpenNewWindowBeleg(beleg):
    positionen = LoadPositions(beleg) # In dieser Methode wird die Hilfsmethode LoadDatafromDB(mdbelegepositionen) aufgerufen
    if beleg[1] == "WE": # anhand der übergebenen Belegart wird das Fenster dynamisch genneriert 
        if positionen.__len__() > 0:
            window = tk.Tk()
            window.title("Positionseingabe")
            window.geometry("400x400")                   
            DarwNewPositionContent(window,positionen,0)
        else:
            print("Keine Positionen vorhanden")
    else:
        if positionen.__len__() > 0:
            window = tk.Tk()
            window.title("Positionseingabe")
            window.geometry("400x400")                   
            DarwNewWAPositionContent(window,positionen,0)
        else:
            print("Keine Positionen vorhanden")
```

**Information zu DrawNewPositionContent**: Hier wird das Fenster selbst übergebn, die Positionen welcher der Beleg hat und die Start Position, von welcher aus die Positionen gezählt werden. Wichtig ist das das Fenster selber übergeben wird, da dies in der Methode sich der Inhalt des Fenster dynamisch neu erzeugt.

### 2.1.2 DrawNewPositionContetnt()
w
```python
### Nur entscheidender Code welcher für weitere Logik relevant ist ###
 menge_txt.insert("end",positionen[i][4])
    if positionen.__len__()-1 > i:
        next_button = tk.Button(window, text="Next",command= lambda : LoadNewPosition(window,positionen,i,menge_txt.get("1.0","end")), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SavePositions(window,positionen), height= 5, width=10) 
    else:
        next_button = tk.Button(window, text="Next",command= lambda : SaveAtLastPositions(window,positionen,i,menge_txt.get("1.0","end").strip()), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SavePositions(window,positionen), height= 5, width=10) 
```