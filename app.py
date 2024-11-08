import pandas as pd
import numpy as np
import io
import seaborn as sns
import shinyswatch
import matplotlib.pyplot as plt
from shiny.types import ImgData
from shiny import App, render, ui, reactive, req, ui

#NOTE: To improve efficency, this part of the code could be run in a separate script 
# and the resulting dataframe saved as a csv file.
# That csv could be uploaded to AWS and read directly via read.csv
# This would save time and resources as the data would not have to be read and processed 
# each time the app is run.

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

#df.to_csv('Contracts_decoded.csv', encoding='utf-8', sep = ';')
df = pd.read_csv(io.StringIO(decoded_data), sep=';')

#TODO; to optimize code get rid of these copies of df. do filtering where applicable.
df_111 = df[df['NumberOfOffers'] == 1]
df_10 = df[["ProcessNumber","ContractingInstitutionName", "Subject",
                "ContractDate" , "ContractNumber" , "VendorName" , 
                "ContractPrice"]]

df_filtered = df[["ProcessNumber","ContractingInstitutionName",
                   "Subject","ContractDate","ContractNumber",
                   "VendorName","ContractPrice"]]

# creating a dict to use for drop-down box 
dict_institution = {k: k for k in df["ContractingInstitutionName"].unique()}

# creating dict for drop-down VendorName
dict_vendor = {k: k for k in df["VendorName"].unique()}

# List of columns to exclude
exclude_cols = ['ProcessNumber','Subject','ProcurementName',
                'ProcedureName','OfferTypeName','UseElectronicTools',
                'ContractDate','ContractNumber','NumberOfOffers',
                'VendorName','EstimatedPrice','ContarctPriceWithoutVat',
                'Vat','ContractPrice']

# creating dict for drop-down checkbox_columns
formatted_data = {item: item for item in df.columns if item not in exclude_cols}


# UI
app_ui = ui.page_navbar(
    shinyswatch.theme.lumen(),
# 1TAB preview
    ui.nav_panel(
    ui.output_image("image", height = "60%"),
        ui.row(
            ui.output_image("image2"),
            style="text-align: center;",
        ),
        ui.row(
        ui.card(  
            ui.card_header("ИЗВОР НА ПОДАТОЦИТЕ"),
            ui.p("Податоците во оваа апликација се превземени од Електронскиот систем за јавни набавки - " +
                 "ЕСЈН во делот на склучени договори објавени во системот во период 01.01.2021 до 30.06.2024"),
            ),
        ui.card(
            ui.card_header("СТАТИСТИЧКИ ПОДАТОЦИ"),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Вкупен број на Јавни Набавки"),
                ui.p(str(df['ProcessNumber'].nunique()), 
                     style="color:red; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    ui.card_header("Вкупен број на СУБЈЕКТИ"),
                ui.p(str(df['Subject'].nunique()), 
                     style="background-color:darkgoldenrod; text-align: center; font-size:400%"),
                    ),
                ui.card(
                    ui.card_header("Вкупен број на носители на набавки/добавувачи"),
                    ui.p(str(df['VendorName'].nunique()),
                         style="text-align: center; font-size:400%",
                         class_="btn-primary"),
                    ),
                ),
            ),
        ),
        ui.layout_columns(  
        ui.card(  
            ui.card_header("ИНОВАТИВНА ЛАБОРАТОРИЈА"),
            ui.p("Овој проект е реализиран според Меморандумот за соработка меѓу Канцеларијата" +
                 "на Главниот ревизор на Норвешка и Државниот завод за ревизија"),
            ),
        ui.card(
            ui.card_header("INNOVATIVE LABORATORY"),
            ui.p("This project is acomplished according Memorandum of cooperation between the" +
                 "Office of the Auditor General of Norway and the State Audit Office"),
            ),
        ),
    ),
# 2TAB preview
    ui.nav_panel(
        "Склучени договори",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image3", height="50%"),
        ui.row(
            ui.column(6,
            ui.tooltip(    
                ui.input_selectize(
                "selectize", 
                "Одбери СУБЈЕКТ:",
                dict_institution,
                multiple=False,
                width="600px"
                ),
            "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
             ),
            ui.output_text("company"),
            ),
            ui.column(6,
            ui.input_date_range("daterange",
                                " ПЕРИОД:",
                                start="2020-01-01" ,
                                width="450px"),
            ),
            ui.input_checkbox_group(  
                "checkbox_columns",  
                "ОТСТРАНЕТЕ ГИ КОЛОНИТЕ КОИ НЕ СЕ РЕЛЕВАНТНИ ЗА ВАШЕТО ПОЛЕ НА ИНТЕРЕС СО СЕЛЕКТИРАЊЕ НА" +
                 "КВАДРАТЧЕТО ПОКРАЈ НАЗИВОТ НА КОЛОНАТА:",  
                formatted_data,
                inline = True,
                width = "100%"
                ),
        ),
        ui.row(
            ui.column(3),
            ui.column(8,
            ui.download_button("downloadData",
                                "Преземи податоци за ОБРАЗЕЦ ЈНПР и ЈНПП",
                                width="800px",
                                class_="btn-primary")),
        ),
        ui.output_data_frame("df_filter_1"),
    ),
# 3TAB preview
    ui.nav_panel(
        "Преглед на набавки",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image4", height="50%"),    
            ui.row(
                ui.column(6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for_plot",
                    "Одбери СУБЈЕКТ:",
                    dict_institution,
                    multiple=False, 
                    width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),),
                ui.column(6,
                ui.input_numeric("numeric", "Внеси ја максималната вредност на ЈН",
                                  10000000,
                                  min = 300000,
                                  max = 1000000000,
                                  width = "500px"), 
                ui.output_text_verbatim("value_n"),
                ),
            ),
        ui.input_slider("slider",
                        "Одбери опсег на вредностa на јавните набавки!",
                        min = 0,
                        max = 20000000,
                        value = [35, 1000000],
                        width = '100%'), 
        ui.output_text("slide_value"),
        ui.output_plot("plot",
                       height = '400px',
                       fill = False),
        ui.tags.h5("Подредена табела по вредност на јавните набавки"), 
        ui.output_data_frame("df_2"),
    ),
# 4TAB preview
    ui.nav_panel(
        "Податоци по носител на набавка",
        ui.h2({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 80px;"}, ""),
        ui.output_image("image5", height="50%"), 
            ui.row(
                ui.column(6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for",
                    "Одбери НОСИТЕЛ на набавка", 
                     dict_vendor,
                     selected = None,
                     multiple = False,
                     width = "600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),),
                ui.column(6,
                          ui.input_date_range("daterange1",
                                              "ПЕРИОД:",
                                              start = "2020-01-01" ,
                                              width = "450px"),
                ),
            ),
        ui.row(
        ui.column(3),
        ui.column(8,
                  ui.download_button("downloadData1",
                                     "Преземи податоци",
                                     width="800px",
                                     class_="btn-primary")),
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
        ui.column(6,
                ui.tooltip(
                    ui.input_selectize(
                    "selectize_for1",
                    "Одбери СУБЈЕКТ:", 
                    dict_institution,
                    selected=None,
                    multiple=False,
                    width="600px"
                    ),
                "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
                ),),
                ui.column(6,
                ui.tags.h4({"style": "text-align: center;background-color:darkgoldenrod; margin-top: 35px;"},""),
                ui.tags.h4({"style": "background-color:Goldenrod; color:white;"},"Од " + str(len(df)) +
                            " јавни набавки, " + str(len(df_111)) + " се со само 1 понуда."),
                    ),
            ),
        ui.output_plot("plot1",
                       height = '400px',
                       fill = False),     
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
                    dict_vendor,
                    selected = None,
                    multiple = False,
                    width = "600px"
            ),
            "Кликнете, избришете го постоечкиот избор и потоа одберете или внесете го субјектот",
            ),
        ui.column(12,
                   ui.output_text("txt"),
                   style="color:red; font-size:180%",
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
    ),
# 8TAB preview
    ui.nav_panel(
        "СТАТИСТИКА",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image8", height="50%"),
        ui.h3({"style": "text-align: center;background-color:powderblue;"},
              "Подредена листа на ДОБАВУВАЧИ по број на добиени набавки! "),
        ui.output_data_frame("df_9"),
        ui.h3({"style": "text-align: center;background-color:powderblue;"},
              "Топ 10.000 најголеми набавки по вредност по ДОБАВУВАЧ ! "),
        ui.output_data_frame("df_8"),
        ui.h3({"style": "text-align: center;background-color:powderblue;"},
              "Подредена листа на ДОБАВУВАЧИ по вкупно добиени пари!"),
        ui.output_data_frame("df_7"),
    ),
# 9TAB preview
    ui.nav_panel(
        "УПАТСТВО",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, ""),
        ui.output_image("image9", height="50%"),
    #TODO; this text could be put in a seperate file and sourced
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
    )),
    position = ("fixed-top"),
    bg = "#d1dae3",
)

# Define a generic filtering function
def filter_df(df,
              institution_name = None,
              vendor_name = None,
              date_range = None,
              min_amount = None,
              max_amount = None,
              group_by = None,
              top_n = None,
              columns = None,
              convert_to_int = False):
    if institution_name:
        df = df[df['ContractingInstitutionName'] == institution_name]
    if vendor_name:
        df = df[df['VendorName'] == vendor_name]
    if date_range:
        start_date, end_date = date_range
        df.loc[:, "ContractDate"] = pd.to_datetime(df["ContractDate"]).dt.date
        mask = (df["ContractDate"] >= start_date) & (df["ContractDate"] <= end_date)
        df = df[mask]
        df.loc[:, "ContractDate"] = pd.to_datetime(df["ContractDate"]).dt.strftime("%Y-%m-%d")
    if min_amount is not None and max_amount is not None:
        df = df[df["ContractPrice"].between(min_amount, max_amount)]
    if group_by:
        df = df.groupby(group_by)['ContractPrice'].sum().reset_index()
    if top_n:
        df = df.sort_values(by='ContractPrice', ascending=False).head(top_n)
    if columns:
        df = df[columns]
    if convert_to_int:
        df['ContractPrice'] = df['ContractPrice'].astype(float).astype(int)
    return df

def server(input, output, session):

    # Image rendering functions
    def render_image(image_name, width="100%"):
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / image_name), "width": width}
        return img

    @render.image
    def image():
        return render_image("logo.png", "80px")
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
    
    @render.text
    def value_n():
        dali = input.numeric()
        ui.update_slider("slider",
                         min = 0,
                         max = dali,
                         value = [35, 1000000])
    @reactive.Calc
    def filter():
        return filter_df(
            df,
            institution_name=input.selectize(),
            date_range=input.daterange(),
            columns=[col for col in df.columns if col not in input.checkbox_columns()],
            convert_to_int=True
        ).sort_values(by='ContractPrice', ascending=False)
        

    #note; this applies all filters defined in filter() and saves the result in df_1
    @output
    @render.data_frame
    def df_filter_1():
        return render.DataGrid(
            filter()
        )
    
    @reactive.Calc
    def export():
        df_export = filter()
        # Insert empty columns
        #TODO; Try using .loc[row_indexer,col_indexer] = value instead
        df_export['IzvorNaSredstva'] = 'NULL'  
        df_export['A'] = ''
        df_export['ID'] = range(1, len(df_export) + 1) 

        # List of columns in the desired order
        df_export = df_export[['ID','A','A','A','A','EstimatedPrice', 'A', 'OfferTypeName',
                               'UseElectronicTools','ProcedureName','Subject','ContractNumber',
                               'ContractDate','ProcurementName','VendorName']] #,'ContractPriceWithoutVat'
        return df_export
    
    @reactive.Calc
    def export1():
        df_export1 = filter_3()
        return df_export1
    
    @render.download(
        filename=lambda: f"JN_SUBJEKT.xlsx")
    def downloadData():
        df = export()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine = 'xlsxwriter') as writer:
            df.to_excel(writer, index = False, sheet_name = 'Sheet1')
        output.seek(0)
        return output.read(), "export.xlsx"
          
    @render.download(
        filename=lambda: f"JN_NOSITEL.xlsx")
    def downloadData1():
        df = export1()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine = 'xlsxwriter') as writer:
            df.to_excel(writer, index = False, sheet_name = 'Sheet1')
        output.seek(0)
        return output.read(), "export.xlsx"

    ### plots ###
    @reactive.Calc
    def filter_for_plot():
        filtered_for_plot = filter_df(
            df,
            institution_name=input.selectize_for_plot()
        )
        min_amount = input.slider()[0]
        max_amount = input.slider()[1]
        filtered_for_plot = filtered_for_plot[filtered_for_plot["ContractPrice"].between(min_amount, max_amount)]
        return filtered_for_plot.sort_values(by='ContractPrice', ascending=False)

    @render.plot(alt="Histogram")  
    def plot():  
        df = filter_for_plot()
        data=df['ContractPrice']
        fig, ax = plt.subplots()
        num_bins = 50
        ax.hist(x = data, bins = 20, linewidth = 0.5, edgecolor = "white")
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
        return filter_df(
        df,
        vendor_name=input.selectize_for(),
        date_range=input.daterange1(),
        columns=["ProcessNumber", "ContractingInstitutionName", "Subject", "ProcurementName",
                 "AgreementStartDate", "AgreementEndDate", "ContractDate", "ContractNumber",
                 "NumberOfOffers", "VendorName", "ContractPrice"],
                 convert_to_int = True
                 ).sort_values(by='ContractPrice', ascending = False)
    
    @render.plot(alt = "Histogram")  
    def plot1():
        df = filter_5_hist()
        ax = sns.histplot(data = df, x = 'ContractDate')
        ax.set_xlabel("Дата на договор")
        ax.set_ylabel("Број на набавки со 1 понуда")
        return ax

    @reactive.Calc
    def filter_5():
        return filter_df(
        df_111,
        institution_name=input.selectize_for1(),
        columns=["ProcessNumber", "ContractingInstitutionName", "Subject", "ProcurementName",
                 "AgreementStartDate", "AgreementEndDate", "ContractDate", "ContractNumber",
                 "NumberOfOffers", "VendorName", "ContractPrice"],
        convert_to_int = False).sort_values(by = 'ContractPrice', ascending = False)

    def filter_5_hist():
        df_5t = filter_df(
            df_111,
            institution_name=input.selectize_for1(),
            columns=["ProcessNumber", "ContractingInstitutionName", "Subject", "ProcurementName",
                     "AgreementStartDate", "AgreementEndDate", "ContractDate", "ContractNumber",
                     "NumberOfOffers", "VendorName", "ContractPrice"],
        ).sort_values(by='ContractPrice', ascending=True)
        df_5t['ContractDate'] = pd.to_datetime(df_5t['ContractDate'], format='%Y-%m-%d')
        df_5t['ContractDate'] = df_5t['ContractDate'].dt.strftime('%Y')
        return df_5t

    @reactive.Calc
    def filter_6():
        return filter_df(
        df_111,
        vendor_name=input.selectize_for11(),
        columns=["ProcessNumber", "ContractingInstitutionName", "Subject", "ProcurementName",
                 "AgreementStartDate", "AgreementEndDate", "ContractDate", "ContractNumber",
                 "NumberOfOffers", "VendorName", "ContractPrice"],
        convert_to_int=False).sort_values(by='ContractPrice', ascending=False)

    @reactive.Calc
    def filter_8():
        return filter_df(
        df,
        group_by = 'VendorName',
        top_n = 10000,
        convert_to_int = True)[["VendorName", "ContractPrice"]]
    
    def filter_7():
        df_7 = filter_df(df, group_by='VendorName', convert_to_int=True)
        df_7['Vendor_amount'] = df_7['ContractPrice']
        return df_7[["VendorName", "Vendor_amount"]].drop_duplicates(subset=['Vendor_amount']).sort_values(by='Vendor_amount', ascending=False)
    
    def filter_9():
        df_9 = df[["VendorName"]]
        counts = df_9['VendorName'].value_counts()
        df_9['VendorName_counts'] = df_9['VendorName'].map(counts)
        return df_9.drop_duplicates(subset=['VendorName']).sort_values(by='VendorName_counts', ascending=False)
       
    @output
    @render.data_frame
    def df_3():
        return render.DataGrid(filter_3())
    
    @render.data_frame
    def df_5():
        return render.DataGrid(filter_5())
    
    @render.data_frame
    def df_6():
        return render.DataGrid(filter_6())
    
    @render.data_frame
    def df_8():
        return render.DataGrid(filter_8(), width = "100%", height = "250px")
    
    @render.data_frame
    def df_7():
        return render.DataGrid(filter_7(), width = "100%", height = "250px")

    @render.data_frame
    def df_9():
        return render.DataGrid(filter_9(), width = "100%", height = "250px")
    
    @render.data_frame
    def df_filter():
        return render.DataTable(
            df_filtered,
            selection_mode = 'rows',
            width = "100%",
           filters = True,
        )

app = App(app_ui, server)