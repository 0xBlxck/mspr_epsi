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
    
    def check_windows_server(self, server_ip, user=None, password=None):
        """Vérifie l'état d'un serveur Windows via WinRM"""
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
        
        try:
            import winrm
        except ImportError:
            results["global_status"] = "ERROR"
            results["error"] = "pywinrm non installé - pip install pywinrm"
            print(f"\n  ❌ WinRM non disponible (pip install pywinrm)")
            filename = self.output_manager.save_json(results, f"diagnostic_windows_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            self.logger.error("pywinrm non installé")
            return results
        
        if not user or not password:
            results["global_status"] = "ERROR"
            results["error"] = "Identifiants WinRM requis (user et password)"
            print(f"  ❌ Identifiants WinRM manquants")
            filename = self.output_manager.save_json(results, f"diagnostic_windows_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            return results
        
        # Connexion WinRM réelle
        try:
            print("  → Connexion WinRM en cours...")
            session = winrm.Session(
                f"http://{server_ip}:5985/wsman",
                auth=(user, password),
                transport='ntlm'
            )
            
            # Test de connexion
            test_result = session.run_ps("$env:COMPUTERNAME")
            if test_result.status_code != 0:
                raise Exception(f"Erreur WinRM: {test_result.std_err.decode()}")
            
            hostname = test_result.std_out.decode().strip()
            results["system_info"]["hostname"] = hostname
            print(f"  ✅ Connexion WinRM établie")
            print(f"  📊 Hostname : {hostname}")
            
            # OS et version
            os_cmd = "Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, LastBootUpTime | ConvertTo-Json"
            os_result = session.run_ps(os_cmd)
            if os_result.status_code == 0:
                import json as json_lib
                os_data = json_lib.loads(os_result.std_out.decode())
                results["system_info"]["os"] = os_data.get("Caption", "Windows Server")
                results["system_info"]["version"] = os_data.get("Version", "Unknown")
                print(f"  📊 Système : {os_data.get('Caption', 'Windows Server')}")
                
                # Calcul uptime
                if "LastBootUpTime" in os_data:
                    boot_time_str = os_data["LastBootUpTime"]
                    # Format: /Date(timestamp)/
                    if "/Date(" in boot_time_str:
                        timestamp_ms = int(boot_time_str.replace("/Date(", "").replace(")/", "").split("+")[0].split("-")[0])
                        boot_time = datetime.fromtimestamp(timestamp_ms / 1000)
                        uptime = datetime.now() - boot_time
                        results["system_info"]["uptime_days"] = uptime.days
                        print(f"  📊 Uptime : {uptime.days} jours")
            
            # CPU Usage
            cpu_cmd = "Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average"
            cpu_result = session.run_ps(cpu_cmd)
            if cpu_result.status_code == 0:
                cpu_usage = float(cpu_result.std_out.decode().strip() or 0)
                results["resources"]["cpu_usage_percent"] = round(cpu_usage, 1)
                print(f"  📊 CPU : {cpu_usage:.1f}%")
            
            # RAM
            ram_cmd = """
            $os = Get-CimInstance Win32_OperatingSystem
            $totalRam = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
            $freeRam = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
            $usedRam = [math]::Round($totalRam - $freeRam, 2)
            $percentUsed = [math]::Round(($usedRam / $totalRam) * 100, 1)
            @{TotalGB=$totalRam; UsedGB=$usedRam; PercentUsed=$percentUsed} | ConvertTo-Json
            """
            ram_result = session.run_ps(ram_cmd)
            if ram_result.status_code == 0:
                import json as json_lib
                ram_data = json_lib.loads(ram_result.std_out.decode())
                results["resources"]["ram_total_gb"] = ram_data.get("TotalGB", 0)
                results["resources"]["ram_used_gb"] = ram_data.get("UsedGB", 0)
                results["resources"]["ram_usage_percent"] = ram_data.get("PercentUsed", 0)
                print(f"  📊 RAM : {ram_data.get('PercentUsed', 0)}% ({ram_data.get('UsedGB', 0)}/{ram_data.get('TotalGB', 0)} GB)")
            
            # Disques
            disk_cmd = """
            Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | 
            Select-Object DeviceID, 
                @{N='TotalGB';E={[math]::Round($_.Size/1GB,2)}}, 
                @{N='UsedGB';E={[math]::Round(($_.Size - $_.FreeSpace)/1GB,2)}}, 
                @{N='PercentUsed';E={[math]::Round((($_.Size - $_.FreeSpace)/$_.Size)*100,1)}} | 
            ConvertTo-Json
            """
            disk_result = session.run_ps(disk_cmd)
            if disk_result.status_code == 0:
                import json as json_lib
                disk_data = json_lib.loads(disk_result.std_out.decode())
                # Si un seul disque, convertir en liste
                if isinstance(disk_data, dict):
                    disk_data = [disk_data]
                
                disks = []
                for disk in disk_data:
                    disks.append({
                        "drive": disk.get("DeviceID", "?"),
                        "total_gb": disk.get("TotalGB", 0),
                        "used_gb": disk.get("UsedGB", 0),
                        "usage_percent": disk.get("PercentUsed", 0)
                    })
                    print(f"  📊 Disque {disk.get('DeviceID', '?')} : {disk.get('PercentUsed', 0)}% ({disk.get('UsedGB', 0)}/{disk.get('TotalGB', 0)} GB)")
                
                results["resources"]["disks"] = disks
            
            results["global_status"] = "OK"
            
        except Exception as e:
            results["global_status"] = "ERROR"
            results["error"] = str(e)
            print(f"  ❌ Erreur WinRM: {e}")
            self.logger.error(f"Erreur diagnostic Windows: {e}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"diagnostic_windows_{server_ip}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Diagnostic Windows terminé - Statut: {results.get('global_status', 'UNKNOWN')}")
        return results
    
    def check_linux_server(self, server_ip, user, password=None, ssh_key_path=None):
        """Vérifie l'état d'un serveur Linux via SSH"""
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
            results["error"] = "Paramiko non installé - pip install paramiko"
            print(f"\n  ❌ SSH non disponible (pip install paramiko)")
            filename = self.output_manager.save_json(results, f"diagnostic_linux_{server_ip}")
            print(f"\n💾 Résultats sauvegardés : {filename}")
            self.logger.error("Paramiko non installé")
            return results
        
        # Connexion SSH réelle
        try:
            print("  → Connexion SSH en cours...")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if ssh_key_path:
                ssh.connect(server_ip, username=user, key_filename=ssh_key_path, timeout=10)
            else:
                ssh.connect(server_ip, username=user, password=password, timeout=10)
            
            print("  ✅ Connexion SSH établie")
            
            # Récupération des informations système
            # OS et version
            stdin, stdout, stderr = ssh.exec_command("cat /etc/os-release | grep -E '^(NAME|VERSION)=' | head -2")
            os_info = stdout.read().decode().strip()
            os_name = "Linux"
            os_version = "Unknown"
            for line in os_info.split('\n'):
                if line.startswith('NAME='):
                    os_name = line.split('=')[1].strip('"')
                elif line.startswith('VERSION='):
                    os_version = line.split('=')[1].strip('"')
            
            results["system_info"]["os"] = f"{os_name} {os_version}"
            print(f"  📊 Système : {os_name} {os_version}")
            
            # Hostname
            stdin, stdout, stderr = ssh.exec_command("hostname")
            hostname = stdout.read().decode().strip()
            results["system_info"]["hostname"] = hostname
            print(f"  📊 Hostname : {hostname}")
            
            # Uptime
            stdin, stdout, stderr = ssh.exec_command("uptime -p")
            uptime = stdout.read().decode().strip()
            results["system_info"]["uptime"] = uptime
            print(f"  📊 Uptime : {uptime}")
            
            # CPU Usage
            stdin, stdout, stderr = ssh.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
            cpu_output = stdout.read().decode().strip()
            try:
                cpu_usage = float(cpu_output)
            except:
                cpu_usage = 0.0
            results["resources"]["cpu_usage_percent"] = round(cpu_usage, 2)
            print(f"  📊 CPU : {cpu_usage:.1f}%")
            
            # RAM
            stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem")
            mem_output = stdout.read().decode().strip().split()
            if len(mem_output) >= 3:
                ram_total = int(mem_output[1]) / 1024  # Convertir en GB
                ram_used = int(mem_output[2]) / 1024
                ram_percent = (ram_used / ram_total) * 100 if ram_total > 0 else 0
                results["resources"]["ram_total_gb"] = round(ram_total, 2)
                results["resources"]["ram_used_gb"] = round(ram_used, 2)
                results["resources"]["ram_usage_percent"] = round(ram_percent, 1)
                print(f"  📊 RAM : {ram_percent:.1f}% ({ram_used:.1f}/{ram_total:.1f} GB)")
            
            # Disques
            stdin, stdout, stderr = ssh.exec_command("df -h --output=target,size,used,pcent | tail -n +2 | grep -E '^/(|home|var|opt|data)'")
            disk_output = stdout.read().decode().strip()
            disks = []
            for line in disk_output.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        mount = parts[0]
                        total = parts[1]
                        used = parts[2]
                        percent = parts[3].replace('%', '')
                        disks.append({
                            "mount": mount,
                            "total": total,
                            "used": used,
                            "usage_percent": int(percent) if percent.isdigit() else 0
                        })
                        print(f"  📊 Disque {mount} : {percent}% ({used}/{total})")
            
            results["resources"]["disks"] = disks
            
            ssh.close()
            results["global_status"] = "OK"
            
        except paramiko.AuthenticationException:
            results["global_status"] = "ERROR"
            results["error"] = "Échec d'authentification SSH"
            print(f"  ❌ Échec d'authentification SSH")
            self.logger.error(f"Échec d'authentification SSH sur {server_ip}")
        except paramiko.SSHException as e:
            results["global_status"] = "ERROR"
            results["error"] = f"Erreur SSH: {str(e)}"
            print(f"  ❌ Erreur SSH: {e}")
            self.logger.error(f"Erreur SSH: {e}")
        except Exception as e:
            results["global_status"] = "ERROR"
            results["error"] = str(e)
            print(f"  ❌ Erreur: {e}")
            self.logger.error(f"Erreur diagnostic Linux: {e}")
        
        # Sauvegarde JSON
        filename = self.output_manager.save_json(results, f"diagnostic_linux_{server_ip}")
        print(f"\n💾 Résultats sauvegardés : {filename}")
        
        self.logger.info(f"Diagnostic Linux terminé - Statut: {results.get('global_status', 'UNKNOWN')}")
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
            # Sur Linux, utiliser -w (en secondes) à la place de -W (non portable)
            command = ["ping", param, "1", "-w", str(timeout), host]
        
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
