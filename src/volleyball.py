import numpy as np
import pandas as pd
import tkinter as tk
import seaborn as sns
import tkinter.messagebox
import statistics
import matplotlib.pyplot as plt

spielfeldhälfte = 1 #1 oder -1. 1 ist bei team A
länge_des_ballwechsels = 0

class Team():
    def __init__(self, name, stärke, risiko = 0.5):
        self.name = name
        self.stärke = stärke
        self.punkte = 0
        self.risiko = risiko

    def onepunkt(self):
        self.punkte += 1

def calculate_strategy():
    try:
        # Lese die Eingaben des Benutzers aus den Eingabefeldern aus
        strength_a = int(entry_a.get())/10
        strength_b = int(entry_b.get())/10
        ermüdung = float(entry_ermüdung.get())
    except ValueError:
        # Wenn die Eingaben des Benutzers ungültig sind, zeige eine Fehlermeldung an
        tk.messagebox.showerror("Fehler", "Bitte gib gültige Zahlen ein.")
        return
    if ermüdung > 0.001:
        tk.messagebox.showerror("Fehler", "Ermüdung zu hoch.")
        raise Exception("Ermüdung zu hoch")
    if strength_a > 1:
        tk.messagebox.showerror("Fehler", "Stärke Team A zu hoch.")
        raise Exception("Stärke Team A zu hoch")
    if strength_b > 1:
        tk.messagebox.showerror("Fehler", "Stärke Team B zu hoch.")
        raise Exception("Stärke Team B zu hoch")
    # Anzeige der Ergebnisse in einem DataFrame
    won_a = 0
    spiele_count = 0
    teams = dict()
    teams["A"] = Team("TeamA", strength_a)
    teams["B"] = Team("TeamB", strength_b)
    #print("Teams:")
    #print(teams["A"].stärke)
    #print(teams["B"].stärke)
    risiko_list = [0.2, 0.4, 0.6, 0.8, 1.0]
    risiko_results = spielen(teams, risiko_list, ermüdung)
    result_window = tk.Toplevel()
    result_window.title("Resultate")
    result_text = tk.Text(result_window)
    #print("Risiko results in calculate_strategy:")
    #print(risiko_results)

    #result_text.insert(tk.END, str(risiko_results))
    for spiel_id,spiel in risiko_results.items():
        #print("spiel_id in calculate_strategy: ")
        #print(spiel_id)
        #print("spiel in calculate_strategy: ")
        #print(spiel)
        #result_text.insert(tk.END, "Spiel: "+str(spiel"\n")
        for risiko,result in spiel.items():
            #print("risiko in for loop calculate_strategy: ")
            #print(risiko)
            #print("result in for loop calculate_strategy: ")
            #print(result)
            result_text.insert(tk.END, "Risiko "+str(risiko)+":\n")
            result_text.insert(tk.END, "A: "+str(result["A"])+" B: "+str(result["B"])+"\n")
            result_text.insert(tk.END, "Ballwechseldurchschnitt: "+str(round(result["ballwechsel"],2))+"\n")
            if result["A"]>result["B"]:
                won_a +=1
            spiele_count += 1
        result_text.insert(tk.END, "***************\n")
    result_text.insert(tk.END, f"Anzahl Spiele {spiele_count} \n")
    result_text.insert(tk.END, f"{won_a} Spiele von A gewonnen\n")
    result_text.insert(tk.END, f"{spiele_count-won_a} Spiele von B gewonnen\n")
    result_text.config(state=tk.DISABLED)
    result_text.pack()

def spielen(teams, risiko_list, ermüdung):
    risiko_results = dict()
    ballwechsel_längen = []
    track_spiele = pd.DataFrame()
    ergebnis_liste = []

    for spiel in range(0,100):
        risiko_results[spiel]=dict()
        #track_spiele[spiel] = dict()
        #spielfeldhälfte = 1
        for risiko in risiko_list:
            #track_spiele[spiel][risiko] = dict()
            risiko_results[spiel][risiko] = dict()
            #print("Risiko: ",risiko)
            teams["A"].risiko = risiko
            teams["A"].punkte = 0
            teams["B"].punkte = 0
            stärke = dict()
            stärke["A"] = teams["A"].stärke
            stärke["B"] = teams["B"].stärke
            ballposession = "A" if np.random.randint(0, 2)==0 else "B"
            #print("startballposession:",ballposession)
            #track_spiel = np.array(30,30)
            zwischenergebnisse = []
            while abs(teams["A"].punkte - teams["B"].punkte) < 2 or max(teams["A"].punkte, teams["B"].punkte) < 21:
                länge_des_ballwechsels = 0
                while True:
                    #ergebnis = np.random.randint(0, 100)
                    ergebnis = np.random.normal(stärke[ballposession], teams[ballposession].risiko)
                    #print("stärke A: "+str(stärke["A"]))
                    #print("stärke B: "+str(stärke["B"]))
                    länge_des_ballwechsels += 1
                    #print("Länge des Ballwechsels:"+str(länge_des_ballwechsels))
                    ballposession = "B" if ballposession=="A" else "A"
                    if ergebnis >= 0.5:      #Erfolgreicher Ball
                        #print("ballposession =",ballposession)
                        pass
                    else:
                        teams[ballposession].onepunkt()
                        #track_spiele[spiel][risiko][teams["A"].punkte] = []
                        #track_spiele[spiel][risiko][teams["A"].punkte][teams["B"].punkte] = 1
                        #track_spiele.at[spiel,risiko,teams["A"].punkte,teams["B"].punkte] = 1
                        zwischenergebnisse.append([teams["A"].punkte, teams["B"].punkte, risiko, stärke["A"]])
                        #track_spiel[teams["A"].punkte][teams["B"].punkte] = risiko
                        break
                    #Ermüdung
                    stärke["A"] -= ermüdung
                    stärke["B"] -= ermüdung
                ballwechsel_längen.append(länge_des_ballwechsels)
                #print(teams["A"].name,str(teams["A"].punkte),teams["B"].name,str(teams["B"].punkte))
            ballwechsel_längen_mittelwert=statistics.mean(ballwechsel_längen)
            #print("Ende des Spiels.  Team A: ",teams["A"].punkte,"Team B:",teams["B"].punkte)
            #print("Spiel:",spiel)
            #print("Ballwechsellängenmittelwert: "+str(ballwechsel_längen_mittelwert))
            risiko_results[spiel][risiko]["A"] = teams["A"].punkte
            risiko_results[spiel][risiko]["B"] = teams["B"].punkte
            risiko_results[spiel][risiko]["ballwechsel"] = ballwechsel_längen_mittelwert
            #track_spiele[spiel][risiko]["won_A"] = 1 if teams["A"].punkte>teams["B"].punkte else 0
            if teams["A"].punkte > teams["B"].punkte:
                for zwischenergebnis in zwischenergebnisse:
                    ergebnis_liste.append(zwischenergebnis)
    #print("Zwischenergebnisse: ")
    #print(zwischenergebnisse)
    #print("Ergebnisliste: ")
    #print(ergebnis_liste)



    heatmap_df = pd.DataFrame([[[] for i in range(40)] for j in range(40)])

    for ergebnis in ergebnis_liste:
        heatmap_df[ergebnis[0]][ergebnis[1]].append(ergebnis[2])


    #heatmap_df.applymap(lambda x: behandel_x(x))
    #print("heatmap_df:")
    #print(heatmap_df)

    for rowIndex, row in heatmap_df.iterrows():  # iterate over rows
        for columnIndex, value in row.items():
            #print("value: ")
            #print(value)
            if not(isinstance(value, float) or isinstance(value, int)) and len(value)>0:
                heatmap_df[rowIndex][columnIndex] = max(set(value), key=value.count)
            else:
                heatmap_df[rowIndex][columnIndex] = 0

    #print("heatmap2:")
    #print(heatmap_df)
    #print("type heatmap:")
    #print(type(heatmap_df))
    #print("type heatmap[0]:")
    #print(type(heatmap_df[0]))
    #print("type heatmap[0][0]:")
    #print(type(heatmap_df[0][0]))
    heatmap_df.to_csv("heatmap.csv", index=False)
    heatmap_df = pd.read_csv("heatmap.csv")
    #heat_map = sns.heatmap(heatmap_df)
    #plt.savefig("heatmap.png")
    #track_spiele.append(track_spiel)
    #for track_spiel in track_spiele:
    #plt = sns.heatmap(heatmap_df, vmin=0, vmax=1.0, cmap='RdYlGn', linewidths=0.30, annot=False, cbar_kws={'label': 'Risk with most observed victories'})

    #plt.xlabel("Score " + teams["A"].name)
    #plt.ylabel("Score " + teams["B"].name)
    #plt.title("Optimal risk by score situation:\n" + teams["A"].name + " skill " + str(teams["A"].stärke) + " vs. " + teams["B"].name + " skill " + str(teams["B"].stärke))

    #heatmap_fig = plt.get_figure()
    #heatmap_fig.savefig("heatmap.png")
    #plt.show()
    plot = sns.heatmap(heatmap_df, cmap='RdYlGn', linewidths=0.30, annot=False,
                       cbar_kws={'label': 'Risk with most observed victories'})

    plt.xlabel("Score " + teams["A"].name)
    plt.ylabel("Score " + teams["B"].name)
    plt.title("Optimal risk by score situation:\n" + teams["A"].name + " skill " + str(
        teams["A"].stärke*10) + " vs. " + teams["B"].name + " skill " + str(teams["B"].stärke*10))
    plt.show()

    return risiko_results

# GUI-Setup
root = tk.Tk()
root.title("Optimale Risikostrategie")

# Label und Eingabefelder für die Spielstärken
label_a = tk.Label(root, text="Spielstärke Mannschaft A (0-10):")
label_a.grid(row=0, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

label_b = tk.Label(root, text="Spielstärke Mannschaft B (0-10):")
label_b.grid(row=1, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1)

label_ermüdung = tk.Label(root, text="Ermüdungsfaktor (0-0.001):")
label_ermüdung.grid(row=2, column=0)
entry_ermüdung = tk.Entry(root)
entry_ermüdung.grid(row=2, column=1)

# Button zum Berechnen der optimalen Risikostrategie
button = tk.Button(root, text="Berechnen", command=calculate_strategy)
button.grid(row=3, column=0, columnspan=2)

# Hauptloop der GUI
root.mainloop()
