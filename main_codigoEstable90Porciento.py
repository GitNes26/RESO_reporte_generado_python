from collections import defaultdict
from tkinter import *

from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

import csv
import openpyxl
import pandas
from Classes.Computation import Mean

from Classes.Register import Register as Register
from Classes.Table import AddTablesGroupbyBredReasFilterLact, AddTablesGroupbyEvSireStudCdFilterLact, AddTablesGroupbyLactFilterEv, AddTablesGroupbySireBullFilterLact, AddTablesGroupbyTechFilterLact, DataRegisterT
from ConvertPDF.PDF import PDF as PDF

# filename = NULL
wb = openpyxl.Workbook()
data_sheet = wb.active
data_sheet.title = "data"


class Data:
   listRegister = []
   listRegister_LACT = []
   filename_selected = ""
   filename_selected_with_ext = ""
   path_file = ""
   
   
   def __init__ (self,window):
      pdf = PDF()
      
      def SelectFile():
         filetypes = (
            ('text files', '*.csv'),
            # ('All files', '*.*')
         )

         filename = fd.askopenfilename(
            title='Open a file',
            initialdir='C:/Users/nesto/OneDrive/Escritorio/RESO_SISTEMAS/ProyectoPython/Documents',
            filetypes=filetypes
         )
         self.filename_selected_with_ext = filename.split('/')[-1]
         self.filename_selected = self.filename_selected_with_ext.split('.')[0]
         self.path_file = filename.replace(self.filename_selected_with_ext,'')
         print(self.path_file)
         print(f'ruta: {self.path_file} | filename_selected sin ext: {self.filename_selected} y filename_selected con ext: {self.filename_selected_with_ext}')
         

         if len(filename) > 0:
            # self.file(text=filename)
            
            with open(filename) as csvfile:
               reader = csv.DictReader(csvfile)
               for column in reader:
                  if len(column['# Preg']) < 1:
                     break
                  
                  register = Register()
                  register.NoPreg = bool(True if int(column['# Preg']) > 0 else False)
                  register.AbortRes = bool(True if int(column['AbortRes']) > 0 else False)
                  register.SireBull = column['SireBull']
                  register.LACT = int(column['LACT'])
                  register.Ev_L = int(column['Ev#L'])
                  register.NoEv = int(column['#Ev'])
                  register.Date = column['Date']
                  register.EvGap = column['EvGap']
                  register.Tech = column['Tech']
                  register.Pen = column['Pen']
                  register.bred_sexed = column['bred.sexed']
                  register.BredReas = column['BredReas']
                  register.DIM_E = column['DIM@E']
                  register.AnId = column['AnId']
                  register.FarmLoc = column['FarmLoc']
                  register.AnOwner = column['AnOwner']
                  register.BRD = column['BRD']
                  register.Age_da = column['Age(da)']
                  register.Other2ID = column['Other2ID']
                  register.Other5ID = column['Other5ID']
                  register.ConceptRate = column['ConceptRate']
                  register.BredUnk = column['BredUnk']
                  register.EvSireBreed = column['EvSireBreed']
                  register.EvSireStudCd = column['EvSireStudCd']
                  register.evWeek = column['evWeek']
                  register.Age1BLT = column['Age1BLT']
                  register.Total = column['Total']
                     
                  self.listRegister.append(register)

            # Instantiation of inherited class
            pdf.alias_nb_pages()
            pdf.add_page()
            GroupBy()
            pdf.output(f'{self.path_file}{self.filename_selected}.pdf', 'F')
            
            showinfo(
               title='SUCCESS',
               message='Reporte creado'
            )
            
      
            
      
      
      def GroupBy():
         print('AgruparPorLactancia():')
         ev_list = []
         lact_list = []
         bredReas_list = []
         sireBull_list = []
         evSireStudCd_list = []
         tech_list = []
         
         registers_groupedby_lact = defaultdict(list)          #LACT
         registers_groupedby_bredReas = defaultdict(list)      #BredReas
         registers_groupedby_sireBull = defaultdict(list)      #SireBull
         registers_groupedby_evSireStudCd = defaultdict(list)  #EvSireStudCd
         registers_groupedby_tech = defaultdict(list)          #Tech
         
         for item in self.listRegister:
            dataRegisterT = DataRegisterT()
            dataRegisterT.Preg = item.NoPreg
            dataRegisterT.Abort = item.AbortRes
            dataRegisterT.Lact = item.LACT
            dataRegisterT.Ev_L = item.Ev_L
            dataRegisterT.NoEv = item.NoEv
            
            registers_groupedby_lact[item.LACT, item.NoEv].append(dataRegisterT)
            registers_groupedby_bredReas[item.BredReas, item.LACT].append(dataRegisterT)
            registers_groupedby_sireBull[item.SireBull, item.LACT].append(dataRegisterT)
            registers_groupedby_evSireStudCd[item.EvSireStudCd, item.LACT].append(dataRegisterT)
            registers_groupedby_tech[ item.Tech, item.LACT].append(dataRegisterT)
            
            ev_list.append(item.NoEv)
            lact_list.append(item.LACT)
            bredReas_list.append(item.BredReas)
            sireBull_list.append(item.SireBull)
            evSireStudCd_list.append(item.EvSireStudCd)
            tech_list.append(item.Tech)
            
         ev_list = pandas.unique(ev_list).tolist()
         ev_list.sort()
         lact_list = pandas.unique(lact_list).tolist()
         lact_list.sort()
         bredReas_list = pandas.unique(bredReas_list).tolist()
         bredReas_list.sort()
         sireBull_list = pandas.unique(sireBull_list).tolist()
         sireBull_list.sort()
         evSireStudCd_list = pandas.unique(evSireStudCd_list).tolist()
         evSireStudCd_list.sort()
         tech_list = pandas.unique(tech_list).tolist()
         tech_list.sort()
         
         tables = AddTablesGroupbyLactFilterEv(registers_groupedby_lact, lact_list, ev_list)
         GeneratePDF(tables)
         tables = AddTablesGroupbyBredReasFilterLact(registers_groupedby_bredReas, bredReas_list, lact_list)
         GeneratePDF(tables)
         tables = AddTablesGroupbySireBullFilterLact(registers_groupedby_sireBull, sireBull_list, lact_list)
         GeneratePDF(tables)
         tables = AddTablesGroupbyEvSireStudCdFilterLact(registers_groupedby_evSireStudCd, evSireStudCd_list, lact_list)
         GeneratePDF(tables)
         tables = AddTablesGroupbyTechFilterLact(registers_groupedby_tech, tech_list, lact_list)
         GeneratePDF(tables)
                           
      
      def GeneratePDF(tables):
         for table in tables:          
            pdf.TableHeader(table.TitleTable)
            pdf.TitleColumn(table.Column1Name,40,'R')
            pdf.TitleColumn(table.Column2Name,40,'R')
            pdf.TitleColumn(table.Column3Name,40,'R')
            pdf.TitleColumn(table.Column4Name,40,'R')
            pdf.LastTitleColumn(table.Column5Name,0,'')
            for register in table.Registers:
               pdf.Column(f"{register.EtiquetaDeFila}",40,'R')
               pdf.Column(f"{register.PromedioPreg}%",40,'R')
               pdf.Column(f"{register.SumaPreg}",40,'R')
               pdf.Column(f"{register.PromedioAbortRes}%",40,'R')
               pdf.LastColumn(f"{register.CuentaPreg2}",0,'')
            pdf.FooterColumn('TOTALES',40,'R')
            pdf.FooterColumn(0,40,'R')
            pdf.FooterColumn(0,40,'R')
            pdf.FooterColumn(0,40,'R')
            pdf.LastFooterColumn(0,0,'')
            pdf.ln(10)
         
         
      self.window = window
      self.window.title("Interfaz para reportes")
      self.window.geometry('300x200')
      # self.window.resizable(False,False)

      # Creando contendeor frame
      frame = LabelFrame(self.window, text="Select file csv")
      frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=W+E) #posicionando el label

      #Creando un intput
      Label(frame, text="File path: ").grid(row=1, column=0)
      self.file = Entry(frame).grid(row=1, column=1)

      # button openFile
      ttk.Button(frame, text='Open a File', command=SelectFile).grid(row=1, column=2, sticky=W+E)
      
      

if __name__ == '__main__':
   window = Tk() #instanciando nuestra interfaz
   application = Data(window)

   window.mainloop()