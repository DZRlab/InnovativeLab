from shiny import App, render, ui
import pandas as pd
import numpy as np
import io
import seaborn as sns
import shinyswatch
import matplotlib.pyplot as plt
from shiny.types import ImgData
from shiny import App, render, ui, reactive, req, ui

#df = pd.read_excel('ContractsALL.xlsx')

# D:\\test\InnovativeLab\ContractsSMALL.csv
with open("InnovativeLab/ContractsSMALL.csv", 'rb') as f:
    bom = f.read(2)

if bom == b'\xff\xfe':
    print('File is encoded as UTF-16-LE')
elif bom == b'\xfe\xff':
    print('File is encoded as UTF-16-BE')
else:
    print('File does not have a BOM, so the version of UTF-16 is unknown')

with open("InnovativeLab/ContractsSMALL.csv", 'rb') as f:
    data = f.read()
    decoded_data = data.decode('utf-16-le', errors='ignore')

# D:\\test\InnovativeLab\ContractsSMALL.csv
df = pd.read_csv(io.StringIO(decoded_data), sep=';')

df_11 = df.copy()
df_111 = df_11[df_11['NumberOfOffers'] == 1]
df_10 = df.copy()
df_10 = df_10[["ProcessNumber","ContractingInstitutionName", "Subject",
                "ContractDate" , "ContractNumber" , "VendorName" , 
                "ContractPrice"]]

df_filtered=df_11[["ProcessNumber","ContractingInstitutionName",
                   "Subject","ContractDate","ContractNumber",
                   "VendorName","ContractPrice"]]

#df.to_csv('Contracts_decoded.csv', encoding='utf-8', sep = ';')

# creating a dict to use for drop-down box 
entity = df["ContractingInstitutionName"].unique()
keys = entity
values = entity
my_dict = {k: v for k, v in zip(keys, values)}

# creating dict for drop-down VendorName
entity1 = df["VendorName"].unique()
keys1 = entity1
values1 = entity1
my_dict1 = {k: v for k, v in zip(keys1, values1)}

df_i = df_11.ContractingInstitutionName.unique()
df_v = df_11.VendorName.unique()

# List of columns to exclude
exclude_cols = ['ProcessNumber','Subject','ProcurementName',
                'ProcedureName','OfferTypeName','UseElectronicTools',
                'ContractDate','ContractNumber','NumberOfOffers',
                'VendorName','EstimatedPrice','ContarctPriceWithoutVat',
                'Vat','ContractPrice']

# creating dict for drop-down checkbox_columns
col_names = df.columns
formatted_data = {item: item for item in col_names if item not in exclude_cols}

#PREVIEW
app_ui = ui.page_navbar(
    shinyswatch.theme.lumen(),
# 1TAB preview
    ui.nav_panel(
    ui.output_image("image", height = "60%"),
        ui.row(
            ui.output_image("image2"), style="text-align: center;",
        ),
        ui.row(
        ui.card(  
            ui.card_header("ИЗВОР НА ПОДАТОЦИТЕ"),
            ui.p("Податоците во оваа апликација се превземени од Електронскиот систем за јавни набавки - ЕСЈН во делот на склучени договори објавени во системот во период 01.01.2021 до 30.06.2024"),
            ),
        ui.card(
            ui.card_header("СТАТИСТИЧКИ ПОДАТОЦИ"),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Вкупен број на Јавни Набавки"),
                ui.p(str(len(df)), style="color:red; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    ui.card_header("Вкупен број на СУБЈЕКТИ"),
                ui.p(str(len(df_i)), style="background-color:darkgoldenrod; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    ui.card_header("Вкупен број на носители на набавки/добавувачи"),
                    ui.p(str(len(df_v)), style="text-align: center; font-size:400%", class_="btn-primary"),
                    ),
                ),    
            ),
        ),

        ui.layout_columns(  
        ui.card(  
            ui.card_header("ИНОВАТИВНА ЛАБОРАТОРИЈА"),
            ui.p("Овој проект е реализиран според Меморандумот за соработка меѓу Канцеларијата на Главниот ревизор на Норвешка и Државниот завод за ревизија"),
            ),
        ui.card(
            ui.card_header("INNOVATIVE LABORATORY"),
            ui.p("This project is acomplished according Memorandum of cooperation between the Office of the Auditor General of Norway and the State Audit Office"),
            ),
        ),
    ),
# 2TAB preview
    ui.nav_panel(
        "Склучени договори",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image3", height="50%"),
        ui.row(
            ui.column(
            6,
            ui.tooltip(    
                ui.input_selectize(
                "selectize", 
                "Одбери СУБЈЕКТ:",
                my_dict,
                multiple=False,
                width="600px"
                ),
            "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
            #id="btn_tooltip",
             ),
            ui.output_text("company"),
            ),
            ui.column(
            6,
            ui.input_date_range("daterange", " ПЕРИОД:", start="2020-01-01" , width="450px"),
            ),
            ui.input_checkbox_group(  
                "checkbox_columns",  
                "ОТСТРАНЕТЕ ГИ КОЛОНИТЕ КОИ НЕ СЕ РЕЛЕВАНТНИ ЗА ВАШЕТО ПОЛЕ НА ИНТЕРЕС СО СЕЛЕКТИРАЊЕ НА КВАДРАТЧЕТО ПОКРАЈ НАЗИВОТ НА КОЛОНАТА:",  
                formatted_data,
                inline=True,
                width="100%"
                ),
        ),
        ui.row(
            ui.column(3),
            ui.column(8, ui.download_button("downloadData", "Преземи податоци за ОБРАЗЕЦ ЈНПР и ЈНПП", width="800px", class_="btn-primary")),
        ),
        ui.output_data_frame("df_1"),

    ),
# 3TAB preview
    ui.nav_panel(
        "Преглед на набавки",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image4", height="50%"),    
            ui.row(
                ui.column(
                6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for_plot",
                    "Одбери СУБЈЕКТ:",
                    my_dict, multiple=False, 
                    width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),
                ),
                ui.column(
                6,
                ui.input_numeric("numeric", "Внеси ја максималната вредност на ЈН", 10000000, min=300000, max=1000000000, width="500px"), 
                ui.output_text_verbatim("value_n"),
                ),
            ),

        ui.input_slider("slider", "Одбери опсег на вредностa на јавните набавки!", min=0, max=20000000, value=[35, 1000000], width='100%'), 
        ui.output_text("slide_value"),
        ui.output_plot("plot", height='400px', fill=False),
        ui.tags.h5("Подредена табела по вредност на јавните набавки"), 
        ui.output_data_frame("df_2"),
    ),
# 4TAB preview
    ui.nav_panel(
        "Податоци по носител на набавка",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image5", height="50%"), 
            ui.row(
                ui.column(
                6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for",
                    "Одбери НОСИТЕЛ на набавка", 
                     my_dict1,
                     selected=None,
                     multiple=False,
                     width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),
                ),
                ui.column(
                6,
                    ui.input_date_range("daterange1", "ПЕРИОД:", start="2020-01-01" , width="450px"),
                ),
            ),
        ui.row(
        ui.column(3),
        ui.column(8, ui.download_button("downloadData1", "Преземи податоци", width="800px", class_="btn-primary")),
        ),
        ui.tags.h5("Подредена табела по вредност на јавните набавки :"), 
        ui.output_data_frame("df_3"),
    ),
# 5TAB preview
    ui.nav_panel(
        "Договори со 1 понуда",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image6", height="50%"),
        ui.row(
                ui.column(
                6,
                ui.tooltip(
                ui.input_selectize(
                    "selectize_for1",
                    "Одбери СУБЈЕКТ:", 
                    my_dict,
                    selected=None,
                    multiple=False,
                    width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),
                ),
                ui.column(
                6,
                ui.tags.h4({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 35px;"},""),
                ui.tags.h4({"style": "background-color:Goldenrod; color:white;"},"Од " + str(len(df)) + " јавни набавки, " + str(len(df_111)) + " се со само 1 понуда."),
                    ),
            ),
        ui.output_plot("plot1", height='400px', fill=False),     
        ui.tags.h5("Подредена табела по вредност на јавните набавки"), 
        ui.output_data_frame("df_5"),
    ),
# 6TAB preview
    ui.nav_panel(
        "Договори со 1 понуда по Носител на набавка",
            ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
            ui.output_image("image7", height="50%"),
            ui.tooltip(
            ui.input_selectize(
            "selectize_for11",
            "Одбери НОСИТЕЛ НА НАБАВКА:", 
            my_dict1,
            selected=None,
            multiple=False,
            width="600px"
            ),
            "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
            ),
        
        ui.column (12,
        ui.output_text("txt"), style="color:red; font-size:180%",
        align="center"),
        ui.tags.h5("Подредена табела по вредност на јавните набавки:"), 
        ui.output_data_frame("df_6"),
    ),
# 7TAB preview
        ui.nav_panel(
        "Пребарување по критериуми",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("imagekr", height="50%"),
        ui.output_data_frame("df_filter"),
        ui.output_text_verbatim("txt1"),
    ),
# 8TAB preview
    ui.nav_panel(
        "СТАТИСТИКА",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image8", height="50%"),
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Подредена листа на ДОБАВУВАЧИ по број на добиени набавки! "),
        ui.output_data_frame("df_9"),
        
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Топ 10.000 најголеми набавки по вредност по ДОБАВУВАЧ ! "),
        ui.output_data_frame("df_8"),
    
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Подредена листа на ДОБАВУВАЧИ по вкупно добиени пари!"),
        ui.output_data_frame("df_7"),
    ),
# 9TAB preview
    ui.nav_panel(
        "УПАТСТВО",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image9", height="50%"),
    ui.markdown(
    """
Апликацијата за пребарување и преземање на податоци од склучени договори по јавни набавки, се базира на податоците кои Бирото за јавни набавки ги објавува на Електронскиот систем за јавни набавки (ЕСЈН) во делот на склучени договори.
Податоците се преземаат и ажурираат на секои 6 месеци од следниов линк:
https://www.e-nabavki.gov.mk/PublicAccess/home.aspx#/contracts/0  

Со апликацијата можете да ги пребарувате и преземате податоците за склучени договори по јавни набавки од страна на субјектите, при што можете да селектирате набавки склучени од одреден субјект, за одреден период како и набавки по одреден вид на набавки за повеќе субјекти.  

За употреба на **ИЗБОР НА СУБЈЕКТ** или **ИЗБОР НА НОСИТЕЛ НА НАБАВКА** потребно е да кликнете на малиот триаголник десно на полето за избор, да го избришете полето со **backspace** и како ги внесувате буквите од името на субјектот така истите се филтрираат и го одбирате субјектот за кои ви требаат податоци.  
При Анализа на податоци по но**сител на набавка** во полето **Одбери најголема вредност** ја внесувате максималната вредност за јавните набавки за кои сакате податоци и истата ќе се прикаже на лизгачот за **Одбери опсег на вредноста на Јавните набавки**.  

Во апликацијата се дефинирани повеќе табови и тоа:  

**Склучени договори** – Ви дава информација за склучени договори по субјект, по период кога е склучен договорот.  

**Преглед на набавки** – Можност за преглед на број на набавки по одредени стратуми во опсег на износи на договорите (Вредноста на договорите не значи и дека вкупната вредност на договорот е реализирана).  

Анализа на податоци по **носител на набавка** – Преглед на склучени договори по носител на набавка и по период на набавка.  

Склучени **договори со една понуда** – Статистика по договорни органи кои склучиле договори за јавни набавки по набавки каде имало една понуда, по периоди.  

Склучени договори со **една понуда по носител на набавка** – Овде можете да видите статистика на склучени договори по носител на набавка при што во набавката понуда дал само еден економски оператор, по субјект и по периоди.  


Пребарување по критериуми – Можност за филтрирање податоци по различни критериуми – Број на набавка, субјект, назив (може и збор кој се содржи во називот – лекови, нафта, антивирус, мобилен и сл.), период на набавка.  

**Статистика** – Статистички податоци за набавки со најголеми износи, наголем број на склучени договори по носител на набавка, најголеми износи на склучени договори по договорен орган.  

**Упатство** – Објаснување за користење на апликацијата.  


Откако ќе ги селектирате сите колони за кои сакате да ги преземете податоците, стартувајте го копчето **`ПРЕЗЕМИ`**.
Податоците ќе се снимат pod име JN_SUBJEKT.xlsx во папката Downloads и за да можете да ги користите, потребно е да ги вчитате во Еxcel и притоа во процесот на вчитување ќе треба да потврдите дека податоците се од доверлив извор.
На ист начин се снимаат и користат преземените податоци кои се однесуваат за Носител на Јавната набавка: JN_NOSITEL.xlsx.


```
Откако ќе ги селектирате сите колони за кои сакате да ги преземете податоците, стартувајте го копчето преземи.
Податоците ќе се снимат во колоната Downloads и за да можете да ги користите, потребно е да ги вчитате во Еxcel при што ќе пристапите до папката и со помош на Get Data from Text/CSV ќе ги вчитате во нов документ.

"""
    )    ),

    position = ("fixed-top"),
    bg = "#d1dae3",
)


def server(input, output, session):
    @render.image
    def image():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "logo.png"), "width": "80px"}
        return img
    @render.image
    def image2():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "dzrA.jpg"), "width": "100%"}
        return img
    @render.image
    def image3():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab2.jpg"), "width": "100%"}
        return img
    @render.image
    def image4():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab3.jpg"), "width": "100%"}
        return img
    @render.image
    def image5():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab4.jpg"), "width": "100%"}
        return img
    @render.image
    def image6():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab5.jpg"), "width": "100%"}
        return img
    @render.image
    def image7():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab6.jpg"), "width": "100%"}
        return img
    @render.image
    def image8():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab7.jpg"), "width": "100%"}
        return img
    @render.image
    def image9():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tab8.jpg"), "width": "100%"}
        return img
    @render.image
    def imagekr():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "tabkr.jpg"), "width": "100%"}
        return img
    @output
    @render.text
    def company1():
        return "You choose: " + str(input.selectize_for_plot())
    @render.text
    def txt_entity():
        return entity
    @render.text
    def txt_entity1():
        return entity1
    @render.text
    def value_n():
        dali = input.numeric()
        ui.update_slider("slider", min=0, max=dali, value=[35, 1000000])
    @render.text
    def value():
        return  f"{input.daterange()[0]} to {input.daterange()[1]}"
    @render.text
    def value1():
        return  f"{input.daterange1()[0]} to {input.daterange1()[1]}"
    @render.text
    def txt():
        return f"Од вкупно: {len(df[df['VendorName'] == input.selectize_for11()])} јавни набавка/и, има {len(df_111[df_111['VendorName'] == input.selectize_for11()])} со само 1 понуда/и."
    @render.text
    def value():
        return ", ".join(input.checkbox_group())
    @reactive.Calc
    def filter():
        # filter 1
        df_1 = df[df['ContractingInstitutionName'] == input.selectize()]
        # filter 2
        start_date = input.daterange()[0]
        end_date = input.daterange()[1]
        df_1 = pd.DataFrame(df_1)
        df_1["ContractDate"] = pd.to_datetime(df_1["ContractDate"]).dt.date 
        mask = (df_1["ContractDate"] >= start_date) & (df_1["ContractDate"] <= end_date)
        filtered_df = df_1[mask]
        filtered_df = pd.DataFrame(filtered_df)
        filtered_df["ContractDate"] = pd.to_datetime(filtered_df["ContractDate"]).dt.strftime("%Y-%m-%d")

        # remmoving decimal places and remove decimal point
        filtered_df[['EstimatedPrice','ContractPriceWithoutVat','ContractPrice']].astype(float).astype(int)
        filtered_df.EstimatedPrice = filtered_df.EstimatedPrice.apply(int)
        filtered_df.ContractPriceWithoutVat = filtered_df.ContractPriceWithoutVat.apply(int)
        filtered_df.ContractPrice = filtered_df.ContractPrice.apply(int)
        
        # filter away chosen columns
        list_1 = list(input.checkbox_columns())
        formatted_data = {item: item for item in list_1}
        keys = list(formatted_data.keys())
        filtered_df = filtered_df.drop(columns=keys)
        return filtered_df.sort_values(by='ContractPrice', ascending=False)

    #TODO; what does this do? 
    @output
    @render.data_frame
    def df_1():
        return render.DataGrid(
            #df[df['ContractingInstitutionName'] == input.selectize()],
            filter()
        )
    
    @reactive.Calc
    def export():
        df = filter()
        df_export = df[['ProcessNumber','Subject','ProcurementName', 'ProcedureName','OfferTypeName','UseElectronicTools', 'ContractDate','ContractNumber','NumberOfOffers', 'VendorName', 'EstimatedPrice', 'ContractPriceWithoutVat','Vat', 'ContractPrice']]
        
        # Insert empty columns
        df_export['IzvorNaSredstva'] = 'NULL'  
        df_export['A'] = ''
        df_export['ID'] = range(1, len(df_export) + 1) 

        # List of columns in the desired order
        df_export = df_export[['ID','A','A','A','A','EstimatedPrice', 'A', 'OfferTypeName','UseElectronicTools','ProcedureName','Subject','ContractNumber','ContractDate','ProcurementName','VendorName','ContractPriceWithoutVat']]
        #new_order = ['ProcessNumber', 'EstimatedPrice', 'Vat', 'OfferTypeName','UseElectronicTools','ProcedureName','Subject','ContractDate','ContractNumber','ProcurementName','VendorName','ContractPriceWithoutVat','ContractPrice','NumberOfOffers']

        # Reorder the DataFrame columns
        #df_export = df[new_order]
        
        return df_export
    
    @reactive.Calc
    def export1():
        #df = filter_3()
        df_export1 = filter_3()
        return df_export1
    
    #@session.download(
    @render.download(
        filename=lambda: f"JN_SUBJEKT.xlsx")
    def downloadData():
        df = export()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return output.read(), "export.xlsx"
          
    @render.download(
        filename=lambda: f"JN_NOSITEL.xlsx")
        #filename=lambda: f"JN_po_nositel.csv")
    def downloadData1():
        df = export1()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return output.read(), "export.xlsx"
        #yield df.to_csv(sep= ';', encoding= 'UTF-8') 


    ### plots ###

    @reactive.Calc
    def filter_for_plot():
        # filter 1
        filtered_for_plot = df[df['ContractingInstitutionName'] == input.selectize_for_plot()]
        # filter 2
        min_amount = input.slider()[0]
        max_amount = input.slider()[1]
        filtered_for_plot = pd.DataFrame(filtered_for_plot)
        filtered_for_plot = filtered_for_plot[filtered_for_plot["ContractPrice"].between(min_amount, max_amount)]
        return filtered_for_plot.sort_values(by='ContractPrice', ascending=False)

    @render.plot(
    alt="Histogram"
    )  
    def plot():  
        df = filter_for_plot()
        data=df['ContractPrice']
        fig, ax = plt.subplots()
        num_bins = 50
        ax.hist(x=data, bins=20, linewidth=0.5, edgecolor="white")
        ax.set_xlabel("Вредност на договор - изразена во милиони денари")
        ax.set_ylabel("Број на набавки")

    @output
    @render.data_frame
    def df_2():
        return render.DataGrid(
            filter_for_plot()
        )
    
    @reactive.Calc
    def filter_3():
        df_3 = df[df['VendorName'] == input.selectize_for()]
        start_date = input.daterange1()[0]
        end_date = input.daterange1()[1]
        df_3 = pd.DataFrame(df_3)
        df_3["ContractDate"] = pd.to_datetime(df_3["ContractDate"]).dt.date 
        mask1 = (df_3["ContractDate"] >= start_date) & (df_3["ContractDate"] <= end_date)
        filtered_df3 = df_3[mask1]
        filtered_df3 = pd.DataFrame(filtered_df3)
        filtered_df3["ContractDate"] = pd.to_datetime(filtered_df3["ContractDate"]).dt.strftime("%Y-%m-%d")
        filtered_df3=filtered_df3[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        
        # remmoving decimal places and remove decimal point
        filtered_df3['ContractPrice'].astype(float).astype(int)
        filtered_df3.ContractPrice = filtered_df3.ContractPrice.apply(int)

        return filtered_df3.sort_values(by='ContractPrice', ascending=False)
    
    @render.plot(
    alt="Histogram"
    )  
    def plot1():
        df = filter_5t()
        ax = sns.histplot(data=df, x='ContractDate')
        ax.set_xlabel("Дата на договор")
        ax.set_ylabel("Број на набавки со 1 понуда")
        return ax

    @reactive.Calc
    def filter_5():
        df_5 = df_111[df_111['ContractingInstitutionName'] == input.selectize_for1()]
        df_5 = df_5[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        return df_5.sort_values(by='ContractPrice', ascending=False)

    def filter_5t():
        df_5t = df_111[df_111['ContractingInstitutionName'] == input.selectize_for1()]
        df_5t = df_5t[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        df_5t = df_5t.sort_values(by='ContractDate', ascending=True)
        df_5t['ContractDate'] = pd.to_datetime(df.ContractDate, format='%Y-%M-%d')
        df_5t['ContractDate']=df_5t['ContractDate'].dt.strftime('%Y')
        return df_5t

    @reactive.Calc
    def filter_6():
        df_6 = df_111[df_111['VendorName'] == input.selectize_for11()]
        df_6 = df_6[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        return df_6.sort_values(by='ContractPrice', ascending=False)

    @reactive.Calc
    def filter_8():
        df_8 = pd.DataFrame(df)
        df_8 = df_8[["VendorName","ContractPrice"]]
        df_8.groupby(['VendorName'])['ContractPrice'].sum()
        df_8 = df_8.sort_values(by='ContractPrice', ascending=False)
        df_8 = df_8.head(10000)
        return df_8
    
    def filter_7():
        df_7 = df[["VendorName","ContractPrice"]]
        df_7 = pd.DataFrame(df_7)
        amount = df_7.groupby('VendorName')['ContractPrice'].sum()
        df_7['Vendor_amount'] = df_7['VendorName'].map(amount)
        df_7 = df_7[["VendorName","Vendor_amount"]]
        filter_df_7= pd.DataFrame(df_7)
        filter_df_7 = filter_df_7.drop_duplicates(subset=['Vendor_amount'])
        
        return filter_df_7.sort_values(by='Vendor_amount', ascending=False)
        #return filter_df_7
    
    def filter_9():
        df_9 = pd.DataFrame(df)
        df_9 = df_9[["VendorName"]]
        counts = df_9['VendorName'].value_counts()
        
        ##add the counts to a new column
        df_9['VendorName_counts'] = df_9['VendorName'].map(counts)
        
        df_9 = df_9.drop_duplicates(subset=['VendorName'])
        return df_9.sort_values(by='VendorName_counts', ascending=False)
 
    @output
    @render.data_frame
    def df_3():
        return render.DataGrid(
        filter_3()
        )
    
    @render.data_frame
    def df_5():
        return render.DataGrid(
        filter_5()  
        )
    
    @render.data_frame
    def df_6():
        return render.DataGrid(
        filter_6()  
        )
    
    @render.data_frame
    def df_8():
        return render.DataGrid(
        filter_8(),
        width="100%",
        height="250px" 
        )
    
    @render.data_frame
    def df_7():
        return render.DataGrid(
        filter_7(),
        width="100%",
        height="250px" 
        )

    @render.data_frame
    def df_9():
        return render.DataGrid(
        filter_9(),
        width="100%",
        height="250px" 
        )
    
    @render.data_frame
    def df_filter():
        
        return render.DataTable(
            df_filtered,
            row_selection_mode='multiple',
            width="100%",
           filters=True,
        )


app = App(app_ui, server)