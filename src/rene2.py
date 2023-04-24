import tkinter as tk
import pandas as pd
import random


def simulate_game(strength_a, strength_b, risk_a):
    # Initialisiere die Punkte der beiden Mannschaften
    team_a_points = 0
    team_b_points = 0

    # Wiederhole den folgenden Block, bis eine Mannschaft gewinnt
    while abs(team_a_points - team_b_points) < 2 or max(team_a_points, team_b_points) < 21:
        # Berechne die Erfolgschance von Mannschaft A für diesen Ballwechsel
        success_chance = (strength_a + (random.random() - 0.5) * risk_a) / (
                    strength_a + strength_b + (random.random() - 0.5) * (risk_a + risk_a))

        # Generiere eine Zufallszahl zwischen 0 und 1
        rand = random.random()

        # Wenn die Zufallszahl kleiner als die Erfolgschance ist, gewinnt Mannschaft A den Ballwechsel
        if rand < success_chance:
            team_a_points += 1
        # Ansonsten gewinnt Mannschaft B den Ballwechsel
        else:
            team_b_points += 1

    # Gib zurück, ob Mannschaft A das Spiel gewonnen hat
    return team_a_points > team_b_points


def calculate_expected_wins(strength_a, strength_b, risk_a):
    # Initialisiere die Anzahl der Siege von Mannschaft A
    wins = 0

    # Simuliere n Spiele
    for i in range(1000):
        # Wenn Mannschaft A das Spiel gewinnt, erhöhe die Anzahl der Siege von Mannschaft A
        if simulate_game(strength_a, strength_b, risk_a):
            wins += 1

    # Gib die Anzahl der Siege von Mannschaft A zurück
    return wins


def calculate_strategy():
    try:
        # Lese die Eingaben des Benutzers aus den Eingabefeldern aus
        strength_a = int(entry_a.get())
        strength_b = int(entry_b.get())
    except ValueError:
        # Wenn die Eingaben des Benutzers ungültig sind, zeige eine Fehlermeldung an
        tk.messagebox.showerror("Fehler", "Bitte gib gültige Zahlen ein.")
        return


    result_window = tk.Toplevel()
    result_window.title("Erwartete Siege")
    result_text = tk.Text(result_window)
    result_text.insert(tk.END, df.to_string())
    result_text.config(state=tk.DISABLED)
    result_text.pack()


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

# Button zum Berechnen der optimalen Risikostrategie
button = tk.Button(root, text="Berechnen", command=calculate_strategy)
button.grid(row=2, column=0, columnspan=2)

# Hauptloop der GUI
root.mainloop()