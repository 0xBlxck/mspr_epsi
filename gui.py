#!/usr/bin/env python3
"""
NTL-SysToolbox - Interface graphique
Interface utilisateur graphique pour l'outil d'administration système
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime
import threading

# Ajout du répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.diagnostic import DiagnosticModule
from modules.backup import BackupModule
from modules.audit import AuditModule
from utils.logger import Logger
from utils.output import OutputManager


class NTLSysToolboxGUI:
    """Interface graphique principale de l'application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NTL-SysToolbox v1.0 - NordTransit Logistics")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Initialisation des modules
        self.logger = Logger()
        self.output_manager = OutputManager()
        self.diagnostic = DiagnosticModule(self.logger, self.output_manager)
        self.backup = BackupModule(self.logger, self.output_manager)
        self.audit = AuditModule(self.logger, self.output_manager)
        
        # Configuration du style
        self.setup_style()
        
        # Création de l'interface
        self.create_widgets()
        
        # Log de démarrage
        self.logger.info("Interface graphique NTL-SysToolbox démarrée")
        self.log_to_console("Application démarrée avec succès")
    
    def setup_style(self):
        """Configure le style de l'application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs personnalisées
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        style.configure('Module.TButton', font=('Arial', 11), padding=10)
        style.configure('Action.TButton', font=('Arial', 10), padding=5)
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # En-tête
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="NTL-SysToolbox",
            font=('Arial', 20, 'bold'),
            bg='#34495e',
            fg='white'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Outil d'administration système - NordTransit Logistics",
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        subtitle_label.pack()
        
        # Frame principal avec deux colonnes
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Colonne gauche - Modules
        left_frame = tk.Frame(main_frame, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        modules_label = ttk.Label(left_frame, text="MODULES", style='Title.TLabel')
        modules_label.pack(pady=(0, 10))
        
        # Boutons des modules
        self.create_module_buttons(left_frame)
        
        # Colonne droite - Console et résultats
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        console_label = ttk.Label(right_frame, text="CONSOLE & RÉSULTATS", style='Title.TLabel')
        console_label.pack(pady=(0, 10))
        
        # Zone de texte pour les résultats
        self.console = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Barre de statut
        status_frame = tk.Frame(self.root, bg='#95a5a6', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"Prêt - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            bg='#95a5a6',
            fg='white',
            font=('Arial', 9)
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def create_module_buttons(self, parent):
        """Crée les boutons des modules"""
        # Module Diagnostic
        diag_frame = tk.LabelFrame(parent, text="Module Diagnostic", font=('Arial', 11, 'bold'), padx=10, pady=10)
        diag_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            diag_frame,
            text="Vérifier AD/DNS",
            command=self.check_ad_dns_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            diag_frame,
            text="Tester MySQL",
            command=self.check_mysql_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            diag_frame,
            text="État serveur Windows",
            command=self.check_windows_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            diag_frame,
            text="État serveur Linux",
            command=self.check_linux_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            diag_frame,
            text="Tester connexion (ping)",
            command=self.test_ping_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            diag_frame,
            text="Diagnostic complet",
            command=self.run_full_diagnostic,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        # Module Sauvegarde
        backup_frame = tk.LabelFrame(parent, text="Module Sauvegarde WMS", font=('Arial', 11, 'bold'), padx=10, pady=10)
        backup_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            backup_frame,
            text="Sauvegarde complète (SQL)",
            command=self.backup_database_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            backup_frame,
            text="Export table (CSV)",
            command=self.export_table_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            backup_frame,
            text="Sauvegarde automatique",
            command=self.backup_all_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        # Module Audit
        audit_frame = tk.LabelFrame(parent, text="Module Audit d'obsolescence", font=('Arial', 11, 'bold'), padx=10, pady=10)
        audit_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            audit_frame,
            text="Scanner réseau",
            command=self.scan_network_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            audit_frame,
            text="Vérifier dates EOL",
            command=self.check_eol_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            audit_frame,
            text="Analyser CSV",
            command=self.analyze_csv_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            audit_frame,
            text="Rapport complet",
            command=self.generate_report_dialog,
            style='Action.TButton'
        ).pack(fill=tk.X, pady=2)
        
        # Boutons utilitaires
        utils_frame = tk.Frame(parent)
        utils_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            utils_frame,
            text="Effacer console",
            command=self.clear_console
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            utils_frame,
            text="Quitter",
            command=self.quit_app
        ).pack(fill=tk.X, pady=2)
    
    def log_to_console(self, message, level="INFO"):
        """Affiche un message dans la console"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        color_tag = {
            "INFO": "info",
            "SUCCESS": "success",
            "WARNING": "warning",
            "ERROR": "error"
        }.get(level, "info")
        
        self.console.tag_config("info", foreground="#3498db")
        self.console.tag_config("success", foreground="#2ecc71")
        self.console.tag_config("warning", foreground="#f39c12")
        self.console.tag_config("error", foreground="#e74c3c")
        
        self.console.insert(tk.END, f"[{timestamp}] ", "info")
        self.console.insert(tk.END, f"{message}\n", color_tag)
        self.console.see(tk.END)
        self.root.update()
    
    def clear_console(self):
        """Efface la console"""
        self.console.delete(1.0, tk.END)
        self.log_to_console("Console effacée")
    
    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_label.config(text=f"{message} - {datetime.now().strftime('%H:%M:%S')}")
    
    def run_in_thread(self, func, *args):
        """Exécute une fonction dans un thread séparé"""
        thread = threading.Thread(target=func, args=args, daemon=True)
        thread.start()
    
    # Dialogues pour le module Diagnostic
    def check_ad_dns_dialog(self):
        """Dialogue pour vérifier AD/DNS"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Vérifier AD/DNS")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP du contrôleur de domaine:", font=('Arial', 10)).pack(pady=10)
        server_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        server_entry.pack(pady=5)
        server_entry.insert(0, "192.168.10.10")
        
        def execute():
            server = server_entry.get().strip()
            if server:
                dialog.destroy()
                self.log_to_console(f"Vérification AD/DNS sur {server}...", "INFO")
                self.update_status("Vérification AD/DNS en cours...")
                self.run_in_thread(self.diagnostic.check_ad_dns, server)
                self.log_to_console("Vérification AD/DNS terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir une adresse IP")
        
        tk.Button(dialog, text="Vérifier", command=execute, bg='#3498db', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def check_mysql_dialog(self):
        """Dialogue pour tester MySQL"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tester MySQL")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP:", font=('Arial', 10)).pack(pady=5)
        host_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        host_entry.pack()
        host_entry.insert(0, "192.168.10.21")
        
        tk.Label(dialog, text="Port:", font=('Arial', 10)).pack(pady=5)
        port_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        port_entry.pack()
        port_entry.insert(0, "3306")
        
        tk.Label(dialog, text="Base de données:", font=('Arial', 10)).pack(pady=5)
        db_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        db_entry.pack()
        db_entry.insert(0, "wms_db")
        
        tk.Label(dialog, text="Utilisateur:", font=('Arial', 10)).pack(pady=5)
        user_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        user_entry.pack()
        user_entry.insert(0, "wms_user")
        
        tk.Label(dialog, text="Mot de passe:", font=('Arial', 10)).pack(pady=5)
        pass_entry = tk.Entry(dialog, width=30, font=('Arial', 10), show='*')
        pass_entry.pack()
        
        def execute():
            host = host_entry.get().strip()
            port = port_entry.get().strip()
            database = db_entry.get().strip()
            user = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if all([host, port, database, user, password]):
                dialog.destroy()
                self.log_to_console(f"Test MySQL sur {host}:{port}...", "INFO")
                self.update_status("Test MySQL en cours...")
                self.run_in_thread(self.diagnostic.check_mysql, host, int(port), database, user, password)
                self.log_to_console("Test MySQL terminé", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        
        tk.Button(dialog, text="Tester", command=execute, bg='#3498db', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def check_windows_dialog(self):
        """Dialogue pour vérifier un serveur Windows"""
        dialog = tk.Toplevel(self.root)
        dialog.title("État serveur Windows")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP du serveur Windows:", font=('Arial', 10)).pack(pady=10)
        server_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        server_entry.pack(pady=5)
        server_entry.insert(0, "192.168.10.10")
        
        def execute():
            server = server_entry.get().strip()
            if server:
                dialog.destroy()
                self.log_to_console(f"Vérification serveur Windows {server}...", "INFO")
                self.update_status("Vérification Windows en cours...")
                self.run_in_thread(self.diagnostic.check_windows_server, server)
                self.log_to_console("Vérification Windows terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir une adresse IP")
        
        tk.Button(dialog, text="Vérifier", command=execute, bg='#3498db', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def check_linux_dialog(self):
        """Dialogue pour vérifier un serveur Linux"""
        dialog = tk.Toplevel(self.root)
        dialog.title("État serveur Linux")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP du serveur Linux:", font=('Arial', 10)).pack(pady=5)
        server_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        server_entry.pack()
        server_entry.insert(0, "192.168.10.21")
        
        tk.Label(dialog, text="Utilisateur SSH:", font=('Arial', 10)).pack(pady=5)
        user_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        user_entry.pack()
        user_entry.insert(0, "admin")
        
        tk.Label(dialog, text="Mot de passe SSH:", font=('Arial', 10)).pack(pady=5)
        pass_entry = tk.Entry(dialog, width=30, font=('Arial', 10), show='*')
        pass_entry.pack()
        
        def execute():
            server = server_entry.get().strip()
            user = user_entry.get().strip()
            password = pass_entry.get().strip() or None
            
            if server and user:
                dialog.destroy()
                self.log_to_console(f"Vérification serveur Linux {server}...", "INFO")
                self.update_status("Vérification Linux en cours...")
                self.run_in_thread(self.diagnostic.check_linux_server, server, user, password)
                self.log_to_console("Vérification Linux terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires")
        
        tk.Button(dialog, text="Vérifier", command=execute, bg='#3498db', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def run_full_diagnostic(self):
        """Lance un diagnostic complet"""
        if messagebox.askyesno("Confirmation", "Lancer un diagnostic complet de tous les systèmes ?"):
            self.log_to_console("Lancement du diagnostic complet...", "INFO")
            self.update_status("Diagnostic complet en cours...")
            self.run_in_thread(self.diagnostic.run_full_diagnostic)
            self.log_to_console("Diagnostic complet terminé", "SUCCESS")
            self.update_status("Prêt")
    
    def test_ping_dialog(self):
        """Dialogue pour tester un ping"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tester connexion (ping)")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP ou nom d'hôte:", font=('Arial', 10)).pack(pady=10)
        host_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        host_entry.pack(pady=5)
        host_entry.insert(0, "192.168.10.1")
        
        def execute():
            host = host_entry.get().strip()
            if host:
                dialog.destroy()
                self.log_to_console(f"Test ping vers {host}...", "INFO")
                self.update_status("Test ping en cours...")
                self.run_in_thread(self.diagnostic.test_ping, host)
                self.log_to_console("Test ping terminé", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir une adresse IP ou un nom d'hôte")
        
        tk.Button(dialog, text="Tester", command=execute, bg='#3498db', fg='white', font=('Arial', 10)).pack(pady=10)
    
    # Dialogues pour le module Sauvegarde
    def backup_database_dialog(self):
        """Dialogue pour sauvegarder la base de données"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sauvegarde complète")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP:", font=('Arial', 10)).pack(pady=5)
        host_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        host_entry.pack()
        host_entry.insert(0, "192.168.10.21")
        
        tk.Label(dialog, text="Port:", font=('Arial', 10)).pack(pady=5)
        port_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        port_entry.pack()
        port_entry.insert(0, "3306")
        
        tk.Label(dialog, text="Base de données:", font=('Arial', 10)).pack(pady=5)
        db_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        db_entry.pack()
        db_entry.insert(0, "wms_db")
        
        tk.Label(dialog, text="Utilisateur:", font=('Arial', 10)).pack(pady=5)
        user_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        user_entry.pack()
        user_entry.insert(0, "wms_user")
        
        tk.Label(dialog, text="Mot de passe:", font=('Arial', 10)).pack(pady=5)
        pass_entry = tk.Entry(dialog, width=30, font=('Arial', 10), show='*')
        pass_entry.pack()
        
        def execute():
            host = host_entry.get().strip()
            port = port_entry.get().strip()
            database = db_entry.get().strip()
            user = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if all([host, port, database, user, password]):
                dialog.destroy()
                self.log_to_console(f"Sauvegarde de {database} en cours...", "INFO")
                self.update_status("Sauvegarde en cours...")
                self.run_in_thread(self.backup.backup_database, host, int(port), database, user, password)
                self.log_to_console("Sauvegarde terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        
        tk.Button(dialog, text="Sauvegarder", command=execute, bg='#2ecc71', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def export_table_dialog(self):
        """Dialogue pour exporter une table"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Export table CSV")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP:", font=('Arial', 10)).pack(pady=5)
        host_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        host_entry.pack()
        host_entry.insert(0, "192.168.10.21")
        
        tk.Label(dialog, text="Port:", font=('Arial', 10)).pack(pady=5)
        port_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        port_entry.pack()
        port_entry.insert(0, "3306")
        
        tk.Label(dialog, text="Base de données:", font=('Arial', 10)).pack(pady=5)
        db_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        db_entry.pack()
        db_entry.insert(0, "wms_db")
        
        tk.Label(dialog, text="Table:", font=('Arial', 10)).pack(pady=5)
        table_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        table_entry.pack()
        
        tk.Label(dialog, text="Utilisateur:", font=('Arial', 10)).pack(pady=5)
        user_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        user_entry.pack()
        user_entry.insert(0, "wms_user")
        
        tk.Label(dialog, text="Mot de passe:", font=('Arial', 10)).pack(pady=5)
        pass_entry = tk.Entry(dialog, width=30, font=('Arial', 10), show='*')
        pass_entry.pack()
        
        def execute():
            host = host_entry.get().strip()
            port = port_entry.get().strip()
            database = db_entry.get().strip()
            table = table_entry.get().strip()
            user = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if all([host, port, database, table, user, password]):
                dialog.destroy()
                self.log_to_console(f"Export de la table {table} en cours...", "INFO")
                self.update_status("Export en cours...")
                self.run_in_thread(self.backup.export_table_csv, host, int(port), database, table, user, password)
                self.log_to_console("Export terminé", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        
        tk.Button(dialog, text="Exporter", command=execute, bg='#2ecc71', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def backup_all_dialog(self):
        """Dialogue pour sauvegarder toutes les tables"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sauvegarde automatique")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Adresse IP:", font=('Arial', 10)).pack(pady=5)
        host_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        host_entry.pack()
        host_entry.insert(0, "192.168.10.21")
        
        tk.Label(dialog, text="Port:", font=('Arial', 10)).pack(pady=5)
        port_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        port_entry.pack()
        port_entry.insert(0, "3306")
        
        tk.Label(dialog, text="Base de données:", font=('Arial', 10)).pack(pady=5)
        db_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        db_entry.pack()
        db_entry.insert(0, "wms_db")
        
        tk.Label(dialog, text="Utilisateur:", font=('Arial', 10)).pack(pady=5)
        user_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        user_entry.pack()
        user_entry.insert(0, "wms_user")
        
        tk.Label(dialog, text="Mot de passe:", font=('Arial', 10)).pack(pady=5)
        pass_entry = tk.Entry(dialog, width=30, font=('Arial', 10), show='*')
        pass_entry.pack()
        
        def execute():
            host = host_entry.get().strip()
            port = port_entry.get().strip()
            database = db_entry.get().strip()
            user = user_entry.get().strip()
            password = pass_entry.get().strip()
            
            if all([host, port, database, user, password]):
                dialog.destroy()
                self.log_to_console(f"Sauvegarde automatique de toutes les tables...", "INFO")
                self.update_status("Sauvegarde automatique en cours...")
                self.run_in_thread(self.backup.backup_all_tables, host, int(port), database, user, password)
                self.log_to_console("Sauvegarde automatique terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
        
        tk.Button(dialog, text="Sauvegarder tout", command=execute, bg='#2ecc71', fg='white', font=('Arial', 10)).pack(pady=10)
    
    # Dialogues pour le module Audit
    def scan_network_dialog(self):
        """Dialogue pour scanner le réseau"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Scanner réseau")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Plage réseau (ex: 192.168.10.0/24):", font=('Arial', 10)).pack(pady=10)
        network_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        network_entry.pack(pady=5)
        network_entry.insert(0, "192.168.10.0/24")
        
        def execute():
            network = network_entry.get().strip()
            if network:
                dialog.destroy()
                self.log_to_console(f"Scan du réseau {network}...", "INFO")
                self.update_status("Scan réseau en cours...")
                self.run_in_thread(self.audit.scan_network, network)
                self.log_to_console("Scan réseau terminé", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir une plage réseau")
        
        tk.Button(dialog, text="Scanner", command=execute, bg='#e67e22', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def check_eol_dialog(self):
        """Dialogue pour vérifier les dates EOL"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Vérifier dates EOL")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Nom de l'OS (ex: Windows Server 2012):", font=('Arial', 10)).pack(pady=10)
        os_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        os_entry.pack(pady=5)
        
        def execute():
            os_name = os_entry.get().strip()
            if os_name:
                dialog.destroy()
                self.log_to_console(f"Vérification EOL pour {os_name}...", "INFO")
                self.update_status("Vérification EOL en cours...")
                self.run_in_thread(self.audit.check_eol_dates, os_name)
                self.log_to_console("Vérification EOL terminée", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir un nom d'OS")
        
        tk.Button(dialog, text="Vérifier", command=execute, bg='#e67e22', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def analyze_csv_dialog(self):
        """Dialogue pour analyser un fichier CSV"""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            self.log_to_console(f"Analyse du fichier {filename}...", "INFO")
            self.update_status("Analyse CSV en cours...")
            self.run_in_thread(self.audit.analyze_csv_inventory, filename)
            self.log_to_console("Analyse CSV terminée", "SUCCESS")
            self.update_status("Prêt")
    
    def generate_report_dialog(self):
        """Dialogue pour générer un rapport complet"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Rapport complet d'obsolescence")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Plage réseau à auditer:", font=('Arial', 10)).pack(pady=10)
        network_entry = tk.Entry(dialog, width=30, font=('Arial', 10))
        network_entry.pack(pady=5)
        network_entry.insert(0, "192.168.10.0/24")
        
        def execute():
            network = network_entry.get().strip()
            if network:
                dialog.destroy()
                self.log_to_console(f"Génération du rapport pour {network}...", "INFO")
                self.update_status("Génération du rapport en cours...")
                self.run_in_thread(self.audit.generate_full_report, network)
                self.log_to_console("Rapport généré avec succès", "SUCCESS")
                self.update_status("Prêt")
            else:
                messagebox.showwarning("Erreur", "Veuillez saisir une plage réseau")
        
        tk.Button(dialog, text="Générer", command=execute, bg='#e67e22', fg='white', font=('Arial', 10)).pack(pady=10)
    
    def quit_app(self):
        """Quitte l'application"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment quitter ?"):
            self.logger.info("Fermeture de l'interface graphique")
            self.root.quit()


def main():
    """Point d'entrée principal"""
    root = tk.Tk()
    app = NTLSysToolboxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
