import os
import subprocess
import argparse

SSH_DIR = os.path.expanduser("~/.sshkeys_dio_project")

def ensure_ssh_dir():
    if not os.path.exists(SSH_DIR):
        os.makedirs(SSH_DIR)


def generate_key(username):
    ensure_ssh_dir()
    key_path = os.path.join(SSH_DIR, f"{username}_id_ed25519")
    if os.path.exists(key_path):
        print(f"[!] A chave SSH para {username} já existe.")
        return
    
    subprocess.run([
        "ssh-keygen", "-t", "ed25519", "-f", key_path, "-N", ""
    ])
    print(f"[+] Chave SSH criada para {username}: {key_path}")


def list_keys():
    ensure_ssh_dir()
    keys = [f for f in os.listdir(SSH_DIR) if f.endswith("_id_ed25519")]
    if not keys:
        print("[!] Nenhuma chave SSH encontrada.")
        return
    
    print("Chaves SSH disponíveis:")
    for key in keys:
        print(f"- {key.replace('_id_ed25519', '')}")


def export_key(username, output_file):
    key_path = os.path.join(SSH_DIR, f"{username}_id_ed25519.pub")
    if not os.path.exists(key_path):
        print(f"[!] Chave pública para {username} não encontrada.")
        return
    
    with open(key_path, "r") as f:
        public_key = f.read().strip()
    
    with open(output_file, "w") as f:
        f.write(public_key + "\n")
    
    print(f"[+] Chave pública exportada para {output_file}")


def rotate_key(username):
    key_path = os.path.join(SSH_DIR, f"{username}_id_ed25519")
    if os.path.exists(key_path):
        os.remove(key_path)
        os.remove(key_path + ".pub")
        print(f"[!] Chave antiga removida para {username}")
    generate_key(username)


def main():
    parser = argparse.ArgumentParser(description="SSH Key Management for Teams")
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", help="Generate SSH key for a user")
    gen_parser.add_argument("--user", required=True, help="Username")
    
    list_parser = subparsers.add_parser("list", help="List existing SSH keys")
    
    export_parser = subparsers.add_parser("export", help="Export SSH public key")
    export_parser.add_argument("--user", required=True, help="Username")
    export_parser.add_argument("--output", required=True, help="Output file")
    
    rotate_parser = subparsers.add_parser("rotate", help="Rotate SSH key for a user")
    rotate_parser.add_argument("--user", required=True, help="Username")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        generate_key(args.user)
    elif args.command == "list":
        list_keys()
    elif args.command == "export":
        export_key(args.user, args.output)
    elif args.command == "rotate":
        rotate_key(args.user)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
