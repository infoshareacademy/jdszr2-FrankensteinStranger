import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import seaborn as sns
import ipywidgets as widgets
import pycountry
import plotly.express as px


# Electricity and heat notebook / Done
# Map notebook / to samo co w Map all
# Map all notebook / Done
# Energy sources per country widget
# ALL_UE_energy_production_analysis_CLEAN / Done


# Przygotowanie danych Electricity and heat notebook
#import pliku z danymi jedynie dla UE
df = pd.read_csv("energy_statistics_UE_v3.csv")

eh = df[(df["wide_category"] == "Electricity_and_Heat") 
        & (df["unit"] == "Kilowatt-hours, million") 
        & (df["transaction"] == "Gross production")]

#wszystkie kategorie/transakcje są w tych samych jednostkach
print(eh["unit"].unique())
print(eh["transaction"].unique())
print(eh["category"].unique())
print(eh["country_or_area"].unique())

# pogrupowanie per rok i kraj
grouped_eh = eh.groupby(by=["year","country_or_area"], as_index = False)
eh_sum = pd.DataFrame(grouped_eh["quantity"].sum())

#top 5 pod względem "quantity" w 2014 (czyli ostatnim okresie w próbie)
eh_sum[eh_sum["year"] == 2014].nlargest(5, "quantity")


#DF dla średniej z top 5 
#warunki
var_1 = eh_sum["country_or_area"] == "Germany"
var_2 = eh_sum["country_or_area"] == "Spain"
var_3 = eh_sum["country_or_area"] == "United Kingdom"
var_4 = eh_sum["country_or_area"] == "France"
var_5 = eh_sum["country_or_area"] == "Italy"
#DF - wszystkie z top 5
top_5_eh = eh_sum[var_1 | var_2 | var_3 | var_4 | var_5] 
#Groupby po roku ze średnią
top_5_grouped_eh = top_5_eh.groupby(by=["year"], as_index = False)
mean_top_5_eh = pd.DataFrame(top_5_grouped_eh["quantity"].mean())


#DEFINICJE dla Electricity and heat notebook

#widget eh
country_list_eh = list(eh_sum["country_or_area"].unique())
choice_widget_country_eh = widgets.Dropdown(options=country_list_eh)
values_eh = {"Kraj": choice_widget_country_eh.value}


def widgets_handler_eh(country_choice_eh):
    values_eh["Kraj"] = country_choice_eh
    
def widget_eh():
    widgets.interact(widgets_handler_eh, country_choice_eh=choice_widget_country_eh)
    
    
#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total_with_top5mean_eh():
    x = eh_sum[eh_sum["country_or_area"] == values_eh["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total electricity produced by {}".format(values_eh["Kraj"]))
    plt.plot("year", "quantity", data = mean_top_5_eh, label = "total electricity produced by top 5 countries (mean)")
    plt.legend()
    plt.xlim(1990, 2015)
    plt.title(label = "electricity produced in {} in comparison with mean of top 5".format(values_eh["Kraj"]))
    plt.show()
    

#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total_eh():
    x = eh_sum[eh_sum["country_or_area"] == values_eh["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total electricity produced by {}".format(values_eh["Kraj"]))
    plt.xlim(1990, 2015)
    plt.title(label = "electricity produced in {}".format(values_eh["Kraj"]))
    plt.show()
    
    
###------------------------    





# MAP_ALL_NOTEBOOK
# Przygotowanie danych Map_all notebook

#import pliku z danymi jedynie dla UE 
df1 = pd.read_csv("energy_statistics_UE_v3.csv")

#lista krajów
list_countries = df1['country_or_area'].unique().tolist()

#przypisanie kodów ISO
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})


#mapping kodów ISO
def mapping(el):
    iso_code = d_country_code.get(el)
    return iso_code

df1["ISO_code"] = df1["country_or_area"].apply(mapping)

#warunki
var_1 = df1["wide_category"] == "Green"
var_2 = df1["wide_category"] == "Nuclear"
var_3 = df1["wide_category"] == "Electricity_and_Heat"
df1 = df1[var_1 | var_2 | var_3]
df1 = df1[df1["unit"] == "Kilowatt-hours, million"]
df1 = df1[df1["transaction"].notna()]
df1 = df1[df1["transaction"].str.contains("production",case = False)]
df1 = df1[df1["transaction"] != "net production"] 
df1 = df1[df1["transaction"] != "total production, main activity"]
df1 = df1[df1["transaction"] != "total production, autoproducer"]
    
#Energia Zielona   
green = df1[df1["wide_category"] == "Green"]
grouped_green = green.groupby(by=["year","country_or_area", "ISO_code"], as_index = False)
gg = pd.DataFrame(grouped_green["quantity"].sum())


#Energia nuklearna
nuclear = df1[df1["wide_category"] == "Nuclear"]
grouped_nuclear = nuclear.groupby(by=["year","country_or_area", "ISO_code"], as_index = False)
gn = pd.DataFrame(grouped_nuclear["quantity"].sum())

#Elektryczność
electricity = df1[df1["wide_category"] == "Electricity_and_Heat"]
grouped_electricity = electricity.groupby(by=["year","country_or_area", "ISO_code"], as_index = False)
ge = pd.DataFrame(grouped_electricity["quantity"].sum())

##DEFINICJE
#lista kategorii do mapy
category_list_map = list(df1["wide_category"].unique())
choice_widget_category_map = widgets.Dropdown(options=category_list_map)
values_map = {"Kategoria": choice_widget_category_map.value}

def widgets_handler_map(category_choice_map):
    values_map["Kategoria"] = category_choice_map

###DO WERSJI z widgetem
def widget_map():
    widgets.interact(widgets_handler_map, category_choice_map=choice_widget_category_map)

def print_map():
    fig = px.choropleth(data_frame = df1[df1["wide_category"] == values_map["Kategoria"]],
                        scope= "europe",
                        locations= "ISO_code",
                        color= "quantity",  # value in column 'quantity' determines color
                        hover_name= "country_or_area",
                        color_continuous_scale= 'RdYlGn',#  color scale red, yellow green
                        animation_frame= "year",
                        title = "{} energy produced in UE (MkWh)".format(values_map["Kategoria"]))
    fig.show()

###DO WERSJI bez widgetu    
def print_map_green():
    fig = px.choropleth(data_frame = gg,
                        scope= "europe",
                        locations= "ISO_code",
                        color= "quantity",  # value in column 'quantity' determines color
                        hover_name= "country_or_area",
                        color_continuous_scale= 'RdYlGn',#  color scale red, yellow green
                        animation_frame= "year",
                        title = "Green energy produced in UE (MkWh)")
    fig.show()

def print_map_nuclear():
    fig = px.choropleth(data_frame = gn,
                        scope= "europe",
                        locations= "ISO_code",
                        color= "quantity",  # value in column 'quantity' determines color
                        hover_name= "country_or_area",
                        color_continuous_scale= 'RdYlGn',#  color scale red, yellow green
                        animation_frame= "year",
                        title = "Nuclear energy produced in UE (MkWh)")
    fig.show()
    
def print_map_electricity():
    fig = px.choropleth(data_frame = ge,
                        scope= "europe",
                        locations= "ISO_code",
                        color= "quantity",  # value in column 'quantity' determines color
                        hover_name= "country_or_area",
                        color_continuous_scale= 'RdYlGn',#  color scale red, yellow green
                        animation_frame= "year",
                        title = "Electricity produced in UE (MkWh)")
    fig.show()

    

###------------------------     
    
    
    
    
    

### Energy sources per country widget

data_frame = pd.read_csv("energy_gross_prod_UE.csv")

#suma energii dla całej EU per rok w rozbiciu na kategorie
cat_prod_sum = data_frame[["wide_category", "year", "quantity","country_or_area"]].groupby(by = ["wide_category", "year","country_or_area"], as_index = False).sum()

#średnia produkcja energii per rok w UE (ilościowo)
gross_prod_mean = data_frame[["year", "quantity"]].groupby(by = ["year"], as_index = False).mean()

#całkowita produkcja per rok kraj (ilościowo)
gross_prod = data_frame[["country_or_area", "year", "quantity"]].groupby(by = ["country_or_area", "year"], as_index = False).sum()

#top 5 pod względem "quantity" w 2014 (czyli ostatnim okresie w próbie)
gross_prod[gross_prod["year"] == 2014].nlargest(5, "quantity")

#DF dla średniej z top 5 
#warunki
var_1 = gross_prod["country_or_area"] == "Germany"
var_2 = gross_prod["country_or_area"] == "Spain"
var_3 = gross_prod["country_or_area"] == "United Kingdom"
var_4 = gross_prod["country_or_area"] == "France"
var_5 = gross_prod["country_or_area"] == "Italy"
#DF - wszystkie z top 5
top_5_gross = gross_prod[var_1 | var_2 | var_3 | var_4 | var_5] 
#Groupby po roku ze średnią
top_5_grouped_gross = top_5_gross.groupby(by=["year"], as_index = False)
mean_top_5_gross = pd.DataFrame(top_5_grouped_gross["quantity"].mean())

#widget
country_list = list(cat_prod_sum["country_or_area"].unique())
category_list = list(cat_prod_sum["wide_category"].unique())
choice_widget_country = widgets.Dropdown(options=country_list)
choice_widget_category = widgets.Dropdown(options=category_list)
values = {"Kraj": choice_widget_country.value, "Kategoria": choice_widget_category.value}


def widgets_handler(country_choice, category_choice):
    values["Kraj"] = country_choice
    values["Kategoria"] = category_choice



###DEFINICJE
#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total():
    x = gross_prod[gross_prod["country_or_area"] == values["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total energy produced by {}".format(values["Kraj"]))
    plt.plot("year", "quantity", data = mean_top_5_gross, label = "total energy produced by top 5 countries (mean)")
    plt.legend()
    plt.title(label = "total energy produced in {} in comparison with mean of top 5 of UE".format(values["Kraj"]))
    plt.show()

#wykres z sumą energii w danym kraju (wybranym z listy) i w wybranej kategorii (też z listy)
def plot_category():
    kraj = cat_prod_sum["country_or_area"] == values["Kraj"]
    kategoria = cat_prod_sum["wide_category"] == values["Kategoria"]
    y = cat_prod_sum[kraj & kategoria]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=y)
    plt.title(label = "{} in {}".format(values["Kategoria"], values["Kraj"]))
    plt.show()
    
plot_category()

#wykres z totalem produkcji energii w danym kraju oraz udziałem poszczególnych
def plot_bar():
    kraj = cat_prod_sum["country_or_area"] == values["Kraj"]
    kategoria = cat_prod_sum["wide_category"] == values["Kategoria"]
    z = cat_prod_sum[kraj]
    z = z[["year", "wide_category", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.plot.bar(stacked = True)
    plt.title(label = "share of energy sources in {}".format(values["Kraj"]))
    plt.legend(title=None)
    plt.show()
    
#wykres z totalem produkcji energii w danym kraju oraz udziałem poszczególnych - stack 100%
def plot_bar_100():
    kraj = cat_prod_sum["country_or_area"] == values["Kraj"]
    kategoria = cat_prod_sum["wide_category"] == values["Kategoria"]
    z = cat_prod_sum[kraj]
    z = z[["year", "wide_category", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
    plt.title(label = "share of energy sources in {}".format(values["Kraj"]))
    plt.legend(title=None)
    plt.show()    

widgets.interact(widgets_handler, country_choice=choice_widget_country, category_choice = choice_widget_category)
plot_total()
plot_category()
plot_bar() #opcja 1
plot_bar_100() #opcja 2



###------------------------ 





### ALL_EU_energy_production_analysis_CLEAN

#Pobieramy dane
data_frame = pd.read_csv("energy_statistics_UE_v3.csv")

#odfiltrowanie wyników dla jednostki kWh w celu sprawdzenia czy da się wyciągnąć procent energii prod z wiatru
df_kWh = data_frame[data_frame["unit"] == "Kilowatt-hours, million"]

#usuwanie NaN z kolumny transaction
df_kWh = df_kWh[df_kWh["transaction"].notna()] 

#odfiltrowanie tylko produkcji energii
df_kWh_prod = df_kWh[df_kWh["transaction"].str.contains("production",case = False)]

#data frame z sumą produkcji energii za dane lata dla całej EU
energy_prod_gr = df_kWh_prod.groupby(by = ["year"], as_index = False)
energy_prod_sum = pd.DataFrame(energy_prod_gr["quantity"].sum())

#wykres ilościowy produkowanej energii dla całej EU
####widać, że ilość produkowanej energii spada - trzeba zweryfikować czy tak jest i dlaczego
#drop po 2008 roku - przez kryzys gospodarczy?

fig, ax = plt.subplots(figsize=(13, 8))
plt.xticks(fontsize=12, rotation = 90)
plt.yticks(fontsize=12)

#ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
ax.set_xlim(0, 2014)
ax.xaxis.set_major_locator(MultipleLocator(1))

#tworzenie siatki, żeby wykres był bardziej czytelny
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

plt.plot(energy_prod_sum[["quantity", "year"]].groupby(by="year").sum(),label="All UE countries")

plt.legend(fontsize=14)
plt.ylabel("Millions of Kilowatts-Hour",fontsize=20)
plt.xlabel('Year',fontsize=20)
plt.title('Total energy production in the EU',fontsize=24)
plt.xlim(1990, 2014)
plt.show()


#przygotowanie list pod wykresy
list_category = df_kWh["wide_category"].unique()

list_transaction = df_kWh["transaction"].unique()

#stworzenie data_framu z całkowitą produkcją roczną energii per kraj - do późniejszych wykresów % udziału
# nuclear + green + gross production z Energy_and_Heat
df_temp = df_kWh_prod.copy()

#przygotowanie wierszy do usunięcia 
to_drop = ['net production', 'total production, autoproducer', 'total production, main activity']
df_temp["to drop"] = np.where(df_temp["transaction"].isin(to_drop), "Y", "N")
df_temp[df_temp["to drop"] == "Y"]

df_temp = df_temp[df_temp["to drop"] == "N"]

#usunięcie już niepotrzebnej kolumny to drop
df_temp = df_temp.drop(columns = "to drop")

df_temp.to_csv("energy_gross_prod_UE.csv") #zapisanie przygotowanego DF

#suma energii dla całej EU per rok w rozbiciu na kategorie
cat_prod_sum = df_temp[["wide_category", "year", "quantity"]].groupby(by = ["wide_category", "year"], as_index = False).sum()

#ogólny wykres dla calej EU dla kategorii z udziałem poszczególnych kategorii
z = cat_prod_sum
z = z[["year", "wide_category", "quantity"]]
z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
z_pivot = z_pivot.fillna(0)
z_pivot.plot.bar(stacked = True)
plt.title(label = "Share of energy sources in EU")
plt.legend(title=None)
plt.show()

#ogólny wykres dla calej EU dla kategorii z udziałem poszczególnych kategorii - stack 
z = cat_prod_sum
z = z[["year", "wide_category", "quantity"]]
z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
z_pivot = z_pivot.fillna(0)
z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
plt.title(label = "Share of green energy sources in EU")
plt.legend(title=None)
plt.show()

#GREEN energy przygotowanie DF
Green_prod = df_kWh_prod[df_kWh_prod["wide_category"] == "Green"]
list_trans_green = Green_prod["transaction"].unique()

#NUCLEAR energy przygotowanie DF
nuclear_prod = df_kWh_prod[df_kWh_prod["wide_category"] == "Nuclear"]

#HEAT energy przygotowanie DF
heat_prod = df_kWh_prod[df_kWh_prod["wide_category"] == "Electricity_and_Heat"]

#DF z sumą energii zielonej per rok dla całej UE
green_prod_gr = Green_prod.groupby(by = ["year"], as_index = False)
green_prod_sum = pd.DataFrame(green_prod_gr["quantity"].sum())

#DF z sumą energii zielonej per rok dla całej UE
nuclear_prod_gr = nuclear_prod.groupby(by = ["year"], as_index = False)
nuclear_prod_sum = pd.DataFrame(nuclear_prod_gr["quantity"].sum())

#DF z sumą energii zielonej per rok dla całej UE
heat_prod_gr = heat_prod.groupby(by = ["year"], as_index = False)
heat_prod_sum = pd.DataFrame(heat_prod_gr["quantity"].sum())

#wykres z totalem produkcji energii zielonej w UE w poszczególnych latach
#widać duży skok po 2005 roku można zrobić research czy nie weszła jakaś dyrektywa/dopłaty - ciekawostka do prezentacji
fig, ax = plt.subplots(figsize=(13, 8))
plt.xticks(fontsize=12, rotation = 90)
plt.yticks(fontsize=12)

#ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
ax.set_xlim(0, 2014)
ax.xaxis.set_major_locator(MultipleLocator(1))

#tworzenie siatki, żeby wykres był bardziej czytelny
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

plt.plot(green_prod_sum[["quantity", "year"]].groupby(by="year").sum(),label="All UE countries")

plt.legend(fontsize=14)
plt.ylabel("Millions of Kilowatts-Hour",fontsize=20)
plt.xlabel('Year',fontsize=20)
plt.title('Total green energy production in the EU',fontsize=24)
plt.xlim(1990, 2014)
plt.show()

#suma energii wyprodukowana w konkretnych latach w podziale na lata i kategorie
gr_green_trans = Green_prod.groupby(by = ["year", "transaction"], as_index = False)
green_trans_sum = pd.DataFrame(gr_green_trans["quantity"].sum())

#wykres z totalem wyprodukowanej energii zielonej w UE w podziale na lata i kategorie  
z = green_trans_sum
z = z[["year", "transaction", "quantity"]]
z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
z_pivot = z_pivot.fillna(0)
z_pivot.plot.bar(stacked = True)
plt.title(label = "Share of green energy sources in EU")
plt.legend(title=None)
plt.show()

#wykres z totalem wyprodukowanej energii zielonej w UE w podziale na lata i kategorie - stack
z = green_trans_sum
z = z[["year", "transaction", "quantity"]]
z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
z_pivot = z_pivot.fillna(0)
z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
plt.title(label = "Share of green energy sources in EU")
plt.legend(title=None)
plt.show()


###DEFINICJE
#wykres ilościowy produkowanej energii dla całej EU
def total_energy_production_in_EU():
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')
    plt.plot(energy_prod_sum[["quantity", "year"]].groupby(by="year").sum(),label="All UE countries")
    plt.legend(fontsize=14)
    plt.ylabel("Millions of Kilowatts-Hour",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('Total energy production in the EU',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
total_energy_production_in_EU()


#ogólny wykres dla calej EU dla kategorii z udziałem poszczególnych kategorii
def share_of_sources_in_EU():
    z = cat_prod_sum
    z = z[["year", "wide_category", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.plot.bar(stacked = True)
    plt.title(label = "Share of energy sources in EU")
    plt.legend(title=None)
    plt.show()

share_of_sources_in_EU()

#ogólny wykres dla calej EU dla kategorii z udziałem poszczególnych kategorii - stack 
def share_of_sources_in_EU_stack():
    z = cat_prod_sum
    z = z[["year", "wide_category", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "wide_category", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
    plt.title(label = "Share of green energy sources in EU")
    plt.legend(title=None)
    plt.show()

share_of_sources_in_EU_stack()
    
#wykres z totalem produkcji energii zielonej w UE w poszczególnych latach
#widać duży skok po 2005 roku można zrobić research czy nie weszła jakaś dyrektywa/dopłaty - ciekawostka do prezentacji
def total_green_energy_prod():    
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)
    ax.set_xlim(0, 2014) #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.grid(which='major', color='#CCCCCC', linestyle='--')    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')
    plt.plot(green_prod_sum[["quantity", "year"]].groupby(by="year").sum(),label="All UE countries")
    plt.legend(fontsize=14)
    plt.ylabel("Millions of Kilowatts-Hour",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('Total green energy production in the EU',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()

total_green_energy_prod()    
    
#wykres z totalem wyprodukowanej energii zielonej w UE w podziale na lata i kategorie  
def share_green_energy_sources_EU():
    z = green_trans_sum
    z = z[["year", "transaction", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.plot.bar(stacked = True)
    plt.title(label = "Share of green energy sources in EU")
    plt.legend(title=None)
    plt.show()

share_green_energy_sources_EU()


#wykres z totalem wyprodukowanej energii zielonej w UE w podziale na lata i kategorie - stack
def share_green_energy_sources_EU_stack():    
    z = green_trans_sum
    z = z[["year", "transaction", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
    plt.title(label = "Share of green energy sources in EU")
    plt.legend(title=None)
    plt.show()
    
share_green_energy_sources_EU_stack()   
  