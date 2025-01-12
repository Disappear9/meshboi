from meshtastic.stream_interface import StreamInterface

from log import logger


class CommandHandler:
    def __init__(self, names, handler_func, description="No description provided"):
        self.names = [names] if isinstance(names, str) else names
        self.handler = handler_func
        self.description = description

    def matches(self, message):
        """Check if the message matches any of the command names"""
        return any(message.startswith(name) for name in self.names)

    def handle(self, from_id, packet, interface: StreamInterface):
        """Execute the command handler"""
        return self.handler(from_id, packet, interface)

    def send_private_message(self, interface: StreamInterface, from_id, message):
        """Send a private message to the user"""
        interface.sendText(message, destinationId=from_id)
        logger.info(f"Sent message to {from_id}: {message}")
