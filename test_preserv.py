#!/usr/bin/env python3
"""
Simple test script for Preserv Archive Integrity Checker
"""

import os
import tempfile
import shutil
import hashlib
from pathlib import Path
from integrity import ArchiveIntegrityChecker


def create_test_files(test_dir):
    """Create test files for testing."""
    # Create some test files
    files = {
        "document1.txt": "This is test document 1",
        "document2.txt": "This is test document 2",
        "subfolder/document3.txt": "This is test document 3 in subfolder",
        "binary.bin": b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    }
    
    for file_path, content in files.items():
        full_path = os.path.join(test_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        if isinstance(content, str):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(full_path, 'wb') as f:
                f.write(content)
    
    return files


def test_integrity_checker():
    """Test the integrity checker functionality."""
    print("🧪 Testing Preserv Archive Integrity Checker")
    print("=" * 50)
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as test_dir:
        print(f"📁 Created test directory: {test_dir}")
        
        # Create test files
        test_files = create_test_files(test_dir)
        print(f"📄 Created {len(test_files)} test files")
        
        # Initialize checker
        checker = ArchiveIntegrityChecker(test_dir)
        print("✅ Initialized integrity checker")
        
        # Test manifest generation
        print("\n🔄 Testing manifest generation...")
        result = checker.generate_manifest(test_dir)
        
        if result["success"]:
            print(f"✅ Manifest generated: {result['message']}")
            print(f"   Files processed: {result['processed_files']}")
        else:
            print(f"❌ Manifest generation failed: {result['message']}")
            return False
        
        # Test manifest stats
        stats = checker.get_manifest_stats()
        if stats["exists"]:
            print(f"✅ Manifest stats: {stats['file_count']} files, {stats['total_size_mb']} MB")
        else:
            print("❌ Manifest stats not found")
            return False
        
        # Test integrity verification
        print("\n🔄 Testing integrity verification...")
        result = checker.verify_integrity(test_dir)
        
        if result["success"]:
            print(f"✅ Integrity verification: {result['message']}")
            results = result["results"]
            print(f"   OK: {len(results['ok'])} files")
            print(f"   Modified: {len(results['modified'])} files")
            print(f"   Missing: {len(results['missing'])} files")
            print(f"   New: {len(results['new'])} files")
        else:
            print(f"❌ Integrity verification failed: {result['message']}")
            return False
        
        # Test file modification detection
        print("\n🔄 Testing file modification detection...")
        test_file = os.path.join(test_dir, "document1.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("This is modified document 1")
        
        result = checker.verify_integrity(test_dir)
        if result["success"]:
            results = result["results"]
            if len(results['modified']) > 0:
                print(f"✅ File modification detected: {len(results['modified'])} files")
            else:
                print("❌ File modification not detected")
                return False
        else:
            print(f"❌ Modification test failed: {result['message']}")
            return False
        
        # Test new file detection
        print("\n🔄 Testing new file detection...")
        new_file = os.path.join(test_dir, "newfile.txt")
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write("This is a new file")
        
        result = checker.verify_integrity(test_dir)
        if result["success"]:
            results = result["results"]
            if len(results['new']) > 0:
                print(f"✅ New file detected: {len(results['new'])} files")
            else:
                print("❌ New file not detected")
                return False
        else:
            print(f"❌ New file test failed: {result['message']}")
            return False
        
        # Test log content
        print("\n🔄 Testing log functionality...")
        log_content = checker.get_log_content(10)
        if log_content:
            print(f"✅ Log content retrieved: {len(log_content)} characters")
        else:
            print("❌ Log content not found")
            return False
    
    print("\n🎉 All tests passed!")
    return True


def test_gui_import():
    """Test that GUI can be imported."""
    print("\n🔄 Testing GUI import...")
    try:
        from gui import PreservGUI
        print("✅ GUI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Preserv Test Suite")
    print("=" * 30)
    
    # Test core functionality
    if not test_integrity_checker():
        print("\n❌ Core functionality tests failed")
        return False
    
    # Test GUI import
    if not test_gui_import():
        print("\n❌ GUI import test failed")
        return False
    
    print("\n🎉 All tests completed successfully!")
    print("\nYou can now run Preserv with:")
    print("  python main.py")
    print("  python run.py")
    print("  preserv (if installed)")
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
