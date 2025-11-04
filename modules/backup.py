"""
Module Sauvegarde - Gestion des sauvegardes de la base WMS
"""

import os
import csv
from datetime import datetime

class BackupModule:
    """Module de sauvegarde de base de données"""
    
    def __init__(self, logger, output_manager):
        self.logger = logger
        self.output_manager = output_manager
        self.backup_dir = "output/backups"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_database(self, host, port, database, user, password):
        """Sauvegarde complète de la base de données au format SQL"""
        print(f"\n💾 Sauvegarde de la base {database} sur {host}:{port}...")
        self.logger.info(f"Début sauvegarde base {database}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"{database}_backup_{timestamp}.sql")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "type": "database_backup",
            "database": database,
            "host": host,
            "port": port,
            "backup_file": backup_file
        }
        
        try:
            import mysql.connector
            
            # Connexion à la base
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            
            # Récupération de toutes les tables
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            print(f"  → {len(tables)} tables trouvées")
            
            # Création du fichier SQL
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(f"-- Sauvegarde de la base {database}\n")
                f.write(f"-- Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- Serveur : {host}:{port}\n\n")
                f.write(f"CREATE DATABASE IF NOT EXISTS `{database}`;\n")
                f.write(f"USE `{database}`;\n\n")
                
                for table in tables:
                    print(f"  → Sauvegarde de la table {table}...")
                    
                    # Structure de la table
                    cursor.execute(f"SHOW CREATE TABLE `{table}`")
                    create_table = cursor.fetchone()[1]
                    f.write(f"-- Table: {table}\n")
                    f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                    f.write(f"{create_table};\n\n")
                    
                    # Données de la table
                    cursor.execute(f"SELECT * FROM `{table}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        cursor.execute(f"DESCRIBE `{table}`")
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        f.write(f"-- Données de {table} ({len(rows)} lignes)\n")
                        f.write(f"INSERT INTO `{table}` (`{'`, `'.join(columns)}`) VALUES\n")
                        
                        for i, row in enumerate(rows):
                            values = []
                            for val in row:
                                if val is None:
                                    values.append("NULL")
                                elif isinstance(val, str):
                                    values.append(f"'{val.replace(chr(39), chr(39)+chr(39))}'")
                                else:
                                    values.append(str(val))
                            
                            line_end = ";" if i == len(rows) - 1 else ","
                            f.write(f"({', '.join(values)}){line_end}\n")
                        
                        f.write("\n")
            
            cursor.close()
            conn.close()
            
            # Vérification de la taille du fichier
            file_size = os.path.getsize(backup_file)
            results["status"] = "OK"
            results["tables_count"] = len(tables)
            results["file_size_mb"] = round(file_size / (1024 * 1024), 2)
            
            print(f"\n  ✅ Sauvegarde réussie !")
            print(f"  📁 Fichier : {backup_file}")
            print(f"  📊 Taille : {results['file_size_mb']} MB")
            print(f"  📊 Tables : {results['tables_count']}")
            
        except ImportError:
            results["status"] = "ERROR"
            results["error"] = "Module mysql-connector-python non installé"
            print("  ❌ Module mysql-connector-python non installé")
            
        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)
            print(f"  ❌ Erreur : {e}")
        
        # Sauvegarde du rapport JSON
        report_file = self.output_manager.save_json(results, f"backup_report_{database}")
        print(f"  💾 Rapport sauvegardé : {report_file}")
        
        self.logger.info(f"Sauvegarde terminée - Statut: {results['status']}")
        return results
    
    def export_table_csv(self, host, port, database, table, user, password):
        """Export d'une table au format CSV"""
        print(f"\n📤 Export de la table {table} en CSV...")
        self.logger.info(f"Début export CSV de {table}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = os.path.join(self.backup_dir, f"{database}_{table}_{timestamp}.csv")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "type": "table_export_csv",
            "database": database,
            "table": table,
            "host": host,
            "csv_file": csv_file
        }
        
        try:
            import mysql.connector
            
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            
            # Récupération des colonnes
            cursor.execute(f"DESCRIBE `{table}`")
            columns = [col[0] for col in cursor.fetchall()]
            
            # Récupération des données
            cursor.execute(f"SELECT * FROM `{table}`")
            rows = cursor.fetchall()
            
            # Écriture du CSV
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(columns)
                writer.writerows(rows)
            
            cursor.close()
            conn.close()
            
            results["status"] = "OK"
            results["rows_count"] = len(rows)
            results["columns_count"] = len(columns)
            
            print(f"  ✅ Export réussi !")
            print(f"  📁 Fichier : {csv_file}")
            print(f"  📊 Lignes : {results['rows_count']}")
            print(f"  📊 Colonnes : {results['columns_count']}")
            
        except ImportError:
            results["status"] = "ERROR"
            results["error"] = "Module mysql-connector-python non installé"
            print("  ❌ Module mysql-connector-python non installé")
            
        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)
            print(f"  ❌ Erreur : {e}")
        
        report_file = self.output_manager.save_json(results, f"export_csv_{table}")
        print(f"  💾 Rapport sauvegardé : {report_file}")
        
        self.logger.info(f"Export CSV terminé - Statut: {results['status']}")
        return results
    
    def backup_all_tables(self, host, port, database, user, password):
        """Sauvegarde automatique de toutes les tables en CSV"""
        print(f"\n💾 Sauvegarde automatique de toutes les tables...")
        self.logger.info(f"Début sauvegarde automatique de {database}")
        
        try:
            import mysql.connector
            
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            conn.close()
            
            print(f"  → {len(tables)} tables à sauvegarder")
            
            results = []
            for table in tables:
                result = self.export_table_csv(host, port, database, table, user, password)
                results.append(result)
            
            success_count = sum(1 for r in results if r.get("status") == "OK")
            print(f"\n  ✅ Sauvegarde terminée : {success_count}/{len(tables)} tables exportées")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
            return []
