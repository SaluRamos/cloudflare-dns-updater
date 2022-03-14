import CloudFlare
import time
import requests
import os

os.system("cls")

time_between_updates = 600 #em segundos
cloudflare_token = ""
cf = CloudFlare.CloudFlare(token = cloudflare_token)
zones = cf.zones.get()
main_zone_id = ""
for zone in zones:
    if zone["name"] == "you website":
        main_zone_id = zone["id"]

frontend_dns_config = {"name":"@", "type":"A", "content":"", "ttl":1, "proxied": True}

# google_mx_1 = {"name":"@", "type":"MX", "content":"aspmx.l.google.com", "priority":1, "ttl":3600}
# google_mx_2 = {"name":"@", "type":"MX", "content":"alt1.aspmx.l.google.com", "priority":5, "ttl":3600}
# google_mx_3 = {"name":"@", "type":"MX", "content":"alt2.aspmx.l.google.com", "priority":5, "ttl":3600}
# google_mx_4 = {"name":"@", "type":"MX", "content":"alt3.aspmx.l.google.com", "priority":10, "ttl":3600}
# google_mx_5 = {"name":"@", "type":"MX", "content":"alt4.aspmx.l.google.com", "priority":10, "ttl":3600}

# def RemoveMXandTXT():
#     zone_dns = cf.zones.dns_records.get(main_zone_id)
#     for x in zone_dns:
#         if x["type"] == "MX" or x["type"] == "TXT":
#             cf.zones.dns_records.delete(main_zone_id, x["id"])

# def AddGoogleDNS():
#     RemoveMXandTXT()
#     cf.zones.dns_records.post(main_zone_id, data = google_mx_1)
#     cf.zones.dns_records.post(main_zone_id, data = google_mx_2)
#     cf.zones.dns_records.post(main_zone_id, data = google_mx_3)
#     cf.zones.dns_records.post(main_zone_id, data = google_mx_4)
#     cf.zones.dns_records.post(main_zone_id, data = google_mx_5)

def SystemTimeLog():
    return str(time.strftime("%d/%b at %H:%M:%S"))

def UpdateIPDNS():
    while True:
        try:
            print(f"{SystemTimeLog()} = NOVA VERIFICAÇÃO DE DNS!")
            my_ip = requests.get("https://api.ipify.org").content.decode("utf8")
            print(f"IPV4 atual = {my_ip}\n")
            frontend_dns_config["content"] = my_ip
            finded_backend_dns = False
            finded_frontend_dns = False
            zone_dns = cf.zones.dns_records.get(main_zone_id)
            for x in zone_dns:
                if x["type"] == "A" and x["name"] == "your website":
                    print("DNS 'your website' encontrado:")
                    if x["content"] != my_ip:
                        print("O ip cadastrado esta desatualizado!")
                        cf.zones.dns_records.delete(main_zone_id, x["id"])
                        print("dns deletado!")
                        cf.zones.dns_records.post(main_zone_id, data = frontend_dns_config)
                        print("dns adicionado!")
                    else:
                        print("ip esta atualizado!")
                    finded_frontend_dns = True
            if finded_frontend_dns == False:
                print("\nDNS 'your website' não encontrado:")
                cf.zones.dns_records.post(main_zone_id, data = frontend_dns_config)
                print("dns adicionado!\n")
            time.sleep(time_between_updates)
        except Exception as e:
            print(f"ocorreu um erro = {e}")
            print("tentando novamente!")

UpdateIPDNS()