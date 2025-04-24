from shiny import App, render, ui
import pandas as pd
import numpy as np
import io
import seaborn as sns
#import shinyswatch
import matplotlib.pyplot as plt
from shiny.types import ImgData
from shiny import App, render, ui, reactive, req, ui

#df = pd.read_excel('ContractsALL.xlsx')

# test merge_temp
# another test
# more test

# use this line when running on the shiny server
with open("ContractsSMALL.csv", 'rb') as f:
# use this line when running locally
#with open("D:\\test\InnovativeLab\ContractsSMALL.csv", 'rb') as f:
    bom = f.read(2)

if bom == b'\xff\xfe':
    print('File is encoded as UTF-16-LE')
elif bom == b'\xfe\xff':
    print('File is encoded as UTF-16-BE')
else:
    print('File does not have a BOM, so the version of UTF-16 is unknown')

# use this line when running on the shiny server
with open("ContractsSMALL.csv", 'rb') as f:
# use this line when running locally
#with open("D:\\test\InnovativeLab\ContractsSMALL.csv", 'rb') as f:
    data = f.read()
    decoded_data = data.decode('utf-16-le', errors='ignore')

df = pd.read_csv(io.StringIO(decoded_data), sep=';')
#df = pd.read_csv(
    #io.StringIO(decoded_data), 
    #sep=';', 
    #dtype={13: str, 16: str},
    #low_memory=False
#)

df_111 = df[df['NumberOfOffers'] == 1]
df_10 = df.copy()
df_10 = df_10[["ProcessNumber","ContractingInstitutionName","Subject","ContractDate","ContractNumber","VendorName","ContractPrice"]]

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

df_i = df.ContractingInstitutionName.unique()
df_v = df.VendorName.unique()

# List of columns to exclude
exclude_cols = ['ProcessNumber','Subject','ProcurementName','ProcedureName','IsDevided',
                'OfferTypeName','UseElectronicTools','ContractDate','ContractNumber','NumberOfOffers',
                'VendorName','EstimatedPrice','ContractPriceWithoutVat','Vat','ContractPrice']

# creating dict for drop-down checkbox_columns
col_names = df.columns
formatted_data = {item: item for item in col_names if item not in exclude_cols}

#PREVIEW
app_ui = ui.page_navbar(
 #   shinyswatch.theme.lumen(),
# 1TAB preview
    ui.nav_panel(
    ui.output_image("image", height = "60%"),
        ui.row(
            ui.output_image("image2"), style="text-align: center;",
        ),
        ui.row(
        ui.card(  
            ui.card_header("ИЗВОР НА ПОДАТОЦИТЕ"),
            ui.p("Податоците во оваа апликација се превземени од Електронскиот систем за јавни набавки - ЕСЈН во делот на склучени договори објавени во системот во период 01.01.2020 до 31.12.2024"),
            ),
        ui.card(
            ui.card_header("СТАТИСТИЧКИ ПОДАТОЦИ"),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Вкупен број на СКЛУЧЕНИ ДОГОВОРИ"),
                ui.p(str(len(df)), style="color:red; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    ui.card_header("Вкупен број на СУБЈЕКТИ - ДОГОВОРНИ ОРГАНИ"),
                ui.p(str(len(df_i)), style="background-color:darkgoldenrod; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    #style="background-color:darkgoldenrod;",
                    ui.card_header("Вкупен број на НОСИТЕЛИ НА НАБАВКИ - ДОБАВУВАЧИ"),
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
        ui.HTML("<br><br>"),  # Adding empty space
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
            #ui.output_text("company"),
            ),
            ui.column(
            6,
            ui.input_date_range("daterange", " ПЕРИОД:", start="2020-01-01" , end="2024-12-31", width="450px"), ##START need corespondent with CSV#
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
            ui.HTML("<br><br>"),  # Adding empty space
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
                #id="btn_tooltip",
                ),
                ),
        #ui.output_text('company1'), #present name of chosen company#
                ui.column(
                6,
                ui.input_numeric("numeric", "Внеси ја максималната вредност на склучените договори", 10000000, min=300000, max=100000000000, width="500px"), 
                ui.output_text_verbatim("value_n"),
                ),
            ),
        ui.input_slider("slider", "Одбери опсег на вредностa на склучените договори!", min=0, max=20000000, value=[35, 1000000], width='100%'), 
        ui.output_text("slide_value"),
        ui.output_plot("plot", height='400px', fill=False),
        ui.tags.h5("Подредена табела по вредност на склучените договори"), 
        ui.output_data_frame("df_2"),
    ),
# 4TAB preview
    ui.nav_panel(
        "Податоци по носител на набавка",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image5", height="50%"), 
            ui.HTML("<br><br>"),  # Adding empty space
            ui.row(
                ui.column(
                6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for",
                    "Одбери НОСИТЕЛ на набавка/склучен договор", 
                     my_dict1,
                     selected=None,
                     multiple=False,
                     width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),
                ),
                #ui.output_text('subject'),
                ui.column(
                6,
                    ui.input_date_range("daterange1", "ПЕРИОД:", start="2020-01-01" , end="2024-12-31", width="450px"), 
                ),
            ),
        ui.row(
        ui.column(3),
        ui.column(8, ui.download_button("downloadData1", "Преземи податоци", width="800px", class_="btn-primary")),
        ),
        ui.tags.h5("Подредена табела по вредност на склучените договори :"), 
        ui.output_data_frame("df_3"),
    ),
# 5TAB preview
    ui.nav_panel(
        "Договори со 1 понуда",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image6", height="50%"),
        ui.HTML("<br><br>"),  # Adding empty space
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
                ui.tags.h5({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 35px;"},""),
                ui.tags.h5({"style": "background-color:Goldenrod; color:white;"},"Од вкупно " + str(len(df)) + " склучени договори преку ЕСЈН, " + str(len(df_111)) + " се со само 1 понуда."),
                    ),
            ),
        ui.output_plot("plot1", height='400px', fill=False),
                ui.row(
        ui.column(3),
        ui.column(8, 
            ui.download_button("downloadData2", "Преземи податоци", width="800px", class_="btn-primary")),
        ),   
        ui.tags.h5("Подредена табела по вредност на склучените договори"), 
        ui.output_data_frame("df_5"),
    ),
# 6TAB preview
    ui.nav_panel(
        "Договори со 1 понуда по Носител на набавка",
            ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
            ui.output_image("image7", height="50%"),
            ui.HTML("<br><br>"),  # Adding empty space
            ui.tooltip(
            ui.input_selectize(
            "selectize_for11",
            "Одбери НОСИТЕЛ НА НАБАВКА/СКЛУЧЕН ДОГОВОР:", 
            my_dict1,
            selected=None,
            multiple=False,
            width="600px"
            ),
            "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
            ),
        ui.column (12,
        ui.output_text("txt"), style="color:black; font-size:180%",
        align="center"),
        ui.tags.h5("Подредена табела по вредност на склучените договори:"), 
        ui.output_data_frame("df_6"),
    ),
# 8TAB preview
    ui.nav_panel(
        "СТАТИСТИКА",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image8", height="50%"),
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Листа на ДОБАВУВАЧИ со број на склучени договори! "),
        ui.output_data_frame("df_9"),
       
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Поединечни склучени договори со најголемата вредност по ДОБАВУВАЧ ! "),
        ui.output_data_frame("df_8"),
    
        ui.h3({"style": "text-align: center;background-color:powderblue;"}, "Листа на ДОБАВУВАЧИ по вкупна вредност на договори!"),
        ui.output_data_frame("df_7"),
    ),
# 9TAB preview
    ui.nav_panel(
        "УПАТСТВО",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image9", height="50%"),
        ui.HTML("<br><br>"),  # Adding empty space
    ui.markdown(
    """
Апликацијата за пребарување и преземање на податоци од склучени договори по јавни набавки, се базира на податоците кои Бирото за јавни набавки ги објавува на Електронскиот систем за јавни набавки (ЕСЈН) во делот на склучени договори.
Податоците се преземаат и ажурираат на секои 6 месеци од следниов линк:
https://www.e-nabavki.gov.mk/PublicAccess/home.aspx#/contracts/0  

Со апликацијата можете да ги пребарувате и преземате податоците за склучени договори по јавни набавки од страна на субјектите, при што можете да селектирате набавки склучени од одреден субјект, за одреден период како и набавки по одреден вид на набавки за повеќе субјекти.  

За употреба на **ИЗБОР НА СУБЈЕКТ** или **ИЗБОР НА НОСИТЕЛ НА НАБАВКА** потребно е да кликнете на малиот триаголник десно на полето за избор, да го избришете полето со **backspace** и како ги внесувате буквите од името на субјектот така истите се филтрираат и го одбирате субјектот за кои ви требаат податоци.  
При Анализа на податоци по **носител на набавка** во полето **Одбери најголема вредност** ја внесувате максималната вредност за јавните набавки за кои сакате податоци и истата ќе се прикаже на лизгачот за **Одбери опсег на вредноста на Јавните набавки**.  

Во апликацијата се дефинирани повеќе табови и тоа:  

**Склучени договори** – Ви дава информација за склучени договори по субјект, по период кога е склучен договорот.  

**Преглед на набавки** – Можност за преглед на број на набавки по одредени стратуми во опсег на износи на договорите (Вредноста на договорите не значи и дека вкупната вредност на договорот е реализирана).  

Анализа на податоци по **носител на набавка** – Преглед на склучени договори по носител на набавка и по период на набавка.  

Склучени **договори со една понуда** – Статистика по договорни органи кои склучиле договори за јавни набавки по набавки каде имало една понуда, по периоди.  

Склучени договори со **една понуда по носител на набавка** – Овде можете да видите статистика на склучени договори по носител на набавка при што во набавката понуда дал само еден економски оператор, по субјект и по периоди.  


**Статистика** – Статистички податоци за набавки со најголеми износи, наголем број на склучени договори по носител на набавка, најголеми износи на склучени договори по договорен орган.  

**Упатство** – Објаснување за користење на апликацијата.  


Откако ќе ги селектирате сите колони за кои сакате да ги преземете податоците, стартувајте го копчето **`ПРЕЗЕМИ ПОДАТОЦИ за ОБРАЗЕЦ ЈНПР и ЈНПП`**.
Податоците ќе се снимат под име ime_na_subjekt_JNPRiJNPP.csv во папката Downloads и за да можете да ги користите, потребно е да го отворите FinalenObrazecJNPRiJNPP_za_CSV и притоа во процесот на вчитување ќе треба да го импортирате снимениот csv фајл.
Потребно е формираниот Образец да го снимите како ексел фајл.

За преземање на податоци во табовите по **носител на набавка** и во табот **договори со една понуда**, при генерирање на csv датотеката и нејзино снимање во папката downloads, потребно е да отворите нов ексел документ и да го внесете истиот со Data > Import > from csv  и да го вчитате на тој начин во ексел.
"""
    )),

    position = ("fixed-top"),
    bg = "#d1dae3",
   # fluid = True
)

def server(input, output, session):

    # Image rendering functions
    def render_image(image_name, width="100%"):
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / image_name), "width": width}
        return img

    @render.image
    def image():
        return render_image("logo.png", "60px")
    @render.image
    def image2():
        return render_image("dzrA.jpg")
    @render.image
    def image3():
        return render_image("tab2.jpg")
    @render.image
    def image4():
        return render_image("tab3.jpg")
    @render.image
    def image5():
        return render_image("tab4.jpg")
    @render.image
    def image6():
        return render_image("tab5.jpg")
    @render.image
    def image7():
        return render_image("tab6.jpg")
    @render.image
    def image8():
        return render_image("tab7.jpg")
    @render.image
    def image9():
        return render_image("tab8.jpg")
    @render.image
    def imagekr():
        return render_image("tabkr.jpg")
    
# 2TAB ##TEMPLATE###
    @reactive.Calc
    @render.text
    def txt_entity():
        return entity
    def filter():
        df_1 = df[df['ContractingInstitutionName'] == input.selectize()]
        start_date, end_date = input.daterange()
        df_1.loc[:, "ContractDate"] = pd.to_datetime(df_1["ContractDate"]).dt.date   # Use .loc to avoid SettingWithCopyWarning     
        mask = (df_1["ContractDate"] >= start_date) & (df_1["ContractDate"] <= end_date)
        filtered_df = df_1.loc[mask].copy()  # Use .copy() to avoid SettingWithCopyWarning
        #filtered_df["ContractDate"] = filtered_df["ContractDate"].astype(str)
        #filtered_df.loc[:, ['EstimatedPrice','ContractPriceWithoutVat','ContractPrice']] = filtered_df[['EstimatedPrice','ContractPriceWithoutVat','ContractPrice']].astype(int)
        
        # Filter away chosen columns
        list_1 = list(input.checkbox_columns())
        formatted_data = {item: item for item in list_1}
        keys = list(formatted_data.keys())
        filtered_df = filtered_df.drop(columns=keys)
        return filtered_df.sort_values(by='ContractPrice', ascending=False)

    @output
    @render.data_frame
    def df_1():
        return render.DataGrid(
            filter()
        )
    #@session.download(
    @reactive.Calc
    def export():
        df = filter()
        df_export = df[['ProcessNumber','Subject','ProcurementName', 'ProcedureName','IsDevided',
                        'OfferTypeName','UseElectronicTools','ContractDate','ContractNumber','NumberOfOffers',
                        'VendorName','EstimatedPrice', 'ContractPriceWithoutVat','Vat','ContractPrice']]
        
        df_export = pd.DataFrame(df_export)

        # Insert empty columns
        df_export = df_export.copy()
        df_export.loc[:, 'A'] = ' '
        ##df_export['A'] = ' '
        ##df_export['ID'] = range(1, len(df_export) + 1)
        #df_export.loc[:, 'ID'] = range(1, len(df_export) + 1) 

            # Sort the DataFrame by 'ProcessNumber' in descending order
        df_export = df_export.sort_values(by='ProcessNumber', ascending=True)
        df_export = pd.DataFrame(df_export)

        # Find duplicate rows based on 'ProcessNumber' and keep the first occurrence
        df_export['EstimatedPrice'] = df_export.groupby('ProcessNumber')['EstimatedPrice'].transform(lambda x: x.mask(x.duplicated(keep='first'), 0))

        # Assign IDs in scending order
        df_export['ID'] = range(1, len(df_export) + 1)

        # List of columns in the desired order
        df_export = df_export[['ID','A','A','A','A','EstimatedPrice', 'A', 'OfferTypeName',
                               'UseElectronicTools','ProcessNumber','IsDevided','ProcedureName','Subject','ContractNumber',
                               'ContractDate','ProcurementName','VendorName','ContractPriceWithoutVat']]  ###added 'ProcessNumber'and 'IsDevided'
        #return df_export.sort_values(by='ProcessNumber', ascending=True)
        return df_export
    @render.download(
        ##filename=lambda: f"JN_SUBJEKT.xlsx")
        filename=lambda: f"{filter()['ContractingInstitutionName'].iloc[0]}JNPRiJNPP.csv")
        #filename=lambda: f"ZaObrazec_JN_new.csv")
    def downloadData():
        df = export()
        ##output = io.BytesIO()
        ##with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            ##df.to_excel(writer, index=False, sheet_name='Sheet1')
        ##output.seek(0)
        ##return output.read(), "export.xlsx"
        yield df.to_csv(sep= ';', encoding= 'UTF-8', index=False) 
        ####df.to_string(index=False)

# 3TAB ### plots ###
    @render.text
    def value_n():
        dali = input.numeric()
        formatted_dali = f"{dali:,}".replace(",", ".")
        ui.update_slider("slider", min=0, max=dali, value=[35, 1000000])
        return formatted_dali
    @reactive.Calc
    def filter_for_plot():
        # Define columns to select
        columns = ['ProcessNumber', 'Subject', 'ProcurementName', 'ProcedureName', 'IsDevided',
               'OfferTypeName', 'UseElectronicTools', 'ContractDate', 'ContractNumber', 'NumberOfOffers',
               'VendorName', 'EstimatedPrice', 'ContractPriceWithoutVat', 'Vat', 'ContractPrice']
    
        # Filter 1: Select relevant rows and columns
        filtered_for_plot = df.loc[df['ContractingInstitutionName'] == input.selectize_for_plot(), columns]
    
        # Filter 2: Apply range filter on 'ContractPrice'
        min_amount, max_amount = input.slider()
        filtered_for_plot = filtered_for_plot[filtered_for_plot["ContractPrice"].between(min_amount, max_amount)]
        return filtered_for_plot.sort_values(by='ContractPrice', ascending=False)
    @render.plot(
    alt="Histogram"
    )  
    def plot():  
        df = filter_for_plot()
        df = df.drop_duplicates(subset='ProcessNumber') ### newline
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
            #df[df['ContractingInstitutionName'] == input.selectize()]
            filter_for_plot()
        )
    
# 4TAB ### VENDOR review ###
    @render.text
    def txt_entity1():
        return entity1
    @reactive.Calc
    def filter_3():
        df_3 = df[df['VendorName'] == input.selectize_for()]
        start_date, end_date = input.daterange1()
    
        # Use .loc to avoid SettingWithCopyWarning
        df_3.loc[:, "ContractDate"] = pd.to_datetime(df_3["ContractDate"]).dt.date
        mask1 = (df_3["ContractDate"] >= start_date) & (df_3["ContractDate"] <= end_date)
    
        # Use .loc to filter and select columns in one step
        filtered_df3 = df_3.loc[mask1, ["ProcessNumber", "ContractingInstitutionName", "Subject", "ProcurementName", 
                                    "AgreeementDurationMonthsDays","ContractDate", "ContractNumber", 
                                    "NumberOfOffers", "VendorName", "ContractPrice"]].copy()
    
        # Convert ContractDate to string format
        filtered_df3.loc[:, "ContractDate"] = filtered_df3["ContractDate"].astype(str)
        
        # remmoving decimal places and remove decimal point
        filtered_df3['ContractPrice'].astype(float).astype(int)
        filtered_df3.ContractPrice = filtered_df3.ContractPrice.apply(int)
        #filtered_df["ContractPrice"] = filtered_df["ContractPrice"].map("{:,.0f}".format)
        return filtered_df3.sort_values(by='ContractPrice', ascending=False)
    @reactive.Calc
    def export1():
        #df = filter_3()
        df_export1 = filter_3()
        return df_export1
    @output
    @render.data_frame
    def df_3():
        return render.DataGrid(
        filter_3()
        )
    @render.download(
        #filename=lambda: f"JN_NOSITEL.xlsx")
        filename=lambda: f"{export1()['VendorName'].iloc[0]}2020do2024.csv")
        #filename=lambda: f"JN_NOSITEL.csv")
    def downloadData1():
        df = export1()
        #output = io.BytesIO()
        #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            #df.to_excel(writer, index=False, sheet_name='Sheet1')
        #output.seek(0)
        #return output.read(), "export.xlsx"
        yield df.to_csv(sep= ';', encoding= 'UTF-8', index=False)

# 5TAB ### 1 OFFER by SUBJECT review ###
    @reactive.Calc
    def filter_5():
        df_5 = df_111[df_111['ContractingInstitutionName'] == input.selectize_for1()]
        df_5 = df_5[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreeementDurationMonthsDays",
                     "ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        return df_5.sort_values(by='ContractPrice', ascending=False)
    def filter_5t():
        df_5t = df_111[df_111['ContractingInstitutionName'] == input.selectize_for1()]
        df_5t = df_5t[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreeementDurationMonthsDays",
                       "ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        df_5t = df_5t.sort_values(by='ContractDate', ascending=True)
        df_5t = df_5t.drop_duplicates(subset='ProcessNumber') ### newline
        df_5t['ContractDate'] = pd.to_datetime(df.ContractDate, format='%Y-%M-%d')
        df_5t['ContractDate']=df_5t['ContractDate'].dt.strftime('%Y')
        return df_5t
    @render.plot(
    alt="Histogram"
    )  
    def plot1():  
        #option = (999)
        df = filter_5t()
        ax = sns.histplot(data=df, x='ContractDate')
        ax.set_xlabel("Дата на договор")
        ax.set_ylabel("Број на набавки со 1 понуда")
        return ax
    @reactive.Calc
    def export2():
        #df = filter_3()
        df_export2 = filter_5()
        return df_export2
    @output
    @render.data_frame
    def df_5():
        return render.DataGrid(
        filter_5t()  
        )
    @render.download(
        ##filename=lambda: f"JN_NOSITEL_1ponuda.xlsx")
        filename=lambda: f"{export2()['ContractingInstitutionName'].iloc[0]}so1ponuda202do2024.csv")
        #filename=lambda: f"JN_NOSITEL_1ponuda.csv")
    def downloadData2():
        df = export2()
        #output = io.BytesIO()
        #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            #df.to_excel(writer, index=False, sheet_name='Sheet1')
        #output.seek(0)
        #return output.read(), "export.xlsx"
        yield df.to_csv(sep= ';', encoding= 'UTF-8', index=False)
    
# 6TAB ### 1 OFFER by VENDOR review ###
    @reactive.Calc
    def filter_6():
        df_6 = df_111[df_111['VendorName'] == input.selectize_for11()]
        df_6 = df_6[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreeementDurationMonthsDays",
                     "ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        return df_6.sort_values(by='ContractPrice', ascending=False)
    @render.data_frame
    def df_6():
        return render.DataGrid(
        filter_6()  
        )
    @render.text
    def txt():
        return f"Носителот на набавка Од вкупно: {len(df[df['VendorName'] == input.selectize_for11()])} склучени договори, има {len(df_111[df_111['VendorName'] == input.selectize_for11()])} со само 1 понуда/и."

# TAB ### STATISTIC 3 table###
    @reactive.Calc
    def filter_9(): #1table#
        df_9 = pd.DataFrame(df_10)
        df_9 = df_9[["VendorName"]]
        counts = df_9['VendorName'].value_counts()
        ##add the counts to a new column
        df_9['VendorName_counts'] = df_9['VendorName'].map(counts)
        df_9 = df_9.drop_duplicates(subset=['VendorName'])
        return df_9.sort_values(by='VendorName_counts', ascending=False)
    @render.data_frame
    def df_9():
        return render.DataGrid(
        filter_9(),
        width="100%",
        height="250px" 
        )
    
    def filter_8(): #2table#
        df_8 = pd.DataFrame(df_10)
        df_8 = df_8[["VendorName","ContractPrice"]]
        df_8 = df_8.sort_values(by='ContractPrice', ascending=False)
        df_8 = df_8.head(10000)
        return df_8
    @render.data_frame
    def df_8():
        return render.DataGrid(
        filter_8(),
        width="100%",
        height="250px" 
        )

    def filter_7(): #3table#
        #df_7 = pd.DataFrame(df)
        df_7 = df_10[["VendorName","ContractPrice"]]
        df_7 = pd.DataFrame(df_7)
        amount = df_7.groupby('VendorName')['ContractPrice'].sum()
        df_7['Vendor_amount'] = df_7['VendorName'].map(amount)
        df_7 = df_7[["VendorName","Vendor_amount"]]
        df_7 = df_7.drop_duplicates(subset=['Vendor_amount'])
        return df_7.sort_values(by='Vendor_amount', ascending=False)
    @render.data_frame
    def df_7():
        return render.DataGrid(
        filter_7(),
        width="100%",
        height="250px" 
        )

app = App(app_ui, server)

#df.loc[['ProcessNumber', 'ContractingInstitutionName']]
#df.loc[df['NumberOfOffers'] == 1 ]
#df.loc[(df['NumberOfOffers'] == 1 ) & (df.ProcessNumber[-1:-4] == 2022)]
