class Ping:
    def execute(self, ip):
        if ip.startswith("192."):
            print(f"Ping a {ip}:")
            for i in range(10):
                print(f"Respuesta {i+1} recibida")
        else:
            print("Error: El método execute solo admite direcciones 192.x.x.x")

    def executefree(self, ip):
        print(f"Ping libre a {ip}:")
        for i in range(10):
            print(f"Respuesta {i+1} recibida")

class PingProxy:
    def __init__(self, real_ping):
        self.real_ping = real_ping

    def execute(self, ip):
        # Lógica de redirección especial solicitada
        if ip == "192.168.0.254":
            print("Proxy: Redirigiendo caso especial a Google...")
            self.real_ping.executefree("www.google.com")
        else:
            print(f"Proxy: Procesando IP {ip} normalmente")
            self.real_ping.execute(ip)

# Test
ping_objeto = Ping()
proxy = PingProxy(ping_objeto)
proxy.execute("192.168.0.254") # Redirige
proxy.execute("192.168.0.1")   # Procesa normal