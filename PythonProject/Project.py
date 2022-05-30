#https://pythonbuch.com/einleitung.html
import tkinter as tk
import webbrowser
import os
import mysql.connector


# Die folgende Funktion soll ausgeführt werden, wenn
# der Benutzer den Button anklickt
def we_button_action():
    Wareneingang()
    
def wa_button_action():
    Warenausgang()    

def iv_button_action():
    mainfenster.title("Easy Log | Inventur")
    PerformInventur()
    
def iv_prt_button_action():
    mainfenster.title("Easy Log | Inventur Druck")
    PrintInventurLog()    
    
def refresh_button_action():
    listbox.delete(0,"end")
    liste = ReadDatafromDB("mdbelege")
    for i in liste:
        if i.__len__() > 0:
            listbox.insert("end",i)


def DarwNewWAPositionContent(window,positionen,i):
    postxt_lbl = tk.Label(window,text="Position", height= 2, width=10)
    pos_lbl = tk.Label(window,text=positionen[i][2], height= 2, width=10)
    arttxt_lbl = tk.Label(window, text="Artikel", height= 2, width=10)
    art_lbl = tk.Label(window, text=positionen[i][3], height= 2, width=10)
    mengetxt_lbl = tk.Label(window, text="Menge", height= 2, width=10)
    menge_txt = tk.Text(window, height= 1, width=10)  
    menge_txt.insert("end",positionen[i][4])
    if positionen.__len__()-1 > i:
        next_button = tk.Button(window, text="Next",command= lambda : LoadNewWAPosition(window,positionen,i,menge_txt.get("1.0","end")), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SaveWAPositions(window,positionen), height= 5, width=10) 
    else:
        next_button = tk.Button(window, text="Next",command= lambda : SaveAtLastWAPositions(window,positionen,i,menge_txt.get("1.0","end").strip()), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SaveWAPositions(window,positionen), height= 5, width=10) 
    save_button.grid(row=3, column=0,padx=5,pady=5) 
    postxt_lbl.grid(row=0, column=0,padx=5,pady=5)
    pos_lbl.grid(row=0, column=1,padx=5,pady=5)
    arttxt_lbl.grid(row=1, column=0,padx=5,pady=5)
    art_lbl.grid(row=1, column=1,padx=5,pady=5)
    mengetxt_lbl.grid(row=2, column=0,padx=5,pady=5)    
    menge_txt.grid(row=2, column=1,padx=5,pady=5)
    next_button.grid(row=3, column=1,padx=5,pady=5)  
    window.mainloop()


def Warenausgang():
    mainfenster.title("Easy Log | Warenausgang")
    listbox.delete(0)
    listbox.delete(0,"end")
    mdBelege = []
    mdBelege = ReadDatafromDB('mdbelege')
    count = mdBelege.__len__()
    for i in range(count):
        for row in mdBelege:
            if row[1] != 'WA':
                mdBelege.remove(row)
    for beleg in mdBelege:
        if beleg.__len__() > 0:
            listbox.insert("end",beleg)
            

def SaveIV(window,iv):    
    con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
    cursor = con.cursor()
    cursor.execute("DELETE FROM inventur")
    con.commit()
    cursor.close()
    con.close()
    for pos in iv:
        con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
        cursor = con.cursor()
        cursor.execute("INSERT INTO inventur (`Artikel`,`MengeSoll`,`MengeIst`,`Diff`) VALUES (%s,%s,%s,%s)",  (pos[1],str(pos[2]),str(pos[3]),str(int(pos[3])-int(pos[2]))))
        con.commit()
        cursor.close()
        con.close()
    window.destroy()

def SaveAtLastIVPositions(window,iv,i,Menge):
    iv[i].append(Menge.strip())
    SaveIV(window,iv)

def LoadNewIVPosition(window,iv,i,Menge):
    iv[i].append(Menge.strip())
    DarwNewIVContent(window, iv,i+1) 

def PerformInventur():
    iv = ReadDatafromDB("lagerplaetze")
    if iv.__len__() > 0:
        window = tk.Tk()
        window.title("Inventur")
        window.geometry("400x400")                   
        DarwNewIVContent(window,iv,0)
    else:
        print("Keine Lagerplätze vorhanden")
    
    
def DarwNewIVContent(window,iv,i):
    postxt_lbl = tk.Label(window,text="Index", height= 2, width=10)
    pos_lbl = tk.Label(window,text=iv[i][0], height= 2, width=10)
    arttxt_lbl = tk.Label(window, text="Artikel", height= 2, width=10)
    art_lbl = tk.Label(window, text=iv[i][1], height= 2, width=10)
    mengetxt_lbl = tk.Label(window, text="Menge", height= 2, width=10)
    menge_txt = tk.Text(window, height= 1, width=10)  
    menge_txt.insert("end",iv[i][2])
    if iv.__len__()-1 > i:
        next_button = tk.Button(window, text="Next",command= lambda : LoadNewIVPosition(window,iv,i,menge_txt.get("1.0","end")), height= 5, width=10)
    else:
        next_button = tk.Button(window, text="Next",command= lambda : SaveAtLastIVPositions(window,iv,i,menge_txt.get("1.0","end").strip()), height= 5, width=10)
    postxt_lbl.grid(row=0, column=0,padx=5,pady=5)
    pos_lbl.grid(row=0, column=1,padx=5,pady=5)
    arttxt_lbl.grid(row=1, column=0,padx=5,pady=5)
    art_lbl.grid(row=1, column=1,padx=5,pady=5)
    mengetxt_lbl.grid(row=2, column=0,padx=5,pady=5)    
    menge_txt.grid(row=2, column=1,padx=5,pady=5)
    next_button.grid(row=3, column=1,padx=5,pady=5)  
    window.mainloop()

def PrintInventurLog():    
    liste = ReadDatafromDB("inventur") 
    with open("H:/Project/DB/Inventur.html",'w') as f:
        f.write("<html>")
        f.write("<table>")
        f.write("<tr><td>ID</td><td>Artikel</td><td>MengeSoll</td><td>MengeIst</td><td>Diff</td></tr>")
        for item in liste: 
            f.write("<tr>")
            for pos in item:                   
                f.write("<td>"+str(pos)+"</td>")
            f.write("</tr>")
        f.write("</table>")
        f.write("</html>")
    webbrowser.open_new_tab("file:///H:/Project/DB/Inventur.html")

def Wareneingang():
    mainfenster.title("Easy Log | Wareneingang")
    mdBelege = []
    listbox.delete(0,"end")
    mdBelege = ReadDatafromDB('mdbelege')
    count = mdBelege.__len__()
    for i in range(count):
        for row in mdBelege:        
            if row[1] != 'WE':                
                mdBelege.remove(row)
    for beleg in mdBelege:
        if beleg.__len__() > 0:
            listbox.insert("end",beleg)     

def ReadDatafromDB(table_name):
    liste = []    
    con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM %s' % table_name)
    result = cursor.fetchall()   
    liste = [list(i) for i in result]   
    cursor.close()
    con.close()
    return liste
    
def LoadNewPosition(window,position,i,Menge):
    position[i][4] = Menge.strip()
    DarwNewPositionContent(window, position,i+1)             
   
def LoadNewWAPosition(window,position,i,Menge):
    position[i][4] = Menge.strip()
    DarwNewWAPositionContent(window, position,i+1)
         
def SaveAtLastPositions(window,position,i,Menge):
    position[i][4] = Menge
    SavePositions(window,position)
    
def SaveAtLastWAPositions(window,position,i,Menge):
    position[i][4] = Menge
    SaveWAPositions(window,position)

def SaveWAPositions(window,positionen):
    liste = ReadDatafromDB("lagerplaetze") 
    for pos in positionen: 
        for i in liste: 
            if i[1] == pos[3]:              
                con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
                cursor = con.cursor()
                cursor.execute("Select Menge FROM lagerplaetze WHERE Artikel = "+ str(pos[3]))
                for cr in cursor:
                    if str(cr[0]) > pos[4]:
                       UpdateDB(cr,pos,i)
                    elif str(cr[0]) == pos[4]:
                        DeleteDB(i)
                    else :
                        print("Fehler ! nicht genügend Ware verfügbar")
                cursor.close()
                con.disconnect()
                con.close()                 
    DeleteFromDB(positionen)
    window.destroy()


def UpdateDB(cr,pos,i):
    newmenge = int(cr[0]) - int(pos[4])
    con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
    cursor = con.cursor()
    cursor.execute("Update lagerplaetze SET Menge = '"+ str(newmenge) +"' WHERE id = "+ str(i[0]))
    con.commit()
    cursor.close()    
    con.disconnect()
    con.close()   
    
def DeleteDB(i):
    con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
    cursor = con.cursor()
    cursor.execute("DELETE FROM lagerplaetze WHERE id = "+ str(i[0]))
    con.commit()
    cursor.close()
    con.disconnect()
    con.close()  

def SavePositions(window,positionen):
    for pos in positionen:
        con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
        cursor = con.cursor()
        cursor.execute("INSERT INTO lagerplaetze (`Artikel`,`Menge`) VALUES ( %s , %s)",  (pos[3] , pos[4]))
        cursor.close()
        con.commit() #commit muss durchgefürt werden, damit die Daten in die Datenbank geschrieben werden un nicht erst im Transaktionsprotokoll geschrieben werden
        con.disconnect()
        con.close()
    DeleteFromDB(positionen)
    window.destroy()

def DeleteFromDB(positionen):   
    for pos in positionen:
        con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
        cursor = con.cursor()
        cursor.execute("DELETE FROM mdbelegepositionen WHERE id = "+ str(pos[0]))
        cursor.close()
        con.commit() 
        con.disconnect()
        con.close()   
        con = mysql.connector.connect(user='inventuruser', password='inventuruser',host='db4free.net',database='pythoninventur')
        cursor = con.cursor()
        cursor.execute("DELETE FROM mdbelege WHERE Id = "+ str(pos[1]))
        cursor.close()
        con.commit() #commit muss durchgefürt werden, damit die Daten in die Datenbank geschrieben werden un nicht erst im Transaktionsprotokoll geschrieben werden
        con.disconnect()
        con.close()
            
def LoadPositions(beleg):
    positionen = []
    tmp = ReadDatafromDB("mdbelegepositionen")
    for pos in tmp:
        if str(pos[1]) == beleg[0]:
            positionen.append(pos)
    return positionen
            
def DarwNewPositionContent(window,positionen,i):
    postxt_lbl = tk.Label(window,text="Position", height= 2, width=10)
    pos_lbl = tk.Label(window,text=positionen[i][2], height= 2, width=10)
    arttxt_lbl = tk.Label(window, text="Artikel", height= 2, width=10)
    art_lbl = tk.Label(window, text=positionen[i][3], height= 2, width=10)
    mengetxt_lbl = tk.Label(window, text="Menge", height= 2, width=10)
    menge_txt = tk.Text(window, height= 1, width=10)  
    menge_txt.insert("end",positionen[i][4])
    if positionen.__len__()-1 > i:
        next_button = tk.Button(window, text="Next",command= lambda : LoadNewPosition(window,positionen,i,menge_txt.get("1.0","end")), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SavePositions(window,positionen), height= 5, width=10) 
    else:
        next_button = tk.Button(window, text="Next",command= lambda : SaveAtLastPositions(window,positionen,i,menge_txt.get("1.0","end").strip()), height= 5, width=10)
        save_button = tk.Button(window,text="Save",command=lambda: SavePositions(window,positionen), height= 5, width=10) 
    save_button.grid(row=3, column=0,padx=5,pady=5) 
    postxt_lbl.grid(row=0, column=0,padx=5,pady=5)
    pos_lbl.grid(row=0, column=1,padx=5,pady=5)
    arttxt_lbl.grid(row=1, column=0,padx=5,pady=5)
    art_lbl.grid(row=1, column=1,padx=5,pady=5)
    mengetxt_lbl.grid(row=2, column=0,padx=5,pady=5)    
    menge_txt.grid(row=2, column=1,padx=5,pady=5)
    next_button.grid(row=3, column=1,padx=5,pady=5)  
    #window.configure(bg="slategray")
    window.mainloop()



def OpenNewWindowBeleg(beleg):
    positionen = LoadPositions(beleg) 
    if beleg[1] == "WE":
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
 
 
def close(mainfenster):
    mainfenster.destroy() 
       

# Draw Main Window
mainfenster = tk.Tk()
mainfenster.title("Easy Log")

# Label und Buttons erstellen.
we_button = tk.Button(mainfenster, text="Wareneingang", command=we_button_action, height=2, width=10, bg="navy", fg="snow")
wa_button = tk.Button(mainfenster, text="Warenausgang", command=wa_button_action, height=2, width=10, bg="darkred", fg="snow")
iv_button = tk.Button(mainfenster, text="Inventur", command=iv_button_action, height=2, width=10, bg="indigo", fg="snow")
iv_prt_button = tk.Button(mainfenster, text="Inventur Print", command=iv_prt_button_action, height=2, width=10,bg="grey", fg= "snow")
refresh_button = tk.Button(mainfenster, text="Refresh", command=refresh_button_action, height=2, width=10,bg="orange", fg= "snow")
exit_button = tk.Button(mainfenster, text="Beenden", command= lambda : close(mainfenster), height=2, width=10)
listbox = tk.Listbox(mainfenster, width=70,height=8)


# Nun fügen wir die Komponenten unserem Fenster 
# in der gwünschten Reihenfolge hinzu.
we_button.grid(row=1, column=0,padx=5,pady=10)
wa_button.grid(row=1, column=1,padx=5,pady=10)
iv_button.grid(row=1, column=2,padx=5,pady=10)
iv_prt_button.grid(row=1, column=3,padx=5,pady=10)
refresh_button.grid(row=1, column=4,padx=5,pady=10)
exit_button.grid(row=1, column=5,padx=5,pady=10)
listbox.grid(row=0,column=0, columnspan=6,pady=10)

listbox.bind('<Double-1>',lambda x : OpenNewWindowBeleg(listbox.selection_get().split()))
mainfenster.geometry("550x300")
mainfenster.configure(bg="slategray")

# In der Ereignisschleife auf Eingabe des Benutzers warten.
mainfenster.mainloop()