import moment #pip install moment
from fpdf import FPDF as FPDF
from pymysql import NULL #pip install fpdf
from ConvertPDF.stylesPDF import *

class PDF(FPDF):
   """HOJA TAMAÑP A4 (210 x 297 mm)"""      
   sheet_width = 210
   sheet_height = 297
   # half_width_sheet = sheet_width / 2
   # image_width = 50
   # half_image_width = image_width / 2
   now = moment.now().format("DD-MM-YYYY HH:mm:ss")
   
   typography = 'Arial'
   text_header_size = 10.0
   text_title_size = 5.0
   text_size = 5.0
   # column_size = 200 / 7
   
   
   def header(self):
      # Logo
      self.image('logo_dpn.png', x=10, y=10, h=10)

      # Title
      # Arial bold 16 - color blue
      FontStyle(self, 'Arial', 'B')
      FontSize(self, 16)
      TextColor(self, 'blue')
      self.cell(w=0, h=8, txt=f'GENERAL REPORT', border=0, ln=1, align='C')
      # SubTitle
      FontSize(self, 12)
      self.cell(w=0, h=7, txt=f'{self.now}', border=0, ln=2, align='C')
      # Line break
      self.ln(10)

   # Page footer
   def footer(self):
      # Position at 1.5 cm from bottom
      self.set_y(-15)
      # Arial italic 8 - color gray
      FontStyle(self, 'Arial', 'I')
      FontSize(self, self.text_title_size)
      TextColor(self,'gray')
      
      # cr,cg,cb = color_dictionary('black')
      # self.set_text_color(cr, cg, cb)
      # Page number
      self.cell(0, 10, f'Page {str(self.page_no())}' + '/{nb}', 0, 0, 'C')
      
   
   def TableHeader(self, text):
      FontSize(self, self.text_header_size)
      FontStyle(self, 'Arial', 'B')
      BackgroundColor(self, 'blue_header')
      TextColor(self, 'white')
      self.multi_cell(w=0, h=8, txt=str(text), border=0, fill=1, align='C')
      
   def TitleColumn(self, text='', width=0, border=0):
      FontSize(self, self.text_title_size)
      FontStyle(self, 'Arial', 'B')
      BackgroundColor(self, 'white')
      TextColor(self, 'black')
      self.cell(w=width, h=8, txt=str(text), border=border, fill=1, align='C')

   def LastTitleColumn(self, text='', width=0, border=0):
      FontSize(self, self.text_title_size)
      FontStyle(self, 'Arial', 'B')
      BackgroundColor(self, 'white')
      TextColor(self, 'black')
      self.multi_cell(w=width, h=8, txt=str(text), border=border, fill=1, align='C')
   
   def Column(self, text='', value=NULL, metas=NULL, width=0, border=0):
      BackgroundColor(self, 'full_white')
      TextColor(self, 'black')
      FontSize(self, self.text_size)
      FontStyle(self, 'Arial', '')
      if metas is not NULL:
         if float(value) < metas:
            BackgroundColor(self, 'red')
            FontStyle(self, 'Arial', 'B')
            TextColor(self, 'white')
         
      self.cell(w=width, h=5, txt=str(text), border=border, fill=1, align='C')

   def LastColumn(self, text='', value=NULL, metas=NULL, width=0, border=0):
      BackgroundColor(self, 'full_white')
      TextColor(self, 'black')
      FontSize(self, self.text_size)
      FontStyle(self, 'Arial', '')
      if metas is not NULL:
         if float(value) < metas:
            BackgroundColor(self, 'red')
            FontStyle(self, 'Arial', 'B')
            TextColor(self, 'white')

      self.multi_cell(w=width, h=5, txt=str(text), border=border, fill=1, align='C')
      
   def FooterColumn(self, text='', width=0, border=0):
      FontSize(self, self.text_title_size)
      FontStyle(self, 'Arial', 'B')
      BackgroundColor(self, 'white')
      TextColor(self, 'black')
      self.cell(w=width, h=8, txt=str(text), border=border, fill=1, align='C')

   def LastFooterColumn(self, text='', width=0, border=0):
      FontSize(self, self.text_title_size)
      FontStyle(self, 'Arial', 'B')
      BackgroundColor(self, 'white')
      TextColor(self, 'black')
      self.multi_cell(w=width, h=8, txt=str(text), border=border, fill=1, align='C')