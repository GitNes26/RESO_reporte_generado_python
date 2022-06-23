from pymysql import NULL


class Register:
   """Modelar para un registro que son todos los datos de un renglón del excel"""
   
   def saludar(self):
      """Imprime un saludo en pantalla."""
      print("¡Hola, mundo!")
      
   def __init__(self):
      self.NoPreg = NULL
      self.AbortRes = NULL
      self.SireBull = NULL
      self.LACT = NULL
      self.Ev_L = NULL
      self.NoEv = NULL
      self.Date = NULL
      self.EvGap = NULL
      self.Tech = NULL
      self.Pen = NULL
      self.bred_sexed = NULL
      self.BredReas = NULL
      self.DIM_E = NULL
      self.AnId = NULL
      self.FarmLoc = NULL
      self.AnOwner = NULL
      self.BRD = NULL
      self.Age_da = NULL
      self.Other2ID = NULL
      self.Other5ID = NULL
      self.ConceptRate = NULL
      self.BredUnk = NULL
      self.EvSireBreed = NULL
      self.EvSireStudCd = NULL
      self.evWeek = NULL
      self.Age1BLT = NULL
      self.Total = NULL
      
        
   # def __init__(self, NoPreg, AbortRes, SireBull ,LACT, Ev_L, NoEv, Date, EvGap, Tech, Pen, bred_sexed, BredReas, DIM_E, AnId, FarmLoc, AnOwner, BRD, Age_da, Other2ID, Other5ID, ConceptRate, BredUnk, EvSireBreed, EvSireStudCd, evWeek, Age1BLT, Total):
      # self.NoPreg = NoPreg
      # self.AbortRes = AbortRes
      # self.SireBull = SireBull
      # self.LACT = LACT
      # self.Ev_L = Ev_L
      # self.NoEv = NoEv
      # self.Date = Date
      # self.EvGap = EvGap
      # self.Tech = Tech
      # self.Pen = Pen
      # self.bred_sexed = bred_sexed
      # self.BredReas = BredReas
      # self.DIM_E = DIM_E
      # self.AnId = AnId
      # self.FarmLoc = FarmLoc
      # self.AnOwner =  AnOwner
      # self.BRD = BRD
      # self.Age_da = Age_da
      # self.Other2ID = Other2ID
      # self.Other5ID = Other5ID
      # self.ConceptRate = ConceptRate
      # self.BredUnk = BredUnk
      # self.EvSireBreed = EvSireBreed
      # self.EvSireStudCd = EvSireStudCd
      # self.evWeek = evWeek
      # self.Age1BLT = Age1BLT
      # self.Total = Total
      
      # print(self.BRD)