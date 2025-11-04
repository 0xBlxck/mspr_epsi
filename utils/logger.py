"""
Utilitaire de gestion des logs
"""

import os
import logging
from datetime import datetime

class Logger:
    """Gestionnaire de logs pour l'application"""
    
    def __init__(self, log_dir="output/logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Configuration du logger
        log_file = os.path.join(log_dir, f"ntl_systoolbox_{datetime.now().strftime('%Y%m%d')}.log")
        
        self.logger = logging.getLogger('NTL-SysToolbox')
        self.logger.setLevel(logging.INFO)
        
        # Handler fichier
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Handler console (seulement pour les warnings et erreurs)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format des logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajout des handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log de niveau INFO"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log de niveau WARNING"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de niveau ERROR"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log de niveau DEBUG"""
        self.logger.debug(message)
    
    def get_recent_logs(self, count=20):
        """Récupère les derniers logs"""
        log_file = os.path.join(self.log_dir, f"ntl_systoolbox_{datetime.now().strftime('%Y%m%d')}.log")
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-count:] if len(lines) > count else lines
        except FileNotFoundError:
            return []
