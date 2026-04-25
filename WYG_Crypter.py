import os
import base64
import hashlib
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

# تفعيل الألوان في الكونسول
init(autoreset=True)

# قاموس الطلاسم (لتحويل النص المشفر إلى رموز غريبة)
RUNES = {
    '0': 'ᛀ', '1': 'ᛁ', '2': 'ᛂ', '3': 'ᛃ', '4': 'ᛄ', '5': 'ᛅ', '6': 'ᛆ', '7': 'ᛇ',
    '8': 'ᛈ', '9': 'ᛉ', 'a': 'ᛊ', 'b': 'ᛋ', 'c': 'ᛌ', 'd': 'ᛍ', 'e': 'ᛎ', 'f': 'ᛏ'
}
INV_RUNES = {v: k for k, v in RUNES.items()}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    clear_screen()
    logo = f"""{Fore.RED}{Style.BRIGHT}
    ██╗    ██╗██╗   ██╗ ██████╗     ██╗  ██╗██╗   ██╗██████╗ 
    ██║    ██║╚██╗ ██╔╝██╔════╝     ██║  ██║██║   ██║██╔══██╗
    ██║ █╗ ██║ ╚████╔╝ ██║  ███╗    ███████║██║   ██║██████╔╝
    ██║███╗██║  ╚██╔╝  ██║   ██║    ██╔══██║██║   ██║██╔══██╗
    ╚███╔███╔╝   ██║   ╚██████╔╝    ██║  ██║╚██████╔╝██████╔╝
     ╚══╝╚══╝    ╚═╝    ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
    {Style.RESET_ALL}"""
    print(logo)
    print(f"{Fore.DARKGRAY}    >> Advanced Encryption/Decryption Tool | By WYG\n")

def generate_key(password):
    # توليد مفتاح تشفير قوي بناءً على الباسورد
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def to_runes(hex_str):
    return ''.join(RUNES.get(c, c) for c in hex_str)

def from_runes(rune_str):
    return ''.join(INV_RUNES.get(c, c) for c in rune_str)

def process_file(file_path, mode, level, password):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        fernet = Fernet(generate_key(password))

        if mode == 'encrypt':
            if level == '1': # Good
                result = fernet.encrypt(data)
                ext = ".good"
            elif level == '2': # Evil
                # تشفير ثم تحويل إلى Hex ثم عكس النص
                enc = fernet.encrypt(data)
                result = enc.hex()[::-1].encode()
                ext = ".evil"
            elif level == '3': # Ultimate (طلاسم)
                # تشفير، تحويل إلى Hex، ثم استبدالها بطلاسم
                enc = fernet.encrypt(data)
                hex_data = enc.hex()
                result = to_runes(hex_data).encode('utf-8')
                ext = ".magic"
            
            out_file = file_path + ext
            with open(out_file, 'wb') as f:
                f.write(result)
            print(f"\n{Fore.GREEN}[+] تم التشفير بنجاح! الملف الجديد: {out_file}")

        elif mode == 'decrypt':
            if level == '1':
                result = fernet.decrypt(data)
            elif level == '2':
                # إرجاع النص المعكوس ثم فك الـ Hex ثم فك التشفير
                rev_hex = data.decode()[::-1]
                enc = bytes.fromhex(rev_hex)
                result = fernet.decrypt(enc)
            elif level == '3':
                # فك الطلاسم إلى Hex ثم فك التشفير
                runes_str = data.decode('utf-8')
                hex_data = from_runes(runes_str)
                enc = bytes.fromhex(hex_data)
                result = fernet.decrypt(enc)
            
            out_file = file_path.replace(".good", "").replace(".evil", "").replace(".magic", "") + "_decrypted"
            with open(out_file, 'wb') as f:
                f.write(result)
            print(f"\n{Fore.GREEN}[+] تم فك التشفير بنجاح! الملف الجديد: {out_file}")

    except Exception as e:
        print(f"\n{Fore.RED}[!] حدث خطأ! تأكد من الباسورد أو أنك اخترت المستوى الصحيح لفك التشفير.\nتفاصيل الخطأ: {e}")

def main():
    print_logo()
    print(f"{Fore.YELLOW}1- تشفير (Encrypt)")
    print(f"{Fore.YELLOW}2- فك تشفير (Decrypt)")
    
    choice = input(f"\n{Fore.CYAN}اختر (1/2): {Style.RESET_ALL}")
    
    if choice not in ['1', '2']:
        print(f"{Fore.RED}خيار غير صحيح!")
        return

    print(f"\n{Fore.YELLOW}مستويات التشفير:")
    print(f"1- Good     (تشفير قياسي قوي)")
    print(f"2- Evil     (تشفير معقد ومقلوب)")
    print(f"3- Ultimate (طلاسم سحرية لا تقرأ)")
    
    level = input(f"\n{Fore.CYAN}اختر المستوى (1/2/3): {Style.RESET_ALL}")
    
    if level not in ['1', '2', '3']:
        print(f"{Fore.RED}مستوى غير صحيح!")
        return

    file_path = input(f"\n{Fore.CYAN}اسحب الملف هنا أو اكتب مساره: {Style.RESET_ALL}").strip('\"')
    password = input(f"{Fore.CYAN}أدخل باسورد التشفير/فك التشفير: {Style.RESET_ALL}")

    if not os.path.exists(file_path):
        print(f"{Fore.RED}[!] الملف غير موجود!")
        return

    mode = 'encrypt' if choice == '1' else 'decrypt'
    process_file(file_path, mode, level, password)

if __name__ == "__main__":
    main()
    