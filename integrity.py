import hashlib
import os
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ArchiveIntegrityChecker:
    """Core class for archive integrity checking and manifest management."""
    
    def __init__(self, archive_path: str = None):
        self.archive_path = archive_path
        self.manifest_file = "manifest.csv"
        self.config_file = "config.json"
        self.log_file = "integrity_log.txt"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
        return {"archive_path": "", "last_run": None}
    
    def _save_config(self):
        """Save configuration to JSON file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file using streaming for memory efficiency."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def _get_file_info(self, file_path: str) -> Tuple[str, int, float]:
        """Get file hash, size, and modification time."""
        try:
            stat = os.stat(file_path)
            file_hash = self._calculate_file_hash(file_path)
            return file_hash, stat.st_size, stat.st_mtime
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {e}")
            return "", 0, 0
    
    def _load_manifest(self) -> Dict[str, Dict]:
        """Load existing manifest from CSV file."""
        manifest = {}
        if os.path.exists(self.manifest_file):
            try:
                with open(self.manifest_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        manifest[row['file_path']] = {
                            'checksum': row['checksum'],
                            'size': int(row['size']),
                            'modified_time': float(row['modified_time']),
                            'date_generated': row['date_generated']
                        }
            except Exception as e:
                self.logger.error(f"Error loading manifest: {e}")
        return manifest
    
    def _save_manifest(self, manifest: Dict[str, Dict]):
        """Save manifest to CSV file."""
        try:
            with open(self.manifest_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['file_path', 'checksum', 'size', 'modified_time', 'date_generated']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for file_path, info in manifest.items():
                    writer.writerow({
                        'file_path': file_path,
                        'checksum': info['checksum'],
                        'size': info['size'],
                        'modified_time': info['modified_time'],
                        'date_generated': info['date_generated']
                    })
        except Exception as e:
            self.logger.error(f"Error saving manifest: {e}")
    
    def generate_manifest(self, archive_path: str = None) -> Dict[str, any]:
        """Generate a new manifest for the archive."""
        if archive_path:
            self.archive_path = archive_path
            self.config['archive_path'] = archive_path
        
        if not self.archive_path or not os.path.exists(self.archive_path):
            return {"success": False, "message": "Invalid archive path"}
        
        self.logger.info(f"Generating manifest for: {self.archive_path}")
        
        manifest = {}
        total_files = 0
        processed_files = 0
        
        # Count total files first
        for root, dirs, files in os.walk(self.archive_path):
            total_files += len(files)
        
        # Process files
        for root, dirs, files in os.walk(self.archive_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.archive_path)
                
                self.logger.info(f"Processing: {relative_path}")
                
                file_hash, file_size, mod_time = self._get_file_info(file_path)
                
                if file_hash:  # Only add if hash calculation succeeded
                    manifest[relative_path] = {
                        'checksum': file_hash,
                        'size': file_size,
                        'modified_time': mod_time,
                        'date_generated': datetime.now().isoformat()
                    }
                    processed_files += 1
        
        # Save manifest
        self._save_manifest(manifest)
        
        # Update config
        self.config['last_run'] = datetime.now().isoformat()
        self._save_config()
        
        result = {
            "success": True,
            "message": f"Manifest generated successfully. {processed_files} files processed.",
            "total_files": total_files,
            "processed_files": processed_files
        }
        
        self.logger.info(f"Manifest generation complete: {result['message']}")
        return result
    
    def verify_integrity(self, archive_path: str = None, add_new_files: bool = False) -> Dict[str, any]:
        """Verify archive integrity against existing manifest."""
        if archive_path:
            self.archive_path = archive_path
            self.config['archive_path'] = archive_path
        
        if not self.archive_path or not os.path.exists(self.archive_path):
            return {"success": False, "message": "Invalid archive path"}
        
        if not os.path.exists(self.manifest_file):
            return {"success": False, "message": "No manifest found. Generate manifest first."}
        
        self.logger.info(f"Verifying integrity for: {self.archive_path}")
        
        manifest = self._load_manifest()
        results = {
            "ok": [],
            "modified": [],
            "missing": [],
            "new": [],
            "errors": []
        }
        
        # Check existing files in manifest
        for relative_path, manifest_info in manifest.items():
            file_path = os.path.join(self.archive_path, relative_path)
            
            if not os.path.exists(file_path):
                results["missing"].append(relative_path)
                self.logger.warning(f"MISSING: {relative_path}")
                continue
            
            try:
                stat = os.stat(file_path)
                current_size = stat.st_size
                current_mod_time = stat.st_mtime
                
                # Check if file needs re-hashing
                if (current_size != manifest_info['size'] or 
                    current_mod_time != manifest_info['modified_time']):
                    
                    # File changed, re-hash
                    current_hash = self._calculate_file_hash(file_path)
                    if current_hash == manifest_info['checksum']:
                        results["ok"].append(relative_path)
                        self.logger.info(f"OK: {relative_path} (size/mod time changed but hash matches)")
                    else:
                        results["modified"].append(relative_path)
                        self.logger.error(f"MODIFIED: {relative_path}")
                else:
                    # File unchanged, skip hashing
                    results["ok"].append(relative_path)
                    self.logger.info(f"OK: {relative_path} (unchanged)")
                    
            except Exception as e:
                results["errors"].append(f"{relative_path}: {str(e)}")
                self.logger.error(f"ERROR processing {relative_path}: {e}")
        
        # Check for new files
        for root, dirs, files in os.walk(self.archive_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.archive_path)
                
                if relative_path not in manifest:
                    results["new"].append(relative_path)
                    self.logger.info(f"NEW: {relative_path}")
        
        # Update manifest with new files if requested
        if add_new_files and results["new"]:
            for relative_path in results["new"]:
                file_path = os.path.join(self.archive_path, relative_path)
                file_hash, file_size, mod_time = self._get_file_info(file_path)
                
                if file_hash:
                    manifest[relative_path] = {
                        'checksum': file_hash,
                        'size': file_size,
                        'modified_time': mod_time,
                        'date_generated': datetime.now().isoformat()
                    }
            
            self._save_manifest(manifest)
            self.logger.info(f"Added {len(results['new'])} new files to manifest")
        
        # Update config
        self.config['last_run'] = datetime.now().isoformat()
        self._save_config()
        
        summary = {
            "success": True,
            "message": f"Integrity check complete. OK: {len(results['ok'])}, Modified: {len(results['modified'])}, Missing: {len(results['missing'])}, New: {len(results['new'])}",
            "results": results
        }
        
        self.logger.info(f"Integrity verification complete: {summary['message']}")
        return summary
    
    def get_log_content(self, lines: int = 100) -> str:
        """Get recent log content."""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        except Exception as e:
            return f"Error reading log file: {e}"
    
    def get_manifest_stats(self) -> Dict[str, any]:
        """Get statistics about the current manifest."""
        if not os.path.exists(self.manifest_file):
            return {"exists": False}
        
        manifest = self._load_manifest()
        total_size = sum(info['size'] for info in manifest.values())
        
        return {
            "exists": True,
            "file_count": len(manifest),
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "last_generated": max(info['date_generated'] for info in manifest.values()) if manifest else None
        }
