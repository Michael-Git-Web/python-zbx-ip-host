from pyzabbix import ZabbixAPI
import time
import csv

# Autenticação no zabbix
zapi = ZabbixAPI('http://192.168.0.120/zabbix/')
zapi.login('Admin', 'zabbix')

# Função que recebe o IP e nome do host e manda para o zabbix
def create_host(ip, name):

    try:
        zapi.host.create(
            host = name,
            groups = [{"groupid": "20"}],
            interfaces = [
                {
                    "type": 2, # 1 Agent / 2 SNMP
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": 1,
                        "bulk": 1,
                        "community": "{$SNMP_COMMUNITY}"
                    },
                }
            ],
            macros = [
                {
                    "macro": "{$SNMP_COMMUNITY}",
                    "value": name
                }
            ],
            templates = [
                {
                    "templateid": 10698
                }
            ]
        )

        print(f'{name} cadastrado com sucesso!')
    except Exception as erro:
        print(erro)

start = time.time()
# Abri arquivo hosts.csv
with open('hosts.csv') as file:

    # Separa as colunas do arquivo
    file_hosts = csv.reader(file, delimiter = ';')

    # Laço de repetição para criar hosts, primeira coluna IP, segunda coluna nome do host
    qtdHost = 0
    for host in file_hosts:
        qtdHost += 1
        create_host(host[0], host[1])

end = time.time()
duracao = (end-start)

print(f'\n{qtdHost} hosts criados em {duracao:.2f} segundos.\n')
