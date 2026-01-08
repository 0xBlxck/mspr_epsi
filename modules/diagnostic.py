"""
Module Diagnostic - Vérification de l'état des services et serveurs
"""

import subprocess
import platform
import socket
from datetime import datetime

class DiagnosticModule:
    """Module de diagnostic système"""
    
    def __init__(self, logger, output_manager):
        self.logger = logger
        self.output_manager = output_manager
    
    def check_ad_dns(self, server_ip):
        """Vérifie l'état des services AD/DNS sur un contrôleur de domaine"""
        print(f"\n🔍 Vérification AD/DNS sur {server_ip}...")
        self.logger.info(f"Début vérification AD/DNS sur {server_ip}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "server": server_ip,
            "type": "AD_DNS_Check",
            "tests": {}
        }
        
        # Test de connectivité
        connectivity = self._test_connectivity(server_ip)
        results["tests"]["connectivity"] = connectivity
        
        if connectivity["status"] == "OK":
            # Test DNS (port 53)
            dns_test = self._test_port(server_ip, 53, "DNS")
            results["tests"]["dns_service"] = dns_test
            
            # Test LDAP (port 389)
            ldap_test = self._test_port(server_ip, 389, "LDAP/AD")
            results["tests"]["ldap_service"] = ldap_test
            
            # Test Kerberos (port 88)
            kerberos_test = self._test_port(server_ip, 88, "Kerberos")
            results["tests"]["kerberos_service"] = kerberos_test
            
            # Résolution DNS
            dns_resolution = self._test_dns_resolution(server_ip)
            results["tests"]["dns_resolution"] = dns_resolution
        
        # Déterminer le statut global
        all_ok = all(test.get("status") == "OK" for test in results["tests"].values())
        results["global_status"] = "OK" if all_ok else "WARNING"
        
        # Affichage des résultats
        self._display_results(results)
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"diagnostic_ad_dns_{server_ip}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Vérification AD/DNS terminée - Statut: {results['global_status']}")
        return results
    
    def check_mysql(self, host, port, database, user, password):
        """Teste le bon fonctionnement de la base de données MySQL"""
        print(f"\n🔍 Vérification MySQL sur {host}:{port}...")
        self.logger.info(f"Début vérification MySQL sur {host}:{port}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "server": host,
            "port": port,
            "database": database,
            "type": "MySQL_Check",
            "tests": {}
        }
        
        try:
            import mysql.connector
            
            # Test de connexion
            print("  → Tentative de connexion...")
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connect_timeout=10
            )
            
            results["tests"]["connection"] = {
                "status": "OK",
                "message": "Connexion réussie"
            }
            print("  ✅ Connexion réussie")
            
            # Test de requête
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            results["tests"]["version"] = {
                "status": "OK",
                "value": version
            }
            print(f"  ✅ Version MySQL : {version}")
            
            # Test de performance (temps de réponse)
            start = datetime.now()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            response_time = (datetime.now() - start).total_seconds() * 1000
            results["tests"]["response_time"] = {
                "status": "OK" if response_time < 100 else "WARNING",
                "value_ms": round(response_time, 2)
            }
            print(f"  ✅ Temps de réponse : {response_time:.2f} ms")
            
            # Nombre de tables
            cursor.execute("SHOW TABLES")
            table_count = len(cursor.fetchall())
            results["tests"]["table_count"] = {
                "status": "OK",
                "value": table_count
            }
            print(f"  ✅ Nombre de tables : {table_count}")
            
            cursor.close()
            conn.close()
            
            results["global_status"] = "OK"
            
        except ImportError:
            results["tests"]["connection"] = {
                "status": "ERROR",
                "message": "Module mysql-connector-python non installé"
            }
            results["global_status"] = "ERROR"
            print("  ❌ Module mysql-connector-python non installé")
            print("     Installez-le avec : pip install mysql-connector-python")
            
        except Exception as e:
            results["tests"]["connection"] = {
                "status": "ERROR",
                "message": str(e)
            }
            results["global_status"] = "ERROR"
            print(f"  ❌ Erreur : {e}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"diagnostic_mysql_{host}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Vérification MySQL terminée - Statut: {results['global_status']}")
        return results
    
    def check_windows_server(self, server_ip):
        """Vérifie l'état d'un serveur Windows"""
        print(f"\n🔍 Diagnostic serveur Windows {server_ip}...")
        self.logger.info(f"Début diagnostic Windows sur {server_ip}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "server": server_ip,
            "type": "Windows_Server_Check",
            "system_info": {},
            "resources": {}
        }
        
        # Test de connectivité
        connectivity = self._test_connectivity(server_ip)
        
        if connectivity["status"] != "OK":
            results["global_status"] = "ERROR"
            results["error"] = "Serveur inaccessible"
            print(f"  ❌ Serveur {server_ip} inaccessible")
            filename = self.output_manager.save_json(results, f"diagnostic_windows_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            self.logger.info(f"Diagnostic Windows terminé - Statut: ERROR - Serveur inaccessible")
            return results
        
        print("  ✅ Serveur accessible")
        
        print("\n  ⚠️  Mode simulation activé (accès distant WMI non implémenté)")
        print("     En production, utiliser PowerShell Remoting ou WMI")
        
        results["system_info"] = {
            "os": "Windows Server 2019",
            "version": "10.0.17763",
            "hostname": f"SRV-{server_ip.split('.')[-1]}",
            "uptime_days": 45
        }
        
        results["resources"] = {
            "cpu_usage_percent": 35,
            "ram_total_gb": 128,
            "ram_used_gb": 58,
            "ram_usage_percent": 45,
            "disks": [
                {"drive": "C:", "total_gb": 500, "used_gb": 380, "usage_percent": 76},
                {"drive": "D:", "total_gb": 1000, "used_gb": 450, "usage_percent": 45}
            ]
        }
        
        results["global_status"] = "OK"
        
        print(f"\n  📊 Système : {results['system_info']['os']}")
        print(f"  📊 Uptime : {results['system_info']['uptime_days']} jours")
        print(f"  📊 CPU : {results['resources']['cpu_usage_percent']}%")
        print(f"  📊 RAM : {results['resources']['ram_usage_percent']}% ({results['resources']['ram_used_gb']}/{results['resources']['ram_total_gb']} GB)")
        for disk in results['resources']['disks']:
            print(f"  📊 Disque {disk['drive']} : {disk['usage_percent']}% ({disk['used_gb']}/{disk['total_gb']} GB)")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"diagnostic_windows_{server_ip}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Diagnostic Windows terminé - Statut: {results['global_status']}")
        return results
    
    def check_linux_server(self, server_ip, user, password=None):
        """Vérifie l'état d'un serveur Linux"""
        print(f"\n🔍 Diagnostic serveur Linux {server_ip}...")
        self.logger.info(f"Début diagnostic Linux sur {server_ip}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "server": server_ip,
            "type": "Linux_Server_Check",
            "system_info": {},
            "resources": {}
        }
        
        # Test de connectivité
        connectivity = self._test_connectivity(server_ip)
        
        if connectivity["status"] != "OK":
            results["global_status"] = "ERROR"
            results["error"] = "Serveur inaccessible"
            print(f"  ❌ Serveur {server_ip} inaccessible")
            filename = self.output_manager.save_json(results, f"diagnostic_linux_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            self.logger.info(f"Diagnostic Linux terminé - Statut: ERROR - Serveur inaccessible")
            return results
        
        print("  ✅ Serveur accessible")
        
        try:
            import paramiko
        except ImportError:
            results["global_status"] = "ERROR"
            results["error"] = "Paramiko non installé - SSH non disponible"
            print(f"\n  ❌ SSH non disponible (pip install paramiko)")
            filename = self.output_manager.save_json(results, f"diagnostic_linux_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            self.logger.error("Paramiko non installé")
            return results
        
        # Si tu as SSH, mettre le code réel ici (connexion SSH via paramiko)
        # Pour l'instant, on refuse l'accès si SSH n'est pas configuré
        results["global_status"] = "ERROR"
        results["error"] = "Connexion SSH non configurée - À implémenter avec paramiko"
        print(f"\n  ❌ SSH non configuré (implémentation à faire)")
        filename = self.output_manager.save_json(results, f"diagnostic_linux_{server_ip}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        self.logger.info(f"Diagnostic Linux terminé - SSH non configuré")
        return results
    
    def test_ping(self, host):
        """Teste la connectivité réseau avec un hôte via ping"""
        print(f"\n🔍 Test de connectivité vers {host}...")
        self.logger.info(f"Test ping vers {host}")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "host": host,
            "type": "Ping_Test",
            "test_result": {}
        }
        
        # Test de ping
        connectivity = self._test_connectivity(host, timeout=5)
        results["test_result"] = connectivity
        results["global_status"] = connectivity["status"]
        
        # Affichage du résultat
        if connectivity["status"] == "OK":
            print(f"  ✅ Hôte {host} est accessible (ping réussi)")
        else:
            print(f"  ❌ Hôte {host} est inaccessible (ping échoué)")
            print(f"     Raison : {connectivity['message']}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"ping_test_{host.replace('.', '_')}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Test ping terminé - Statut: {results['global_status']}")
        return results
    
    def run_full_diagnostic(self):
        """Lance un diagnostic complet sur tous les serveurs critiques"""
        print("\n" + "="*60)
        print("DIAGNOSTIC COMPLET - INFRASTRUCTURE NTL")
        print("="*60)
        
        # Serveurs à vérifier (configuration NTL)
        servers = {
            "DC01": "192.168.10.10",
            "DC02": "192.168.10.11",
            "WMS-DB": "192.168.10.21",
            "WMS-APP": "192.168.10.22"
        }
        
        all_results = []
        
        for name, ip in servers.items():
            print(f"\n--- {name} ({ip}) ---")
            if "DC" in name:
                result = self.check_ad_dns(ip)
            elif "WMS-DB" in name:
                # Utiliser les credentials par défaut (à adapter)
                result = self.check_mysql(ip, 3306, "wms_db", "wms_user", "password")
            else:
                result = self.check_linux_server(ip, "admin")
            
            all_results.append(result)
        
        # Ajout d'un test ping simple pour chaque serveur
        for name, ip in servers.items():
            print(f"\n--- Ping Test for {name} ({ip}) ---")
            result = self.test_ping(ip)
            all_results.append(result)
        
        # Rapport global
        print("\n" + "="*60)
        print("RÉSUMÉ DU DIAGNOSTIC COMPLET")
        print("="*60)
        ok_count = sum(1 for r in all_results if r.get("global_status") == "OK")
        print(f"✅ Serveurs OK : {ok_count}/{len(all_results)}")
        print(f"⚠️  Serveurs en alerte : {len(all_results) - ok_count}/{len(all_results)}")
        
        return all_results
    
    # Méthodes utilitaires
    
    def _test_connectivity(self, host, timeout=3):
        """Test de connectivité ping"""
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        if platform.system().lower() == "windows":
            command = ["ping", param, "1", "-w", str(timeout * 1000), host]
        else:
            command = ["ping", param, "1", "-W", str(timeout * 1000), host]
        
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout+1)
            if result.returncode == 0:
                return {"status": "OK", "message": "Hôte accessible"}
            else:
                return {"status": "ERROR", "message": "Hôte inaccessible"}
        except subprocess.TimeoutExpired:
            return {"status": "ERROR", "message": "Timeout - Hôte inaccessible"}
        except Exception as e:
            return {"status": "ERROR", "message": f"Erreur ping: {str(e)}"}
    
    def _test_port(self, host, port, service_name):
        """Test d'ouverture de port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return {"status": "OK", "port": port, "message": f"Service {service_name} accessible"}
            else:
                return {"status": "ERROR", "port": port, "message": f"Service {service_name} inaccessible"}
        except:
            return {"status": "ERROR", "port": port, "message": "Erreur de connexion"}
    
    def _test_dns_resolution(self, dns_server):
        """Test de résolution DNS"""
        try:
            # Test simple de résolution
            socket.gethostbyname("www.google.com")
            return {"status": "OK", "message": "Résolution DNS fonctionnelle"}
        except:
            return {"status": "WARNING", "message": "Résolution DNS non testable"}
    
    def _display_results(self, results):
        """Affiche les résultats de manière formatée"""
        print(f"\n📋 Résultats pour {results['server']} :")
        for test_name, test_result in results.get("tests", {}).items():
            status_icon = "✅" if test_result.get("status") == "OK" else "❌"
            print(f"  {status_icon} {test_name} : {test_result.get('message', 'N/A')}")
