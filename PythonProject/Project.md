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

Dies ist die Vorbereitungsmethode um alle Wareneingangsbelege aus der Datenbank zu landen und in der Optionsliste anzuzeigen. Hierzu wird die Hilfsmethode [ReadDatafromDB(table_name)]() benutzt. Nun werden alle Belege welche nicht ‚WE‘ sind aus dieser Liste entfernt und die restlichen werden in die Auswahlliste hinzugefügt.

---

## 2.2 Listenauswahl

Hierbei wird auf das „OnDoubleClick“-Event der Listbox reagiert. Und dann entsprechend die Methode OpenNewWindowBeleg() aufgerufen. Dabei wird als Parameter der selektierte Beleg übergeben.

```python
listbox.bind('<Double-1>',lambda x : OpenNewWindowBeleg(listbox.selection_get().split())) 
```

**Information zum Vorgehen**: Durch den Lambda-ausdruck wird auf das entwspecehende Event die selbstdefenierte Methode gebunden/ zugeordnet.

---

### 2.2.1 OpenNewWindowBeleg

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

---

### 2.2.2 DrawNewPositionContetnt()

In dieser Methode wird der Inhalt des Fenster neu gezeichnet und neu defeniert. Dahher muss in der Methode vorhher das Fenster Objekt übergeben werden damit für die Nächten Button aufrufe, das gleiche Fentser besetehen kann, aber lediglich der Inhalt des Fensters neu gezeichnet werden kann.

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

- Wie man in Codeausschnitt erkenn kann, wird hier wirder mit dem Lambda-Ausdruck gearbeit , welcher dem command des Buttons eine Methode mit parametern zuweisen kann, statt einer Methode, welche keine Parameter entgegen nimmt.

- Desweitern wird unterschieden, ob wir uns an de letzten Position befinden oder in einer vorhherigen, denn sobald die letzte Position erreicht wurde, muss der Command für den Next-Button geändert werden und auf eine andere Funktion zu verweisen. Denn an der letzten Postion müssen alle eingaben verarbeitet werden.

- Durch den Save-Button kann das bearbeiten einer Buchung unterbrochen werden, alle bis dahin bearbeiten Positonen werden dann gebucht.

**Hinweis:** Für den Warenausgang ist es genau gleich wie für den Wareneingang. Es werden zwei unterschidliche Methoden genutzt um es in der Erstellung einfacher zu handhaben.

---

### 2.2.2.1 SavePositions()

Hier werden als Parameter alle Positionen aus dem Beleg übergeben, desweitern wird auch das Fenster-Objekt übergeben. Desweitern werden die bearbieteten Position und belege aus der Datenbak entfernt, damit diese nicht mehrfach gebucht werden können. Dafür wird die Hilfsmethode [DeleteFromDB(positionen)]() verwendet.

```python
def SavePositions(window,positionen):
    for pos in positionen:
        con = mysql.connector.connect(user='root', password='*****',host='localhost',database='dbo')
        cursor = con.cursor()
        cursor.execute("INSERT INTO lagerplaetze (`Artikel`,`Menge`) VALUES ( %s , %s)",  (pos[3] , pos[4])) # %s dient als Parameter
        cursor.close()
        con.commit() 
        con.disconnect()
        con.close()
    DeleteFromDB(positionen)
    window.destroy()
```

Es wird für jede einzelene Position der Artikel und die Menge es Artikels in die Datenbank geschrieben. Hierbei muss geachtet werden, das ``` con.commit() ``` ausgeführt wird. Dies sorgt dafür, das die Änderungen welche durch den Cursor ausgeführet werden auch in die Datenbank übermittelt werden.

### 2.2.2.2 SaveWAPositions()

Hierbei werden die Positionen welche in einem Warenausgang gebucht werden aus der Datenbank gebucht, anhand der angeführeten Matrix wird entschieden die Daten verbucht werden.

| Fall | Umsetzung Code | Datenbank Operation |
|:------------------ |:-------------------:| -------------------:|
| Lagermenge > gebuchte Menge | ``` if menge > pos[menge] ```| Update lagerplaetze Set Menge = (menge-pos[menge])|
| Lagermenge = gebuchte Menge| ``` elif menge == pos[menge] ``` | DELETE FROM lagerplaetze Where Artikel = pos[artikel]|
| Lagermenge < gebuchte Menge|``` else ```| print("Fehler ! nicht genügend Ware verfügbar")|

Dementsrpechend werden die Datenbank Operationen der Hilfsmothoden aufgerufen ([UpdateDB()]() oder [DeleteDB()]())

## 2.3 Inventur

Über den Button Inventur kann eine Inventur über das gesamte Lager durchgeführt werden.
