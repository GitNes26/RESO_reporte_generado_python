import json
import moment #pip install moment
import openpyxl #pip install openpyxl
import pandas #pip install pandas
from pymysql import NULL #pip install PyMySQL
from collections import defaultdict
import csv

from Classes.Register import Register as Register
from Classes.Table import *
from Classes.TableEmail import *
from ConvertPDF.PDF import PDF as PDF
from send_email import SendEmail

wb = openpyxl.Workbook()
data_sheet = wb.active
data_sheet.title = "data"


class CreateReport:  
   """Paramtetros:
   @path_file = ruta de origen del arcihvo csv (con extencion del arcihvo)
   @output_filename = nombre del arcihvo pdf a crear (sin extención de arcihvo)
   @output_path_file = ruta destino del arcihvo pdf (sin extención de archivo)

   SI EL PARAMETRO @output_path_file NO SE ESPECIFICA (NULL), EL ARCHIVO PDF SE CREARA EN LA MISMA RUTA QUE EL ARCIVHO ORIGEN CON EL NOMBRE ESPECIFICADO.
   """
         
   def __init__ (self, path_file, output_filename, output_path_file=NULL):
      
      self.pdf = PDF()
      self.pdf.set_left_margin(5)
      self.pdf.set_right_margin(5)
      self.listRegister = []
      
      # Registramos el historial de ejecuciones en el siguiente archivo .txt
      self.log_file = open("./log.txt", "a")
      fecha_ejecucion = moment.now().format("DD-MM-YYYY HH:mm:ss")
      self.log_file.write(f"Archivo ejecutado... {fecha_ejecucion}\n")
      print(f"Archivo ejecutado... {fecha_ejecucion}")
      file_type = path_file.split('.')[-1].upper()
      if file_type == 'CSV':
         self.GetDataCSV(path_file)
      elif file_type == 'JSON':
         self.GetDataJson(path_file)
         # self.GetDataCsvJson(path_file)
      self.Process(path_file, output_filename, output_path_file)

   def GetDataJson(self, path_file):
      """Obtengo los datos de un archivo JSON y los guardo en un objeto Registro"""
      with open(path_file, 'r') as dataJson:
         data = json.load(dataJson)
         for row in data:
            # print(row)
            register = Register()
            register.NoPreg = bool(False if row.get('=BredPreg') in (False,NULL,"",None) else True)
            register.AbortRes = bool(False if row.get('=if(BredAbort,1,0)') in (False,NULL,"",None) else True)
            register.SireBull = str('' if row.get('=evsireNAAB') in (NULL,None) else row.get('=evsireNAAB'))
            register.LACT = int(0 if row.get('=@date(LACT)') in ("",NULL,None) else row.get('=@date(LACT)'))
            # register.Ev_L = int(0 if row.get('Ev#L') in ("",NULL,None) else row.get('Ev#L'))
            register.NoEv = int(0 if row.get('=evnum') in ("",NULL,None) else row.get('=evnum'))
            # register.Date = str('' if row.get('Date') in (NULL,None) else row.get('Date'))
            # register.EvGap = str('' if row.get('EvGap') in (NULL,None) else row.get('EvGap'))
            register.Tech = str('' if row.get('Tech') in (NULL,None) else row.get('Tech'))
            # register.Pen = int(0 if row.get('Pen') in ("",NULL,None) else row.get('Pen'))
            # register.bred_sexed = str('' if row.get('bred.sexed') in (NULL,None) else row.get('bred.sexed'))
            register.BredReas = str('' if row.get('BredReas') in (NULL,None) else row.get('BredReas'))
            # register.DIM_E = int(0 if row.get('DIM@E') in ("",NULL,None) else row.get('DIM@E'))
            # register.AnId = int(0 if row.get('AnId') in ("",NULL,None) else row.get('AnId'))
            # register.FarmLoc = str('' if row.get('FarmLoc') in (NULL,None) else row.get('FarmLoc'))
            # register.AnOwner = str('' if row.get('AnOwner') in (NULL,None) else row.get('AnOwner'))
            # register.BRD = str('' if row.get('BRD') in (NULL,None) else row.get('BRD'))
            # register.Age_da = int(0 if row.get('Age(da)') in ("",NULL,None) else row.get('Age(da)'))
            # register.Other2ID = int(0 if row.get('Other2ID') in ("",NULL,None) else row.get('Other2ID'))
            # register.Other5ID = int(0 if row.get('Other5ID') in ("",NULL,None) else row.get('Other5ID'))
            register.ConceptRate = int(0 if row.get('ConceptRate') in ("",NULL,None) else row.get('ConceptRate'))
            register.BredUnk = bool(False if row.get('BredUnk') in (False,NULL,None,"",None) else True)
            register.EvSireBreed = str('' if row.get('EvSireBreed') in (NULL,None) else row.get('EvSireBreed'))
            register.EvSireStudCd = int(0 if row.get('EvSireStudCd') in ("",NULL,None) else row.get('EvSireStudCd'))
            # register.evWeek = str('' if row.get('evWeek') in (NULL,None) else row.get('evWeek'))
            # register.Age1BLT = int(0 if row.get('Age1BLT') in ("",NULL,None) else row.get('Age1BLT'))
            # register.Total = str('' if row.get('Total') in (NULL,None) else row.get('Total'))
               
            self.listRegister.append(register)
      pass

   def GetDataCsvJson(self, path_file):
      """Obtengo los datos de un archivo JSON que fue convertido desde un csv a json y los guardo en un objeto Registro"""
      with open(path_file, 'r') as dataJson:
         data = json.load(dataJson)
         for row in data:
            # print(row)
            register = Register()
            register.NoPreg = bool(True if int(row.get('# Preg')) > 0 else False)
            register.AbortRes = bool(True if int(row.get('AbortRes')) > 0 else False)
            register.SireBull = row.get('SireBull')
            register.LACT = int(0 if row.get('LACT') in ("",NULL,None) else row.get('LACT'))
            register.Ev_L = int(0 if row.get('Ev#L') in ("",NULL,None) else row.get('Ev#L'))
            register.NoEv = int(0 if row.get('#Ev') in ("",NULL,None) else row.get('#Ev'))
            register.Date = row.get('Date')
            register.EvGap = row.get('EvGap')
            register.Tech = row.get('Tech')
            register.Pen = int(0 if row.get('Pen') in ("",NULL,None) else row.get('Pen'))
            register.bred_sexed = row.get('bred.sexed')
            register.BredReas = row.get('BredReas')
            register.DIM_E = int(0 if row.get('DIM@E') in ("",NULL,None) else row.get('DIM@E'))
            register.AnId = int(0 if row.get('AnId') in ("",NULL,None) else row.get('AnId'))
            register.FarmLoc = row.get('FarmLoc')
            register.AnOwner = row.get('AnOwner')
            register.BRD = row.get('BRD')
            register.Age_da = int(0 if row.get('Age(da)') in ("",NULL,None) else row.get('Age(da)'))
            register.Other2ID = int(0 if row.get('Other2ID') in ("",NULL,None) else row.get('Other2ID'))
            register.Other5ID = int(0 if row.get('Other5ID') in ("",NULL,None) else row.get('Other5ID'))
            register.ConceptRate = int(0 if row.get('ConceptRate') in ("",NULL,None) else row.get('ConceptRate'))
            register.BredUnk = bool(True if row.get('BredUnk').upper() == 'TRUE' else False)
            register.EvSireBreed = row.get('EvSireBreed')
            register.EvSireStudCd = int(0 if row.get('EvSireStudCd') in ("",NULL,None) else row.get('EvSireStudCd'))
            register.evWeek = row.get('evWeek')
            register.Age1BLT = int(0 if row.get('Age1BLT') in ("",NULL,None) else row.get('Age1BLT'))
            register.Total = row.get('Total')
               
            self.listRegister.append(register)
      pass

   def GetDataCSV(self, path_file):
      """Obtengo los datos de un archivo CSV y los guardo en un objeto Registro"""
      if len(path_file) > 0:
         with open(path_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for column in reader:
               # print(column)
               # if len(column['# Preg'] and column['AbortRes']) < 1:
               #    break
               
               register = Register()
               register.NoPreg = bool(True if int(column['# Preg']) > 0 else False)
               register.AbortRes = bool(True if int(column['AbortRes']) > 0 else False)
               register.SireBull = column['SireBull']
               register.LACT = int(0 if column['LACT'] in ("",NULL,None) else column['LACT'])
               register.Ev_L = int(0 if column['Ev#L'] in ("",NULL,None) else column['Ev#L'])
               register.NoEv = int(0 if column['#Ev'] in ("",NULL,None) else column['#Ev'])
               register.Date = column['Date']
               register.EvGap = column['EvGap']
               register.Tech = column['Tech']
               register.Pen = int(0 if column['Pen'] in ("",NULL,None) else column['Pen'])
               register.bred_sexed = column['bred.sexed']
               register.BredReas = column['BredReas']
               register.DIM_E = int(0 if column['DIM@E'] in ("",NULL,None) else column['DIM@E'])
               register.AnId = int(0 if column['AnId'] in ("",NULL,None) else column['AnId'])
               register.FarmLoc = column['FarmLoc']
               register.AnOwner = column['AnOwner']
               register.BRD = column['BRD']
               register.Age_da = int(0 if column['Age(da)'] in ("",NULL,None) else column['Age(da)'])
               register.Other2ID = int(0 if column['Other2ID'] in ("",NULL,None) else column['Other2ID'])
               register.Other5ID = int(0 if column['Other5ID'] in ("",NULL,None) else column['Other5ID'])
               register.ConceptRate = int(0 if column['ConceptRate'] in ("",NULL,None) else column['ConceptRate'])
               register.BredUnk = bool(True if column['BredUnk'].upper() == 'TRUE' else False)
               register.EvSireBreed = column['EvSireBreed']
               register.EvSireStudCd = int(0 if column['EvSireStudCd'] in ("",NULL,None) else column['EvSireStudCd'])
               register.evWeek = column['evWeek']
               register.Age1BLT = int(0 if column['Age1BLT'] in ("",NULL,None) else column['Age1BLT'])
               register.Total = column['Total']
                  
               self.listRegister.append(register)
      pass


   def Process(self, path_file, output_filename, output_path_file):
      # Agregar pagina al PDF
      self.pdf.alias_nb_pages()
      self.pdf.add_page()
      self.GroupBy()
      
      if output_path_file is NULL:
         current_filename = path_file.split('/')[-1]
         output_path_file = path_file.replace(current_filename,'')

      output_path_file += output_filename
      self.pdf.output(f'{output_path_file}.pdf', 'F')
         
      print(f'ARCHIVO {output_filename}.pdf CREADO CREADO en --> {output_path_file}.pdf\n')
      self.log_file.write(f"{output_filename}.pdf CREADO en --> {output_path_file}.pdf\n\n")
      self.log_file.close()     
      
   def GroupBy(self):
      # print('AgruparPorLactancia():')
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
         dataRegisterT.BredUnk = item.BredUnk
         # dataRegisterT.Ev_L = item.Ev_L
         dataRegisterT.NoEv = item.NoEv
         
         registers_groupedby_lact[item.LACT, item.NoEv].append(dataRegisterT)
         registers_groupedby_bredReas[item.BredReas, item.LACT].append(dataRegisterT)
         registers_groupedby_sireBull[item.SireBull, item.LACT].append(dataRegisterT)
         registers_groupedby_evSireStudCd[item.EvSireStudCd, item.LACT].append(dataRegisterT)
         registers_groupedby_tech[ item.Tech, item.LACT].append(dataRegisterT)
         
         ev_list.append(item.NoEv) # [1,1,2,2,0,1,3,2,2]
         lact_list.append(item.LACT)
         bredReas_list.append(item.BredReas)
         sireBull_list.append(item.SireBull)
         evSireStudCd_list.append(item.EvSireStudCd)
         tech_list.append(item.Tech)
         
      ev_list = pandas.unique(ev_list).tolist() # [2,3,1]
      ev_list.sort() # [1,2,3]
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
      
      tableEmail = TableEmail()
      tables = AddTablesGroupbyLactFilterEv(registers_groupedby_lact, lact_list, ev_list)
      self.GeneratePDF(tables,tableEmail)
      tables = AddTablesGroupbyBredReasFilterLact(registers_groupedby_bredReas, bredReas_list, lact_list)
      self.GeneratePDF(tables,tableEmail)
      tables = AddTablesGroupbySireBullFilterLact(registers_groupedby_sireBull, sireBull_list, lact_list)
      self.GeneratePDF(tables,tableEmail)
      tables = AddTablesGroupbyEvSireStudCdFilterLact(registers_groupedby_evSireStudCd, evSireStudCd_list, lact_list)
      self.GeneratePDF(tables,tableEmail)
      tables = AddTablesGroupbyTechFilterLact(registers_groupedby_tech, tech_list, lact_list)
      self.GeneratePDF(tables,tableEmail)
      SendEmail(tableEmail)
   
   def GeneratePDF(self, tables, tableEmail):
      column_size = 205 / 8 #Ancho de tabla (200) entre Numero de columnas (7)
      meta = 35 # meta 
      for table in tables:
         self.pdf.TableHeader(table.TitleTable)
         self.pdf.TitleColumn(table.Column1Name,column_size,'R')
         self.pdf.TitleColumn(table.Column2Name,column_size,'R')
         self.pdf.TitleColumn(table.Column3Name,column_size,'R')
         self.pdf.TitleColumn(table.Column4Name,column_size,'R')
         self.pdf.TitleColumn(table.Column5Name,column_size,'R')
         self.pdf.TitleColumn(table.Column6Name,column_size,'R')
         self.pdf.TitleColumn(table.Column7Name,column_size,'R')
         self.pdf.LastTitleColumn(table.Column8Name,0,'')
         for register in table.Registers:
            value = register.PromedioPreg #valor del PromedioPreg para comparar con la meta
            if value < meta:
               self.AddRegisterTableEmail(tableEmail,register,table.TitleTable)

            self.pdf.Column(f"{register.EtiquetaDeFila}",value,meta,column_size,'R')
            self.pdf.Column(f"{register.PromedioPreg}%",register.PromedioPreg,meta,column_size,'R')
            self.pdf.Column(f"{register.SumaPreg}",value,meta,column_size,'R')
            self.pdf.Column(f"{register.PromedioAbortRes}%",value,meta,column_size,'R')
            self.pdf.Column(f"{register.BredOpenSum}",value,meta,column_size,'R')
            self.pdf.Column(f"{register.ConceptAbortRate}%",value,meta,column_size,'R')
            self.pdf.Column(f"{register.BredUnk}",value,meta,column_size,'R')
            self.pdf.LastColumn(f"{register.CuentaPreg2}",value,meta,0,'')
         self.pdf.FooterColumn('TOTALES',column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalPromedioPreg}%",column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalSumaPreg}",column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalPromedioAbortRes}%",column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalBredOpenSum}",column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalConceptAbortRate}%",column_size,'R')
         self.pdf.FooterColumn(f"{table.TotalBredUnk}",column_size,'R')
         self.pdf.LastFooterColumn(f"{table.TotalCuentaPreg2}",0,'')
         self.pdf.ln(10)

   def AddRegisterTableEmail(self, tableEmail, register, titleTable):
      registerTE = RegisterTableEmail()
      registerTE.tableTitle = titleTable
      registerTE.EtiquetaDeFila = register.EtiquetaDeFila
      registerTE.PromedioPreg = f"{register.PromedioPreg}%"
      tableEmail.Registers.append(registerTE)
      pass
      
       

if __name__ == '__main__':
   CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/pruebaCompleta.csv', 'pruebasCSV_PDF', NULL)
   # CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/datosJSON.json', 'pruebasCsvJSON_PDF_sinRutaDestino', NULL)
   CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/DPN_CR_Download_Template.sync.json', 'pruebasJSON_PDF_conRutaDestino', 'D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/')