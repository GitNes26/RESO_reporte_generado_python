from asyncio import create_task
from collections import defaultdict
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from msilib.schema import tables
from ntpath import join
import smtplib

import pandas


class SendEmail:
   def __init__(self, data):
      content = self.CreateTable(data)
      self.MailBody(content)
      pass

   def EmailSender(self, htmlContent):
         fromaddr = "dairystash@gmail.com"
         email_list = ['nestorpuentesin@gmail.com']
         # email_list = ['manny@dairyperformancenetwork.com',
         #               'gilberto@dpnconnect.com',
         #               'support@dairyperformancenetwork.com',
         #               'redrockdairy92@gmail.com']

         print("Sending...")
         for email in email_list:
            toaddr = email

            # instance of MIMEMultipart
            msg = MIMEMultipart()

            # storing the senders email address
            msg['From'] = fromaddr

            # storing the receivers email address
            msg['To'] = toaddr

            # storing the subject
            msg['Subject'] = "Report General Python"

            # string to store the body of the mail
            body = htmlContent

            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'html'))

            #region APARTADO PARA ENVIAR ARCHIVOS
            # # open the file to be sent
            # filename = "Download Pdf File From Here.pdf"
            # attachment = open("output.pdf", "rb")

            # # instance of MIMEBase and named as p
            # p = MIMEBase('application', 'octet-stream')

            # # To change the payload into encoded form
            # p.set_payload((attachment).read())

            # # encode into base64
            # encoders.encode_base64(p)

            # p.add_header('Content-Disposition',
            #              "attachment; filename= %s" % filename)

            # # attach the instance 'p' to instance 'msg'
            # msg.attach(p)
            #endregion

            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # start TLS for security
            s.starttls()

            # Authentication
            s.login(fromaddr, "clqkejzowmyyjbbz")

            # Converts the Multipart msg into a string
            text = msg.as_string()

            # sending the mail
            s.sendmail(fromaddr, toaddr, text)

            # terminating the session
            s.quit()

            print("Email Sent Successfully!")
            pass

   def CreateTable(self,data):
      tableTitle_list = []
      registers_groupby_titleTable = defaultdict(list)          #etiqueta
      for register in data.Registers:
         registers_groupby_titleTable[register.tableTitle].append(register)
         tableTitle_list.append(register.tableTitle)
      
      tableTitle_list = pandas.unique(tableTitle_list).tolist()
      tableTitle_list.sort()
     
      print("creando tabla de metas no cumplidas...")
      table = f"""
      <table class="content-table">
         <thead>
            <tr>
               <th colspan="2" align="center">Tabla de registros que no cumplieron con la meta <i>( <i 35% en Promedio Preg)</i></th>
            </tr>
            <tr>
               <th>Etiqueta De Fila</th>
               <th>Promedio Preg</th>
            </tr>
         </thead>
         <tbody>"""
      tbody = ""
      for titleTable in tableTitle_list:
         tbody += f"""
         <tr>
            <th colspan="2" align="center">{titleTable}</td>
         </tr>
         """
         for register in registers_groupby_titleTable[titleTable]:
            # for register in register_grouped:
            tbody += f"""<tr>
               <td>{register.EtiquetaDeFila}</td>
               <td>{register.PromedioPreg}</td>
            </tr>
            """
         # table = table.join(tbody)

         tfooter= """</tbody>
         </table>"""
      table = ''.join([table,tbody,tfooter])
      return table
   
   def MailBody(self, content):
      image = """
         'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABXgAAAH0CAYAAACHNkWHAAAACXBIWXMAAAsTAAALEwEAmpwYAAANFmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTA0LTEyVDA4OjM2OjU5LTA1OjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIyLTA0LTEyVDA4OjUzOjA5LTA1OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0wNC0xMlQwODo1MzowOS0wNTowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MzJlNmFhMzYtMTBkNC00OWQwLWE3ZjAtYjA1OWFiZmNjMTViIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ODE5ZWE0MjgtNjcyZS1iYTQ3LTg1NTYtYTdjYzY1YzJmNTZmIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZjA1YjkxMWMtYzc5ZS00OTdmLTlkZGItNjk1MTJmZTRmODJmIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmYwNWI5MTFjLWM3OWUtNDk3Zi05ZGRiLTY5NTEyZmU0ZjgyZiIgc3RFdnQ6d2hlbj0iMjAyMi0wNC0xMlQwODozNjo1OS0wNTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjkxMmQ1YmQyLWQxNTktNDM4NS1iNzg3LTZjZTczYmU4NmZjMCIgc3RFdnQ6d2hlbj0iMjAyMi0wNC0xMlQwODo1MzowOS0wNTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNvbnZlcnRlZCIgc3RFdnQ6cGFyYW1ldGVycz0iZnJvbSBhcHBsaWNhdGlvbi92bmQuYWRvYmUucGhvdG9zaG9wIHRvIGltYWdlL3BuZyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iZGVyaXZlZCIgc3RFdnQ6cGFyYW1ldGVycz0iY29udmVydGVkIGZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmciLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjMyZTZhYTM2LTEwZDQtNDlkMC1hN2YwLWIwNTlhYmZjYzE1YiIgc3RFdnQ6d2hlbj0iMjAyMi0wNC0xMlQwODo1MzowOS0wNTowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDx4bXBNTTpJbmdyZWRpZW50cz4gPHJkZjpCYWc+IDxyZGY6bGkgc3RSZWY6bGlua0Zvcm09IlJlZmVyZW5jZVN0cmVhbSIgc3RSZWY6ZmlsZVBhdGg9ImNsb3VkLWFzc2V0Oi8vY2MtYXBpLXN0b3JhZ2UuYWRvYmUuaW8vYXNzZXRzL2Fkb2JlLWxpYnJhcmllcy81NmMwNzcwNS01OGYzLTQ2YjAtYmZjNS1lZTVmMDFiNDNmZWY7bm9kZT0yYzZlOTZiNC02NmIwLTQyMzYtYWZmYy0zZDBkN2I0ZjI5MWUiIHN0UmVmOkRvY3VtZW50SUQ9InV1aWQ6ZDExNTY5OGYtZDc2YS02ODQzLTgxMGYtZTg0ZDVmZDhmYjRjIi8+IDxyZGY6bGkgc3RSZWY6bGlua0Zvcm09IlJlZmVyZW5jZVN0cmVhbSIgc3RSZWY6ZmlsZVBhdGg9ImNsb3VkLWFzc2V0Oi8vY2MtYXBpLXN0b3JhZ2UuYWRvYmUuaW8vYXNzZXRzL2Fkb2JlLWxpYnJhcmllcy81NmMwNzcwNS01OGYzLTQ2YjAtYmZjNS1lZTVmMDFiNDNmZWY7bm9kZT0yMjczODY2Yy0xODQ0LTQ5YzAtODQ0YS04NjRmYjkzYWM2NTYiIHN0UmVmOkRvY3VtZW50SUQ9InV1aWQ6YjVjOTA3MWUtOGU4Yi1hMjQwLWIwZTItMjQzYzAyMGNiZDhhIi8+IDxyZGY6bGkgc3RSZWY6bGlua0Zvcm09IlJlZmVyZW5jZVN0cmVhbSIgc3RSZWY6ZmlsZVBhdGg9ImNsb3VkLWFzc2V0Oi8vY2MtYXBpLXN0b3JhZ2UuYWRvYmUuaW8vYXNzZXRzL2Fkb2JlLWxpYnJhcmllcy81NmMwNzcwNS01OGYzLTQ2YjAtYmZjNS1lZTVmMDFiNDNmZWY7bm9kZT1kYzUzMDkzNS1kM2NhLTQ1YTEtYTZjMy1jNzM3NTY4MTI2N2IiIHN0UmVmOkRvY3VtZW50SUQ9InV1aWQ6ZjhhYjY3ZmQtZmM2Yy0xMDQ3LWEwMDItYTQ0ZTU2Y2Q0ZDE5Ii8+IDxyZGY6bGkgc3RSZWY6bGlua0Zvcm09IlJlZmVyZW5jZVN0cmVhbSIgc3RSZWY6ZmlsZVBhdGg9ImNsb3VkLWFzc2V0Oi8vY2MtYXBpLXN0b3JhZ2UuYWRvYmUuaW8vYXNzZXRzL2Fkb2JlLWxpYnJhcmllcy81NmMwNzcwNS01OGYzLTQ2YjAtYmZjNS1lZTVmMDFiNDNmZWY7bm9kZT01MGMxMjFhOC0xNGQxLTQwMGItOTdhZC00ZjkzNWYyMzdkZjYiIHN0UmVmOkRvY3VtZW50SUQ9InV1aWQ6MWQxNTNmYzAtOGRmZS05MTRkLWFlMWUtZDQ1N2I4NjExMTEwIi8+IDwvcmRmOkJhZz4gPC94bXBNTTpJbmdyZWRpZW50cz4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OTEyZDViZDItZDE1OS00Mzg1LWI3ODctNmNlNzNiZTg2ZmMwIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOmYwNWI5MTFjLWM3OWUtNDk3Zi05ZGRiLTY5NTEyZmU0ZjgyZiIgc3RSZWY6b3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmYwNWI5MTFjLWM3OWUtNDk3Zi05ZGRiLTY5NTEyZmU0ZjgyZiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PtM8FoMAAFldSURBVHgB7MEJoKWFwD/+z3NmmrRNe2m/LUipUI42WrWQCiFbtpDsyyviQe8he+K1a6E3JFvZSpZKmx4qrUSpadXepJpMM/P8f8zfqzT3zr0z9557znO+n09R17WIiIiIiIiIiIiI6D8tEREREREREREREdGXWiIiIiIiIiIiIiKiL7VERERERERERERERF9qiYiIiIiIiIiIiIi+1BIRERERERERERERfaklIiIiIiIiIiIiIvpSS0RERERERERERET0pZaIiIiIiIiIiIiI6EstEREREREREREREdGXWiIiIiIiIiIiIiKiL7VERERERERERERERF9qiYiIiIiIiIiIiIi+1BIRERERERERERERfaklIiIiIiIiIiIiIvpSS0RERERERERERET0pZaIiIiIiIiIiIiI6EstEREREREREREREdGXWiIiIiIiIiIiIiKiL7VERERERERERERERF9qiYiIiIiIiIiIiIi+1BIRERERERERERERfaklIiIiIiIiIiIiIvpSS0RERERERERERET0pZaIiIiIiIiIiIiI6EstEREREREREREREdGXWiIiIiIiIiIiIiKiL7VERERERERERERERF9qiYiIiIiIiIiIiIi+1BIRERERERERERERfaklIiIiIiIiIiIiIvpSS0RERERERERERET0pZaIiIiIiIiIiIiI6EstEREREREREREREdGXWiIiIiIiIiIiIiKiL7VERERERERERERERF9qiYiIiIiIiIiIiIi+1BIRERERERERERERfaklIiIiIiIiIiIiIvpSS0RERERERERERET0pani/xRFIaIp2p26hTWwLtbDulgZK2ElrIhVMB3LYioKTPdIM803G/fjbtyBO3En7sTtuA7XYQZuqcqiFhEREYtiRayHNbE21sCqWAkrYSUsi6UxHY/CUv5tBoZERERENFhd14KirmsxX1EUIvpNu1OvhCdgE2yCJ2B9rI2pJs9sXI+/4ApcjitweVUWd4uIiIgpeAw2wWbYBBthA6xg8czAkIiIiIgGq+taUNR1LeYrikJEL2t36lXRxtZo44lYTf+5CRfhN6hQVWVxt4iIiGZ7NHZAG208GUubGDMwJCIiIqLB6roWFHVdi/mKohDRS9qdeiPsgh3Rxgaa60qcj9Pxy6osrhcREdHfpmM37IGn4bG6ZwaGRERERDRYXdeCoq5rMV9RFCImU7tTr4ZdsAt2xXoG15/xc/wSp1dlcZeIiIjetyb2w3OwPaaaHDMwJCIiIqLB6roWFHVdi/mKohDRbe1OvSGeg32xLQrxn+bg1/gBTqrK4gYRERG9YzpejJdgOxQm3wwMiYiIiGiwuq4FRV3XYr6iKER0Q7tTb4oX4jl4ghir3+EHOLEqi6tERERMjm1wEJ6PpfSWGRgSERER0WB1XQuKuq7FfEVRiJgo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'/>
            </div>
            <div align="center">
         """

      # image = """'imagen'/>
      #          </div>
      #          <div align="center">"""

      first_part = """
         <!DOCTYPE html>
            <html>
            <head>
               <title>Report</title>
            
               <style type="text/css">
                  * {
                     font-family: sans-serif; /* Change your font family */
                  }
                  
                  .content-table {
                     border-collapse: collapse;
                     margin: 25px 0;
                     font-size: 1em;
                     width: 500px;
                     border-radius: 5px 5px 0 0;
                     overflow: hidden;
                     box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                  }
                  
                  .content-table thead tr {
                     background-color: blue;
                     color: #ffffff;
                     text-align: left;
                     font-weight: bold;
                  }
                  
                  .content-table th,
                  .content-table td {
                     padding: 12px 15px;
                     width: 100%;
                  }
                  
                  .content-table tbody tr {
                     border-bottom: 1px solid #dddddd;
                  }
                  
                  .content-table tbody tr:nth-of-type(even) {
                     background-color: #f3f3f3;
                  }
                  
                  .content-table tbody tr:last-of-type {
                     border-bottom: 2px solid #009879;
                  }
                  
                  .content-table tbody tr.active-row {
                     font-weight: bold;
                     color: #009879;
                  }
               </style>
            </head>
            <body>
               <div align="center">
                  <img width="200" height="100" src="""

      last_part = """
            </div>
         </body>
      </html>
      """

      htmlContent = (''.join([first_part,image,content,last_part]))
      # print(htmlContent)
      self.EmailSender(htmlContent)
      pass


if __name__ == '__main__':
   email = SendEmail("hola mundo")