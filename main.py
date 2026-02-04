#!/usr/bin/env python3
"""
NTL-SysToolbox - Outil d'administration système pour NordTransit Logistics
Point d'entrée principal avec menu interactif CLI
"""

import sys
import os
from datetime import datetime

# Ajout du répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.diagnostic import DiagnosticModule
from modules.backup import BackupModule
from modules.audit import AuditModule
from utils.logger import Logger
from utils.output import OutputManager

class NTLSysToolbox:
    """Classe principale de l'application"""
    
    def __init__(self):
        self.logger = Logger()
        self.output_manager = OutputManager()
        self.diagnostic = DiagnosticModule(self.logger, self.output_manager)
        self.backup = BackupModule(self.logger, self.output_manager)
        self.audit = AuditModule(self.logger, self.output_manager)
        
    def display_banner(self):
        """Affiche la bannière de l'application"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║           NTL-SysToolbox v1.0                             ║
║     Outil d'administration système et réseau              ║
║     NordTransit Logistics - Hauts-de-France               ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"Session démarrée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
    
    def display_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Module Diagnostic")
        print("   └─ Vérifier l'état des services et serveurs")
        print("\n2. Module Sauvegarde WMS")
        print("   └─ Sauvegarder la base de données métier")
        print("\n3. Module Audit d'obsolescence")
        print("   └─ Scanner le réseau et vérifier les versions EOL")
        print("\n4. Afficher les logs")
        print("\n0. Quitter")
        print("="*60)
    
    def diagnostic_submenu(self):
        """Sous-menu du module diagnostic"""
        while True:
            print("\n" + "-"*60)
            print("MODULE DIAGNOSTIC")
            print("-"*60)
            print("1. Vérifier les services AD/DNS")
            print("2. Tester la base de données MySQL")
            print("3. État d'un serveur Windows")
            print("4. État d'un serveur Linux")
            print("5. Tester la connexion (ping)")
            print("6. Diagnostic complet")
            print("0. Retour au menu principal")
            print("-"*60)
            
            choice = input("\nVotre choix : ").strip()
            
            if choice == "1":
                server = input("Adresse IP du contrôleur de domaine : ").strip()
                self.diagnostic.check_ad_dns(server)
            elif choice == "2":
                host = input("Adresse IP du serveur MySQL : ").strip()
                port = input("Port MySQL (défaut 3306) : ").strip() or "3306"
                database = input("Nom de la base de données : ").strip()
                user = input("Utilisateur MySQL : ").strip()
                password = input("Mot de passe MySQL : ").strip()
                self.diagnostic.check_mysql(host, int(port), database, user, password)
            elif choice == "3":
                server = input("Adresse IP du serveur Windows : ").strip()
                user = input("Utilisateur WinRM (ex: Administrator) : ").strip()
                password = input("Mot de passe WinRM : ").strip()
                self.diagnostic.check_windows_server(server, user, password)
            elif choice == "4":
                server = input("Adresse IP du serveur Linux : ").strip()
                user = input("Utilisateur SSH : ").strip()
                auth_method = input("Méthode d'auth [1=mot de passe, 2=clé SSH] : ").strip()
                if auth_method == "2":
                    ssh_key = input("Chemin de la clé SSH : ").strip()
                    self.diagnostic.check_linux_server(server, user, ssh_key_path=ssh_key)
                else:
                    password = input("Mot de passe SSH : ").strip()
                    self.diagnostic.check_linux_server(server, user, password=password)
            elif choice == "5":
                host = input("Adresse IP ou nom d'hôte à tester : ").strip()
                self.diagnostic.test_ping(host)
            elif choice == "6":
                self.diagnostic.run_full_diagnostic()
            elif choice == "0":
                break
            else:
                print("❌ Choix invalide")
    
    def backup_submenu(self):
        """Sous-menu du module sauvegarde"""
        while True:
            print("\n" + "-"*60)
            print("MODULE SAUVEGARDE WMS")
            print("-"*60)
            print("1. Sauvegarde complète de la base (SQL)")
            print("2. Export d'une table (CSV)")
            print("3. Sauvegarde automatique (toutes les tables)")
            print("0. Retour au menu principal")
            print("-"*60)
            
            choice = input("\nVotre choix : ").strip()
            
            if choice == "1":
                host = input("Adresse IP du serveur MySQL : ").strip()
                port = input("Port MySQL (défaut 3306) : ").strip() or "3306"
                database = input("Nom de la base de données : ").strip()
                user = input("Utilisateur MySQL : ").strip()
                password = input("Mot de passe MySQL : ").strip()
                self.backup.backup_database(host, int(port), database, user, password)
            elif choice == "2":
                host = input("Adresse IP du serveur MySQL : ").strip()
                port = input("Port MySQL (défaut 3306) : ").strip() or "3306"
                database = input("Nom de la base de données : ").strip()
                table = input("Nom de la table à exporter : ").strip()
                user = input("Utilisateur MySQL : ").strip()
                password = input("Mot de passe MySQL : ").strip()
                self.backup.export_table_csv(host, int(port), database, table, user, password)
            elif choice == "3":
                host = input("Adresse IP du serveur MySQL : ").strip()
                port = input("Port MySQL (défaut 3306) : ").strip() or "3306"
                database = input("Nom de la base de données : ").strip()
                user = input("Utilisateur MySQL : ").strip()
                password = input("Mot de passe MySQL : ").strip()
                self.backup.backup_all_tables(host, int(port), database, user, password)
            elif choice == "0":
                break
            else:
                print("❌ Choix invalide")
    
    def audit_submenu(self):
        """Sous-menu du module audit"""
        while True:
            print("\n" + "-"*60)
            print("MODULE AUDIT D'OBSOLESCENCE")
            print("-"*60)
            print("1. Scanner une plage réseau")
            print("2. Vérifier les dates EOL d'un OS")
            print("3. Analyser un fichier CSV d'inventaire")
            print("4. Générer un rapport complet d'obsolescence")
            print("0. Retour au menu principal")
            print("-"*60)
            
            choice = input("\nVotre choix : ").strip()
            
            if choice == "1":
                network = input("Plage réseau (ex: 192.168.10.0/24) : ").strip()
                self.audit.scan_network(network)
            elif choice == "2":
                os_name = input("Nom de l'OS (ex: Windows Server 2012) : ").strip()
                self.audit.check_eol_dates(os_name)
            elif choice == "3":
                csv_file = input("Chemin du fichier CSV : ").strip()
                self.audit.analyze_csv_inventory(csv_file)
            elif choice == "4":
                network = input("Plage réseau à auditer (ex: 192.168.10.0/24) : ").strip()
                self.audit.generate_full_report(network)
            elif choice == "0":
                break
            else:
                print("❌ Choix invalide")
    
    def show_logs(self):
        """Affiche les derniers logs"""
        print("\n" + "-"*60)
        print("DERNIERS LOGS")
        print("-"*60)
        logs = self.logger.get_recent_logs(20)
        if logs:
            for log in logs:
                print(log)
        else:
            print("Aucun log disponible")
        print("-"*60)
    
    def run(self):
        """Lance l'application"""
        self.display_banner()
        self.logger.info("Application NTL-SysToolbox démarrée")
        
        while True:
            self.display_menu()
            choice = input("\nVotre choix : ").strip()
            
            if choice == "1":
                self.diagnostic_submenu()
            elif choice == "2":
                self.backup_submenu()
            elif choice == "3":
                self.audit_submenu()
            elif choice == "4":
                self.show_logs()
            elif choice == "0":
                print("\n✅ Fermeture de NTL-SysToolbox...")
                self.logger.info("Application NTL-SysToolbox arrêtée")
                print("Au revoir !\n")
                sys.exit(0)
            else:
                print("❌ Choix invalide. Veuillez saisir un nombre entre 0 et 4.")

def main():
    """Point d'entrée principal"""
    try:
        app = NTLSysToolbox()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur (Ctrl+C)")
        print("Au revoir !\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
