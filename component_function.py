import os
import webbrowser
import subprocess


def open_html_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Diretório do script atual
    file_path = os.path.join(script_dir, 'Comprovante/operacao.html')  # Caminho completo para o arquivo HTML

    # Configura o Brave como navegador padrão
    webbrowser.register('brave', None, webbrowser.BackgroundBrowser('C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'))

    # Abre o arquivo HTML no navegador padrão (que será o Brave)
    webbrowser.get('brave').open(file_path)


    webbrowser.open(file_path)