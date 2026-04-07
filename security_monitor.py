# ============================================================
# SECURITY MONITOR - Fail2ban and Snort monitoring
# ============================================================

import logging
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)


class SecurityMonitor:
    """
    Monitor system security using Fail2ban and Snort
    Detect intrusion attempts and suspicious activity
    """

    def __init__(self):
        """Initialize security monitor"""
        self.alerts = []
        self.failed_logins = []
        self.suspicious_activity = []
        self.threat_level = "low"
        
        logger.info("Security monitor initialized")

    def check_for_threats(self) -> List[Dict]:
        """Check system for security threats"""
        self.alerts = []
        
        if config.FAIL2BAN_ENABLED:
            self._check_fail2ban()
        
        if config.SNORT_ENABLED:
            self._check_snort()
        
        self._update_threat_level()
        
        return self.alerts

    def _check_fail2ban(self):
        """Check Fail2ban logs for failed login attempts"""
        try:
            # Try to read fail2ban log
            try:
                with open(config.FAIL2BAN_LOG_FILE, 'r') as f:
                    lines = f.readlines()
            except PermissionError:
                logger.warning("No permission to read fail2ban logs")
                return
            
            # Parse recent failures
            failed_attempts = {}
            
            for line in lines[-100:]:  # Check last 100 lines
                # Look for failed password patterns
                if 'Failed password' in line or 'Invalid user' in line:
                    # Extract IP address
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
            
            # Check threshold
            for ip, count in failed_attempts.items():
                if count >= config.FAIL2BAN_THRESHOLD:
                    alert = {
                        'type': 'failed_login',
                        'severity': 'high',
                        'source_ip': ip,
                        'attempt_count': count,
                        'message': f"⚠️ Multiple failed login attempts from {ip} ({count} attempts)",
                        'timestamp': datetime.now().isoformat()
                    }
                    self.alerts.append(alert)
                    logger.warning(f"Failed login alert: {ip} - {count} attempts")
            
        except Exception as e:
            logger.error(f"Fail2ban check error: {e}")

    def _check_snort(self):
        """Check Snort for network intrusion detection"""
        try:
            # This requires Snort to be installed
            result = subprocess.run(['snort', '-c', '/etc/snort/snort.conf', '-A', 'alert'],
                                  capture_output=True, text=True, timeout=5)
            
            if result.stdout:
                alerts = result.stdout.split('\n')
                for alert in alerts:
                    if alert.strip():
                        # Parse Snort alert
                        alert_dict = {
                            'type': 'network_threat',
                            'severity': 'high',
                            'message': f"🔴 Network threat detected: {alert[:80]}",
                            'timestamp': datetime.now().isoformat()
                        }
                        self.alerts.append(alert_dict)
                        logger.warning(f"Snort alert: {alert}")
            
        except FileNotFoundError:
            logger.debug("Snort not installed")
        except Exception as e:
            logger.error(f"Snort check error: {e}")

    def check_unauthorized_access(self) -> List[Dict]:
        """Check for unauthorized access attempts"""
        alerts = []
        
        try:
            # Check for sudo usage
            result = subprocess.run(['sudo', 'grep', 'sudo', '/var/log/auth.log'],
                                  capture_output=True, text=True, timeout=5)
            
            if result.stdout:
                for line in result.stdout.split('\n')[-10:]:
                    if 'COMMAND=' in line:
                        alert = {
                            'type': 'sudo_usage',
                            'severity': 'medium',
                            'message': f"🔍 Sudo command executed: {line[:80]}",
                            'timestamp': datetime.now().isoformat()
                        }
                        alerts.append(alert)
        
        except Exception as e:
            logger.debug(f"Unauthorized access check error: {e}")
        
        return alerts

    def check_port_scanning(self) -> List[Dict]:
        """Detect port scanning attempts"""
        alerts = []
        
        try:
            # Check for unusual port access patterns
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=5)
            
            # Look for excessive connection attempts
            connections = result.stdout.split('\n')
            state_counts = {}
            
            for conn in connections:
                if 'ESTABLISHED' in conn or 'TIME_WAIT' in conn:
                    state_counts['ESTABLISHED'] = state_counts.get('ESTABLISHED', 0) + 1
            
            if state_counts.get('ESTABLISHED', 0) > 50:
                alert = {
                    'type': 'suspicious_activity',
                    'severity': 'medium',
                    'message': f"⚠️ Unusual number of connections: {state_counts['ESTABLISHED']}",
                    'timestamp': datetime.now().isoformat()
                }
                alerts.append(alert)
                logger.warning(f"Unusual connection activity detected")
        
        except Exception as e:
            logger.debug(f"Port scanning detection error: {e}")
        
        return alerts

    def _update_threat_level(self):
        """Update overall threat level"""
        if not self.alerts:
            self.threat_level = "low"
        else:
            critical_count = sum(1 for a in self.alerts if a.get('severity') == 'critical')
            high_count = sum(1 for a in self.alerts if a.get('severity') == 'high')
            
            if critical_count > 0:
                self.threat_level = "critical"
            elif high_count > 2:
                self.threat_level = "high"
            elif high_count > 0:
                self.threat_level = "medium"
            else:
                self.threat_level = "low"

    def get_threat_level(self) -> str:
        """Get current threat level"""
        return self.threat_level

    def get_threat_summary(self) -> Dict:
        """Get summary of threats"""
        return {
            'threat_level': self.threat_level,
            'total_alerts': len(self.alerts),
            'critical': sum(1 for a in self.alerts if a.get('severity') == 'critical'),
            'high': sum(1 for a in self.alerts if a.get('severity') == 'high'),
            'medium': sum(1 for a in self.alerts if a.get('severity') == 'medium'),
            'low': sum(1 for a in self.alerts if a.get('severity') == 'low')
        }

    def get_recent_alerts(self, limit: int = 5) -> List[Dict]:
        """Get recent security alerts"""
        return self.alerts[-limit:]

    def block_ip(self, ip_address: str):
        """Block an IP address using fail2ban"""
        try:
            subprocess.run(['sudo', 'fail2ban-client', 'set', 'sshd', 'banip', ip_address],
                         timeout=5)
            logger.warning(f"IP blocked: {ip_address}")
        except Exception as e:
            logger.error(f"Error blocking IP: {e}")

    def unblock_ip(self, ip_address: str):
        """Unblock an IP address"""
        try:
            subprocess.run(['sudo', 'fail2ban-client', 'set', 'sshd', 'unbanip', ip_address],
                         timeout=5)
            logger.info(f"IP unblocked: {ip_address}")
        except Exception as e:
            logger.error(f"Error unblocking IP: {e}")
