# Copper/Fiber Serial Scanner (CFSS) v3.0.0

A cross-platform desktop application for scanning and verifying jumper cable serial numbers in network infrastructure. This tool helps network technicians ensure proper cable connections by comparing scanned serial numbers against expected values from circuit documentation.

## Platform Support

- **Windows 10/11**: Full support with native executable
- **macOS**: Compatible with macOS 10.14+ (Intel and Apple Silicon)
- **Cross-Platform**: Built with Python for maximum compatibility

## Features

### Core Functionality
- **Serial Number Verification**: Scan jumper cable serials and compare against expected values
- **Multiple Circuit Support**: Load and manage multiple network circuits from CSV files
- **Progress Tracking**: Visual progress bars showing completion percentage (matches only)
- **Persistent State**: Automatically saves and resumes scan progress across sessions

### User Interface
- **Modern Dark Theme**: Clean, professional interface built with CustomTkinter
- **Real-time Feedback**: Visual and audio feedback for matches, non-matches, and completion
- **Search Functionality**: Quickly jump to specific locations within circuits
- **Status Tracking**: Track matches, non-matches, and skipped items with reasons

### Data Management
- **CSV Import**: Import circuit data from CSV files with standardized column formats
- **Smart Sorting**: Intelligent sorting based on circuit type and jumper position
- **Deduplication**: Automatic removal of duplicate entries during import
- **Export Results**: Generate detailed text reports of scan results

### Audio Feedback
- **Cross-Platform Audio**: Uses pygame for reliable audio playback on all platforms
- **Match Sound**: Confirmation tone for successful matches
- **Non-Match Sound**: Alert tone for mismatches or issues  
- **Completion Sound**: Celebration tone when circuit is 100% complete

## Supported Circuit Types

- **Standard Circuits**: A-location to Z-location connections
- **CSW Circuits**: Special handling for CSW (Circuit Switch) configurations
- **Multi-Jumper Circuits**: Support for circuits with multiple jumper segments
- **Port-based Connections**: Handles various port numbering schemes (1, 2, 4, 7, etc.)

## Technical Specifications

### Requirements
- **Windows**: Windows 10/11, audio output device
- **macOS**: macOS 10.14+ (Mojave or later), audio output device
- **Development**: Python 3.8+ with required dependencies

### File Formats
- **Input**: CSV files with network circuit data
- **Output**: Text-based reports with tabular formatting
- **Database**: SQLite for persistent storage and state management

### Architecture
- **Modular Design**: Separate managers for data, circuits, and scan control
- **SQLite Backend**: Fast, reliable data storage and retrieval
- **Cross-Platform Audio**: Pygame mixer for consistent audio across platforms
- **Efficient Processing**: Hash-based change detection for fast CSV reloading

## Installation

### Windows
1. Download the latest Windows release (.exe) from the releases page
2. Extract to desired directory
3. Place CSV circuit files in the data folder
4. Run `cfss_app.exe`

### macOS
1. Download the latest macOS release (.app or .dmg) from the releases page
2. Install/extract to Applications folder or desired location
3. Place CSV circuit files in the data folder
4. Run the application (may need to allow in Security & Privacy settings)

### From Source (Both Platforms)
```bash
# Clone the repository
git clone [repository-url]
cd cfss_app

# Install dependencies
pip install -r requirements.txt

# Run the application
python cfss_app.py
```

## Usage

1. **Load Circuits**: Place CSV files in the data folder or use "Import CSV(s)"
2. **Select Circuit**: Choose from the circuit dropdown
3. **Select Jumper**: Choose which jumper segment to scan
4. **Scan Serials**: Use barcode scanner or manual entry
5. **Track Progress**: Monitor completion via progress bar and statistics
6. **Export Results**: Save scan results to text reports

## CSV Format Requirements

Your CSV files should include these columns:
- Length, A location, A device, A interface, A jumper serial
- Port 1-8 location, container, cassette, port, jumper serial
- Z location, Z device, Z interface, Z jumper serial

## Key Benefits

- **Cross-Platform**: Works on both Windows and macOS environments
- **Accuracy**: Eliminates human error in cable verification
- **Efficiency**: Faster than manual documentation methods  
- **Reliability**: Persistent state prevents data loss
- **Flexibility**: Handles various circuit types and configurations
- **Reporting**: Professional documentation for compliance and records

## Development

Built with Python using modern, cross-platform libraries:
- **CustomTkinter**: Modern UI framework (cross-platform)
- **SQLite**: Database management (built into Python)
- **Pygame**: Cross-platform audio system
- **Natural Sorting**: Intelligent data ordering

### Dependencies
```
customtkinter>=5.0.0
pygame>=2.0.0
natsort>=8.0.0
```

## Building from Source

### For Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed cfss_app.py
```

### For macOS
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --osx-bundle-identifier com.yourcompany.cfss cfss_app.py
```

---

*Perfect for network technicians, data center operations, and infrastructure teams requiring accurate cable documentation and verification across Windows and macOS environments.*
