"""
Utilitaire de gestion des sorties JSON
"""

import json
import os
from datetime import datetime

class OutputManager:
    """Gestionnaire des fichiers de sortie JSON"""
    
    def __init__(self, output_dir="output/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_json(self, data, filename_prefix):
        """Sauvegarde des données au format JSON avec horodatage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Ajout de métadonnées
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tool": "NTL-SysToolbox v1.0",
                "format_version": "1.0"
            },
            "data": data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            return filepath
        except Exception as e:
            print(f"Erreur lors de la sauvegarde JSON : {e}")
            return None
    
    def load_json(self, filepath):
        """Charge un fichier JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement JSON : {e}")
            return None
