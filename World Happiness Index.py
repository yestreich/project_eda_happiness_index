'''
==========================
= Python - Projektarbeit =
==========================


'''

#%% Pakete importieren

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#%% CSV - laden und einsehen

metadata = pd.read_csv("Datensatz\worldhappinessreport.csv")

print(metadata.head())
print(metadata.shape)       #2199 Reihen, 13 Spalten

#%% Detailliertes Einsehen

#Alle Spaltennamen
for col in metadata.columns:
    print(col)

summary = metadata.describe()
for col in summary:
    print(summary[col])

metadata["Country Name"].value_counts() #Nicht für alle Länder gibt es Einträge
                                        #Es fehlen Jahresdaten innerhalb der Länder

#%% Umbenennen diverser Werte

#Dictionary der Spaltenkategorien für einfachen Zugriff (und später revers für Plot-labels)
col_abb = {"Country Name":"country", 
           "Regional Indicator":"region",
           "Year":"year",
           "Life Ladder":"ladder",
           "Log GDP Per Capita":"GDP",
           "Social Support":"social_support",
           "Healthy Life Expectancy At Birth":"life_expectancy",
           "Freedom To Make Life Choices":"freedom_choices",
           "Generosity":"generosity",
           "Perceptions Of Corruption":"corruption",
           "Positive Affect":"positive_affect",
           "Negative Affect":"negative_affect",
           "Confidence In National Government":"confidence_gov"}

#Umbenennen der Spaltenkategorien
metadata = metadata.rename(columns = col_abb)

#manuelle Zuweisung von Regionen bei NaN-Regionen
metadata.loc[metadata["country"] == "Congo (Kinshasa)" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Angola" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Belize" , ["region"]] = "Latin America and Caribbean"
metadata.loc[metadata["country"] == "Bhutan" , ["region"]] = "South Asia"
metadata.loc[metadata["country"] == "Central African Republic" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Cuba" , ["region"]] = "Latin America and Caribbean"
metadata.loc[metadata["country"] == "Czechia" , ["region"]] = "Central and Eastern Europe"
metadata.loc[metadata["country"] == "Djibouti" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Eswatini" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Guyana" , ["region"]] = "Latin America and Caribbean"
metadata.loc[metadata["country"] == "Oman" , ["region"]] = "Middle East and North Africa"
metadata.loc[metadata["country"] == "Qatar" , ["region"]] = "Middle East and North Africa"
metadata.loc[metadata["country"] == "Somalia" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Somaliland region" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "South Sudan" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "State of Palestina" , ["region"]] = "Middle East and North Africa"
metadata.loc[metadata["country"] == "Sudan" , ["region"]] = "Sub-Saharan Africa"
metadata.loc[metadata["country"] == "Suriname" , ["region"]] = "Latin America and Caribbean"
metadata.loc[metadata["country"] == "Syria" , ["region"]] = "Middle East and North Africa"
metadata.loc[metadata["country"] == "Trinidad and Tobago" , ["region"]] = "Latin America and Caribbean"
metadata.loc[metadata["country"] == "Turkyie" , ["region"]] = "Central and Eastern Europe"

#%% Legend-Farben für gleichbleibende Farben von Regionen/Ländern zwischen Plots

col_set2 = sns.color_palette("husl", 11)
col_regio = {region: color for region, color in zip(metadata["region"].unique(), col_set2)}

#%% Glücklichkeit der letzten 10 Jahre

#Ersten 10 Ränge

#Sortiere nach Jahr und Ladder, gruppiere die Jahre und gebe mir jeweils die erste Zeile jedes Jahres
last10_h = metadata.sort_values(["year", "ladder"], ascending = True).groupby("year").tail(1)[metadata.year >= 2013]

#Mean-Wert
mean_h = round(last10_h.ladder.mean(), 1)
print(mean_h)
    
fig = plt.figure(figsize=(8, 5))
sns.set_style("whitegrid")
g = sns.barplot(x = "year", y = "ladder", hue = "country", data = last10_h, dodge = False)
g.set_xticklabels(last10_h["year"], fontsize  = 13)
plt.xlabel("Year", fontsize = 16)
plt.ylabel("Life Ladder", fontsize = 16)
plt.legend(bbox_to_anchor=(1.25, 0.5), loc = "right", fontsize = 13)
plt.title("Last 10 Years : Highest Happiness Index", fontsize = 20)
plt.savefig("01_1322_happy", bbox_inches='tight')
plt.show()


#Letzten 10 Ränge

#Sortiere nach Jahr und Ladder, gruppiere die Jahre und gebe mir jeweils die letzte Zeile jedes Jahres
last10_u = metadata.sort_values(["year", "ladder"], ascending = True).groupby("year").head(1)[metadata.year >= 2013]

#Mean-Wert
mean_u = round(last10_u.ladder.mean(), 1)
print(mean_u)

fig = plt.figure(figsize=(8, 5))
sns.set_style("whitegrid")
g = sns.barplot(x = "year", y = "ladder", hue = "country", data = last10_u, dodge = False)
g.set_xticklabels(last10_u["year"], fontsize  = 13)
plt.ylabel("Life Ladder", fontsize = 16)
plt.legend(bbox_to_anchor=(1.45, 0.5), loc = "right", fontsize = 13)
plt.title("Last 10 Years : Lowest Happiness Index", fontsize = 20)
plt.savefig("02_1322_unhappy", bbox_inches='tight')
plt.show()

#%% aktuellstes Jahr : 2022
                            
#Neuer DataFrame, ausschließlich 2022
latest_y = metadata[metadata.year == 2022]
#Mean-Wert
mean_22 = round(latest_y.ladder.mean(), 1)
print(mean_22)

#2022 per Region

#um die Regionen gegeneinander zu plotten. Durchschnitt, da nicht alle gleich viel pro Region
group = latest_y.groupby(by = "region").mean(numeric_only = True)

#happiness by region - aufsteigend
fig = plt.figure(figsize=(6, 5))
sns.set_style("whitegrid")
g = sns.barplot(x = group.index, y = "ladder", data = group, palette=col_regio, 
            order = group.sort_values("ladder").index)  #aufsteigende Reihenfolge
plt.xticks(rotation = 45, ha = "right", fontsize = 13)     #ha : Ausrichtung
plt.xlabel("Region", fontsize = 16)
plt.ylabel("Life Ladder", fontsize = 16)
plt.title("2022 : Happiness Index By Region", fontsize = 20)
plt.savefig("03_region", bbox_inches='tight')
plt.show()

# 2022: 10 glücklichsten Länder
happy_22 = latest_y.nlargest(10, "ladder")

#Mean-Wert und Standardbweichung (wegen großer Diskrepanz bei nächstem Plot)
mean_h_22 = round(happy_22.ladder.mean(), 1)
print(mean_h_22)
print(np.std(happy_22.ladder))

fig = plt.figure(figsize=(8, 5))
sns.set_style("whitegrid")
sns.barplot(x = "country", y = "ladder", data = happy_22, hue = "region",
            palette=col_regio, order = happy_22.sort_values("ladder").country, dodge = False)           #dodge: hue erwartet mehr als 1 Wert pro x-Achse und setzt den Bar neben den Tick
plt.xticks(rotation = 45, ha = "right", fontsize = 13)
plt.xlabel("Country", fontsize = 16)
plt.ylabel("Life Ladder", fontsize = 16)
plt.legend(bbox_to_anchor=(1.5, 0.5), loc = "right", fontsize = 13)
plt.title("2022 : Highest Happiness Index", fontsize = 20)
plt.savefig("04_22_happy", bbox_inches='tight')
plt.show()

# 2022_ 10 unglücklichsten Länder
unhappy_22 = latest_y.nsmallest(10, "ladder")

#Mean-Wert und Standardbweichung (wegen großer Diskrepanz bei diesem Plot)
mean_u_22 = round(unhappy_22.ladder.mean(), 1)
print(mean_u_22)
print(np.std(unhappy_22.ladder))

fig = plt.figure(figsize=(8, 5))
sns.set_style("whitegrid")
sns.barplot(x = "country", y = "ladder", data = unhappy_22, hue = "region",
            palette=col_regio, dodge = False)
plt.xticks(rotation = 45, ha = "right", fontsize = 13)
plt.xlabel("Country", fontsize = 16)
plt.ylabel("Life Ladder", fontsize = 16)
plt.legend(bbox_to_anchor=(1.5, 0.5), loc = "right", fontsize = 13)
plt.title("2022 : Lowest Happiness Index", fontsize = 20)
plt.savefig("05_22_unhappy", bbox_inches='tight')
plt.show()

#%% Was hat Finnland was Afghanistan (in 2022) nicht hat?

fin = metadata.loc[metadata["country"] == "Finland"]
afg = metadata.loc[metadata["country"] == "Afghanistan"]

#adding and filling missing years
fin_afg = pd.concat([fin, afg]).fillna(method = "ffill", limit = 1)

for i in range(2006,2023):
    for j in ["Finland", "Afghanistan"]:
        if len(fin_afg.query('country == @j & year == @i')) == 0:  # "@" um Variable in Query kenntlich zu machen
            new_row = pd.DataFrame([[i,j]], columns = ["year", "country"])
            fin_afg = pd.concat([fin_afg, new_row], ignore_index = True).sort_values(["country", "year"]) #neue Reihe an die richtige Stelle 
            fin_afg = fin_afg.fillna(method = 'ffill', limit = 1) # NaN-Werte der neuen Reihen mit Vorjahreswerten füllen

# Fehlende Jahre 2006 und 2007 von Afgh. werden absichtlich nicht rückwärtsgefüllt

#Plot
fig = plt.figure(figsize=(10, 6))           #Leinwand generieren
j = 1                                       #Positionscounter
sns.set_style("ticks")
for i in fin_afg.loc[:, "ladder":"confidence_gov"].columns: #Jahr und region brauch ich nicht
    axes = fig.add_subplot(2,5,j)         #2Reihen, 5 Spalten, Position wird mit jedem Loop neu zugewiesen
    sns.lineplot(ax = axes, x = "year", y = i, hue = "country", data = fin_afg)
    axes.get_legend().remove()              #Jeder Subplot bringt seine eigene Legende. Brauch ich nicht
    plt.xlabel("Year", fontsize = 12)
    plt.ylabel([k for k,v in col_abb.items() if v == i][0], fontsize = 12)    #"Orginalbeschreibung wieder zuweisen 
    j += 1
    
handles, labels = axes.get_legend_handles_labels()          #von letztem Plot Legenden nehmen
fig.legend(handles, labels, bbox_to_anchor = (1.13, 0.63))  #Legende manuell hinzu
plt.subplots_adjust(wspace = 0.7)
plt.suptitle("Comparison Of Environmental Factors Between Finland and Afghanistan",
             x = 0.52, y = 1.0, fontsize = 20)
plt.tight_layout()
plt.savefig("06_Fin_Afgh", bbox_inches='tight')
plt.show()

#%% Wie hängen die Faktoren zusammen? Haben "Umweltfaktoren" einen Einfluss auf die Zufriedenheit?

#Heatmap
corr = metadata.corr(numeric_only = True)

#Oberes Dreieck entfernen
mask = np.triu(np.ones_like(corr))
#"leere" äußerste Reihe und Spalte entfernen
corr = corr.iloc[1:,:-1]                    #iloc weil DataFrame-Struktur
mask = mask[1:,:-1]                         #normale Indexierung weil einfaches Array

fig = plt.figure(figsize=(8, 5))
sns.set_style("ticks")
sns.heatmap(corr, fmt = ".2f", annot = True, annot_kws = {'size':11}, #Parameter für Annotations
            mask = mask, 
            xticklabels = [k for k,v in col_abb.items() if v == v in corr.loc[:, "year":].columns],
            yticklabels = [k for k,v in col_abb.items() if v == v in corr.loc[:, "ladder":].index]
            )
plt.xticks(rotation = 45, ha = "right", fontsize = 13)
plt.yticks(fontsize = 13)
plt.title("Correlation Of Environmental Factors", fontsize = 20)
plt.savefig("07_Factors_Corr", bbox_inches='tight')



'''
Zufriedenheit:
Starker positiver Zusammenhang mit GDP, sozialem Support und Lebenserwartung.
Mittelstarker positiver Zusammenhang mit der Entscheidungsfreiheit und positive affect.
Mittelstarker negativer Zusammenhang mit Korruption und negative affect.
Fast kein Zusammenhang mit Großzügigkeit und Vertrauen in Regierung.

Am stärksten sind Zufriedenheit und die Lebenserwartung an den GDP geknüpft.
    Je höher der GDP, desto zufriedener und höher die Lebenserwartung

In die andere Richtung ist das meiste an Korruption geknüpft.
    Besonders die Entscheidungsfreiheit, Vertrauen in die Regierung und Zufriedenheit
    
Obwohl das Vertrauen in die Regierung positiv mit der Entscheidungsfreiheit korreliert,
    korreliert sie negativ(nur leicht) mit sozialem Support und der Lebenserwartung
'''

#%% Wie ist der Zufriedenheitstrend für die einzelnen Faktoren?

#Regression (x: Kategorie, y = ladder)
fig = plt.figure(figsize=(9, 5))           
j = 1                                       
sns.set_style("ticks")
for i in metadata.loc[:, "GDP":"life_expectancy"].columns: 
    axes = fig.add_subplot(1,3,j)         
    sns.regplot(ax = axes, x = "ladder", y = i, data = metadata, line_kws={"color":"red"}, scatter_kws={"alpha":0.3})
    plt.xlabel("Life Ladder", fontsize = 12)
    plt.ylabel([k for k,v in col_abb.items() if v == i][0], fontsize = 12)    #"Orginalbeschreibung wieder zuweisen 
    j += 1

plt.tight_layout()
plt.suptitle("Regression Of GDP, Social Support and Life Expectancy\n Regarding Happiness",
             y = 1.1, fontsize = 20)
plt.savefig("08_Factors_Regression", bbox_inches='tight')
plt.show()