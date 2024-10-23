import os
import shutil
import subprocess
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, messagebox, Frame
from modules.capturar_id import capture_session_id  # Importa a função para capturar o ID da sessão

def install_printer_interface():
    # Cria a janela da interface de instalação da impressora
    window = Tk()
    window.title("Instalar Impressora Remotamente")
    window.geometry("300x300")

    # Campo para o hostname
    Label(window, text="Hostname da Máquina:").place(x=10, y=10)
    host_entry = Entry(window)
    host_entry.place(x=10, y=40, width=280)

    # Variável para o modelo da impressora
    model_type = StringVar(window)
    model_type.set("Kyocera")  # Padrão é Kyocera
    Label(window, text="Modelo da Impressora:").place(x=10, y=80)
    model_type_menu = OptionMenu(window, model_type, "Kyocera", "Epson", command=lambda _: toggle_printer_type())
    model_type_menu.place(x=10, y=110, width=280)

    # Frame para o tipo de impressora
    type_frame = Frame(window)
    type_frame.place(x=10, y=140)

    # Variável para o tipo de impressora
    printer_type = StringVar(window)
    printer_type.set("3655")  # Padrão é 3655
    Label(type_frame, text="Tipo de Impressora:").pack(side="left")
    printer_type_menu = OptionMenu(type_frame, printer_type, "3655", "308")
    printer_type_menu.pack(side="left")

    # Campo para o nome da impressora
    Label(window, text="Nome da Impressora:").place(x=10, y=180)
    printer_name_entry = Entry(window)
    printer_name_entry.place(x=10, y=210, width=280)

    # Função para instalar a impressora
    def install_printer():
        hostname = host_entry.get()
        printer_name = printer_name_entry.get()

        if not hostname or not printer_name:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # Captura o ID da sessão
        session_id = capture_session_id(hostname)
        if session_id is None:
            messagebox.showwarning("Aviso", "Não foi possível capturar o ID da sessão.")
            return

        # Caminho do executável da impressora
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Install_printer'))
        print(f"Caminho base: {base_dir}")

        kyocera_path = os.path.join(base_dir, 'kyocera.exe')
        epson_path = os.path.join(base_dir, 'install_epson.exe')
        epson_exe_path = os.path.join(base_dir, 'epson.exe')
        config_path = os.path.join(base_dir, 'config.txt')
        epconfig_path = os.path.join(base_dir, 'epconfig.txt')
        impressora_path = os.path.join(base_dir, 'impressora.exe')  # Caminho do impressora.exe

        # Verifique se os arquivos existem
        for path in [kyocera_path, epson_path, epson_exe_path, impressora_path]:
            if not os.path.exists(path):
                print(f"Arquivo não encontrado: {path}")
                messagebox.showerror("Erro", f"Arquivo não encontrado: {path}")
                return

        # Se for Kyocera
        if model_type.get() == "Kyocera":
            printer_type_value = printer_type.get()
            # Criação/alteração do config.txt
            with open(config_path, 'w') as config_file:
                config_file.write(f"{printer_type_value}\n{printer_name}")

            remote_kyocera_path = f"\\\\{hostname}\\C$\\Temp\\kyocera.exe"
            remote_config_path = f"\\\\{hostname}\\C$\\Temp\\config.txt"
            remote_exe_path = f"\\\\{hostname}\\C$\\Temp\\impressora.exe"

            # Copiar os arquivos para a máquina remota
            try:
                shutil.copy(kyocera_path, remote_kyocera_path)
                shutil.copy(config_path, remote_config_path)
                shutil.copy(impressora_path, remote_exe_path)
                messagebox.showinfo("Sucesso", "Arquivos transferidos com sucesso.")
            except Exception as e:
                print(f"Erro ao transferir arquivos Kyocera: {e}")
                messagebox.showerror("Erro", f"Erro ao transferir arquivos: {e}")
                return

            # Executar o instalador na máquina remota
            psexec_command = f'psexec \\\\{hostname} -s -i {session_id} cmd /c "{remote_exe_path}"'
            print(f"Executando comando: {psexec_command}")

            try:
                subprocess.run(psexec_command, shell=True, check=True)
                messagebox.showinfo("Sucesso", "Instalação da impressora iniciada.")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar psexec: {e}")
                messagebox.showerror("Erro", f"Erro ao executar o instalador: {e}")

        # Se for Epson
        elif model_type.get() == "Epson":
            with open(epconfig_path, 'w') as epconfig_file:
                epconfig_file.write(f"{printer_name}")

            remote_epson_path = f"\\\\{hostname}\\C$\\Temp\\install_epson.exe"
            remote_epconfig_path = f"\\\\{hostname}\\C$\\Temp\\epconfig.txt"
            remote_epson_exe_path = f"\\\\{hostname}\\C$\\Temp\\epson.exe"

            # Copiar os arquivos para a máquina remota
            try:
                shutil.copy(epson_path, remote_epson_path)
                shutil.copy(epconfig_path, remote_epconfig_path)
                shutil.copy(epson_exe_path, remote_epson_exe_path)
                messagebox.showinfo("Sucesso", "Arquivos transferidos com sucesso.")
            except Exception as e:
                print(f"Erro ao transferir arquivos Epson: {e}")
                messagebox.showerror("Erro", f"Erro ao transferir arquivos: {e}")
                return

            # Executar o instalador na máquina remota
            psexec_command = f'psexec \\\\{hostname} -s -i {session_id} cmd /c "{remote_epson_path}"'
            print(f"Executando comando: {psexec_command}")

            try:
                subprocess.run(psexec_command, shell=True, check=True)
                messagebox.showinfo("Sucesso", "Instalação da impressora iniciada.")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar psexec: {e}")
                messagebox.showerror("Erro", f"Erro ao executar o instalador: {e}")

    # Botão para instalar a impressora
    install_button = Button(window, text="Instalar Impressora", command=install_printer)
    install_button.place(x=10, y=240, width=280)

    # Função para mostrar/ocultar o tipo de impressora
    def toggle_printer_type():
        if model_type.get() == "Epson":
            type_frame.place_forget()  # Oculta o frame de tipo de impressora
        else:
            type_frame.place(x=10, y=140)  # Mostra o frame de tipo de impressora

    # Mantém a janela aberta
    window.mainloop()

# Para testar, você pode descomentar a linha abaixo.
# install_printer_interface()
