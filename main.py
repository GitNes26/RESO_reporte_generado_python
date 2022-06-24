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


class CreateReport():  
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
      log_file = open("./log.txt", "a")
      fecha_ejecucion = moment.now().format("DD-MM-YYYY HH:mm:ss")
      log_file.write(f"Archivo ejecutado... {fecha_ejecucion}\n")
      print(f"Archivo ejecutado... {fecha_ejecucion}")


      def GroupBy():
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
            dataRegisterT.Ev_L = item.Ev_L
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
         GeneratePDF(tables,tableEmail)
         tables = AddTablesGroupbyBredReasFilterLact(registers_groupedby_bredReas, bredReas_list, lact_list)
         GeneratePDF(tables,tableEmail)
         tables = AddTablesGroupbySireBullFilterLact(registers_groupedby_sireBull, sireBull_list, lact_list)
         GeneratePDF(tables,tableEmail)
         tables = AddTablesGroupbyEvSireStudCdFilterLact(registers_groupedby_evSireStudCd, evSireStudCd_list, lact_list)
         GeneratePDF(tables,tableEmail)
         tables = AddTablesGroupbyTechFilterLact(registers_groupedby_tech, tech_list, lact_list)
         GeneratePDF(tables,tableEmail)
         SendEmail(tableEmail)
                           
      
      def GeneratePDF(tables,tableEmail):
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
                  AddRegisterTableEmail(tableEmail,register,table.TitleTable)

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

        
      def AddRegisterTableEmail(tableEmail, register, titleTable):
         registerTE = RegisterTableEmail()
         registerTE.tableTitle = titleTable
         registerTE.EtiquetaDeFila = register.EtiquetaDeFila
         registerTE.PromedioPreg = f"{register.PromedioPreg}%"
         tableEmail.Registers.append(registerTE)
         pass
      
         
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
               register.BredUnk = bool(True if column['BredUnk'].upper() == 'TRUE' else False)
               register.EvSireBreed = column['EvSireBreed']
               register.EvSireStudCd = column['EvSireStudCd']
               register.evWeek = column['evWeek']
               register.Age1BLT = column['Age1BLT']
               register.Total = column['Total']
                  
               self.listRegister.append(register)

         # Agregar pagina al PDF
         self.pdf.alias_nb_pages()
         self.pdf.add_page()
         GroupBy()
         
         if output_path_file is NULL:
            current_filename = path_file.split('/')[-1]
            output_path_file = path_file.replace(current_filename,'')

         output_path_file += output_filename
         self.pdf.output(f'{output_path_file}.pdf', 'F')
            
         print(f'ARCHIVO {output_filename}.pdf CREADO CREADO en --> {output_path_file}.pdf\n')
         log_file.write(f"{output_filename}.pdf CREADO en --> {output_path_file}.pdf\n\n")
      log_file.close()     
      
               

if __name__ == '__main__':
   report1 = CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/pruebaCompleta.csv', 'pruebasPDF', NULL)
   # report1 = CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/prueba.csv', 'pruebasPDF_sinRutaDestino', NULL)
   # report2 = CreateReport('D:/TRABAJO/RESO_SISTEMAS/ProyectoPython/Documents/prueba.csv', 'pruebasPDF_conRutaDestino', 'D:/RESO_SISTEMAS/ProyectoPython/')