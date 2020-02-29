import os
import subprocess
import paramiko
import socket
import pysftp as sftp
import threading
import time
import sys
conexa = ""
host='192.168.43.14'
port=22

class conexao:
	def __init__(self,host,port):
		self.host=host
		self.port=port	
	def comunicacao(self):
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#Capturar o ip do host.
	    
		try:
			client.connect(host,username='victor-server',password='senha77')
			paramiko.util.log_to_file("filename.log") 
			print('Conexão efetuada com sucesso')
    	
		except:
			print("Erro ao conectar")
	
		ssh=client.get_transport()

		stdin,stdout,stderr=client.exec_command('pwd')
		outlines=stdout.readlines()
		resp=''.join(outlines)
		conexa = resp 

		print(resp)
		conexao_ssh = client
		client.close()

def cria_inventario():
	var = subprocess.getoutput("ls")
	type(var)
        
	print(str(var))       

def le_envia_ftp():

	full_path = os.path.abspath('inventario.txt')
	print(full_path)

	var = subprocess.getoutput("ls")
	type(var)
	print(str(var))
	file = open('inventario.txt',"w")
	file.write(var)
	file.close() 
	print(full_path)

	##depois de alimentar o arquivo de inventario do cliente kali, vamos replica-lo ao servidor, 
	##lendo seu conteudo, chamando a conex ssh e alimentando outro invent la


	f = open(full_path, 'r+')

	for linha_path in f.readlines():
		cada_file_full = os.path.abspath(linha_path)
		print(cada_file_full)##exemplo para ver o que a linha retorna antes de enviar o arquivo
	#Colocar o comando de envio ftp para cada caminhd de arquivo capturado por linha

		#UPLOAD

		cnopts = sftp.CnOpts()
		cnopts.hostkeys = None
		s = sftp.Connection(host=host, username='victor-server', password='senha77', cnopts=cnopts)

		local_path_upload= '/home/victor/Desktop/origem/'+linha_path.replace('\n', '')

		remote_path_upload = '/home/victor-server/arquivos/'+linha_path.replace('\n', '')

		s.put(local_path_upload, remote_path_upload)
		s.close()

t=conexao(host,port)
t.comunicacao()

def sinc():    
	for i in range(0,3):
		le_envia_ftp()
		time.sleep(15)
    
s = threading.Thread(target=sinc)

acao = input('Deseja fazer o upload dos seus dados? [s/n]\n')
if(acao.lower()=='s'):
	print(acao)
	s.start()
else: 
	sys.exit()
