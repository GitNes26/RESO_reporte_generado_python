def color_dictionary(color):
      colors = {
         'black' : (33, 37, 43),
         'blue' : (0, 49, 91),
         'blue_header' : (0, 0, 255),
         'gray' : (52, 58, 64), 
         'white' : (233, 236, 239), 
         'full_white' : (255, 255, 255),
         'red' : (235, 83, 83),
      }
      return colors[color]

def DrawColor(sheet, color):
   cr,cg,cb = color_dictionary(color)
   sheet.set_draw_color(cr, cg, cb)
   
def BackgroundColor(sheet, color):
   cr,cg,cb = color_dictionary(color)
   sheet.set_fill_color(cr, cg, cb)
   
def TextColor(sheet, color):
   cr,cg,cb = color_dictionary(color)
   sheet.set_text_color(cr, cg, cb)
   
def FontSize(sheet, size):
   sheet.set_font_size(size)
   
def FontStyle(sheet, family='Arial', style=''):
   sheet.set_font(family, style)