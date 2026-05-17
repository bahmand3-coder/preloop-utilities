# PRELOOP UTILITIES - Professional IT-Toolkit

A comprehensive bootloader and system diagnostics toolkit for IT professionals and system technicians. Available as both GUI and CLI applications for Windows and Linux.

## 🎯 Features

### 🖥️ Multi-Boot Management
- Windows Boot Manager integration
- Linux system detection and boot
- ISO image loading (Ubuntu, SystemRescue, GParted, Seatools)
- UEFI/Legacy BIOS automatic detection
- PXE Network Boot support

### 🔧 Diagnostics & Tools
- Memory stress testing (MemTest86+ compatible)
- SSD/HDD diagnostics and health monitoring
- Network interface scanning
- Hardware information display
- System recovery tools
- EFI Shell access
- BIOS/UEFI firmware settings
- Secure Boot status detection
- TPM information display

### 🎨 Professional UI
- Cyberpunk-themed interface (matching original design)
- Real-time system information
- Intuitive menu navigation
- Responsive design
- Dark mode optimized for visibility

## 📦 Project Structure

```
preloop-utilities/
├── preloop_gui.py           # Main GUI application (PyQt6)
├── preloop_cli.py           # CLI application (Click framework)
├── core/
│   ├── boot_manager.py      # Boot management engine
│   ├── diagnostics.py       # Hardware diagnostics module
│   ├── system_info.py       # System information provider
│   └── utils.py             # Utility functions
├── configs/
│   ├── grub.cfg             # GRUB bootloader configuration
│   └── theme.txt            # GRUB theme settings
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Installation

### Requirements
- Python 3.10+
- pip (Python package manager)
- Administrator/Root privileges (for full functionality)

### Windows Installation

```bash
# Clone repository
git clone https://github.com/bahmand3-coder/preloop-utilities.git
cd preloop-utilities

# Install dependencies
pip install -r requirements.txt

# Run GUI (recommended)
python preloop_gui.py

# Or run CLI
python preloop_cli.py --help
```

### Linux Installation

```bash
# Clone repository
git clone https://github.com/bahmand3-coder/preloop-utilities.git
cd preloop-utilities

# Install dependencies
sudo pip install -r requirements.txt

# Run GUI (with sudo for full features)
sudo python preloop_gui.py

# Or run CLI
sudo python preloop_cli.py --help
```

## 💻 Usage

### GUI Version (Recommended)

```bash
python preloop_gui.py
```

**Features:**
- Dashboard with real-time system status
- System Information tab with hardware details
- Boot Options tab showing available boot entries
- Diagnostics tab with storage information
- Tools tab with quick access to utilities

### CLI Version

```bash
# Display detailed system information
python preloop_cli.py sysinfo

# Show storage devices and usage
python preloop_cli.py storage

# Display boot configuration
python preloop_cli.py bootinfo

# Run memory stress test (default 60 seconds)
python preloop_cli.py memtest

# Custom memory test duration
python preloop_cli.py memtest --duration 120

# Check disk health
python preloop_cli.py diskcheck

# Run full system diagnostics
python preloop_cli.py diagnostics

# Display application information
python preloop_cli.py about

# Show help
python preloop_cli.py --help
```

## 📋 CLI Commands

| Command | Description |
|---------|-------------|
| `sysinfo` | Display detailed system information (CPU, RAM, GPU, BIOS, etc.) |
| `storage` | Show all storage devices with capacity and usage information |
| `bootinfo` | Display current boot mode and available boot entries |
| `memtest [--duration N]` | Run memory stress test for N seconds (default: 60) |
| `diskcheck` | Check disk health and display warnings |
| `diagnostics` | Run full system diagnostics (memory, disk, network) |
| `about` | Display application information and version |

## 🔌 Core Modules

### `boot_manager.py`
Handles boot configuration and boot entry detection:
- Boot mode detection (UEFI/BIOS)
- Operating system detection
- Boot entry scanning
- ISO image detection

### `diagnostics.py`
Provides system diagnostics and testing:
- Memory stress testing
- Disk health checking
- Network interface scanning
- Full diagnostics report generation

### `system_info.py`
Gathers comprehensive system information:
- CPU details and performance info
- RAM information
- GPU detection
- BIOS/UEFI information
- Secure Boot status
- Storage device enumeration

### `utils.py`
Utility functions:
- Administrator/root privilege checking
- Command execution wrapper
- Byte formatting utilities
- Admin privilege decorator

## 🎨 Design

The application features a professional Cyberpunk-themed design with:
- Dark background (#051a24)
- Cyan accent colors (#00ccff, #00ffff)
- Glowing borders and effects
- Responsive layout for various screen sizes
- Optimized for both dark monitors and professional environments

## 📋 System Requirements

### Windows
- Windows 10 or later
- Administrator privileges for full features
- Python 3.10+

### Linux
- Any Linux distribution
- Root/sudo privileges for full features
- Python 3.10+

## 🔐 Permissions

Some features require elevated privileges:
- Memory testing
- Disk health checks
- Network diagnostics
- BIOS settings access
- Boot configuration access

Run with administrator/root privileges for full functionality:
```bash
# Windows (run as administrator)
# Linux/macOS
sudo python preloop_gui.py
```

## 📝 Configuration

### GRUB Configuration
Edit `configs/grub.cfg` to customize:
- Boot timeout
- Default boot entry
- Boot mode settings
- ISO image paths

### Theme Customization
Edit `configs/theme.txt` to modify:
- Colors and styling
- Menu position and size
- Font settings
- Progress bar appearance

## 🐛 Troubleshooting

### "Permission Denied" Errors
**Solution:** Run with administrator/root privileges
```bash
# Windows: Run as Administrator
# Linux/macOS
sudo python preloop_gui.py
```

### PyQt6 Installation Issues
**Solution:** Install with system packages
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt6

# Or via pip
pip install PyQt6
```

### Module Import Errors
**Solution:** Install all dependencies
```bash
pip install -r requirements.txt
```

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/bahmand3-coder/preloop-utilities/issues
- GitHub Discussions: https://github.com/bahmand3-coder/preloop-utilities/discussions

## 📄 License

Professional Use License - See LICENSE file for details

## 🙏 Acknowledgments

- Original GRUB configuration and design concept
- PRELOOP Development Team
- Community contributions and feedback

## 📈 Version History

### v1.0.0 (2026-05-17)
- Initial release
- GUI with PyQt6
- Full CLI functionality
- Boot management system
- Complete diagnostics suite
- Multi-platform support (Windows/Linux)

---

**PRELOOP UTILITIES v1.0.0** - Professional Technician Toolkit
