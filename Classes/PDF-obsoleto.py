from fpdf import FPDF as FPDF 

class PDF(FPDF):
   """HOJA TAMAÑP A4 (210 x 297 mm)"""      
   sheet_width = 210
   sheet_height = 297
   half_width_sheet = sheet_width / 2
   
   typography = 'Arial'
   text_size = 12.0,
   black_color = (33, 37, 43)
   blue_color = (0, 49, 91)

   
   def AddLogo(self,file,x,y,w):
      self.image(file, x, y, w)
      # self.image(name=file, x=x, y=y, w=w, h=h)
      
   def AddText(self, x, y, text):
      self.set_font(self.typography, '', 12)
      self.text(x=x, y=y, txt=text)
      
   def AddGridTitle(self, title):
      self.set_xy(0, 10)
      self.set_font(self.typography, 'B', 16)
      self.set_text_color(self.blue_color[0], self.blue_color[1], self.blue_color[2])
      self.cell(w=0, h=40.0, align='C', txt=title, border=1)
      
   def AddCell(self, text):
      self.set_xy(0, 0)
      self.set_font(self.typography, '', 12)
      self.set_text_color(self.black_color[0], self.black_color[1], self.black_color[2])
      self.cell(w=0, h=10, txt=text, border=1)
      
   def AddMultiCell(self, text):
      self.set_xy(0, 0)
      self.set_font(self.typography, '', 12)
      self.set_text_color(self.black_color[0], self.black_color[1], self.black_color[2])
      self.multi_cell(w=0, h=10, txt=text, align='L')
      


image_width = 50
half_image_width = image_width / 2

pdf = PDF()
pdf.add_page()
pdf.set_left_margin(30)
pdf.set_right_margin(30)
pdf.set_top_margin(10)
pdf.AddLogo('logo_dpn.png',pdf.half_width_sheet-half_image_width ,5,image_width)
# pdf.AddLogo('logo_dpn.png',50,0,60,15)
# pdf.AddTitle('PDF DE PRUEBA')
# pdf.AddTitle('AJAS')
pdf.AddText(0,10,'Texto de prueba...........................................................................................................................................................................................................................................................................................................................................................\nTexto de prueba..')
# pdf.AddTitle('BLA BLA BLA')

pdf.set_author('Nombre del autor')
pdf.output('C:/Users/nesto/OneDrive/Escritorio/RESO_SISTEMAS/ProyectoPython/tuto1.pdf', 'F')
