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

with open("/workspaces/InnovativeLab/Contracts.csv", 'rb') as f:
    bom = f.read(2)

if bom == b'\xff\xfe':
    print('File is encoded as UTF-16-LE')
elif bom == b'\xfe\xff':
    print('File is encoded as UTF-16-BE')
else:
    print('File does not have a BOM, so the version of UTF-16 is unknown')

with open("/workspaces/InnovativeLab/Contracts.csv", 'rb') as f:
    data = f.read()
    decoded_data = data.decode('utf-16-le', errors='ignore')

df = pd.read_csv(io.StringIO(decoded_data), sep=';')


#df['ContractPrice '] = df['ContractPrice'].astype(float).astype(int)
#df['ContractPrice'] = df['ContractPrice'].astype(str).replace('\.\d+', '', regex=True).astype(int)

df_11 = df.copy()
df_111 = df_11[df_11['NumberOfOffers'] == 1]
df_10 = df.copy()
df_10 = df_10[["ProcessNumber","ContractingInstitutionName", "Subject", "ContractDate" , "ContractNumber" , "VendorName" , "ContractPrice"]]

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

#PREVIEW
app_ui = ui.page_navbar(
    shinyswatch.theme.lumen(),

    ui.nav_panel(
    ui.output_image("image", height = "60%"),
    ui.tags.h2("ДОБРОДОЈДОВТЕ! / WELCOME!", align = "center", style="background-color:powderblue; margin-top: 80px;"), 
        ui.row(
        #ui.output_image("image1", width="50%", height="100px"),
        ui.output_image("image2"), style="text-align: center;",
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
    ui.nav_panel(
        "Дата за експорт/СУБЈЕКТ",
        ui.h2({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Експортирање податоци за субјект! / Export data for the subject!"),
        ui.row(
            ui.column(
            6,        
            ui.input_selectize(
                "selectize", 
                "Одбери ИНСТИТУЦИЈА / Select INSTITUTION:",
                my_dict,
                multiple=False,
                width="600px"
                ),
            ui.output_text("company"),
            ),
            ui.column(
            6,
            ui.input_date_range("daterange", " Одберете го периодот / Select the period:", start="2020-01-01" , width="450px"),
            ),
        ),
        ui.row(
            ui.column(3),
            ui.column(8, ui.download_button("downloadData", "DOWNLOAD", width="800px", class_="btn-primary")),
        ),
        ui.tags.h2({"style":" margin-top: 20px;"}, ), 
        ui.output_data_frame("df_1"),

    ),
    ui.nav_panel(
        "Визуелизација/СУБЈЕКТ",
        ui.h2({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Визуелизација на набавките по СУБЈЕКТ! / Visualization of procurement SUBJECT!"),
            ui.row(
                ui.column(
                6,
                    ui.input_selectize(
                    "selectize_for_plot",
                    "Одбери ИНСТИТУЦИЈА / Select INSTITUTION:",
                    my_dict, multiple=False, 
                    width="600px"
                    ),
                ),
        #ui.output_text('company1'),
                ui.column(
                6,
                ui.input_numeric("numeric", "Максимален износ на договор / Max amount of Contract Value", 10000000, min=300000, max=1000000000, width="500px"), 
                ui.output_text_verbatim("value_n"),
                ),
            ),

        ui.input_slider("slider", "Одбери ранг на вредностa на јавните набавки /Select a value ranking for public procurement !", min=0, max=20000000, value=[35, 1000000], width='100%'), 
        ui.output_text("slide_value"),
        ui.output_plot("plot", height='400px', fill=False),
        ui.tags.h5("Подредена табела по вредност на јавните набавки / Arranged table by value of public procurement"), 
        ui.output_data_frame("df_2"),
    ),
    ui.nav_panel(
        "Дата/ДОБАВУВАЧ",
        ui.h2({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Анализа на податоци по ДОБАВУВАЧ / CONTRACTOR data analysis"),
            ui.row(
                ui.column(
                6,
                    ui.input_selectize(
                    "selectize_for",
                    "Одбери ДОБАВУВАЧ / Select CONTRACTOR:", 
                     my_dict1,
                     selected=None,
                     multiple=False,
                     width="600px"
                    ),
                ),
                #ui.output_text('subject'),
                ui.column(
                6,
                    ui.input_date_range("daterange1", "Одберете го периодот / Select the period:", start="2020-01-01" , width="450px"), 
                    #ui.output_data_frame("df_1"),
                ),
            ),
        ui.tags.h5("Подредена табела по вредност на јавните набавки / Arranged table by value of public procurement:"), 
        ui.output_data_frame("df_3"),
    ),
    ui.nav_panel(
        "1понуда/СУБЈЕКТ",
        ui.h2({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Набавки за ИНСТИТУЦИЈА со само 1 понуда! / Procurement for INSTITUTION with only 1 offer!"),
        ui.row(
                ui.column(
                6,
                ui.input_selectize(
                    "selectize_for1",
                    "Одбери ИНСТИТУЦИЈА / Select INSTITUTION:", 
                    my_dict,
                    selected=None,
                    multiple=False,
                    width="600px"
                    ),
                ),
                ui.column(
                6,
                ui.tags.h4({"style": "background-color:Gainsboro;"},"Од " + str(len(df)) + " јавни набавки, " + str(len(df_111)) + " се со само 1 понуда."),
                ui.tags.h4({"style": "background-color:Gainsboro;"}, " From " + str(len(df)) + " public procurements, " + str(len(df_111)) + " is with only 1 offer."),
                ),
        ),
        ui.output_plot("plot1", height='400px', fill=False),     
        ui.tags.h5("Подредена табела по вредност на јавните набавки / Arranged table by value of public procurement:"), 
        ui.output_data_frame("df_5"),
    ),
    ui.nav_panel(
        "1понуда/ДОБАВУВАЧ",
        ui.h2({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Набавки од ДОБАВУВАЧ со само 1 понуда! / Contractor procurement with only 1 offer!"),
                    ui.input_selectize(
                    "selectize_for11",
                    "Одбери ДОБАВУВАЧ / Select CONTRACTOR:", 
                    my_dict1,
                    selected=None,
                    multiple=False,
                    width="600px"
                    ),
        ui.column (12,
        ui.output_text_verbatim("txt"),
        align="center"),
        ui.tags.h5("Подредена табела по вредност на јавните набавки / Arranged table by value of public procurement:"), 
        ui.output_data_frame("df_6"),
    ),
        ui.nav_panel(
        "ТОПлиста/ВРЕДНОСТ",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Топ 10.000 најголеми набавки по вредност! / Top 10,000 largest procurements by value! "),
        ui.output_data_frame("df_8"),
    ),
    ui.nav_panel(
        "ТОПлиста/Бр.на ДОГОВОРИ",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Подредена листа по број на добиени набавки! / Arranged list by number of procurements received!"),
        ui.output_data_frame("df_9"),
    ),
        ui.nav_panel(
        "ФИЛТЕР",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Филтрирање на податоци / Data filtering"),
        ui.output_data_frame("df_f"),
        ui.output_text_verbatim("txt1"),
    ),
        ui.nav_panel(
        "ТОПлиста/Вкупно пари",
        ui.h3({"style": "text-align: center;background-color:powderblue; margin-top: 80px;"}, "Подредена листа по вкупно добиени пари! / Arranged list by amount of money of procurements received!"),
        ui.output_data_frame("df_7"),
    ),
    position = ("fixed-top"),
    bg = "#d1dae3",
    #fluid = True
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
        img: ImgData = {"src": str(dir / "dzrA.png"), "width": "100%"}
        return img
    
    @render.image
    def image3():
        from pathlib import Path
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "aaa.png"), "width": "400px",}
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
        #return input.numeric()
        dali = input.numeric()
        ui.update_slider("slider", min=0, max=dali, value=[35, 1000000])
        #return ui.update_slider("slider", "Одбери ранг на вредностa на јавните набавки / Ranking of the value of public procurement:", min=0, max=dali, value=[35, 1000000])

    @render.text
    def value():
        return  f"{input.daterange()[0]} to {input.daterange()[1]}"

    @render.text
    def value1():
        return  f"{input.daterange1()[0]} to {input.daterange1()[1]}"
    
    @render.text
    def txt():
        return f"Од вкупно: {len(df[df['VendorName'] == input.selectize_for11()])} јавни набавка/и, има {len(df_111[df_111['VendorName'] == input.selectize_for11()])} со само 1 понуда/и.     From all: {len(df[df['VendorName'] == input.selectize_for11()])} public procurements, there are {len(df_111[df_111['VendorName'] == input.selectize_for11()])} with only 1 offer. "
    
#filter().dtypes

    @reactive.Calc
    def filter():
        # filter 1
        df_1 = df[df['ContractingInstitutionName'] == input.selectize()]
        #df_1 = df.copy()
        # filter 2
        # TO DO: include more logic checks on dates (e.g. duration should be included)
        start_date = input.daterange()[0]
        end_date = input.daterange()[1]
        df_1 = pd.DataFrame(df_1)
        df_1["ContractDate"] = pd.to_datetime(df_1["ContractDate"]).dt.date 
        mask = (df_1["ContractDate"] >= start_date) & (df_1["ContractDate"] <= end_date)
        filtered_df = df_1[mask]
        filtered_df = pd.DataFrame(filtered_df)
        filtered_df["ContractDate"] = pd.to_datetime(filtered_df["ContractDate"]).dt.strftime("%Y-%m-%d")

        # remmoving decimal places and remove decimal point
        filtered_df['ContractPrice'].astype(float).astype(int)
        filtered_df.ContractPrice = filtered_df.ContractPrice.apply(int)
        #filtered_df.loc[:, "ContractPrice"] = filtered_df["ContractPrice"].map('{:,}'.format)
        return filtered_df
    
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

        #df_export = df_export.encode(encoding = 'UTF-8', errors = 'strict')
        #df_export.sort_values(by='ContractPrice')
        return df_export

    
    #@session.download(
    @render.download(
        filename=lambda: f"ZaObrazec_JN_new.csv")
    def downloadData():
        df = export()
        yield df.to_csv(sep= ';', encoding= 'UTF-8') #df.to_string(index=False)
          

    ### plots ###

    @reactive.Calc
    def filter_for_plot():
        # filter 1
        filtered_for_plot = df[df['ContractingInstitutionName'] == input.selectize_for_plot()]
        # filter 2
        min_amount = input.slider()[0]
        max_amount = input.slider()[1]
        filtered_for_plot = pd.DataFrame(filtered_for_plot) 
        #filtered_for_plot['ContractPrice'] = filtered_for_plot['ContractPrice'].astype(int)
        filtered_for_plot = filtered_for_plot[filtered_for_plot["ContractPrice"].between(min_amount, max_amount)]
        #>= min_amount) & (filtered_for_plot["ContractDate"] <= max_amount]
        #filtered_for_plot= filtered_for_plot[mask]
        #filtered_df = pd.DataFrame(filtered_df)
        return filtered_for_plot.sort_values(by='ContractPrice', ascending=False)
    
    # OLD PLOT changed for shinyserver, matplotlib instead seaborn
    #@render.plot(
    #alt="Histogram"
    #)  
    #def plot():  
    #    #option = (999)
    #    df = filter_for_plot()
    #    ax = sns.histplot(data=df, x='ContractPrice')
    #    ax.set_xlabel("Вредност на набавката / Contract Price")
    #    ax.set_ylabel("Број на набавки / Number of Contracts")
    #    return ax 

    @render.plot(
    alt="Histogram"
    )  
    def plot():  
        df = filter_for_plot()
        data=df['ContractPrice']
        fig, ax = plt.subplots()
        num_bins = 50
        ax.hist(x=data, bins=20, linewidth=0.5, edgecolor="white")

    @output
    @render.data_frame
    def df_2():
        return render.DataGrid(
            #df[df['ContractingInstitutionName'] == input.selectize()]
            filter_for_plot()
        )
    
    @reactive.Calc
    def filter_3():
        df_3 = df[df['VendorName'] == input.selectize_for()]
        # filter 2
        # TO DO: include more logic checks on dates (e.g. duration should be included)
        start_date = input.daterange1()[0]
        end_date = input.daterange1()[1]
        df_3 = pd.DataFrame(df_3)
        df_3["ContractDate"] = pd.to_datetime(df_3["ContractDate"]).dt.date 
        mask1 = (df_3["ContractDate"] >= start_date) & (df_3["ContractDate"] <= end_date)
        filtered_df3 = df_3[mask1]
        filtered_df3 = pd.DataFrame(filtered_df3)
        filtered_df3["ContractDate"] = pd.to_datetime(filtered_df3["ContractDate"]).dt.strftime("%Y-%m-%d")
        filtered_df3=filtered_df3[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        return filtered_df3.sort_values(by='ContractPrice', ascending=False)
    
    #@reactive.Calc
    #def filter_4():
        ##df_4 = df[df['NumberOfOffers'] == 1]
        #df_4 = df_111[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        #df_4=df_4[["ProcessNumber","ContractingInstitutionName","Subject","ProcurementName","AgreementStartDate","AgreementEndDate","ContractDate","ContractNumber","NumberOfOffers","VendorName","ContractPrice"]]
        #return df_4.sort_values(by='ContractPrice', ascending=False)
    
    @render.plot(
    alt="Histogram"
    )  
    def plot1():  
        #option = (999)
        df = filter_5t()
        ax = sns.histplot(data=df, x='ContractDate')
        ax.set_xlabel("Дата на договор / Contract Date")
        ax.set_ylabel("Број на набавки / Number of Contracts")
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
        #df_8.groupby(['ContractPrice']).sum()
        ##df_8 = df_8.drop_duplicates(subset=['VendorName'])
        ##return df_8.sort_values(by='VendorName_counts', ascending=False)
        return df_8
    
    def filter_7():
        #df_7 = pd.DataFrame(df)
        df_7 = df[["VendorName","ContractPrice"]]
        df_7 = pd.DataFrame(df_7)
        #df_7.groupby(["VendorName"], sort=False).sum()
        #df_7 = df_7.groupby('VendorName')['ContractPrice'].sum()
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
    
    #def filter_10():
        #df_10 = pd.DataFrame(df)
        #df_10 = df_10[["ContractingInstitutionName", "Subject", "ContractDate" , "ContractNumber" , "VendorName" , "ContractPrice"]]
        #return df_10
 

    @output
    @render.data_frame
    def df_3():
        return render.DataGrid(
        filter_3()
        )
    
    #@render.data_frame
    #def df_4():
    #    return render.DataGrid(
    #    filter_4()  
    #    )
    
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
        )
    
    @render.data_frame
    def df_7():
        return render.DataGrid(
        filter_7(),
        width="100%", 
        )

    @render.data_frame
    def df_9():
        return render.DataGrid(
        filter_9(),
        width="100%", 
        )
    
    @render.data_frame
    def df_f():
        return render.DataGrid(
            df_10,
            row_selection_mode='multiple',
            width="100%",
           filters=True,
        )


# Export the DataFrame to an Excel file
# df.to_excel('ZaObrazec_JN.xlsx', index=False)
# df.output_data_frame("ZaObrazec_JN.xlsx")
#@ render.data_frame
# return render.DataGrid(data)


app = App(app_ui, server)


#df.loc[['ProcessNumber', 'ContractingInstitutionName']]
#df.loc[df['NumberOfOffers'] == 1 ]
#df.loc[(df['NumberOfOffers'] == 1 ) & (df.ProcessNumber[-1:-4] == 2022)]