import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from matplotlib.pyplot import cm
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)


##PRZYGOTOWANIE DANYCH GREEN##
df = pd.read_csv("energy_statistics_UE_v3.csv")
green = df[df["wide_category"] == "Green"]
#suma wyprodukowanej zielonej energii (wszystkie kategorie) posortowana wg lat i krajów
grouped_green = green.groupby(by=["year","country_or_area"], as_index = False)
green_sum = pd.DataFrame(grouped_green["quantity"].sum())
#DF dla średniej z top 5 
#warunki
var_1 = green_sum["country_or_area"] == "Germany"
var_2 = green_sum["country_or_area"] == "Spain"
var_3 = green_sum["country_or_area"] == "Italy"
var_4 = green_sum["country_or_area"] == "France"
var_5 = green_sum["country_or_area"] == "Sweden"
#DF - wszystkie z top 5
top_5 = green_sum[var_1 | var_2 | var_3 | var_4 | var_5] 
#Groupby po roku ze średnią
top_5_grouped = top_5.groupby(by=["year"], as_index = False)
mean_top_5 = pd.DataFrame(top_5_grouped["quantity"].mean())
#suma energii wyprodukowana w konkretnych latach w podziale na kraje i kategorie
grouped_green_category = green.groupby(by=["year","country_or_area", "transaction"], as_index = False)
green_sum_cat = pd.DataFrame(grouped_green_category["quantity"].sum())

#green_sum = pd.read_csv("green_sum_mod.csv")
#green_sum_cat = pd.read_csv("green_sum_cat_mod.csv")
#green = df[df["wide_category"] == "Green"]
#mean_top_5 = pd.read_csv("mean_top_5_mod.csv")





##PRZYGOTOWANIE DANYCH NUCLEAR##
nuclear = df[df["wide_category"] == "Nuclear"]
#suma wyprodukowanej energii nuklearnej posortowana wg lat i krajów
grouped_nuc = nuclear.groupby(by=["year","country_or_area"], as_index = False)
nuc_sum = pd.DataFrame(grouped_nuc["quantity"].sum())
#top 5 pod względem "quantity" w 2014 (czyli ostatnim okresie w próbie)
nuc_sum[nuc_sum["year"] == 2014].nlargest(5, "quantity")
#DF dla średniej z top 5 
#warunki
var_1 = nuc_sum["country_or_area"] == "Germany"
var_2 = nuc_sum["country_or_area"] == "Spain"
var_3 = nuc_sum["country_or_area"] == "United Kingdom"
var_4 = nuc_sum["country_or_area"] == "France"
var_5 = nuc_sum["country_or_area"] == "Sweden"
#DF - wszystkie z top 5
top_5_nuc = nuc_sum[var_1 | var_2 | var_3 | var_4 | var_5] 
#Groupby po roku ze średnią
top_5_grouped_nuc = top_5_nuc.groupby(by=["year"], as_index = False)
mean_top_5_nuc = pd.DataFrame(top_5_grouped_nuc["quantity"].mean())
# opis nuclear
nuclear_descr = "Nuclear power is the use of nuclear reactions that release nuclear energy to generate heat, which most frequently is then used in steam turbines to produce electricity in a nuclear power plant. Nuclear power can be obtained from nuclear fission, nuclear decay and nuclear fusion reactions."
#widget nuc
country_list_nuc = list(nuc_sum["country_or_area"].unique())
choice_widget_country_nuc = widgets.Dropdown(options=country_list_nuc)
values_nuc = {"Kraj": choice_widget_country_nuc.value}






##PRZYGOTOWANIE DANYCH HEAT##
df = pd.read_csv("energy_gross_prod_UE.csv")
heat = df[df["wide_category"] == "Electricity_and_Heat"]
#suma wyprodukowanej energii nuklearnej posortowana wg lat i krajów
grouped_heat = heat.groupby(by=["year","country_or_area"], as_index = False)
heat_sum = pd.DataFrame(grouped_heat["quantity"].sum())
#DF dla średniej z top 5 
#warunki
var_1 = heat_sum["country_or_area"] == "Germany"
var_2 = heat_sum["country_or_area"] == "Spain"
var_3 = heat_sum["country_or_area"] == "United Kingdom"
var_4 = heat_sum["country_or_area"] == "France"
var_5 = heat_sum["country_or_area"] == "Italy"
#DF - wszystkie z top 5
top_5_heat = heat_sum[var_1 | var_2 | var_3 | var_4 | var_5] 
#Groupby po roku ze średnią
top_5_grouped_heat = top_5_heat.groupby(by=["year"], as_index = False)
mean_top_5_heat = pd.DataFrame(top_5_grouped_heat["quantity"].mean())
#widget heat
country_list_heat = list(heat_sum["country_or_area"].unique())
choice_widget_country_heat = widgets.Dropdown(options=country_list_heat)
values_heat = {"Kraj": choice_widget_country_heat.value}


##KONFIGURACJA WIDGETU##
country_list = list(green_sum["country_or_area"].unique())
transaction_list = list(green["transaction"].unique())
choice_widget_country = widgets.Dropdown(options=country_list)
choice_widget_category = widgets.Dropdown(options=transaction_list)
values = {"Kraj": choice_widget_country.value, "Kategoria": choice_widget_category.value}



###PRZYGOTOWANIE DANYCH ALL UE###

data_frame = pd.read_csv("energy_gross_prod_UE.csv")
#data_frame z produkcją energii per rok per kraj - będzie przydatne w wykresach %
gross_prod = data_frame[["country_or_area", "year", "quantity"]].groupby(by = ["country_or_area", "year"], as_index = False).sum()
#DF gross green energy production per kraj per rok
green_only = data_frame[data_frame["wide_category"] == "Green"]
gross_green_prod = green_only[["country_or_area", "year", "quantity"]].groupby(by = ["country_or_area", "year"], as_index = False).sum()
#dołączenie nowej kulmny do DF z sumą całkowitej energii per rok per kraj
green = pd.merge(gross_green_prod, gross_prod, on = ["country_or_area","year"], how = "right")
#zamiana NaN na 0 dla krajów, które nie mają w ogóle green energy
green["quantity_x"] = green["quantity_x"].fillna(0)
#zmiana nazw dla kolumn wskazujących ilość - kolumna gross_year_qty pokazuje całkowitą ilość produkcji energii dla danego kraju
green = green.rename(columns={"quantity_x":"quantity_green", "quantity_y":"gross_year_qty"})
#dodanie kolumny z procentowym udziałem green energy 
green["% udział"] = green["quantity_green"]/green["gross_year_qty"]

green_top10 = green[green["year"] == 2014].nlargest(10, "% udział")

#DF gross green energy production per kraj per rok
bad_only = data_frame[data_frame["wide_category"] == "Electricity_and_Heat"]
gross_bad_prod = bad_only[["country_or_area", "year", "quantity"]].groupby(by = ["country_or_area", "year"], as_index = False).sum()
#dołączenie nowej kulmny do DF z sumą całkowitej energii per rok per kraj
heat_and_el = pd.merge(gross_bad_prod, gross_prod, on = ["country_or_area","year"], how = "right")
#zamiana NaN na 0 dla krajów, które nie mają w ogóle green energy
heat_and_el["quantity_x"] = heat_and_el["quantity_x"].fillna(0)
#zmiana nazw dla kolumn wskazujących ilość - kolumna gross_year_qty pokazuje całkowitą ilość produkcji energii dla danego kraju
heat_and_el = heat_and_el.rename(columns={"quantity_x":"quantity_heat", "quantity_y":"gross_year_qty"})
#dodanie kolumny z procentowym udziałem green energy 
heat_and_el["% udział"] = heat_and_el["quantity_heat"]/heat_and_el["gross_year_qty"]
#ten sam wykres co wyżej, ale dla top 10 krajów z największym udziałem procentowym 
bad_top10 = heat_and_el[heat_and_el["year"] == 2014].nlargest(10, "% udział")

#DF gross nuclear energy production per kraj per rok
nuclear_only = data_frame[data_frame["wide_category"] == "Nuclear"]
gross_nuclear_prod = nuclear_only[["country_or_area", "year", "quantity"]].groupby(by = ["country_or_area", "year"], as_index = False).sum()
#dołączenie nowej kulmny do DF z sumą całkowitej energii per rok per kraj
nuclear_prod = pd.merge(gross_nuclear_prod, gross_prod, on = ["country_or_area","year"], how = "right")
#zamiana NaN na 0 dla krajów, które nie mają w ogóle nuclear energy
nuclear_prod["quantity_x"] = nuclear_prod["quantity_x"].fillna(0)
#zmiana nazw dla kolumn wskazujących ilość - kolumna gross_year_qty pokazuje całkowitą ilość produkcji energii dla danego kraju
nuclear_prod = nuclear_prod.rename(columns={"quantity_x":"quantity_nuclear", "quantity_y":"gross_year_qty"})
#dodanie kolumny z procentowym udziałem green energy 
nuclear_prod["% udział"] = nuclear_prod["quantity_nuclear"]/nuclear_prod["gross_year_qty"]
#top 10 krajów pod względem produkcji energii nuklearnej w UE
nuclear_top10 = nuclear_prod[nuclear_prod["year"] == 2014].nlargest(10, "% udział")







###DEFINICJE heat,nuclear, green##
def widgets_interact():
    widgets.interact(widgets_handler, country_choice=choice_widget_country, category_choice = choice_widget_category)

def widgets_handler(country_choice, category_choice):
    values["Kraj"] = country_choice
    values["Kategoria"] = category_choice
    
#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total():
    x = green_sum[green_sum["country_or_area"] == values["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total green energy produced by {}".format(values["Kraj"]))
    plt.plot("year", "quantity", data = mean_top_5, label = "total green energy produced by top 5 countries (mean)")
    plt.legend()
    plt.xlim(1990, 2015)
    plt.title(label = "green energy produced in {} in comparison with mean of top 5".format(values["Kraj"]))
    plt.show()
    
#wykres z sumą energii w danym kraju (wybranym z listy) i w wybranej kategorii (też z listy)
#dodatkowo drukuje opis wybranej kategorii
def plot_category():
    #słownik opisów kategorii
    category_descr = {"total geothermal production": "Geothermal energy is heat derived within the sub-surface of the earth. Water and/or steam carry the geothermal energy to the Earth's surface. Depending on its characteristics, geothermal energy can be used for heating and cooling purposes or be harnessed to generate clean electricity.",
                  "total hydro production": "Hydropower or water power is power derived from the energy of falling or fast-running water, which may be harnessed for useful purposes. Since ancient times, hydropower from many kinds of watermills has been used as a renewable energy source for irrigation and the operation of various mechanical devices. A trompe, which produces compressed air from falling water, is sometimes used to power other machinery at a distance.",
                  "total solar production": "Solar power is the conversion of energy from sunlight into electricity, either directly using photovoltaics, indirectly using concentrated solar power, or a combination. Concentrated solar power systems use lenses or mirrors and solar tracking systems to focus a large area of sunlight into a small beam. Photovoltaic cells convert light into an electric current using the photovoltaic effect.",
                  "total tide, wave production": "Tidal energy is a renewable energy powered by the natural rise and fall of ocean tides and currents. Some of these technologies include turbines and paddles. Tidal energy is produced by the surge of ocean waters during the rise and fall of tides.",
                  "total wind production": "Wind energy (or wind power) refers to the process of creating electricity using the wind, or air flows that occur naturally in the earth’s atmosphere. Modern wind turbines are used to capture kinetic energy from the wind and generate electricity."}
    kraj = green_sum_cat["country_or_area"] == values["Kraj"]
    kategoria = green_sum_cat["transaction"] == values["Kategoria"]
    print("Description of the energy source:")
    for key, value in category_descr.items():
        if values["Kategoria"] == key:
            print(value)
    y = green_sum_cat[kraj & kategoria]
    plt.figure(figsize=(8, 6))
    plt.xlim(1990, 2015)
    plt.plot("year", "quantity", data=y)
    plt.title(label = "{} in {}".format(values["Kategoria"], values["Kraj"]))
    plt.show()
    
#wykres z totalem produkcji energii w danym kraju oraz udziałem poszczególnych
def plot_bar():
    kraj = green_sum_cat["country_or_area"] == values["Kraj"]
    kategoria = green_sum_cat["transaction"] == values["Kategoria"]
    z = green_sum_cat[kraj]
    z = z[["year", "transaction", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.plot.bar(stacked = True)
    plt.title(label = "share of green energy sources in {}".format(values["Kraj"]))    
    plt.legend(title=None)
    plt.show()
    
#wykres z totalem produkcji energii w danym kraju oraz udziałem poszczególnych - stack 100%
def plot_bar_100():
    kraj = green_sum_cat["country_or_area"] == values["Kraj"]
    kategoria = green_sum_cat["transaction"] == values["Kategoria"]
    z = green_sum_cat[kraj]
    z = z[["year", "transaction", "quantity"]]
    z_pivot = z.pivot(index = "year", columns = "transaction", values = "quantity")
    z_pivot = z_pivot.fillna(0)
    z_pivot.apply(lambda x: x*100/sum(x), axis=1).plot(kind="bar", stacked=True)
    plt.title(label = "share of green energy sources in {}".format(values["Kraj"]))
    plt.legend(title=None)
    plt.show()

    
def widgets_handler_nuc(country_choice_nuc):
    values_nuc["Kraj"] = country_choice_nuc
    
def widget_nuc():
    widgets.interact(widgets_handler_nuc, country_choice_nuc=choice_widget_country_nuc)
    print(nuclear_descr)
    
#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total_nuc():
    x = nuc_sum[nuc_sum["country_or_area"] == values_nuc["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total nuclear energy produced by {}".format(values_nuc["Kraj"]))
    plt.plot("year", "quantity", data = mean_top_5_nuc, label = "total nuclear energy produced by top 5 countries (mean)")
    plt.legend()
    plt.xlim(1990, 2015)
    plt.title(label = "nuclear energy produced in {} in comparison with mean of top 5".format(values_nuc["Kraj"]))
    plt.show()

def widgets_handler_heat(country_choice_heat):
    values_heat["Kraj"] = country_choice_heat
    
def widget_heat():
    widgets.interact(widgets_handler_heat, country_choice_heat=choice_widget_country_heat)
 
#wykres z sumą energii w totalu w danym kraju (wybranym z listy)
def plot_total_heat():
    x = heat_sum[heat_sum["country_or_area"] == values_heat["Kraj"]]
    plt.figure(figsize=(8, 6))
    plt.plot("year", "quantity", data=x, label = "total heat energy produced by {}".format(values_heat["Kraj"]))
    plt.plot("year", "quantity", data = mean_top_5_heat, label = "total heat energy produced by top 5 countries (mean)")
    plt.legend()
    plt.xlim(1990, 2015)
    plt.title(label = "heat energy produced in {} in comparison with mean of top 5".format(values_heat["Kraj"]))
    plt.show()
    

 


##DEFINICJE ALL UE##

#wykres pokazujący procentowy udział energii zielonej dla wszystkich krajów UE
#kolorki już są różne dla każdego kraju, ale wykres jest bardzo nieczytelny

def udzial_green_UE():
    list_countries = green["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    plt.figure(figsize=(15,10))
    plt.xticks( fontsize=16)
    plt.yticks( fontsize=16)

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.gist_rainbow(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = green[green.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("Green energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of green energy production per country per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
#wykres pokazujący max, min i średnią procentowego udziału energii zielonej w UE per rok
def max_min_avg_green_UE():
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    plot_data_mean = green[["year", "% udział"]].groupby(by = ["year"], as_index = False).mean()
    plot_data_min = green[["year", "% udział"]].groupby(by = ["year"], as_index = False).min()
    plot_data_max = green[["year", "% udział"]].groupby(by = ["year"], as_index = False).max()

    plt.plot(plot_data_mean["year"],plot_data_mean["% udział"]*100,label="UE mean")
    plt.plot(plot_data_min["year"],plot_data_min["% udział"]*100,label="UE min")
    plt.plot(plot_data_max["year"],plot_data_max["% udział"]*100,label="UE max")

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("Green energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of green energy production in UE by mean, max and min',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
def green_top10():
    list_countries = green_top10["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.tab10(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = green[green.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("Green energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of green energy production per top 10 countries per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()

#wykres pokazujący procentowy udział energii "burdnej" dla wszystkich krajów UE
#kolorki już są różne dla każdego kraju, ale wykres jest bardzo nieczytelny
def udzial_heat_UE():
    list_countries = heat_and_el["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    plt.figure(figsize=(15,10))
    plt.xticks( fontsize=16)
    plt.yticks( fontsize=16)

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.gist_rainbow(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = heat_and_el[heat_and_el.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("heat energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of heat energy production per country per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
#wykres pokazujący max, min i średnią procentowego udziału energii brudnej w UE per rok
def max_min_avg_heat_UE():
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    plot_data_mean = heat_and_el[["year", "% udział"]].groupby(by = ["year"], as_index = False).mean()
    plot_data_min = heat_and_el[["year", "% udział"]].groupby(by = ["year"], as_index = False).min()
    plot_data_max = heat_and_el[["year", "% udział"]].groupby(by = ["year"], as_index = False).max()

    plt.plot(plot_data_mean["year"],plot_data_mean["% udział"]*100,label="UE mean")
    plt.plot(plot_data_min["year"],plot_data_min["% udział"]*100,label="UE min")
    plt.plot(plot_data_max["year"],plot_data_max["% udział"]*100,label="UE max")

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("Green energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of heat energy production in UE by mean, max and min',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
    
def heat_top10_UE():
    list_countries = bad_top10["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.tab10(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = heat_and_el[heat_and_el.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("heat energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of heat energy production per top 10 countries per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
    
#wykres pokazujący procentowy udział energii nuklearnej dla wszystkich krajów UE
def udział_nuclear_UE():
    list_countries = nuclear_prod["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    plt.figure(figsize=(15,10))
    plt.xticks( fontsize=16)
    plt.yticks( fontsize=16)

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.gist_rainbow(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = nuclear_prod[nuclear_prod.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("nuclear energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of nuclear energy production per country per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
#wykres pokazujący max, min i średnią procentowego udziału energii nuklearnej w UE per rok
def max_min_avg_nuclear_UE():
    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    plot_data_mean = nuclear_prod[["year", "% udział"]].groupby(by = ["year"], as_index = False).mean()
    plot_data_min = nuclear_prod[["year", "% udział"]].groupby(by = ["year"], as_index = False).min()
    plot_data_max = nuclear_prod[["year", "% udział"]].groupby(by = ["year"], as_index = False).max()

    plt.plot(plot_data_mean["year"],plot_data_mean["% udział"]*100,label="UE mean")
    plt.plot(plot_data_min["year"],plot_data_min["% udział"]*100,label="UE min")
    plt.plot(plot_data_max["year"],plot_data_max["% udział"]*100,label="UE max")

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("nuclear energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of nuclear energy production in UE by mean, max and min',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()
    
def nuclear_top10():
    list_countries = nuclear_top10["country_or_area"].unique()

    n = len(list_countries) #ilość kolorów potrzebna do wykresu

    fig, ax = plt.subplots(figsize=(13, 8))
    plt.xticks(fontsize=12, rotation = 90)
    plt.yticks(fontsize=12)

    #ustawianie osi X, żeby wyświetlała wszystkie lata po kolei, a nie co 5.
    ax.set_xlim(0, 2014)
    ax.xaxis.set_major_locator(MultipleLocator(1))

    #tworzenie siatki, żeby wykres był bardziej czytelny
    ax.grid(which='major', color='#CCCCCC', linestyle='--')
    ax.grid(which='minor', color='#CCCCCC', linestyle=':')

    #definiowanie linii kolorystycznej
    #https://matplotlib.org/3.3.3/gallery/color/colormap_reference.html

    color = iter(cm.tab10(np.linspace(0,1,n)))

    for country in list(list_countries):
        country_data = nuclear_prod[nuclear_prod.country_or_area.isin([country])].sort_values('year')
        c = next(color)
        plt.plot(country_data["year"],country_data["% udział"]*100,label=country,c=c)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=15)
    plt.ylabel("nuclear energy %",fontsize=20)
    plt.xlabel('Year',fontsize=20)
    plt.title('% of nuclear energy production per top 10 countries per year',fontsize=24)
    plt.xlim(1990, 2014)
    plt.show()