#!/usr/bin/env python3
"""
Interface graphique pour NTL-SysToolbox
GUI moderne avec tkinter pour l'administration système
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os
from datetime import datetime

# Ajout du répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.diagnostic import DiagnosticModule
from modules.backup import BackupModule
from modules.audit import AuditModule
from utils.logger import Logger
from utils.output import OutputManager


class NTLSysToolboxGUI:
    """Interface graphique principale"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("NTL-SysToolbox - Administration Système")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialisation des modules
        self.logger = Logger()
        self.output_manager = OutputManager()
        self.diagnostic = DiagnosticModule(self.logger, self.output_manager)
        self.backup = BackupModule(self.logger, self.output_manager)
        self.audit = AuditModule(self.logger, self.output_manager)
        
        # Configuration du style
        self.setup_styles()
        
        # Création de l'interface
        self.create_widgets()
        
        # Log de démarrage
        self.logger.info("Interface graphique NTL-SysToolbox démarrée")
        self.log_message("✅ Application démarrée", "info")
    
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs professionnelles
        bg_color = "#f0f0f0"
        accent_color = "#0066cc"
        success_color = "#28a745"
        warning_color = "#ffc107"
        error_color = "#dc3545"
        
        # Configuration des styles
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=accent_color)
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure("Accent.TButton", foreground="white", background=accent_color)
        style.map("Accent.TButton", background=[("active", "#0052a3")])
        
        self.root.configure(bg=bg_color)
    
    def create_widgets(self):
        """Crée les widgets de l'interface"""
        # En-tête
        header_frame = ttk.Frame(self.root, padding="20 10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="🖥️ NTL-SysToolbox",
            style="Title.TLabel"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Outil d'administration système - NordTransit Logistics",
            font=("Segoe UI", 9)
        )
        subtitle_label.pack(side=tk.LEFT, padx=20)
        
        # Notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Création des onglets
        self.create_diagnostic_tab()
        self.create_backup_tab()
        self.create_audit_tab()
        self.create_logs_tab()
        
        # Barre de statut
        self.create_status_bar()
    
    def create_diagnostic_tab(self):
        """Crée l'onglet Diagnostic"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="🔍 Diagnostic")
        
        # Section AD/DNS
        ad_frame = ttk.LabelFrame(tab, text="Vérification AD/DNS", padding="15")
        ad_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(ad_frame, text="Adresse IP du contrôleur de domaine:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ad_ip_entry = ttk.Entry(ad_frame, width=30)
        self.ad_ip_entry.grid(row=0, column=1, padx=10, pady=5)
        self.ad_ip_entry.insert(0, "192.168.10.10")
        
        ttk.Button(
            ad_frame,
            text="Vérifier AD/DNS",
            command=self.run_ad_dns_check,
            style="Accent.TButton"
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Section MySQL
        mysql_frame = ttk.LabelFrame(tab, text="Test Base de Données MySQL", padding="15")
        mysql_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(mysql_frame, text="Hôte:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mysql_host_entry = ttk.Entry(mysql_frame, width=20)
        self.mysql_host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.mysql_host_entry.insert(0, "192.168.10.21")
        
        ttk.Label(mysql_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(15, 0), pady=5)
        self.mysql_port_entry = ttk.Entry(mysql_frame, width=10)
        self.mysql_port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.mysql_port_entry.insert(0, "3306")
        
        ttk.Label(mysql_frame, text="Base de données:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mysql_db_entry = ttk.Entry(mysql_frame, width=20)
        self.mysql_db_entry.grid(row=1, column=1, padx=5, pady=5)
        self.mysql_db_entry.insert(0, "wms_db")
        
        ttk.Label(mysql_frame, text="Utilisateur:").grid(row=1, column=2, sticky=tk.W, padx=(15, 0), pady=5)
        self.mysql_user_entry = ttk.Entry(mysql_frame, width=20)
        self.mysql_user_entry.grid(row=1, column=3, padx=5, pady=5)
        self.mysql_user_entry.insert(0, "wms_user")
        
        ttk.Label(mysql_frame, text="Mot de passe:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.mysql_pass_entry = ttk.Entry(mysql_frame, width=20, show="*")
        self.mysql_pass_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(
            mysql_frame,
            text="Tester MySQL",
            command=self.run_mysql_check,
            style="Accent.TButton"
        ).grid(row=2, column=3, padx=5, pady=5)
        
        # Section Serveurs
        server_frame = ttk.LabelFrame(tab, text="Diagnostic Serveur", padding="15")
        server_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(server_frame, text="Adresse IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_ip_entry = ttk.Entry(server_frame, width=30)
        self.server_ip_entry.grid(row=0, column=1, padx=10, pady=5)
        self.server_ip_entry.insert(0, "192.168.10.22")
        
        ttk.Button(
            server_frame,
            text="Diagnostic Windows",
            command=self.run_windows_check
        ).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(
            server_frame,
            text="Diagnostic Linux",
            command=self.run_linux_check
        ).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(
            server_frame,
            text="Diagnostic Complet",
            command=self.run_full_diagnostic,
            style="Accent.TButton"
        ).grid(row=0, column=4, padx=5, pady=5)
        
        # Zone de résultats
        result_frame = ttk.LabelFrame(tab, text="Résultats", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.diagnostic_result = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=15
        )
        self.diagnostic_result.pack(fill=tk.BOTH, expand=True)
    
    def create_backup_tab(self):
        """Crée l'onglet Sauvegarde"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="💾 Sauvegarde")
        
        # Configuration MySQL
        config_frame = ttk.LabelFrame(tab, text="Configuration MySQL", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(config_frame, text="Hôte:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.backup_host_entry = ttk.Entry(config_frame, width=20)
        self.backup_host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.backup_host_entry.insert(0, "192.168.10.21")
        
        ttk.Label(config_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(15, 0), pady=5)
        self.backup_port_entry = ttk.Entry(config_frame, width=10)
        self.backup_port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.backup_port_entry.insert(0, "3306")
        
        ttk.Label(config_frame, text="Base de données:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.backup_db_entry = ttk.Entry(config_frame, width=20)
        self.backup_db_entry.grid(row=1, column=1, padx=5, pady=5)
        self.backup_db_entry.insert(0, "wms_db")
        
        ttk.Label(config_frame, text="Utilisateur:").grid(row=1, column=2, sticky=tk.W, padx=(15, 0), pady=5)
        self.backup_user_entry = ttk.Entry(config_frame, width=20)
        self.backup_user_entry.grid(row=1, column=3, padx=5, pady=5)
        self.backup_user_entry.insert(0, "wms_user")
        
        ttk.Label(config_frame, text="Mot de passe:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.backup_pass_entry = ttk.Entry(config_frame, width=20, show="*")
        self.backup_pass_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Actions de sauvegarde
        action_frame = ttk.LabelFrame(tab, text="Actions de Sauvegarde", padding="15")
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            action_frame,
            text="Sauvegarde Complète (SQL)",
            command=self.run_full_backup,
            style="Accent.TButton",
            width=30
        ).pack(pady=5)
        
        # Export de table
        table_frame = ttk.Frame(action_frame)
        table_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(table_frame, text="Nom de la table:").pack(side=tk.LEFT, padx=5)
        self.table_name_entry = ttk.Entry(table_frame, width=25)
        self.table_name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            table_frame,
            text="Export CSV",
            command=self.run_table_export
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Sauvegarde Toutes les Tables",
            command=self.run_all_tables_backup,
            width=30
        ).pack(pady=5)
        
        # Zone de résultats
        result_frame = ttk.LabelFrame(tab, text="Résultats", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.backup_result = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=15
        )
        self.backup_result.pack(fill=tk.BOTH, expand=True)
    
    def create_audit_tab(self):
        """Crée l'onglet Audit"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="📊 Audit EOL")
        
        # Scan réseau
        scan_frame = ttk.LabelFrame(tab, text="Scan Réseau", padding="15")
        scan_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(scan_frame, text="Plage réseau (ex: 192.168.10.0/24):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.network_entry = ttk.Entry(scan_frame, width=30)
        self.network_entry.grid(row=0, column=1, padx=10, pady=5)
        self.network_entry.insert(0, "192.168.10.0/24")
        
        ttk.Button(
            scan_frame,
            text="Scanner le Réseau",
            command=self.run_network_scan,
            style="Accent.TButton"
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Vérification EOL
        eol_frame = ttk.LabelFrame(tab, text="Vérification EOL", padding="15")
        eol_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(eol_frame, text="Nom de l'OS:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.os_name_entry = ttk.Entry(eol_frame, width=30)
        self.os_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.os_name_entry.insert(0, "Windows Server 2012")
        
        ttk.Button(
            eol_frame,
            text="Vérifier EOL",
            command=self.run_eol_check
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Analyse CSV
        csv_frame = ttk.LabelFrame(tab, text="Analyse Inventaire CSV", padding="15")
        csv_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(csv_frame, text="Fichier CSV:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.csv_path_entry = ttk.Entry(csv_frame, width=40)
        self.csv_path_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(
            csv_frame,
            text="Parcourir...",
            command=self.browse_csv_file
        ).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(
            csv_frame,
            text="Analyser CSV",
            command=self.run_csv_analysis,
            style="Accent.TButton"
        ).grid(row=0, column=3, padx=5, pady=5)
        
        # Rapport complet
        report_frame = ttk.LabelFrame(tab, text="Rapport Complet", padding="15")
        report_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(
            report_frame,
            text="Générer Rapport Complet d'Obsolescence",
            command=self.run_full_report,
            style="Accent.TButton",
            width=40
        ).pack(pady=5)
        
        # Zone de résultats
        result_frame = ttk.LabelFrame(tab, text="Résultats", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.audit_result = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=15
        )
        self.audit_result.pack(fill=tk.BOTH, expand=True)
    
    def create_logs_tab(self):
        """Crée l'onglet Logs"""
        tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(tab, text="📝 Logs")
        
        # Barre d'outils
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            toolbar,
            text="Rafraîchir",
            command=self.refresh_logs
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            toolbar,
            text="Effacer l'affichage",
            command=self.clear_log_display
        ).pack(side=tk.LEFT, padx=5)
        
        # Zone de logs
        self.log_display = scrolledtext.ScrolledText(
            tab,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=30
        )
        self.log_display.pack(fill=tk.BOTH, expand=True)
        
        # Configuration des tags de couleur
        self.log_display.tag_config("info", foreground="#0066cc")
        self.log_display.tag_config("success", foreground="#28a745")
        self.log_display.tag_config("warning", foreground="#ffc107")
        self.log_display.tag_config("error", foreground="#dc3545")
    
    def create_status_bar(self):
        """Crée la barre de statut"""
        self.status_bar = ttk.Label(
            self.root,
            text="Prêt",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Méthodes pour les actions Diagnostic
    
    def run_ad_dns_check(self):
        """Lance la vérification AD/DNS"""
        server_ip = self.ad_ip_entry.get().strip()
        if not server_ip:
            messagebox.showwarning("Attention", "Veuillez saisir une adresse IP")
            return
        
        self.diagnostic_result.delete(1.0, tk.END)
        self.diagnostic_result.insert(tk.END, f"🔍 Vérification AD/DNS sur {server_ip}...\n\n")
        self.update_status("Vérification AD/DNS en cours...")
        
        def task():
            try:
                result = self.diagnostic.check_ad_dns(server_ip)
                self.root.after(0, lambda: self.display_diagnostic_result(result))
                self.root.after(0, lambda: self.update_status("Vérification AD/DNS terminée"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de la vérification"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_mysql_check(self):
        """Lance le test MySQL"""
        host = self.mysql_host_entry.get().strip()
        port = self.mysql_port_entry.get().strip()
        database = self.mysql_db_entry.get().strip()
        user = self.mysql_user_entry.get().strip()
        password = self.mysql_pass_entry.get()
        
        if not all([host, port, database, user]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
            return
        
        self.diagnostic_result.delete(1.0, tk.END)
        self.diagnostic_result.insert(tk.END, f"🔍 Test MySQL sur {host}:{port}...\n\n")
        self.update_status("Test MySQL en cours...")
        
        def task():
            try:
                result = self.diagnostic.check_mysql(host, int(port), database, user, password)
                self.root.after(0, lambda: self.display_diagnostic_result(result))
                self.root.after(0, lambda: self.update_status("Test MySQL terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors du test"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_windows_check(self):
        """Lance le diagnostic Windows"""
        server_ip = self.server_ip_entry.get().strip()
        if not server_ip:
            messagebox.showwarning("Attention", "Veuillez saisir une adresse IP")
            return
        
        self.diagnostic_result.delete(1.0, tk.END)
        self.diagnostic_result.insert(tk.END, f"🔍 Diagnostic Windows sur {server_ip}...\n\n")
        self.update_status("Diagnostic Windows en cours...")
        
        def task():
            try:
                result = self.diagnostic.check_windows_server(server_ip)
                self.root.after(0, lambda: self.display_diagnostic_result(result))
                self.root.after(0, lambda: self.update_status("Diagnostic Windows terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors du diagnostic"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_linux_check(self):
        """Lance le diagnostic Linux"""
        server_ip = self.server_ip_entry.get().strip()
        if not server_ip:
            messagebox.showwarning("Attention", "Veuillez saisir une adresse IP")
            return
        
        self.diagnostic_result.delete(1.0, tk.END)
        self.diagnostic_result.insert(tk.END, f"🔍 Diagnostic Linux sur {server_ip}...\n\n")
        self.update_status("Diagnostic Linux en cours...")
        
        def task():
            try:
                result = self.diagnostic.check_linux_server(server_ip, "admin")
                self.root.after(0, lambda: self.display_diagnostic_result(result))
                self.root.after(0, lambda: self.update_status("Diagnostic Linux terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors du diagnostic"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        self.diagnostic_result.delete(1.0, tk.END)
        self.diagnostic_result.insert(tk.END, "🔍 Diagnostic complet en cours...\n\n")
        self.update_status("Diagnostic complet en cours...")
        
        def task():
            try:
                results = self.diagnostic.run_full_diagnostic()
                self.root.after(0, lambda: self.display_full_diagnostic_results(results))
                self.root.after(0, lambda: self.update_status("Diagnostic complet terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors du diagnostic"))
        
        threading.Thread(target=task, daemon=True).start()
    
    # Méthodes pour les actions Sauvegarde
    
    def run_full_backup(self):
        """Lance une sauvegarde complète"""
        host = self.backup_host_entry.get().strip()
        port = self.backup_port_entry.get().strip()
        database = self.backup_db_entry.get().strip()
        user = self.backup_user_entry.get().strip()
        password = self.backup_pass_entry.get()
        
        if not all([host, port, database, user]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
            return
        
        self.backup_result.delete(1.0, tk.END)
        self.backup_result.insert(tk.END, f"💾 Sauvegarde complète de {database}...\n\n")
        self.update_status("Sauvegarde en cours...")
        
        def task():
            try:
                result = self.backup.backup_database(host, int(port), database, user, password)
                self.root.after(0, lambda: self.display_backup_result(result))
                self.root.after(0, lambda: self.update_status("Sauvegarde terminée"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de la sauvegarde"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_table_export(self):
        """Lance l'export d'une table"""
        host = self.backup_host_entry.get().strip()
        port = self.backup_port_entry.get().strip()
        database = self.backup_db_entry.get().strip()
        table = self.table_name_entry.get().strip()
        user = self.backup_user_entry.get().strip()
        password = self.backup_pass_entry.get()
        
        if not all([host, port, database, table, user]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
            return
        
        self.backup_result.delete(1.0, tk.END)
        self.backup_result.insert(tk.END, f"💾 Export de la table {table}...\n\n")
        self.update_status("Export en cours...")
        
        def task():
            try:
                result = self.backup.export_table_csv(host, int(port), database, table, user, password)
                self.root.after(0, lambda: self.display_backup_result(result))
                self.root.after(0, lambda: self.update_status("Export terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de l'export"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_all_tables_backup(self):
        """Lance la sauvegarde de toutes les tables"""
        host = self.backup_host_entry.get().strip()
        port = self.backup_port_entry.get().strip()
        database = self.backup_db_entry.get().strip()
        user = self.backup_user_entry.get().strip()
        password = self.backup_pass_entry.get()
        
        if not all([host, port, database, user]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
            return
        
        self.backup_result.delete(1.0, tk.END)
        self.backup_result.insert(tk.END, f"💾 Sauvegarde de toutes les tables...\n\n")
        self.update_status("Sauvegarde en cours...")
        
        def task():
            try:
                result = self.backup.backup_all_tables(host, int(port), database, user, password)
                self.root.after(0, lambda: self.display_backup_result(result))
                self.root.after(0, lambda: self.update_status("Sauvegarde terminée"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de la sauvegarde"))
        
        threading.Thread(target=task, daemon=True).start()
    
    # Méthodes pour les actions Audit
    
    def run_network_scan(self):
        """Lance le scan réseau"""
        network = self.network_entry.get().strip()
        if not network:
            messagebox.showwarning("Attention", "Veuillez saisir une plage réseau")
            return
        
        self.audit_result.delete(1.0, tk.END)
        self.audit_result.insert(tk.END, f"🔍 Scan du réseau {network}...\n\n")
        self.update_status("Scan réseau en cours...")
        
        def task():
            try:
                result = self.audit.scan_network(network)
                self.root.after(0, lambda: self.display_audit_result(result))
                self.root.after(0, lambda: self.update_status("Scan réseau terminé"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors du scan"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_eol_check(self):
        """Lance la vérification EOL"""
        os_name = self.os_name_entry.get().strip()
        if not os_name:
            messagebox.showwarning("Attention", "Veuillez saisir un nom d'OS")
            return
        
        self.audit_result.delete(1.0, tk.END)
        self.audit_result.insert(tk.END, f"📅 Vérification EOL pour {os_name}...\n\n")
        self.update_status("Vérification EOL en cours...")
        
        def task():
            try:
                result = self.audit.check_eol_dates(os_name)
                self.root.after(0, lambda: self.display_audit_result(result))
                self.root.after(0, lambda: self.update_status("Vérification EOL terminée"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de la vérification"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def browse_csv_file(self):
        """Ouvre un dialogue pour sélectionner un fichier CSV"""
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.csv_path_entry.delete(0, tk.END)
            self.csv_path_entry.insert(0, filename)
    
    def run_csv_analysis(self):
        """Lance l'analyse CSV"""
        csv_file = self.csv_path_entry.get().strip()
        if not csv_file:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier CSV")
            return
        
        self.audit_result.delete(1.0, tk.END)
        self.audit_result.insert(tk.END, f"📊 Analyse du fichier {csv_file}...\n\n")
        self.update_status("Analyse CSV en cours...")
        
        def task():
            try:
                result = self.audit.analyze_csv_inventory(csv_file)
                self.root.after(0, lambda: self.display_audit_result(result))
                self.root.after(0, lambda: self.update_status("Analyse CSV terminée"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de l'analyse"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_full_report(self):
        """Lance la génération du rapport complet"""
        network = self.network_entry.get().strip()
        if not network:
            messagebox.showwarning("Attention", "Veuillez saisir une plage réseau")
            return
        
        self.audit_result.delete(1.0, tk.END)
        self.audit_result.insert(tk.END, f"📋 Génération du rapport complet...\n\n")
        self.update_status("Génération du rapport en cours...")
        
        def task():
            try:
                result = self.audit.generate_full_report(network)
                self.root.after(0, lambda: self.display_audit_result(result))
                self.root.after(0, lambda: self.update_status("Rapport généré"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ Erreur: {e}", "error"))
                self.root.after(0, lambda: self.update_status("Erreur lors de la génération"))
        
        threading.Thread(target=task, daemon=True).start()
    
    # Méthodes d'affichage des résultats
    
    def display_diagnostic_result(self, result):
        """Affiche les résultats de diagnostic"""
        import json
        self.diagnostic_result.insert(tk.END, json.dumps(result, indent=2, ensure_ascii=False))
        self.log_message(f"✅ Diagnostic terminé - Statut: {result.get('global_status', 'N/A')}", "success")
    
    def display_full_diagnostic_results(self, results):
        """Affiche les résultats du diagnostic complet"""
        import json
        for result in results:
            self.diagnostic_result.insert(tk.END, f"\n{'='*60}\n")
            self.diagnostic_result.insert(tk.END, json.dumps(result, indent=2, ensure_ascii=False))
        self.log_message(f"✅ Diagnostic complet terminé - {len(results)} serveurs vérifiés", "success")
    
    def display_backup_result(self, result):
        """Affiche les résultats de sauvegarde"""
        import json
        self.backup_result.insert(tk.END, json.dumps(result, indent=2, ensure_ascii=False))
        self.log_message(f"✅ Sauvegarde terminée", "success")
    
    def display_audit_result(self, result):
        """Affiche les résultats d'audit"""
        import json
        self.audit_result.insert(tk.END, json.dumps(result, indent=2, ensure_ascii=False))
        self.log_message(f"✅ Audit terminé", "success")
    
    # Méthodes utilitaires
    
    def log_message(self, message, level="info"):
        """Ajoute un message dans les logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_display.insert(tk.END, log_entry, level)
        self.log_display.see(tk.END)
    
    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_bar.config(text=message)
    
    def refresh_logs(self):
        """Rafraîchit l'affichage des logs"""
        logs = self.logger.get_recent_logs(50)
        self.log_display.delete(1.0, tk.END)
        for log in logs:
            self.log_display.insert(tk.END, log + "\n")
        self.log_display.see(tk.END)
    
    def clear_log_display(self):
        """Efface l'affichage des logs"""
        self.log_display.delete(1.0, tk.END)


def main():
    """Point d'entrée de l'application GUI"""
    root = tk.Tk()
    app = NTLSysToolboxGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
