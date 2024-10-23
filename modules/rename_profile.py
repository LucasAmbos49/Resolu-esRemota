# modules/rename_profile.py
import subprocess
import os
from tkinter import messagebox
import getpass
import datetime

# Caminho para o PsExec e o script BAT local
PSEXEC_PATH = r"C:\Windows\System32\psexec.exe"
BAT_PATH_LOCAL = r"D:\teste.bat"

def log_renomeacao(hostname, username):
    usuario = getpass.getuser()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Cria a pasta 'logs' se não existir
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file_name = os.path.join(log_dir, f"{usuario}Log.txt")

    with open(log_file_name, "a") as log_file:
        log_file.write(f"{usuario} refez o perfil do {username} no computador {hostname} em {data_hora}\n")

def execute_refazer_perfil(hostname, username):
    """
    Função para renomear o perfil de usuário em uma máquina remota.
    Ela abre o CMD localmente e executa o comando PsExec para rodar o script BAT na máquina remota.
    """
    try:
        # Verifica se o arquivo BAT existe
        if not os.path.exists(BAT_PATH_LOCAL):
            messagebox.showerror("Erro", f"O arquivo {BAT_PATH_LOCAL} não foi encontrado.")
            return

        # Comando para abrir o CMD na máquina local e executar o psexec
        command = f'start cmd /k "{PSEXEC_PATH} \\\\{hostname} -s {BAT_PATH_LOCAL} {username}"'
        subprocess.Popen(command, shell=True)

        # Log da renomeação
        log_renomeacao(hostname, username)

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", "O comando para renomear o perfil foi enviado. Verifique o CMD para detalhes.")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar comando remoto: {e}")
