import smtplib
import os.path
import json

from email.message          import EmailMessage
from email.headerregistry   import Address
from jinja2                 import Environment, select_autoescape, FileSystemLoader
from modelo                 import DatosCorreo

class Correo:
    # variable de entorno para la API de jinja2
    ENV = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    # constructor de la clase - cada correo tiene un email que recibe, un servidor que recibe, un nombre del que recibe y el modelo con los datos
    def __init__(self, tipo, emaRec, serRec, namRec, datosCorreo: DatosCorreo):
        # lee desde un archivo json los datos del servidor de correo que remite
        with open(os.path.join('json', 'sercorreo.json'), 'r') as conex:
            arc = json.load(conex)
        
        self._emaEnv        = arc[tipo]["emailRemitente"] 
        self._serEnv        = arc[tipo]["servidorRemitente"] 
        self._namEnv        = arc[tipo]["nombreRemitente"] 
        self._asunto        = arc[tipo]["asunto"] 
        self._templa        = arc[tipo]["template"]

        self._emaRec        = emaRec            # email destino
        self._serRec        = serRec            # servidor destino
        self._namRec        = namRec            # nombre destino
        self._datosCorreo   = datosCorreo       # datos del correo
        
        self._email_message = EmailMessage()    # contiene el empaquetado que se va a enviar 

    # renderiza la plantilla -template- con los datos -modelo-
    def render_html(self):
        return Correo.ENV.get_template(self._templa).render(datosCorreo=self._datosCorreo, asunto = self._asunto)

    # construye el cuerpo del email con los datos pasados en el parametro
    def build_email(self):
        self._email_message["Subject"]    = self._asunto
        self._email_message["From"]       = Address(username=self._emaEnv, domain=self._serEnv, display_name=self._namEnv)
        self._email_message["To"]         = Address(username=self._emaRec, domain=self._serRec, display_name=self._namRec)
        html_data: str                    = self.render_html()
        self._email_message.add_alternative(html_data, subtype="html")

    # metodo que envia el email
    def send_email(self):
        self.build_email()
        remitente       = self._emaEnv + "@" + self._serEnv
        destinatario    = self._emaRec + "@" + self._serRec

        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, "ddycjigkgqrtsray") # para enviar correo desde la cuenta formacionvirtualcsf@gmail.com
        smtp.sendmail(remitente, destinatario, self._email_message.as_string())
        smtp.quit()


from modelo import Instructor
if __name__ == '__main__':
    datosCorreo = DatosCorreo(  
                                instructor = Instructor(
                                                cedula                  = '99999999'                ,    
                                                nombre                  = 'LEONARDO'                ,
                                                vinculacion             = 'Planta'                  , 
                                                correo                  = 'leo66@homtail.com'       , 
                                                correo2                 = None                      , 
                                                competencia             = 'COM'
                                            ),
                                fichas     = [
                                                [   'TECNOLOGO'                             ,
                                                    'ANALISIS Y DESARROLLO DE SOFTWARE'     ,
                                                    '999239'                                ,
                                                    '15-SEP-2022'                           ,
                                                    '98'                                    ,
                                                    'MARIA'                                 ,
                                                    '23-mar-2024'                           ,
                                                    '22-may-2024'
                                                ],
                                                [   'TECNICO'                               ,
                                                    'CONTABILIDAD'                          ,
                                                    '999128'                                ,
                                                    '15-SEP-2022'                           ,
                                                    '98'                                    ,
                                                    'MARI0 de LAS PAVAS Y OTROS APellidos'  ,
                                                    '23-mar-2024'                           ,
                                                    '22-may-2024'
                                                ],
                                            ],
                                descripcion_competencia = 'COMPETENCIA DE PRUEBA'
                            )

    correo = Correo('TRANS','lhernandezs', 'sena.edu.co', 'LeonardoSENA', datosCorreo)
    correo.send_email() 

