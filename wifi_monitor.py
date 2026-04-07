# ============================================================
# WIFI MONITOR - Network monitoring and threat detection
# ============================================================

import logging
import subprocess
import re
from typing import Dict, List
import config

logger = logging.getLogger(__name__)


class WiFiMonitor:
    """
    Monitor WiFi connection and detect threats
    Analyze network traffic and suspicious activity
    """

    def __init__(self):
        """Initialize WiFi monitor"""
        self.interface = config.NETWORK_INTERFACE
        self.network_stats = {}
        self.connected_devices = []
        self.threats_detected = []
        
        logger.info(f"WiFi monitor initialized on {self.interface}")

    def get_network_stats(self) -> Dict:
        """Get current network statistics"""
        try:
            stats = {
                'interface': self.interface,
                'ssid': self._get_ssid(),
                'signal_strength': self._get_signal_strength(),
                'channel': self._get_channel(),
                'frequency': self._get_frequency(),
                'ip_address': self._get_ip_address(),
                'mac_address': self._get_mac_address(),
                'bandwidth': self._get_bandwidth_usage(),
                'connected_devices': len(self.connected_devices),
                'timestamp': self._get_timestamp()
            }
            
            self.network_stats = stats
            logger.info(f"Network stats updated: {stats['ssid']} ({stats['signal_strength']}%)")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting network stats: {e}")
            return {}

    def _get_ssid(self) -> str:
        """Get current WiFi SSID"""
        try:
            result = subprocess.run(['iwconfig', self.interface], 
                                  capture_output=True, text=True, timeout=5)
            match = re.search(r'ESSID:"([^"]*)"', result.stdout)
            return match.group(1) if match else "Unknown"
        except Exception as e:
            logger.debug(f"Error getting SSID: {e}")
            return "Unknown"

    def _get_signal_strength(self) -> int:
        """Get WiFi signal strength (0-100%)"""
        try:
            result = subprocess.run(['iwconfig', self.interface],
                                  capture_output=True, text=True, timeout=5)
            
            # Look for signal level
            match = re.search(r'Signal level[=:]([^ ]+ dBm)', result.stdout)
            if match:
                dbm_str = match.group(1).replace(' dBm', '')
                dbm = int(dbm_str)
                
                # Convert dBm to percentage (roughly)
                # -30 dBm = 100%, -90 dBm = 0%
                percentage = max(0, min(100, (dbm + 90) * 100 // 60))
                return percentage
            
            return 50  # Default
        except Exception as e:
            logger.debug(f"Error getting signal strength: {e}")
            return 50

    def _get_channel(self) -> str:
        """Get WiFi channel"""
        try:
            result = subprocess.run(['iwconfig', self.interface],
                                  capture_output=True, text=True, timeout=5)
            match = re.search(r'Frequency[=:]([^ ]+)', result.stdout)
            return match.group(1) if match else "Unknown"
        except Exception as e:
            logger.debug(f"Error getting channel: {e}")
            return "Unknown"

    def _get_frequency(self) -> str:
        """Get WiFi frequency"""
        try:
            result = subprocess.run(['iw', self.interface, 'link'],
                                  capture_output=True, text=True, timeout=5)
            match = re.search(r'freq: (\d+)', result.stdout)
            return f"{int(match.group(1)) / 1000} MHz" if match else "Unknown"
        except Exception as e:
            logger.debug(f"Error getting frequency: {e}")
            return "Unknown"

    def _get_ip_address(self) -> str:
        """Get current IP address"""
        try:
            result = subprocess.run(['hostname', '-I'],
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip().split()[0] if result.stdout else "Unknown"
        except Exception as e:
            logger.debug(f"Error getting IP address: {e}")
            return "Unknown"

    def _get_mac_address(self) -> str:
        """Get MAC address"""
        try:
            result = subprocess.run(['cat', f'/sys/class/net/{self.interface}/address'],
                                  capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.stdout else "Unknown"
        except Exception as e:
            logger.debug(f"Error getting MAC address: {e}")
            return "Unknown"

    def _get_bandwidth_usage(self) -> str:
        """Get current bandwidth usage"""
        try:
            result = subprocess.run(['cat', f'/proc/net/dev'],
                                  capture_output=True, text=True, timeout=5)
            
            for line in result.stdout.split('\n'):
                if self.interface in line:
                    parts = line.split()
                    if len(parts) >= 10:
                        rx_bytes = int(parts[1])
                        tx_bytes = int(parts[9])
                        
                        # Simple conversion
                        rx_mb = rx_bytes / 1024 / 1024
                        tx_mb = tx_bytes / 1024 / 1024
                        
                        return f"↓{rx_mb:.1f}MB ↑{tx_mb:.1f}MB"
            
            return "N/A"
        except Exception as e:
            logger.debug(f"Error getting bandwidth: {e}")
            return "N/A"

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def scan_networks(self) -> List[Dict]:
        """Scan for available WiFi networks"""
        try:
            result = subprocess.run(['sudo', 'iwlist', self.interface, 'scan'],
                                  capture_output=True, text=True, timeout=10)
            
            networks = []
            current_network = {}
            
            for line in result.stdout.split('\n'):
                if 'ESSID:' in line:
                    match = re.search(r'ESSID:"([^"]*)"', line)
                    if match:
                        current_network['ssid'] = match.group(1)
                elif 'Signal level=' in line:
                    match = re.search(r'Signal level[=:]([^ ]+ dBm)', line)
                    if match and current_network:
                        current_network['signal'] = match.group(1)
                        networks.append(current_network)
                        current_network = {}
            
            logger.info(f"Scan complete: {len(networks)} networks found")
            return networks
            
        except Exception as e:
            logger.error(f"Network scan error: {e}")
            return []

    def detect_threats(self) -> List[Dict]:
        """Detect network threats"""
        self.threats_detected = []
        
        try:
            # Check for unusual traffic patterns
            if config.DETECT_UNUSUAL_TRAFFIC:
                self._check_unusual_traffic()
            
            # Check for unauthorized devices
            if config.DETECT_UNAUTHORIZED_DEVICES:
                self._check_unauthorized_devices()
            
            # Check for port scanning
            if config.DETECT_PORT_SCANNING:
                self._check_port_scanning()
            
            if self.threats_detected:
                logger.warning(f"Threats detected: {len(self.threats_detected)}")
            
            return self.threats_detected
            
        except Exception as e:
            logger.error(f"Threat detection error: {e}")
            return []

    def _check_unusual_traffic(self):
        """Check for unusual network traffic"""
        try:
            result = subprocess.run(['netstat', '-an'],
                                  capture_output=True, text=True, timeout=5)
            
            connections = result.stdout.split('\n')
            
            # Count connections by state
            state_counts = {}
            for conn in connections:
                if 'ESTABLISHED' in conn or 'TIME_WAIT' in conn:
                    state = 'ESTABLISHED' if 'ESTABLISHED' in conn else 'TIME_WAIT'
                    state_counts[state] = state_counts.get(state, 0) + 1
            
            # Alert if too many connections
            if state_counts.get('ESTABLISHED', 0) > 100:
                threat = {
                    'type': 'unusual_traffic',
                    'severity': 'medium',
                    'message': f"⚠️ High number of connections: {state_counts['ESTABLISHED']}",
                    'connections': state_counts.get('ESTABLISHED', 0)
                }
                self.threats_detected.append(threat)
        
        except Exception as e:
            logger.debug(f"Unusual traffic check error: {e}")

    def _check_unauthorized_devices(self):
        """Check for unauthorized devices on network"""
        try:
            result = subprocess.run(['arp', '-a'],
                                  capture_output=True, text=True, timeout=5)
            
            devices = []
            for line in result.stdout.split('\n'):
                match = re.search(r'\(([0-9.]+)\)', line)
                if match:
                    devices.append(match.group(1))
            
            self.connected_devices = devices
            logger.info(f"Found {len(devices)} devices on network")
        
        except Exception as e:
            logger.debug(f"Device check error: {e}")

    def _check_port_scanning(self):
        """Check for port scanning attempts"""
        try:
            result = subprocess.run(['sudo', 'tail', '-100', '/var/log/syslog'],
                                  capture_output=True, text=True, timeout=5)
            
            # Look for port scan indicators
            if 'UFO' in result.stdout or 'INVALID' in result.stdout:
                threat = {
                    'type': 'port_scan',
                    'severity': 'high',
                    'message': '🚨 Possible port scanning detected'
                }
                self.threats_detected.append(threat)
        
        except Exception as e:
            logger.debug(f"Port scan check error: {e}")

    def get_connected_devices(self) -> List[str]:
        """Get list of connected devices"""
        return self.connected_devices

    def get_summary(self) -> Dict:
        """Get network summary"""
        return {
            'interface': self.interface,
            'connected': bool(self.network_stats.get('ssid')),
            'signal_strength': self.network_stats.get('signal_strength', 0),
            'threats_detected': len(self.threats_detected),
            'devices_connected': len(self.connected_devices)
        }

    def format_for_display(self) -> str:
        """Format network info for display"""
        ssid = self.network_stats.get('ssid', 'Disconnected')
        signal = self.network_stats.get('signal_strength', 0)
        ip = self.network_stats.get('ip_address', 'Unknown')
        devices = len(self.connected_devices)
        
        return f"📶 {ssid}\n🔌 {ip} | 📊 {signal}% | 🖥️ {devices} devices"
