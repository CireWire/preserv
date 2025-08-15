#!/usr/bin/env python3
"""
Preserv - Archive Integrity Checker
A professional tool for archivists to maintain digital preservation integrity.

Usage:
    python main.py                    # Launch GUI
    python main.py --verify           # Run verification in headless mode
    python main.py --generate         # Generate manifest in headless mode
    python main.py --help             # Show help
"""

import sys
import argparse
import os
from pathlib import Path
from integrity import ArchiveIntegrityChecker
from gui import PreservGUI


def main():
    """Main entry point for Preserv application."""
    parser = argparse.ArgumentParser(
        description="Preserv - Archive Integrity Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch GUI
  python main.py --verify /path/to/archive    # Verify archive integrity
  python main.py --generate /path/to/archive  # Generate new manifest
  python main.py --verify --add-new /path/to/archive  # Verify and add new files
        """
    )
    
    parser.add_argument(
        '--verify',
        nargs='?',
        const=True,
        metavar='ARCHIVE_PATH',
        help='Verify archive integrity (headless mode)'
    )
    
    parser.add_argument(
        '--generate',
        nargs='?',
        const=True,
        metavar='ARCHIVE_PATH',
        help='Generate manifest (headless mode)'
    )
    
    parser.add_argument(
        '--add-new',
        action='store_true',
        help='Add new files to manifest during verification'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--manifest',
        help='Path to manifest file'
    )
    
    parser.add_argument(
        '--log',
        help='Path to log file'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, launch GUI
    if len(sys.argv) == 1:
        launch_gui()
        return
    
    # Command-line mode
    if args.verify or args.generate:
        run_cli_mode(args)
    else:
        # If arguments provided but not recognized, show help
        parser.print_help()


def launch_gui():
    """Launch the GUI application."""
    try:
        app = PreservGUI()
        print("Starting Preserv Archive Integrity Checker...")
        print("GUI launched successfully.")
        app.run()
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)


def run_cli_mode(args):
    """Run Preserv in command-line mode."""
    # Determine archive path
    archive_path = None
    
    if args.verify and args.verify is not True:
        archive_path = args.verify
    elif args.generate and args.generate is not True:
        archive_path = args.generate
    else:
        # Try to get from config
        checker = ArchiveIntegrityChecker()
        archive_path = checker.config.get('archive_path')
        
        if not archive_path:
            print("Error: No archive path specified and none found in config.")
            print("Please provide archive path or run GUI to set it up.")
            sys.exit(1)
    
    # Validate archive path
    if not os.path.exists(archive_path):
        print(f"Error: Archive path does not exist: {archive_path}")
        sys.exit(1)
    
    # Initialize checker
    checker = ArchiveIntegrityChecker(archive_path)
    
    # Override file paths if specified
    if args.config:
        checker.config_file = args.config
    if args.manifest:
        checker.manifest_file = args.manifest
    if args.log:
        checker.log_file = args.log
    
    print(f"Preserv - Archive Integrity Checker")
    print(f"Archive: {archive_path}")
    print("-" * 50)
    
    try:
        if args.generate:
            print("Generating manifest...")
            result = checker.generate_manifest(archive_path)
            
            if result["success"]:
                print(f"✓ {result['message']}")
                print(f"  Files processed: {result['processed_files']}")
                print(f"  Total files found: {result['total_files']}")
            else:
                print(f"✗ {result['message']}")
                sys.exit(1)
        
        elif args.verify:
            print("Verifying integrity...")
            result = checker.verify_integrity(archive_path, add_new_files=args.add_new)
            
            if result["success"]:
                print(f"✓ {result['message']}")
                
                results = result["results"]
                print(f"\nResults:")
                print(f"  OK: {len(results['ok'])} files")
                print(f"  Modified: {len(results['modified'])} files")
                print(f"  Missing: {len(results['missing'])} files")
                print(f"  New: {len(results['new'])} files")
                
                if results['errors']:
                    print(f"  Errors: {len(results['errors'])}")
                
                # Show details for issues
                if results['modified']:
                    print(f"\nModified files:")
                    for file in results['modified'][:10]:  # Show first 10
                        print(f"  - {file}")
                    if len(results['modified']) > 10:
                        print(f"  ... and {len(results['modified']) - 10} more")
                
                if results['missing']:
                    print(f"\nMissing files:")
                    for file in results['missing'][:10]:  # Show first 10
                        print(f"  - {file}")
                    if len(results['missing']) > 10:
                        print(f"  ... and {len(results['missing']) - 10} more")
                
                if results['new']:
                    print(f"\nNew files:")
                    for file in results['new'][:10]:  # Show first 10
                        print(f"  - {file}")
                    if len(results['new']) > 10:
                        print(f"  ... and {len(results['new']) - 10} more")
                
                # Exit with error code if issues found
                if results['modified'] or results['missing']:
                    sys.exit(1)
            else:
                print(f"✗ {result['message']}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
