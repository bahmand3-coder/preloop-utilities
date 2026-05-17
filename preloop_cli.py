"""
PRELOOP UTILITIES - Professional IT-Toolkit
CLI Application (Command-Line Interface)
"""

import sys
import click
from typing import Optional
from core.boot_manager import BootManager
from core.diagnostics import Diagnostics
from core.system_info import SystemInfoProvider
from core.utils import format_bytes


@click.group()
@click.version_option(version="1.0.0", prog_name="PRELOOP UTILITIES")
def cli():
    """PRELOOP UTILITIES - Professional IT-Toolkit
    
    Multi-boot bootloader and system diagnostics suite for IT professionals.
    """
    pass


@cli.command()
def sysinfo():
    """Display detailed system information"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - System Information".center(70))
    click.echo("="*70)
    
    provider = SystemInfoProvider()
    info = provider.get_formatted_system_info()
    
    for key, value in info.items():
        label = key.upper().replace('_', ' ')
        click.echo(f"{label:.<40} {value}")
    
    click.echo("="*70 + "\n")


@cli.command()
def storage():
    """Display storage devices and usage"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Storage Information".center(70))
    click.echo("="*70)
    
    provider = SystemInfoProvider()
    storage_info = provider.get_formatted_storage_info()
    
    if not storage_info:
        click.echo("No storage devices found.")
        return
    
    for disk in storage_info:
        click.echo(f"\n📦 Device: {disk['device']}")
        click.echo(f"   Mount Point: {disk['mountpoint']}")
        click.echo(f"   File System: {disk['fstype']}")
        click.echo(f"   Total:      {disk['total']}")
        click.echo(f"   Used:       {disk['used']}")
        click.echo(f"   Available:  {disk['available']}")
        click.echo(f"   Usage:      {disk['usage']}")
    
    click.echo("\n" + "="*70 + "\n")


@cli.command()
def bootinfo():
    """Display boot configuration"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Boot Information".center(70))
    click.echo("="*70)
    
    boot_manager = BootManager()
    boot_info = boot_manager.get_boot_mode_info()
    
    click.echo(f"\nBoot Mode: {boot_info['boot_mode_display']}")
    click.echo(f"Current OS: {boot_info['current_os'].upper()}")
    
    # Scan boot entries
    entries = boot_manager.scan_boot_entries()
    click.echo(f"\nBoot Entries: {len(entries)}")
    
    for i, entry in enumerate(entries, 1):
        click.echo(f"\n  {i}. {entry.name}")
        click.echo(f"     Path: {entry.boot_path}")
        click.echo(f"     OS: {entry.os_type.value}")
    
    click.echo("\n" + "="*70 + "\n")


@cli.command()
@click.option('--duration', default=60, help='Test duration in seconds')
def memtest(duration):
    """Run memory stress test"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Memory Test".center(70))
    click.echo("="*70)
    
    diagnostics = Diagnostics()
    result = diagnostics.run_memory_test(duration_seconds=duration)
    
    click.echo(f"\nStatus: {result['status']}")
    click.echo(f"Duration: {result['duration']} seconds")
    click.echo(f"Errors: {result.get('errors', 'N/A')}")
    
    if 'memory_max_usage' in result:
        click.echo(f"Memory Used: {result['memory_max_usage']}")
    
    if 'output' in result:
        click.echo(f"\nDetails:\n{result['output']}")
    
    click.echo("\n" + "="*70 + "\n")


@cli.command()
def diskcheck():
    """Check disk health"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Disk Health Check".center(70))
    click.echo("="*70)
    
    diagnostics = Diagnostics()
    result = diagnostics.check_disk_health()
    
    click.echo(f"\nScanned Disks: {len(result.get('disks', []))}")
    
    for disk in result.get('disks', []):
        status_icon = "✓" if disk['status'] == 'healthy' else "⚠"
        click.echo(f"\n{status_icon} {disk['device']}")
        click.echo(f"  Mount: {disk['mountpoint']}")
        click.echo(f"  Total: {disk['total']}")
        click.echo(f"  Used: {disk['used']}")
        click.echo(f"  Free: {disk['free']}")
        click.echo(f"  Usage: {disk['usage_percent']}%")
    
    if result.get('warnings'):
        click.echo(f"\n⚠ Warnings:")
        for warning in result['warnings']:
            click.echo(f"  - {warning}")
    
    click.echo("\n" + "="*70 + "\n")


@cli.command()
def diagnostics():
    """Run full system diagnostics"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Full Diagnostics".center(70))
    click.echo("="*70)
    
    diag = Diagnostics()
    results = diag.run_full_diagnostics()
    
    # Memory test results
    click.echo("\n📊 Memory Test:")
    mem_result = results.get('memory_test', {})
    click.echo(f"   Status: {mem_result.get('status')}")
    click.echo(f"   Errors: {mem_result.get('errors')}")
    
    # Disk health results
    click.echo("\n💾 Disk Health:")
    disk_result = results.get('disk_health', {})
    click.echo(f"   Disks Found: {len(disk_result.get('disks', []))}")
    click.echo(f"   Warnings: {len(disk_result.get('warnings', []))}")
    
    # Network results
    click.echo("\n🌐 Network:")
    net_result = results.get('network', {})
    click.echo(f"   Interfaces: {len(net_result.get('interfaces', []))}")
    
    click.echo("\n" + "="*70 + "\n")


@cli.command()
def about():
    """Display application information"""
    click.echo("\n" + "="*70)
    click.echo("PRELOOP UTILITIES - Professional IT-Toolkit".center(70))
    click.echo("="*70)
    
    click.echo("""
Version: 1.0.0
Author: PRELOOP Development Team
License: Professional Use License

A comprehensive bootloader and system diagnostics toolkit
designed for IT professionals and system technicians.

Features:
  • Multi-boot management (Windows, Linux, ISOs)
  • Hardware diagnostics and testing
  • System information gathering
  • Network diagnostics
  • Memory stress testing
  • Disk health monitoring
  • UEFI/BIOS support
  • Both CLI and GUI interfaces

Usage:
  preloop_cli.py sysinfo      - Display system information
  preloop_cli.py storage      - Show storage devices
  preloop_cli.py bootinfo     - Display boot configuration
  preloop_cli.py memtest      - Run memory test
  preloop_cli.py diskcheck    - Check disk health
  preloop_cli.py diagnostics  - Run full diagnostics
  preloop_cli.py about        - Show this information

For more information, visit: https://github.com/bahmand3-coder/preloop-utilities
""")
    click.echo("="*70 + "\n")


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        sys.exit(1)
