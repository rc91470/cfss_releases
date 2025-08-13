#!/usr/bin/env python3
"""
CFSS Installation Validator
Checks for all required files and folders and provides fixes
"""
import os
import sys
import shutil
import logging
from typing import Dict, List

class CFSSValidator:
    def __init__(self, app_dir: str = None):
        self.app_dir = app_dir or os.getcwd()
        self.critical_folders = ['sounds', 'data']
        self.critical_files = {
            'sounds': ['match.mp3', 'nonmatch.mp3', 'complete.mp3'],
            'data': []  # Data folder contents vary by installation
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cfss_validation.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def validate_installation(self) -> Dict[str, List[str]]:
        """Validate that all critical files and folders exist"""
        missing = {'folders': [], 'files': []}
        
        logging.info(f"Validating CFSS installation in: {self.app_dir}")
        
        for folder in self.critical_folders:
            folder_path = os.path.join(self.app_dir, folder)
            if not os.path.exists(folder_path):
                missing['folders'].append(folder)
                logging.warning(f"Missing critical folder: {folder}")
            else:
                logging.info(f"✓ Found folder: {folder}")
                # Check critical files in this folder
                if folder in self.critical_files:
                    for file in self.critical_files[folder]:
                        file_path = os.path.join(folder_path, file)
                        if not os.path.exists(file_path):
                            missing['files'].append(f"{folder}/{file}")
                            logging.warning(f"Missing critical file: {folder}/{file}")
                        else:
                            logging.info(f"✓ Found file: {folder}/{file}")
        
        # Check for executable
        exe_files = [f for f in os.listdir(self.app_dir) if f.startswith('CFSS') and f.endswith('.exe')]
        if exe_files:
            logging.info(f"✓ Found executable: {exe_files[0]}")
        else:
            logging.warning("No CFSS executable found")
            missing['files'].append("CFSS_*.exe")
        
        return missing
    
    def create_missing_folders(self, missing_folders: List[str]) -> bool:
        """Create missing folders with default content"""
        success = True
        
        for folder in missing_folders:
            folder_path = os.path.join(self.app_dir, folder)
            try:
                os.makedirs(folder_path, exist_ok=True)
                logging.info(f"Created folder: {folder}")
                
                # Add default content for sounds folder
                if folder == 'sounds':
                    readme_path = os.path.join(folder_path, 'README.txt')
                    with open(readme_path, 'w') as f:
                        f.write("CFSS Sound Files\n")
                        f.write("================\n\n")
                        f.write("This folder should contain:\n")
                        f.write("- match.mp3: Played when scan finds a match\n")
                        f.write("- nonmatch.mp3: Played when scan finds no match\n") 
                        f.write("- complete.mp3: Played when scan is complete\n\n")
                        f.write("If these files are missing, the application will show\n")
                        f.write("Windows popups instead of audio/visual feedback.\n\n")
                        f.write("To fix: Download the complete installation package\n")
                        f.write("from GitHub and copy the sounds folder.\n")
                    logging.info(f"Created {folder}/README.txt with instructions")
                
                # Add default content for data folder
                elif folder == 'data':
                    readme_path = os.path.join(folder_path, 'README.txt')
                    with open(readme_path, 'w') as f:
                        f.write("CFSS Data Files\n")
                        f.write("===============\n\n")
                        f.write("This folder contains CSV files with circuit data:\n")
                        f.write("- BB-DR.csv, CORP.csv, CS-EB.csv, etc.\n\n")
                        f.write("These files are required for serial number lookup.\n")
                        f.write("Without them, scans will show 'no match found'.\n\n")
                        f.write("Contact your administrator to get the correct\n")
                        f.write("CSV files for your location.\n")
                    logging.info(f"Created {folder}/README.txt with instructions")
                    
            except Exception as e:
                logging.error(f"Failed to create folder {folder}: {e}")
                success = False
        
        return success
    
    def generate_report(self, missing: Dict[str, List[str]]) -> str:
        """Generate a detailed validation report"""
        report = []
        report.append("CFSS Installation Validation Report")
        report.append("=" * 40)
        report.append(f"App Directory: {self.app_dir}")
        report.append(f"Validation Time: {logging.Formatter().formatTime(logging.LogRecord('','','','','','','','',''))}")
        report.append("")
        
        if not missing['folders'] and not missing['files']:
            report.append("✅ VALIDATION PASSED")
            report.append("All required components are present.")
        else:
            report.append("❌ VALIDATION FAILED")
            report.append("Missing components detected:")
            report.append("")
            
            if missing['folders']:
                report.append("Missing Folders:")
                for folder in missing['folders']:
                    report.append(f"  - {folder}")
                report.append("")
            
            if missing['files']:
                report.append("Missing Files:")
                for file in missing['files']:
                    report.append(f"  - {file}")
                report.append("")
            
            report.append("IMPACT:")
            if 'sounds' in missing['folders']:
                report.append("- Without sounds folder: No audio feedback, Windows popups instead of visual indicators")
            if 'data' in missing['folders']:
                report.append("- Without data folder: Cannot perform serial number lookups")
            report.append("")
            
            report.append("SOLUTIONS:")
            report.append("1. Download the complete ZIP package from GitHub releases")
            report.append("2. Extract the full package (not just the .exe file)")
            report.append("3. Run this validator again to confirm")
            report.append("")
            report.append("Or run: python cfss_validator.py --fix")
        
        return "\n".join(report)
    
    def run_validation(self, create_missing: bool = False) -> bool:
        """Run complete validation and optionally fix issues"""
        print("🔍 CFSS Installation Validator")
        print("=" * 30)
        
        missing = self.validate_installation()
        
        if create_missing and missing['folders']:
            print(f"\n🔧 Creating missing folders...")
            self.create_missing_folders(missing['folders'])
            # Re-validate after creating folders
            missing = self.validate_installation()
        
        # Generate and save report
        report = self.generate_report(missing)
        
        report_file = os.path.join(self.app_dir, 'validation_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n📋 Report saved to: {report_file}")
        print("\n" + report)
        
        return len(missing['folders']) == 0 and len(missing['files']) == 0

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate CFSS installation')
    parser.add_argument('--dir', '-d', help='CFSS installation directory', default=os.getcwd())
    parser.add_argument('--fix', '-f', action='store_true', help='Create missing folders with instructions')
    
    args = parser.parse_args()
    
    validator = CFSSValidator(args.dir)
    success = validator.run_validation(create_missing=args.fix)
    
    if success:
        print("\n✅ Validation completed successfully!")
        exit(0)
    else:
        print("\n❌ Validation failed - missing components detected")
        print("Run with --fix to create missing folders with instructions")
        exit(1)

if __name__ == "__main__":
    main()
