"""
Module Audit d'obsolescence - Scan réseau et vérification EOL
"""

import json
import os
import csv
import ipaddress
import socket
from datetime import datetime, timedelta

class AuditModule:
    """Module d'audit d'obsolescence"""
    
    def __init__(self, logger, output_manager):
        self.logger = logger
        self.output_manager = output_manager
        self.eol_database = self._load_eol_database()
    
    def _load_eol_database(self):
        """Charge la base de données des dates EOL"""
        eol_file = "data/eol_database.json"
        try:
            with open(eol_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Base de données EOL non trouvée, utilisation des données par défaut")
            return self._get_default_eol_data()
    
    def _get_default_eol_data(self):
        """Retourne les données EOL par défaut"""
        return {
            "windows_server": [
                {"version": "Windows Server 2008", "eol_date": "2020-01-14", "status": "obsolete"},
                {"version": "Windows Server 2008 R2", "eol_date": "2020-01-14", "status": "obsolete"},
                {"version": "Windows Server 2012", "eol_date": "2023-10-10", "status": "obsolete"},
                {"version": "Windows Server 2012 R2", "eol_date": "2023-10-10", "status": "obsolete"},
                {"version": "Windows Server 2016", "eol_date": "2027-01-12", "status": "supported"},
                {"version": "Windows Server 2019", "eol_date": "2029-01-09", "status": "supported"},
                {"version": "Windows Server 2022", "eol_date": "2031-10-14", "status": "supported"}
            ],
            "ubuntu": [
                {"version": "Ubuntu 16.04 LTS", "eol_date": "2021-04-30", "status": "obsolete"},
                {"version": "Ubuntu 18.04 LTS", "eol_date": "2023-05-31", "status": "obsolete"},
                {"version": "Ubuntu 20.04 LTS", "eol_date": "2025-04-30", "status": "ending_soon"},
                {"version": "Ubuntu 22.04 LTS", "eol_date": "2027-04-30", "status": "supported"},
                {"version": "Ubuntu 24.04 LTS", "eol_date": "2029-04-30", "status": "supported"}
            ],
            "centos": [
                {"version": "CentOS 6", "eol_date": "2020-11-30", "status": "obsolete"},
                {"version": "CentOS 7", "eol_date": "2024-06-30", "status": "obsolete"},
                {"version": "CentOS 8", "eol_date": "2021-12-31", "status": "obsolete"}
            ],
            "debian": [
                {"version": "Debian 9", "eol_date": "2022-06-30", "status": "obsolete"},
                {"version": "Debian 10", "eol_date": "2024-06-30", "status": "obsolete"},
                {"version": "Debian 11", "eol_date": "2026-06-30", "status": "supported"},
                {"version": "Debian 12", "eol_date": "2028-06-30", "status": "supported"}
            ]
        }
    
    def scan_network(self, network_range):
        """Scanne une plage réseau et détecte les composants"""
        print(f"\n🔍 Scan du réseau {network_range}...")
        self.logger.info(f"Début scan réseau {network_range}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "network": network_range,
            "type": "network_scan",
            "hosts": []
        }
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            total_hosts = network.num_addresses
            
            print(f"  → Scan de {total_hosts} adresses...")
            print("  ⚠️  Cela peut prendre plusieurs minutes")
            
            scanned = 0
            found = 0
            
            for ip in network.hosts():
                scanned += 1
                if scanned % 10 == 0:
                    print(f"  → Progression : {scanned}/{total_hosts} ({found} hôtes trouvés)")
                
                host_info = self._scan_host(str(ip))
                if host_info["status"] == "up":
                    results["hosts"].append(host_info)
                    found += 1
                    print(f"  ✅ Hôte trouvé : {ip} - {host_info.get('os_guess', 'OS inconnu')}")
            
            results["total_scanned"] = scanned
            results["hosts_found"] = found
            
            print(f"\n  ✅ Scan terminé : {found} hôtes actifs sur {scanned} adresses scannées")
            
        except Exception as e:
            results["error"] = str(e)
            print(f"  ❌ Erreur : {e}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"network_scan_{network_range.replace('/', '_')}")
        print(f"  💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Scan réseau terminé - {results.get('hosts_found', 0)} hôtes trouvés")
        return results
    
    def _scan_host(self, ip):
        """Scanne un hôte individuel"""
        host_info = {
            "ip": ip,
            "status": "down",
            "hostname": None,
            "os_guess": None,
            "open_ports": []
        }
        
        # Test de connectivité rapide
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        
        # Test de quelques ports communs
        common_ports = [22, 80, 443, 445, 3389, 3306]
        
        for port in common_ports:
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    host_info["status"] = "up"
                    host_info["open_ports"].append(port)
            except:
                pass
        
        sock.close()
        
        if host_info["status"] == "up":
            # Tentative de résolution du nom d'hôte
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                host_info["hostname"] = hostname
            except:
                pass
            
            # Détection basique de l'OS basée sur les ports ouverts
            if 3389 in host_info["open_ports"] or 445 in host_info["open_ports"]:
                host_info["os_guess"] = "Windows Server"
            elif 22 in host_info["open_ports"]:
                host_info["os_guess"] = "Linux/Unix"
            else:
                host_info["os_guess"] = "Unknown"
        
        return host_info
    
    def check_eol_dates(self, os_name):
        """Vérifie les dates EOL pour un OS donné"""
        print(f"\n📅 Vérification des dates EOL pour {os_name}...")
        self.logger.info(f"Vérification EOL pour {os_name}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "os_name": os_name,
            "type": "eol_check",
            "versions": []
        }
        
        # Recherche dans la base EOL
        os_key = None
        if "windows" in os_name.lower():
            os_key = "windows_server"
        elif "ubuntu" in os_name.lower():
            os_key = "ubuntu"
        elif "centos" in os_name.lower():
            os_key = "centos"
        elif "debian" in os_name.lower():
            os_key = "debian"
        
        if os_key and os_key in self.eol_database:
            results["versions"] = self.eol_database[os_key]
            
            print(f"\n  📋 Versions disponibles pour {os_name} :")
            for version in results["versions"]:
                status_icon = {
                    "supported": "✅",
                    "ending_soon": "⚠️",
                    "obsolete": "❌"
                }.get(version["status"], "❓")
                
                print(f"  {status_icon} {version['version']} - EOL: {version['eol_date']} ({version['status']})")
        else:
            print(f"  ⚠️  Aucune information EOL trouvée pour {os_name}")
            results["error"] = "OS non trouvé dans la base de données"
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"eol_check_{os_name.replace(' ', '_')}")
        print(f"\n  💾 Résultats sauvegardés : {filename}")
        
        return results
    
    def analyze_csv_inventory(self, csv_file):
        """Analyse un fichier CSV d'inventaire et vérifie les dates EOL"""
        print(f"\n📊 Analyse du fichier d'inventaire {csv_file}...")
        self.logger.info(f"Analyse inventaire CSV : {csv_file}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "csv_file": csv_file,
            "type": "csv_inventory_analysis",
            "systems": [],
            "summary": {
                "total": 0,
                "obsolete": 0,
                "ending_soon": 0,
                "supported": 0,
                "unknown": 0
            }
        }
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                
                for row in reader:
                    system = {
                        "hostname": row.get("hostname", "N/A"),
                        "ip": row.get("ip", "N/A"),
                        "os": row.get("os", "N/A"),
                        "version": row.get("version", "N/A")
                    }
                    
                    # Recherche de l'EOL
                    eol_info = self._find_eol_info(system["os"], system["version"])
                    system.update(eol_info)
                    
                    results["systems"].append(system)
                    results["summary"]["total"] += 1
                    results["summary"][eol_info["status"]] += 1
            
            # Affichage du résumé
            print(f"\n  📊 Résumé de l'analyse :")
            print(f"  Total de systèmes : {results['summary']['total']}")
            print(f"  ✅ Supportés : {results['summary']['supported']}")
            print(f"  ⚠️  Fin de support proche : {results['summary']['ending_soon']}")
            print(f"  ❌ Obsolètes : {results['summary']['obsolete']}")
            print(f"  ❓ Inconnus : {results['summary']['unknown']}")
            
            # Affichage des systèmes obsolètes
            if results['summary']['obsolete'] > 0:
                print(f"\n  ⚠️  SYSTÈMES OBSOLÈTES À METTRE À JOUR :")
                for system in results["systems"]:
                    if system["status"] == "obsolete":
                        print(f"    ❌ {system['hostname']} ({system['ip']}) - {system['os']} {system['version']}")
            
        except FileNotFoundError:
            results["error"] = "Fichier CSV non trouvé"
            print(f"  ❌ Fichier {csv_file} non trouvé")
        except Exception as e:
            results["error"] = str(e)
            print(f"  ❌ Erreur : {e}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, "csv_inventory_analysis")
        print(f"\n  💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Analyse CSV terminée - {results['summary']['obsolete']} systèmes obsolètes")
        return results
    
    def generate_full_report(self, network_range):
        """Génère un rapport complet d'obsolescence"""
        print(f"\n📋 Génération du rapport complet d'obsolescence...")
        self.logger.info(f"Génération rapport complet pour {network_range}")
        
        # Scan du réseau
        scan_results = self.scan_network(network_range)
        
        # Analyse EOL pour chaque hôte trouvé
        report = {
            "timestamp": datetime.now().isoformat(),
            "network": network_range,
            "type": "full_obsolescence_report",
            "scan_summary": {
                "total_scanned": scan_results.get("total_scanned", 0),
                "hosts_found": scan_results.get("hosts_found", 0)
            },
            "hosts_analysis": [],
            "recommendations": []
        }
        
        for host in scan_results.get("hosts", []):
            host_analysis = {
                "ip": host["ip"],
                "hostname": host.get("hostname", "N/A"),
                "os_guess": host.get("os_guess", "Unknown")
            }
            
            # Recherche EOL basée sur l'OS détecté
            if host["os_guess"] and host["os_guess"] != "Unknown":
                eol_info = self._find_eol_info(host["os_guess"], None)
                host_analysis.update(eol_info)
            else:
                host_analysis["status"] = "unknown"
                host_analysis["eol_date"] = None
            
            report["hosts_analysis"].append(host_analysis)
        
        # Génération des recommandations
        obsolete_hosts = [h for h in report["hosts_analysis"] if h.get("status") == "obsolete"]
        ending_soon_hosts = [h for h in report["hosts_analysis"] if h.get("status") == "ending_soon"]
        
        if obsolete_hosts:
            report["recommendations"].append({
                "priority": "HIGH",
                "message": f"{len(obsolete_hosts)} systèmes obsolètes détectés - Mise à jour urgente requise"
            })
        
        if ending_soon_hosts:
            report["recommendations"].append({
                "priority": "MEDIUM",
                "message": f"{len(ending_soon_hosts)} systèmes en fin de support proche - Planifier la migration"
            })
        
        # Affichage du rapport
        print(f"\n" + "="*60)
        print("RAPPORT COMPLET D'OBSOLESCENCE")
        print("="*60)
        print(f"Réseau scanné : {network_range}")
        print(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"\nHôtes scannés : {report['scan_summary']['total_scanned']}")
        print(f"Hôtes actifs : {report['scan_summary']['hosts_found']}")
        
        if report["recommendations"]:
            print(f"\n⚠️  RECOMMANDATIONS :")
            for rec in report["recommendations"]:
                priority_icon = "🔴" if rec["priority"] == "HIGH" else "🟡"
                print(f"  {priority_icon} [{rec['priority']}] {rec['message']}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(report, f"full_obsolescence_report_{network_range.replace('/', '_')}")
        print(f"\n💾 Rapport complet sauvegardé : {filename}")
        
        self.logger.info("Rapport complet généré")
        return report
    
    def _find_eol_info(self, os_name, version):
        """Recherche les informations EOL pour un OS/version"""
        eol_info = {
            "eol_date": None,
            "status": "unknown",
            "days_until_eol": None
        }
        
        if not os_name:
            return eol_info
        
        # Déterminer la catégorie d'OS
        os_key = None
        if "windows" in os_name.lower():
            os_key = "windows_server"
        elif "ubuntu" in os_name.lower():
            os_key = "ubuntu"
        elif "centos" in os_name.lower():
            os_key = "centos"
        elif "debian" in os_name.lower():
            os_key = "debian"
        
        if os_key and os_key in self.eol_database:
            # Si version spécifiée, recherche exacte
            if version:
                for v in self.eol_database[os_key]:
                    if version.lower() in v["version"].lower():
                        eol_info["eol_date"] = v["eol_date"]
                        eol_info["status"] = v["status"]
                        
                        # Calcul des jours restants
                        eol_date = datetime.strptime(v["eol_date"], "%Y-%m-%d")
                        days_until = (eol_date - datetime.now()).days
                        eol_info["days_until_eol"] = days_until
                        break
            else:
                # Prendre la version la plus récente supportée
                supported = [v for v in self.eol_database[os_key] if v["status"] == "supported"]
                if supported:
                    latest = supported[-1]
                    eol_info["eol_date"] = latest["eol_date"]
                    eol_info["status"] = latest["status"]
                    eol_info["recommended_version"] = latest["version"]
        
        return eol_info
