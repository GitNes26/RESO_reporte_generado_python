from ast import For
from collections import defaultdict
from pymysql import NULL #pip install PyMySQL

from Classes.Computation import Mean
   
   
class DataRegisterT:
   """Este objeto ayudara a construir las Tablas"""
   
   def __init__(self):
      self.Preg = NULL
      """La vaca fue preñada"""
      self.Abort =  NULL
      """La vaca preñada aborto"""
      self.Lact = NULL
      """Lactancia"""
      self.Ev_L = NULL
      """..."""
      self.NoEv = NULL
      """Numero de Evento"""


class RegisterTable:
   """Este objeto es un registro en la tabla"""

   def __init__(self):
      self.EtiquetaDeFila = 0
      """Lactancias"""
      self.PromedioPreg = 0
      """Promediar las vacas preñadas según lactancia, pero que no abortaron"""
      self.SumaPreg = 0
      """Sumar las vacas preñadas según lactancia, pero que no abortaron"""
      self.PromedioAbortRes = 0
      """Promediar las vacas preñadas según lactancia, pero que abortaron"""
      self.BredOpenSum = 0
      """Diferencia del total de las vacas menos las vacas preñadas"""
      self.ConceptAbortRate = 0
      """Porcentaje de vacas preñadas menos los abortos entre el total de vacas"""
      self.CuentaPreg2 = 0
      """Sumar las vacas preñadas según lactancia, no importa si abortaron (total de vacas)"""

      #variables extras
      self.CowsPreg = 0 
      """Suma de vacas preñadas"""
      self.CowsAbort= 0 
      """Suma de vacas que abortaton"""


class Table:
   """Esta tabla agrupa los resultados por lactancia y filtra por #Ev"""
   def __init__(self):
      self.TitleTable = 'Datos filtrados por #Ev 1'
      self.Column1Name = 'Etiqueta De Fila'
      self.Column2Name = 'Promedio de # Preg (%)'
      self.Column3Name = 'Suma de # Preg'
      self.Column4Name = 'Promedio de AbortRes (%)'
      self.Column5Name = 'Bred Open Sum'
      self.Column6Name = 'Concept Abort Rate (%)'
      self.Column7Name = 'Cuenta de # Preg2'
      self.Registers = []
      
      self.TotalPromedioPreg = 0
      self.TotalSumaPreg = 0
      self.TotalPromedioAbortRes = 0
      self.TotalCuentaPreg2 = 0
      self.TotalBredOpenSum = 0
      self.TotalConceptAbortRate = 0
   
   
   
   
def AddRegisterGroupedbyLactOnlyEv(table, register_list, groupby, filter, groupby_lact, register_grouped, last_lact):
   """Caluclar los campos de la tabla de un solo filtro (para la tabla agrupados por Lact)"""
   
   register = RegisterTable()
   register.EtiquetaDeFila = groupby
   if groupby_lact is True:
      register = register_grouped
   
   for item in register_list[groupby,filter]:
      if item.Preg==True and item.Abort==False:
         register.SumaPreg += 1
      if item.Preg==True:
         register.CowsPreg += 1
      if item.Abort==True:
         register.CowsAbort += 1
      register.CuentaPreg2 += 1
      
   if register.CuentaPreg2 > 0:
      register.BredOpenSum = register.CuentaPreg2 - register.CowsPreg
      register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
      register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
      register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)
   
   if groupby_lact is False:
      table.Registers.append(register)
   if groupby_lact is True and groupby==last_lact:
      table.Registers.append(register)

def AddRegisterGroupedbyLactMuchEv(table, register_list, groupby_list, filter, groupby_lact, register_grouped, last_lact, groupby_lact_or_more, last_env):
   """Caluclar los campos de la tabla con más de un filtro (para la tabla agrupados por Lact)"""
   
   for lact in groupby_list:         
      register = RegisterTable()
      register.EtiquetaDeFila = lact
      register.Ev = filter

      if lact >= groupby_lact_or_more:
         groupby_lact = True

      if groupby_lact is True:
         register = register_grouped

      if lact <= groupby_lact_or_more:
         register.CowsAbort= 0
         register.CowsPreg= 0

      for item in register_list[lact,filter]:
         if item.Preg==True and item.Abort==False:
            register.SumaPreg += 1
         if item.Preg==True:
            register.CowsPreg += 1
         if item.Abort==True:
            register.CowsAbort += 1
         register.CuentaPreg2 += 1
         
      if register.CuentaPreg2 > 0:
         register.BredOpenSum = register.CuentaPreg2 - register.CowsPreg
         # if lact <= groupby_lact_or_more:
         #    register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
         #    register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
         #    register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)
      
      if groupby_lact is False:
         table.Registers.append(register)
      if groupby_lact is True and lact==last_lact and filter==last_env:
         table.Registers.append(register)

def GroupRegisterGroupedbyLactByFilter(table, register_list, groupby_list, groupby_lact, register_grouped, last_lact, groupby_lact_or_more):
   """Agrupar los registros por filtro( con más de un filtro) y Caluclar los campos de la tabla (para la tabla agrupados por Lact)"""
   
   registers_groupedby_lact = defaultdict(list)
   for item in register_list:
      registers_groupedby_lact[item.EtiquetaDeFila].append(item)
   
   for lact in groupby_list:
      register = RegisterTable()
      register.EtiquetaDeFila = lact

      if lact >= groupby_lact_or_more:
         groupby_lact = True
      if groupby_lact is True:
         register = register_grouped
      
      for item in registers_groupedby_lact[lact]:
         register.SumaPreg += item.SumaPreg
         register.CuentaPreg2 += item.CuentaPreg2
         register.BredOpenSum += item.BredOpenSum

         register.ConceptAbortRate += item.ConceptAbortRate
         register.PromedioPreg += item.PromedioPreg
         register.PromedioAbortRes += item.PromedioAbortRes

      if register.CuentaPreg2 > 0:
         register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
         register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
         register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)

      if groupby_lact is False:
         table.Registers.append(register)
   if groupby_lact is True and lact==last_lact:
      register.EtiquetaDeFila = f"{groupby_lact_or_more}+"
      table.Registers.append(register)
     


def AddRegisterOnlyEv(table, register_list, groupby, filter):
   """Caluclar los campos de la tabla de un solo filtro"""
   
   register = RegisterTable()
   register.EtiquetaDeFila = groupby
   
   for item in register_list[groupby,filter]:
      if item.Preg==True and item.Abort==False:
         register.SumaPreg += 1
      if item.Preg==True:
         register.CowsPreg += 1
      if item.Abort==True:
         register.CowsAbort += 1
      register.CuentaPreg2 += 1
      
   if register.CuentaPreg2 > 0:
      register.BredOpenSum = register.CuentaPreg2 - register.CowsPreg
      register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)
      register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
      register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
   table.Registers.append(register)
 
def AddRegisterMuchEv(table, register_list, groupby_list, filter):
   """Caluclar los campos de la tabla con más de un filtro"""
   
   for groupby in groupby_list:         
      register = RegisterTable()
      register.EtiquetaDeFila = groupby
      register.CowsAbort= 0
      register.CowsPreg= 0

      for item in register_list[groupby,filter]:
         if item.Preg==True and item.Abort==False:
            register.SumaPreg += 1
         if item.Preg==True:
            register.CowsPreg += 1
         if item.Abort==True:
            register.CowsAbort += 1
         register.CuentaPreg2 += 1
         
      # if register.CuentaPreg2 > 0:
      #    register.BredOpenSum = register.CuentaPreg2 - register.CowsPreg
      #    register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)
      #    register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
      #    register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
      table.Registers.append(register)
   
def GroupRegisterByFilter(table, register_list, groupby_list):
   """Agrupar los registros por filtro( con más de un filtro) y Caluclar los campos de la tabla"""
   
   registers_grouped = defaultdict(list)
   for item in register_list:
      registers_grouped[item.EtiquetaDeFila].append(item)
   
   for groupby in groupby_list:         
      register = RegisterTable()
      register.EtiquetaDeFila = groupby
      for item in registers_grouped[groupby]:
         register.SumaPreg += item.SumaPreg
         register.CuentaPreg2 += item.CuentaPreg2
         register.BredOpenSum += item.BredOpenSum

         register.ConceptAbortRate += item.ConceptAbortRate
         register.PromedioPreg += item.PromedioPreg
         register.PromedioAbortRes += item.PromedioAbortRes
         
      if register.CuentaPreg2 > 0:
         register.PromedioPreg = Mean(register.SumaPreg, register.CuentaPreg2)
         register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
         register.ConceptAbortRate = Mean((register.CowsPreg-register.CowsAbort), register.CuentaPreg2)
      table.Registers.append(register)
         
def Totals(tables):
   """Calcular Totales de tabla"""

   total_preg = 0
   total_abort = 0
   for table in tables:
      for register in table.Registers:
         table.TotalSumaPreg += register.SumaPreg
         table.TotalCuentaPreg2 += register.CuentaPreg2
         table.TotalBredOpenSum += register.BredOpenSum
         total_preg += register.CowsPreg
         total_abort += register.CowsAbort

      table.TotalPromedioPreg = Mean(table.TotalSumaPreg, table.TotalCuentaPreg2)
      table.TotalPromedioAbortRes = Mean(total_abort, table.TotalCuentaPreg2)
      table.TotalConceptAbortRate = Mean((total_preg - total_abort), table.TotalCuentaPreg2)

      

def AddTablesGroupbyLactFilterEv(grouped_registers, lact_list, ev_list):       
   """Agregar registros a la tabla agrupados por LACT y filtrados por Ev"""
   # print('AddTablesGroupbyLactFilterEv():')
   tables = []
   mas_de_un_ev = False
   groupby_lact_or_more = 3
   register_grouped = RegisterTable()
   register_grouped.EtiquetaDeFila = f'{groupby_lact_or_more}+'
   last_lact = lact_list[-1]
   last_env = ev_list[-1]

   for ev in ev_list:
      mas_de_un_ev = False #Bandera para agrupar registros que corresponden a más de un filtro

      if ev == 1:
         table = Table()
         table.TitleTable = f"Datos agrupados por Lact y filtrados por #Ev {ev}"            
         for lact in lact_list:
            groupby_lact = False
            if lact >= groupby_lact_or_more:
               groupby_lact = True
            AddRegisterGroupedbyLactOnlyEv(table, grouped_registers, lact, ev, groupby_lact, register_grouped, last_lact)
         tables.append(table)
         register_grouped = RegisterTable()

         table = Table()
         temporal_table = Table()
         continue
      
      
      if 'table' in locals(): #Condicion para crear tabla en caso de que no haya entrado al evento 1
         if len(table.Registers) == 0 and len(temporal_table.Registers) == 0:
            table = Table()
            temporal_table = Table()
      else:
         table = Table()
         temporal_table = Table()
      
      mas_de_un_ev = True
      table.TitleTable = f"Datos agrupados por Lact y filtrados por #Ev 1+"
      groupby_lact = False      
      AddRegisterGroupedbyLactMuchEv(temporal_table, grouped_registers, lact_list, ev, groupby_lact, register_grouped, last_lact, groupby_lact_or_more, last_env)

   if mas_de_un_ev: #Este código se ejecuta para agrupar los registros con más de un evento, pasamos los registros de la tabla temporal a la tabla final ya agrupados
      GroupRegisterGroupedbyLactByFilter(table, temporal_table.Registers, lact_list, groupby_lact, register_grouped, last_lact, groupby_lact_or_more)
      tables.append(table)
   Totals(tables) #Calculamos los totales
   register_grouped = RegisterTable() #Limpiamos la variable para asegurarnos de que no se agreguen datos anteriores
   return tables
   

def AddTablesGroupbyBredReasFilterLact(grouped_registers, bredReas_list, lact_list):       
   """Agregar registros a la tabla agrupados por BredReas y filtrados por LACT"""
   # print('AddTablesGroupbyBredReasFilterLact():')
   tables = []
   mas_de_un_ev = False

   for lact in lact_list:
      mas_de_un_ev = False
      if lact == 0:
         table = Table()
         table.TitleTable = f"Datos agrupados por bredReas y filtrados por #Lact {lact}"            
         for bredReas in bredReas_list:
            AddRegisterOnlyEv(table, grouped_registers, bredReas, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      elif lact == 1:
         table = Table()
         table.TitleTable = f"Datos agrupados por bredReas y filtrados por #Lact {lact}"            
         for bredReas in bredReas_list:
            AddRegisterOnlyEv(table, grouped_registers, bredReas, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      else:
         if 'table' in locals():
            if len(table.Registers) == 0 and len(temporal_table.Registers) == 0:
               table = Table()
               temporal_table = Table()
         else:
            table = Table()
            temporal_table = Table()
         
         mas_de_un_ev = True
         table.TitleTable = f"Datos agrupados por bredReas y filtrados por #Lact 2+"            
         AddRegisterMuchEv(temporal_table, grouped_registers, bredReas_list, lact)

   if mas_de_un_ev:
      GroupRegisterByFilter(table, temporal_table.Registers, bredReas_list)
      tables.append(table)
   Totals(tables)
   return tables
   
      
def AddTablesGroupbySireBullFilterLact(grouped_registers, sireBull_list, lact_list):       
   """Agregar registros a la tabla agrupados por SireBull y filtrados por LACT"""
   # print('AddTablesGroupbySireBullFilterLact():')
   tables = []
   mas_de_un_ev = False

   for lact in lact_list:
      mas_de_un_ev = False
      if lact == 0:
         table = Table()
         table.TitleTable = f"Datos agrupados por sireBull y filtrados por #Lact {lact}"            
         for sireBull in sireBull_list:
            AddRegisterOnlyEv(table, grouped_registers, sireBull, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      else:
         if 'table' in locals():
            if len(table.Registers) == 0 and len(temporal_table.Registers) == 0:
               table = Table()
               temporal_table = Table()
         else:
            table = Table()
            temporal_table = Table()
         
         mas_de_un_ev = True
         table.TitleTable = f"Datos agrupados por sireBull y filtrados por #Lact 1+"            
         AddRegisterMuchEv(temporal_table, grouped_registers, sireBull_list, lact)

   if mas_de_un_ev:
      GroupRegisterByFilter(table, temporal_table.Registers, sireBull_list)
      tables.append(table)
   Totals(tables)
   return tables


def AddTablesGroupbyEvSireStudCdFilterLact(grouped_registers, evSireStudCd_list, lact_list):       
   """Agregar registros a la tabla agrupados por EvSireStudCd y filtrados por LACT"""
   # print('AddTablesGroupbyEvSireStudCdFilterLact():')
   tables = []
   mas_de_un_ev = False

   for lact in lact_list:
      mas_de_un_ev = False
      if lact == 0:
         table = Table()
         table.TitleTable = f"Datos agrupados por evSireStudCd y filtrados por #Lact {lact}"            
         for evSireStudCd in evSireStudCd_list:
            AddRegisterOnlyEv(table, grouped_registers, evSireStudCd, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      else:
         if 'table' in locals():
            if len(table.Registers) == 0 and len(temporal_table.Registers) == 0:
               table = Table()
               temporal_table = Table()
         else:
            table = Table()
            temporal_table = Table()
         
         mas_de_un_ev = True
         table.TitleTable = f"Datos agrupados por evSireStudCd y filtrados por #Lact 1+"            
         AddRegisterMuchEv(temporal_table, grouped_registers, evSireStudCd_list, lact)

   if mas_de_un_ev:
      GroupRegisterByFilter(table, temporal_table.Registers, evSireStudCd_list)
      tables.append(table)
   Totals(tables)
   return tables


def AddTablesGroupbyTechFilterLact(grouped_registers, tech_list, lact_list):       
   """Agregar registros a la tabla agrupados por Tech y filtrados por LACT"""
   # print('AddTablesGroupbyTechFilterLact():')
   tables = []
   mas_de_un_ev = False

   for lact in lact_list:
      mas_de_un_ev = False
      if lact == 0:
         table = Table()
         table.TitleTable = f"Datos agrupados por tech y filtrados por #Lact {lact}"            
         for tech in tech_list:
            AddRegisterOnlyEv(table, grouped_registers, tech, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      elif lact == 1:
         table = Table()
         table.TitleTable = f"Datos agrupados por tech y filtrados por #Lact {lact}"            
         for tech in tech_list:
            AddRegisterOnlyEv(table, grouped_registers, tech, lact)
         tables.append(table)

         table = Table()
         temporal_table = Table()
         continue
      else:
         if 'table' in locals():
            if len(table.Registers) == 0 and len(temporal_table.Registers) == 0:
               table = Table()
               temporal_table = Table()
         else:
            table = Table()
            temporal_table = Table()
         
         mas_de_un_ev = True
         table.TitleTable = f"Datos agrupados por tech y filtrados por #Lact 2+"            
         AddRegisterMuchEv(temporal_table, grouped_registers, tech_list, lact)

   if mas_de_un_ev:
      GroupRegisterByFilter(table, temporal_table.Registers, tech_list)
      tables.append(table)
   Totals(tables)
   return tables
   