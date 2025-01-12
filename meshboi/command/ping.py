from datetime import datetime

from meshboi.command import CommandHandler


class PingCommand(CommandHandler):
    MAX_HOP = 3

    def __init__(self):
        super().__init__(["#ping"], self.handle_ping_command, "Ping the bot")

    def handle_ping_command(self, from_id, packet, interface):
        via_mqtt = packet.get("viaMqtt", False)
        if not via_mqtt:
            rx_time = packet.get("rxTime", "")
            rx_snr = packet.get("rxSnr", "")
            rx_rssi = packet.get("rxRssi", "")
            rx_time = datetime.fromtimestamp(rx_time).strftime("%Y-%m-%d %H:%M:%S")
            hop_limit = packet.get("hopLimit", 3)
            through_hop = self.MAX_HOP - hop_limit
            self.send_private_message(
                interface,
                from_id,
                f"pong: rx_time: {rx_time}, rx_snr: {rx_snr}, rx_rssi: {rx_rssi}, through_hop: {through_hop}",
            )
        else:
            self.send_private_message(interface, from_id, "pong: via mqtt")
