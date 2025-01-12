import meshtastic
import meshtastic.serial_interface
from meshtastic import tcp_interface
from pubsub import pub
from threading import Event

from meshboi.command import CommandHandler

from log import logger


class MeshtasticBot:
    def __init__(self, connection_type="serial", hostname=None, serial_port=None):
        self.interface = None
        self.handlers = []
        self.connected = False
        self.register_default_handlers()
        try:
            self.setup_connection(connection_type, hostname, serial_port)
            self.setup_subscribers()
        except Exception as e:
            logger.error(f"Failed to initialize connection: {e}")
            raise

    def register_handler(self, handler):
        """Register a CommandHandler instance"""
        if not isinstance(handler, CommandHandler):
            raise TypeError("Handler must be an instance of CommandHandler")
        self.handlers.append(handler)

    def register_default_handlers(self):
        """Register the default bot command handlers"""

        # Add a test command
        self.register_handler(
            CommandHandler(
                ["#test", "#測試", "#测试"],
                lambda from_id, packet, interface: self.send_private_message(
                    interface,
                    from_id,
                    f"Test message from your nodeID {from_id}",
                ),
                "Test the bot connection",
            )
        )

        # Add a help command
        self.register_handler(
            CommandHandler(
                ["#help", "#幫助", "#帮助"],
                self._handle_help_command,
                "Show available commands",
            )
        )

    def _handle_help_command(self, from_id, packet, interface):
        """Handle the help command by displaying all available commands"""
        help_text = ["Available commands:"]
        help_text.extend(
            f"{', '.join(handler.names)}: {handler.description}"
            for handler in self.handlers
        )
        self.send_private_message(interface, from_id, "\n".join(help_text))

    def setup_connection(self, connection_type, hostname, serial_port):
        if connection_type == "wifi":
            if not hostname:
                raise ValueError("Hostname is required for WiFi connection")
            self.interface = tcp_interface.TCPInterface(hostname=hostname)
        elif connection_type == "serial":
            # If no serial_port provided, use the first available port
            if not serial_port:
                available_ports = meshtastic.util.findPorts()
                if not available_ports:
                    raise ValueError("No Meshtastic devices found")
                serial_port = available_ports[0]

            self.interface = meshtastic.serial_interface.SerialInterface(
                devPath=serial_port
            )
        else:
            raise ValueError(f"Unsupported connection type: {connection_type}")

    def setup_subscribers(self):
        pub.subscribe(self.on_receive, "meshtastic.receive")
        pub.subscribe(self.on_connection, "meshtastic.connection.established")

    def on_receive(self, packet, interface):
        logger.debug(f"Received packet: {packet}")
        logger.debug(f"-------------------------")
        try:
            from_id = packet.get("fromId")
            decoded = packet.get("decoded", {})
            if decoded.get("portnum") == "TEXT_MESSAGE_APP":
                message = decoded.get("text", "").strip()
                logger.info(f"Received message from {from_id}: {message}")
                if message.startswith("#"):
                    self._handle_command(from_id, message, packet, interface)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _handle_command(self, from_id, message, packet, interface):
        """Handle incoming command messages"""
        for handler in self.handlers:
            if handler.matches(message):
                try:
                    handler.handle(from_id, packet, interface)
                    return
                except Exception as e:
                    error_msg = f"Error executing command: {e}"
                    logger.error(error_msg)
                    self.send_private_message(interface, from_id, error_msg)
                    return
        self.send_private_message(interface, from_id, "Unknown command")

    def send_private_message(self, interface, from_id, message):
        interface.sendText(message, destinationId=from_id)

    def on_connection(self, interface, topic=pub.AUTO_TOPIC):
        self.connected = True
        logger.info("Connected to Meshtastic device")

    def run(self):
        logger.info("Bot is running. Press Ctrl+C to exit.")
        try:
            Event().wait()
        except KeyboardInterrupt:
            logger.info("\nShutting down bot...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.interface:
            try:
                self.interface.close()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
