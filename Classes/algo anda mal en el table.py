def AddRegisterOnlyEv(table, register_list, groupby, filter):
   """Caluclar los campos de la tabla de un solo filtro"""
   
   register = RegisterTable()
   register.EtiquetaDeFila = groupby
   
   for item in register_list[groupby,filter]:
      if item.Preg==True:
         register.SumaPreg += 1
      if item.Abort==True:
         register.CowsAbort += 1
      if item.BredUnk==True:
         register.BredUnk += 1
      register.CuentaPreg2 += 1
      
   if register.CuentaPreg2 > 0:
      register.BredOpenSum = register.CuentaPreg2 - register.SumaPreg
      register.ConceptAbortRate = Mean((register.SumaPreg-register.CowsAbort), register.CuentaPreg2)
      register.PromedioPreg = Mean(register.SumaPreg, (register.CuentaPreg2-register.BredUnk))
      register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
   
   if register.CuentaPreg2 > 0:
      table.Registers.append(register)
 
def AddRegisterMuchEv(table, register_list, groupby_list, filter):
   """Caluclar los campos de la tabla con más de un filtro"""
   
   for groupby in groupby_list:         
      register = RegisterTable()
      register.EtiquetaDeFila = groupby
      register.CowsAbort= 0

      for item in register_list[groupby,filter]:
         if item.Preg==True:
            register.SumaPreg += 1
         if item.Abort==True:
            register.CowsAbort += 1
         if item.BredUnk==True:
            register.BredUnk += 1
         register.CuentaPreg2 += 1

         if register.CuentaPreg2 > 0:
            register.BredOpenSum = register.CuentaPreg2 - register.SumaPreg

         if register.CuentaPreg2 > 0:
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
         register.CowsAbort += item.CowsAbort
         register.SumaPreg += item.SumaPreg
         register.CuentaPreg2 += item.CuentaPreg2
         register.BredOpenSum += item.BredOpenSum
         register.BredUnk += item.BredUnk
         register.ConceptAbortRate += item.ConceptAbortRate
         register.PromedioPreg += item.PromedioPreg
         register.PromedioAbortRes += item.PromedioAbortRes
         
      if register.CuentaPreg2 > 0:
         register.PromedioPreg = Mean(register.SumaPreg, (register.CuentaPreg2-register.BredUnk))
         register.PromedioAbortRes = Mean(register.CowsAbort, register.CuentaPreg2)
         register.ConceptAbortRate = Mean((register.SumaPreg-register.CowsAbort), register.CuentaPreg2)
      
      if register.CuentaPreg2 > 0:
         table.Registers.append(register)
         
def Totals(tables):
   """Calcular Totales de tabla"""

   for table in tables:
      total_abort = 0
      table.TotalPromedioPreg = 0
      table.TotalSumaPreg = 0
      table.TotalPromedioAbortRes = 0
      table.TotalBredOpenSum = 0
      table.TotalConceptAbortRate = 0
      table.TotalBredUnk = 0
      table.TotalCuentaPreg2 = 0

      for register in table.Registers:
         table.TotalSumaPreg += register.SumaPreg
         table.TotalCuentaPreg2 += register.CuentaPreg2
         table.TotalBredOpenSum += register.BredOpenSum
         table.TotalBredUnk += register.BredUnk
         total_abort += register.CowsAbort

      if table.TotalCuentaPreg2 > 0:
         table.TotalPromedioPreg = Mean(table.TotalSumaPreg, (register.CuentaPreg2-register.BredUnk))
         table.TotalPromedioAbortRes = Mean(total_abort, table.TotalCuentaPreg2)
         table.TotalConceptAbortRate = Mean((table.TotalSumaPreg - total_abort), table.TotalCuentaPreg2)
