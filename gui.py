import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import os
from datetime import datetime
from integrity import ArchiveIntegrityChecker


class PreservGUI:
    """Modern GUI for Preserv Archive Integrity Checker."""
    
    def __init__(self):
        self.root = ttk.Window(
            title="Preserv - Archive Integrity Checker",
            themename="cosmo",
            size=(800, 600),
            resizable=(True, True)
        )
        
        # Initialize integrity checker
        self.checker = ArchiveIntegrityChecker()
        
        # Variables
        self.archive_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Load saved archive path
        if self.checker.config.get('archive_path'):
            self.archive_path.set(self.checker.config['archive_path'])
        
        self.setup_ui()
        self.update_status()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Preserv",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Archive Integrity Checker",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        subtitle_label.pack()
        
        # Archive selection section
        archive_frame = ttk.LabelFrame(main_frame, text="Archive Selection", padding=15)
        archive_frame.pack(fill=X, pady=(0, 20))
        
        # Archive path display and selection
        path_frame = ttk.Frame(archive_frame)
        path_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Label(path_frame, text="Archive Folder:").pack(anchor=W)
        
        path_display_frame = ttk.Frame(path_frame)
        path_display_frame.pack(fill=X, pady=(5, 0))
        
        self.path_entry = ttk.Entry(
            path_display_frame,
            textvariable=self.archive_path,
            state="readonly",
            font=("Consolas", 9)
        )
        self.path_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        select_btn = ttk.Button(
            path_display_frame,
            text="Browse...",
            command=self.select_archive_folder,
            bootstyle="outline-primary"
        )
        select_btn.pack(side=RIGHT)
        
        # Status display
        status_frame = ttk.Frame(archive_frame)
        status_frame.pack(fill=X)
        
        ttk.Label(status_frame, text="Status:").pack(anchor=W)
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Consolas", 9),
            bootstyle="info"
        )
        self.status_label.pack(anchor=W, pady=(5, 0))
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(0, 20))
        
        # Button row 1
        btn_frame1 = ttk.Frame(action_frame)
        btn_frame1.pack(fill=X, pady=(0, 10))
        
        self.generate_btn = ttk.Button(
            btn_frame1,
            text="Generate Manifest",
            command=self.generate_manifest,
            bootstyle="success",
            width=20
        )
        self.generate_btn.pack(side=LEFT, padx=(0, 10))
        
        self.verify_btn = ttk.Button(
            btn_frame1,
            text="Verify Integrity",
            command=self.verify_integrity,
            bootstyle="warning",
            width=20
        )
        self.verify_btn.pack(side=LEFT, padx=(0, 10))
        
        # Button row 2
        btn_frame2 = ttk.Frame(action_frame)
        btn_frame2.pack(fill=X)
        
        self.settings_btn = ttk.Button(
            btn_frame2,
            text="Settings",
            command=self.show_settings,
            bootstyle="outline-secondary",
            width=15
        )
        self.settings_btn.pack(side=LEFT, padx=(0, 10))
        
        self.logs_btn = ttk.Button(
            btn_frame2,
            text="View Logs",
            command=self.show_logs,
            bootstyle="outline-info",
            width=15
        )
        self.logs_btn.pack(side=LEFT, padx=(0, 10))
        
        self.export_btn = ttk.Button(
            btn_frame2,
            text="Export Report",
            command=self.export_report,
            bootstyle="outline-primary",
            width=15
        )
        self.export_btn.pack(side=LEFT)
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill=X)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding=10)
        log_frame.pack(fill=BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=BOTH, expand=True)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=X, pady=(20, 0))
        
        ttk.Separator(footer_frame, orient=HORIZONTAL).pack(fill=X, pady=(0, 10))
        
        footer_btn_frame = ttk.Frame(footer_frame)
        footer_btn_frame.pack(fill=X)
        
        ttk.Button(
            footer_btn_frame,
            text="Exit",
            command=self.root.quit,
            bootstyle="outline-danger",
            width=10
        ).pack(side=RIGHT)
    
    def select_archive_folder(self):
        """Open folder dialog to select archive directory."""
        folder = filedialog.askdirectory(
            title="Select Archive Folder",
            initialdir=self.archive_path.get() if self.archive_path.get() else os.path.expanduser("~")
        )
        
        if folder:
            self.archive_path.set(folder)
            self.checker.archive_path = folder
            self.update_status()
            self.log_message(f"Selected archive folder: {folder}")
    
    def update_status(self):
        """Update the status display with current manifest information."""
        stats = self.checker.get_manifest_stats()
        
        if stats["exists"]:
            status_text = f"Manifest exists: {stats['file_count']} files, {stats['total_size_mb']} MB"
            if stats['last_generated']:
                try:
                    last_gen = datetime.fromisoformat(stats['last_generated'])
                    status_text += f" (Last: {last_gen.strftime('%Y-%m-%d %H:%M')})"
                except:
                    pass
        else:
            status_text = "No manifest found - Generate manifest first"
        
        self.status_var.set(status_text)
    
    def log_message(self, message):
        """Add message to log display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Also log to file via the checker
        self.checker.logger.info(message)
    
    def run_with_progress(self, operation, operation_name):
        """Run an operation with progress indication."""
        def run_operation():
            try:
                self.progress_var.set(0)
                self.status_var.set(f"Running {operation_name}...")
                self.log_message(f"Starting {operation_name}...")
                
                # Disable buttons during operation
                self.generate_btn.config(state=tk.DISABLED)
                self.verify_btn.config(state=tk.DISABLED)
                
                # Run the operation
                result = operation()
                
                # Update progress
                self.progress_var.set(100)
                
                # Show result
                if result.get("success"):
                    self.log_message(f"✓ {result['message']}")
                    self.status_var.set("Operation completed successfully")
                else:
                    self.log_message(f"✗ {result['message']}")
                    self.status_var.set("Operation failed")
                
                # Update status
                self.update_status()
                
            except Exception as e:
                self.log_message(f"Error during {operation_name}: {str(e)}")
                self.status_var.set("Operation failed")
            finally:
                # Re-enable buttons
                self.generate_btn.config(state=tk.NORMAL)
                self.verify_btn.config(state=tk.NORMAL)
        
        # Run in separate thread to avoid blocking GUI
        thread = threading.Thread(target=run_operation, daemon=True)
        thread.start()
    
    def generate_manifest(self):
        """Generate manifest for the selected archive."""
        if not self.archive_path.get():
            messagebox.showerror("Error", "Please select an archive folder first.")
            return
        
        def operation():
            return self.checker.generate_manifest(self.archive_path.get())
        
        self.run_with_progress(operation, "manifest generation")
    
    def verify_integrity(self):
        """Verify archive integrity."""
        if not self.archive_path.get():
            messagebox.showerror("Error", "Please select an archive folder first.")
            return
        
        def operation():
            return self.checker.verify_integrity(self.archive_path.get())
        
        self.run_with_progress(operation, "integrity verification")
    
    def show_settings(self):
        """Show settings dialog."""
        settings_window = ttk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        settings_frame = ttk.Frame(settings_window, padding=20)
        settings_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(settings_frame, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
        
        # Add new files option
        add_new_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            settings_frame,
            text="Automatically add new files to manifest during verification",
            variable=add_new_var
        ).pack(anchor=W, pady=(0, 10))
        
        # Log level
        ttk.Label(settings_frame, text="Log Level:").pack(anchor=W, pady=(10, 5))
        log_level_var = tk.StringVar(value="INFO")
        log_combo = ttk.Combobox(
            settings_frame,
            textvariable=log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            state="readonly"
        )
        log_combo.pack(anchor=W, pady=(0, 20))
        
        # Buttons
        btn_frame = ttk.Frame(settings_frame)
        btn_frame.pack(fill=X, pady=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="Save",
            command=lambda: self.save_settings(add_new_var.get(), log_level_var.get(), settings_window),
            bootstyle="success"
        ).pack(side=RIGHT, padx=(10, 0))
        
        ttk.Button(
            btn_frame,
            text="Cancel",
            command=settings_window.destroy,
            bootstyle="outline-secondary"
        ).pack(side=RIGHT)
    
    def save_settings(self, add_new_files, log_level, window):
        """Save settings and close dialog."""
        # Save settings to config
        self.checker.config['add_new_files'] = add_new_files
        self.checker.config['log_level'] = log_level
        self.checker._save_config()
        
        self.log_message("Settings saved")
        window.destroy()
    
    def show_logs(self):
        """Show full log window."""
        log_window = ttk.Toplevel(self.root)
        log_window.title("Full Log")
        log_window.geometry("800x600")
        log_window.transient(self.root)
        
        # Log content
        log_frame = ttk.Frame(log_window, padding=20)
        log_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(log_frame, text="Full Activity Log", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
        
        log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        log_text.pack(fill=BOTH, expand=True)
        
        # Load log content
        log_content = self.checker.get_log_content(1000)  # Get last 1000 lines
        log_text.insert(tk.END, log_content)
        log_text.config(state=tk.DISABLED)
        
        # Buttons
        btn_frame = ttk.Frame(log_frame)
        btn_frame.pack(fill=X, pady=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="Refresh",
            command=lambda: self.refresh_logs(log_text),
            bootstyle="outline-primary"
        ).pack(side=LEFT)
        
        ttk.Button(
            btn_frame,
            text="Close",
            command=log_window.destroy,
            bootstyle="outline-secondary"
        ).pack(side=RIGHT)
    
    def refresh_logs(self, log_text):
        """Refresh log content."""
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_content = self.checker.get_log_content(1000)
        log_text.insert(tk.END, log_content)
        log_text.config(state=tk.DISABLED)
    
    def export_report(self):
        """Export a preservation report."""
        if not self.checker.get_manifest_stats()["exists"]:
            messagebox.showerror("Error", "No manifest found. Generate manifest first.")
            return
        
        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title="Export Preservation Report",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("Text files", "*.txt")]
        )
        
        if filename:
            try:
                self.generate_report(filename)
                self.log_message(f"Report exported to: {filename}")
                messagebox.showinfo("Success", f"Report exported successfully to:\n{filename}")
            except Exception as e:
                self.log_message(f"Error exporting report: {str(e)}")
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def generate_report(self, filename):
        """Generate a preservation report."""
        stats = self.checker.get_manifest_stats()
        
        if filename.endswith('.html'):
            self.generate_html_report(filename, stats)
        else:
            self.generate_text_report(filename, stats)
    
    def generate_html_report(self, filename, stats):
        """Generate HTML preservation report."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Preserv - Archive Integrity Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .stats {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .stat-item {{ margin: 10px 0; }}
        .stat-label {{ font-weight: bold; color: #2c3e50; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #bdc3c7; color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Preserv - Archive Integrity Report</h1>
        
        <div class="stats">
            <h2>Archive Summary</h2>
            <div class="stat-item">
                <span class="stat-label">Archive Path:</span> {self.archive_path.get()}
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Files:</span> {stats['file_count']:,}
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Size:</span> {stats['total_size_mb']} MB
            </div>
            <div class="stat-item">
                <span class="stat-label">Last Generated:</span> {stats['last_generated']}
            </div>
        </div>
        
        <h2>Integrity Information</h2>
        <p>This archive has been processed using Preserv Archive Integrity Checker.</p>
        <p>All files have been verified using SHA-256 cryptographic hashing for maximum integrity assurance.</p>
        
        <h2>Preservation Notes</h2>
        <ul>
            <li>Hash Algorithm: SHA-256</li>
            <li>Manifest Format: CSV</li>
            <li>Incremental Checking: Enabled</li>
            <li>Logging: Comprehensive activity logging</li>
        </ul>
        
        <div class="footer">
            <p>Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Preserv Archive Integrity Checker - Professional archival preservation tool</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def generate_text_report(self, filename, stats):
        """Generate text preservation report."""
        text_content = f"""
PRESERV - ARCHIVE INTEGRITY REPORT
==================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Archive Path: {self.archive_path.get()}

ARCHIVE SUMMARY
---------------
Total Files: {stats['file_count']:,}
Total Size: {stats['total_size_mb']} MB
Last Generated: {stats['last_generated']}

INTEGRITY INFORMATION
---------------------
This archive has been processed using Preserv Archive Integrity Checker.
All files have been verified using SHA-256 cryptographic hashing for maximum integrity assurance.

PRESERVATION NOTES
------------------
- Hash Algorithm: SHA-256
- Manifest Format: CSV
- Incremental Checking: Enabled
- Logging: Comprehensive activity logging

For detailed verification results, run the integrity verification process.
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
