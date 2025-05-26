"""
Network server for managing PC communications
"""
import socket
import threading
import time
import json
from typing import Dict, List, Callable, Optional
from .protocol import NetworkMessage, MessageType, PCStatusData
from core.config.xml_manager import config_manager


class NetworkServer:
    def __init__(self):
        self.server_socket = None
        self.client_sockets = {}  # ip_address -> socket
        self.pc_status = {}  # ip_address -> PCStatusData
        self.message_handlers = {}
        self.running = False
        self.server_thread = None
        self.broadcast_thread = None
        
        # Get configuration
        self.server_port = int(config_manager.get('network.server_port', 8080))
        self.broadcast_port = int(config_manager.get('network.broadcast_port', 8081))
        self.broadcast_interval = int(config_manager.get('network.broadcast_interval', 30))
        self.connection_timeout = int(config_manager.get('network.connection_timeout', 5))
        
        # Setup default message handlers
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default message handlers"""
        self.register_handler(MessageType.DISCOVER_RESPONSE, self._handle_discover_response)
        self.register_handler(MessageType.STATUS_RESPONSE, self._handle_status_response)
        self.register_handler(MessageType.STATUS_UPDATE, self._handle_status_update)
    
    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register message handler"""
        self.message_handlers[message_type] = handler
    
    def start_server(self) -> bool:
        """Start the network server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.server_port))
            self.server_socket.listen(50)
            
            self.running = True
            
            # Start server thread
            self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
            self.server_thread.start()
            
            # Start broadcast thread
            self.broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
            self.broadcast_thread.start()
            
            print(f"✅ Network server started on port {self.server_port}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the network server"""
        self.running = False
        
        # Close all client connections
        for client_socket in self.client_sockets.values():
            try:
                client_socket.close()
            except:
                pass
        self.client_sockets.clear()
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("✅ Network server stopped")
    
    def _server_loop(self):
        """Main server loop to accept connections"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_socket.settimeout(self.connection_timeout)
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"❌ Server error: {e}")
                break
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """Handle individual client connection"""
        ip_address = client_address[0]
        self.client_sockets[ip_address] = client_socket
        
        try:
            while self.running:
                # Receive message
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # Parse message
                try:
                    message = NetworkMessage.from_json(data)
                    self._process_message(message, ip_address)
                except Exception as e:
                    print(f"❌ Error processing message from {ip_address}: {e}")
                
        except Exception as e:
            print(f"❌ Client {ip_address} disconnected: {e}")
        finally:
            # Clean up
            if ip_address in self.client_sockets:
                del self.client_sockets[ip_address]
            if ip_address in self.pc_status:
                self.pc_status[ip_address]['status'] = 'offline'
            try:
                client_socket.close()
            except:
                pass
    
    def _process_message(self, message: NetworkMessage, sender_ip: str):
        """Process received message"""
        # Update sender IP in message
        message.source = sender_ip
        
        # Call appropriate handler
        if message.message_type in self.message_handlers:
            try:
                self.message_handlers[message.message_type](message)
            except Exception as e:
                print(f"❌ Error handling message {message.message_type}: {e}")
        else:
            print(f"⚠️ No handler for message type: {message.message_type}")
    
    def _handle_discover_response(self, message: NetworkMessage):
        """Handle PC discovery response"""
        pc_info = message.data
        ip_address = message.source
        
        print(f"🔍 Discovered PC: {pc_info.get('pc_name', 'Unknown')} at {ip_address}")
        
        # Update PC status
        if ip_address not in self.pc_status:
            self.pc_status[ip_address] = PCStatusData()
        
        status = self.pc_status[ip_address]
        status.pc_name = pc_info.get('pc_name', '')
        status.ip_address = ip_address
        status.mac_address = pc_info.get('mac_address', '')
        status.status = 'idle'
    
    def _handle_status_response(self, message: NetworkMessage):
        """Handle PC status response"""
        ip_address = message.source
        status_data = PCStatusData.from_dict(message.data)
        status_data.ip_address = ip_address
        
        self.pc_status[ip_address] = status_data
        print(f"📊 Updated status for {status_data.pc_name}: {status_data.status}")
    
    def _handle_status_update(self, message: NetworkMessage):
        """Handle PC status update"""
        self._handle_status_response(message)  # Same processing
    
    def _broadcast_loop(self):
        """Broadcast discovery messages periodically"""
        while self.running:
            try:
                self.broadcast_discover()
                time.sleep(self.broadcast_interval)
            except Exception as e:
                print(f"❌ Broadcast error: {e}")
    
    def broadcast_discover(self):
        """Broadcast PC discovery message"""
        try:
            broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            discover_msg = NetworkMessage(
                message_type=MessageType.DISCOVER,
                source="server",
                target="broadcast"
            )
            
            broadcast_socket.sendto(
                discover_msg.to_json().encode('utf-8'),
                ('<broadcast>', self.broadcast_port)
            )
            broadcast_socket.close()
            
        except Exception as e:
            print(f"❌ Broadcast discover error: {e}")
    
    def send_message_to_pc(self, ip_address: str, message: NetworkMessage) -> bool:
        """Send message to specific PC"""
        if ip_address not in self.client_sockets:
            print(f"❌ PC {ip_address} not connected")
            return False
        
        try:
            client_socket = self.client_sockets[ip_address]
            client_socket.send(message.to_json().encode('utf-8'))
            return True
        except Exception as e:
            print(f"❌ Error sending message to {ip_address}: {e}")
            return False
    
    def request_pc_status(self, ip_address: str) -> bool:
        """Request status from specific PC"""
        status_msg = NetworkMessage(
            message_type=MessageType.STATUS_REQUEST,
            source="server",
            target=ip_address
        )
        return self.send_message_to_pc(ip_address, status_msg)
    
    def shutdown_pc(self, ip_address: str) -> bool:
        """Send shutdown command to PC"""
        shutdown_msg = NetworkMessage(
            message_type=MessageType.SHUTDOWN,
            source="server",
            target=ip_address
        )
        return self.send_message_to_pc(ip_address, shutdown_msg)
    
    def restart_pc(self, ip_address: str) -> bool:
