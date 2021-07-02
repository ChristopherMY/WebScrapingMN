# Importar libreria tinker {sirve crear app de escritorio}
import pandas as pd

import tkinter as tk

import src.progressbar as pg
import src.whatsapp
import src.campaña

from pandas.core.reshape.concat import concat
from PIL import Image, ImageTk
import sys
import os
import shutil

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    path_documents = os.path.expanduser(
        '~/Documents').replace('/', r'\ ').replace(' ', '')

from tkinter import messagebox
from tkinter.constants import NW, W
from src.tkinter_custom_button import TkinterCustomButton

# Crear instancia
window = tk.Tk()
window.geometry("480x800")
window.resizable(width=0, height=0)


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        # Icono de App
        ico = Image.open(r"{}\assets\img\48x48.png".format(application_path))
        photo = ImageTk.PhotoImage(ico)
        window.wm_iconphoto(False, photo)

    def createWidgets(self):
        self.config(height=800, width=480)

        self.background_image = tk.PhotoImage(
            file="./assets/img/480x800px.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=200, height=200,
                                bg='#F68302', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.place(x=130, y=100, anchor=NW)

        # Generate circle
        self.progressbar = pg.CircularProgressbar(
            self.canvas, 0, 0, 200, 200, 20)

        # Crear Button Personalizado

        button_2 = TkinterCustomButton(
            text="Ver Numeros", corner_radius=10, text_color="#F68302", width=140, height=40, hover_color="#eac3b7",
            bg_color="#F68302",  fg_color="white", command=self.verNumeros)
        button_2.place(relx=0.20, rely=0.75, anchor=tk.CENTER)

        button_4 = TkinterCustomButton(
            text="Ver Campaña", corner_radius=10, text_color="#F68302", width=140, height=40, hover_color="#eac3b7",
            bg_color="#F68302",  fg_color="white", command=self.verCampaña)
        button_4.place(relx=0.50, rely=0.75, anchor=tk.CENTER)

        button_2 = TkinterCustomButton(
            text="Ver Logs", corner_radius=10, text_color="#F68302", width=140, height=40, hover_color="#eac3b7",
            bg_color="#F68302",  fg_color="white", command=self.verLogs)
        button_2.place(relx=0.80, rely=0.75, anchor=tk.CENTER)

        button_5 = TkinterCustomButton(
            text="Obtener Numeros", corner_radius=10, text_color="#F68302", width=180, height=40, hover_color="#eac3b7",
            bg_color="#F68302",  fg_color="white", command=self.obtenerNumeros)
        button_5.place(relx=0.25, rely=0.85, anchor=tk.CENTER)

        button_3 = TkinterCustomButton(
            text="Enviar Campaña", corner_radius=10, text_color="#F68302", width=180, height=40, hover_color="#eac3b7",
            bg_color="#F68302",  fg_color="white", command=self.enviarCampaña)
        button_3.place(relx=0.7, rely=0.85, anchor=tk.CENTER)

    def start(self):
        self.progressbar.start()

    def pause(self):
        self.progressbar.toggle_pause()

    def step(self, aceleration):
        self.progressbar.step(aceleration)

    # Lanzamos mensaje
    def verNumeros(self):
        # Abrir Excel
        try:
            os.startfile(
                r'{}\assets\files\maestros\NumerosCampaña.xlsx'.format(application_path))
        except Exception:
            messagebox.showwarning(
                message="Aun no obtuvo los numeros de su WhatsApp", title="Abrir excel numeros de campaña")
            pass
        return True

    def verLogs(self):
        # Abrir Excel
        try:
            os.startfile(r'{}\assets\files\Logs'.format(application_path))
        except Exception:
            messagebox.showwarning(
                message="Aun no se registraron logs de uso", title="Abrir logs")
            pass
        return True

    def verCampaña(self):
        # Abrir Excel
        try:
            os.startfile(
                r'{}\assets\files\maestros\Campaña.xlsx'.format(application_path))
        except Exception:
            messagebox.showwarning(
                message="Ups, no encontramos el documento de campaña.", title="Abrir campaña")
            pass
        return True

    def obtenerNumeros(self):
        self.canvas.delete('all')

        # Generate circle
        self.progressbar = pg.CircularProgressbar(
            self.canvas, 0, 0, 200, 200, 20)

        self.start()
        whatsapp = src.whatsapp.WhatsApp(800)
        user_names = whatsapp.unread_usernames(scrolls=727)

        # Create row Header excel
        df = pd.DataFrame(columns=['Celular', 'Codigo_Pais'])

        row = 0
        for name in user_names:
            row = row + 1

            messages = whatsapp.get_last_message_for(name)

            if len(messages) != 0:
                split = messages.split()
                if len(split) == 2:
                    df.at[name, 'Celular'] = split[1]
                else:
                    df.at[name, 'Celular'] = split[1] + \
                        "" + split[2] + "" + split[3]

                df.at[name, 'Codigo_Pais'] = split[0]

        #now = datetime.now()
        #FFH = now.strftime("%Y%m%d_%H%M")
        #nombre = 'NumerosCampaña'
        # Registrar datos en excel

        self.step(40)

        try:
            df.to_excel(r'{}\assets\files\maestros\NumerosCampaña.xlsx'.format(
                application_path), index=False)
        except Exception:
            if messagebox.showwarning(message="Cierre el excel NumerosCampaña para poder continuar", title="Atención"):
                if messagebox.askyesno(message="¿Cerro el documento?", title="Numeros de Campaña"):
                    df.to_excel(r'{}\assets\files\maestros\NumerosCampaña.xlsx'.format(
                        application_path), index=False)
                    pass

        # Abrir Excel
        if messagebox.askyesno(message="¿Desea abrir documento?", title="Título"):
            os.startfile(
                r'{}\assets\files\maestros\NumerosCampaña.xlsx'.format(application_path))

        return True

    def registrarModulos(self):

        if os.path.exists(r'{}/MundoNegocio'.format(path_documents)) is False:
            os.mkdir(r"{}\MundoNegocio".format(path_documents))
            os.mkdir(r"{}\MundoNegocio\Logs".format(path_documents))

            contenidos = os.listdir(
                r"{}\assets\files\campaña".format(application_path))
            for elemento in contenidos:
                try:
                    print(
                        f"Copiando {elemento} --> {application_path}\\assets\\files\campaña ....", end="")
                    if os.path.exists(r'{}\MundoNegocio\Campaña'.format(path_documents)) is False:
                        os.mkdir(r"{}\MundoNegocio\Campaña".format(
                            path_documents))

                    src = os.path.join(r"{}\assets\files\campaña".format(
                        application_path), elemento)  # origen
                    dst = os.path.join(r"{}\MundoNegocio\Campaña".format(
                        path_documents), elemento)  # destino

                    shutil.copy(src, dst)
                    print("Correcto")
                except:
                    print("Falló")
                    print(
                        "Error, no se pudo copiar el archivo. Verifique los permisos de escritura")

            contenidos = os.listdir(
                r"{}\assets\files\maestros".format(application_path))
            for elemento in contenidos:
                try:
                    print(
                        f"Copiando {elemento} --> {application_path}\\assets\\files\maestros ....", end="")
                    if os.path.exists(r'{}\MundoNegocio\Maestros'.format(path_documents)) is False:
                        os.mkdir(r"{}\MundoNegocio\Maestros".format(
                            path_documents))

                    src = os.path.join(r"{}\assets\files\maestros".format(
                        application_path), elemento)  # origen
                    dst = os.path.join(r"{}\MundoNegocio\Maestros".format(
                        path_documents), elemento)  # destino

                    shutil.copy(src, dst)
                    print("Correcto")
                except:
                    print("Falló")
                    print(
                        "Error, no se pudo copiar el archivo. Verifique los permisos de escritura")

        return True

    def enviarCampaña(self):
        self.start()
        # Generate circle
        self.progressbar = pg.CircularProgressbar(
            self.canvas, 0, 0, 200, 200, 20)

        campaña = src.campaña.Campaña(400)
        if campaña.send_campaña():
            self.step(40)

        return True

    def get_correct_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
# Creamos nuestro titulo
if __name__ == '__main__':
    app = Application()
    app.master.title('App WebScraping WhatsApp')
    app.mainloop()