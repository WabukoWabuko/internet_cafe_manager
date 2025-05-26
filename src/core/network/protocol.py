"""
Network protocol definitions for PC communication
"""
import json
from enum import Enum
from typing import Dict, Any
from datetime import datetime


class MessageType(Enum):
    """Message types for network communication"""
    # Discovery
    DISCOVER = "discover"
    DISCOVER_RESPONSE = "discover_response"
    
    # Status
    STATUS_REQUEST = "status_request"
    STATUS_RESPONSE = "status_response"
    STATUS_UPDATE = "status_update"
    
    # Control
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    LOCK_SCREEN = "lock_screen"
    UNLOCK_SCREEN = "unlock_screen"
    SEND_MESSAGE = "send_message"
    
    # Session
    START_SESSION = "start_session"
    END_SESSION = "end_session"
    EXTEND_SESSION = "extend_session"
    
    # Response
    ACK = "ack"
    ERROR = "error"


class NetworkMessage:
    """Network message structure"""
    
    def __init__(self, message_type: MessageType, data: Dict[str, Any] = None, 
                 source: str = "", target: str = ""):
        self.message_type = message_type
        self.data = data or {}
        self.source = source
        self.target = target
        self.timestamp = datetime.now().isoformat()
        self.message_id = self._generate_message_id()
    
    def _generate_message_id(self) -> str:
        """Generate unique message ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def to_json(self) -> str:
        """Convert message to JSON string"""
        return json.dumps({
            'message_type': self.message_type.value,
            'data': self.data,
            'source': self.source,
            'target': self.target,
            'timestamp': self.timestamp,
            'message_id': self.message_id
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NetworkMessage':
        """Create message from JSON string"""
        try:
            data = json.loads(json_str)
            message = cls(
                message_type=MessageType(data['message_type']),
                data=data.get('data', {}),
                source=data.get('source', ''),
                target=data.get('target', '')
            )
            message.timestamp = data.get('timestamp', '')
            message.message_id = data.get('message_id', '')
            return message
        except Exception as e:
            raise ValueError(f"Invalid message format: {e}")
    
    def create_response(self, response_type: MessageType, response_data: Dict[str, Any] = None) -> 'NetworkMessage':
        """Create response message"""
        return NetworkMessage(
            message_type=response_type,
            data=response_data or {},
            source=self.target,
            target=self.source
        )
    
    def __str__(self):
        return f"NetworkMessage({self.message_type.value}: {self.source} -> {self.target})"


class PCStatusData:
    """PC status information structure"""
    
    def __init__(self):
        self.pc_name = ""
        self.ip_address = ""
        self.mac_address = ""
        self.status = "offline"  # offline, idle, busy, locked
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.disk_usage = 0.0
        self.network_usage = 0.0
        self.current_user = ""
        self.session_start_time = None
        self.uptime_seconds = 0
        self.last_activity = None
        self.running_processes = []
        self.installed_software = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for network transmission"""
        return {
            'pc_name': self.pc_name,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'status': self.status,
            'cpu_usage': self.cpu_usage,
            'ram_usage': self.ram_usage,
            'disk_usage': self.disk_usage,
            'network_usage': self.network_usage,
            'current_user': self.current_user,
            'session_start_time': self.session_start_time,
            'uptime_seconds': self.uptime_seconds,
            'last_activity': self.last_activity,
            'running_processes': self.running_processes,
            'installed_software': self.installed_software
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PCStatusData':
        """Create from dictionary"""
        status = cls()
        for key, value in data.items():
            if hasattr(status, key):
                setattr(status, key, value)
        return status


def create_discover_message(source: str) -> NetworkMessage:
    """Create PC discovery message"""
    return NetworkMessage(
        message_type=MessageType.DISCOVER,
        source=source,
        target="broadcast"
    )


def create_status_request(source: str, target: str) -> NetworkMessage:
    """Create status request message"""
    return NetworkMessage(
        message_type=MessageType.STATUS_REQUEST,
        source=source,
        target=target
    )


def create_control_message(command: MessageType, source: str, target: str, 
                          params: Dict[str, Any] = None) -> NetworkMessage:
    """Create control command message"""
    return NetworkMessage(
        message_type=command,
        data=params or {},
        source=source,
        target=target
    )


def create_ack_message(original_message: NetworkMessage, success: bool = True, 
                      error_msg: str = "") -> NetworkMessage:
    """Create acknowledgment message"""
    response_type = MessageType.ACK if success else MessageType.ERROR
    response_data = {}
    
    if not success and error_msg:
        response_data['error'] = error_msg
    
    response_data['original_message_id'] = original_message.message_id
    
    return original_message.create_response(response_type, response_data)
