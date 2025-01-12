import argparse

from meshboi.meshtastic.bot import MeshtasticBot
from meshboi.command.ping import PingCommand


def main():
    parser = argparse.ArgumentParser(
        description="Meshtastic Bot with Weather Functionality"
    )
    parser.add_argument(
        "--connection-type", choices=["serial", "wifi"], default="serial"
    )
    parser.add_argument("--hostname")
    parser.add_argument("--serial-port")

    args = parser.parse_args()

    bot = MeshtasticBot(
        connection_type=args.connection_type,
        hostname=args.hostname,
        serial_port=args.serial_port,
    )
    bot.register_handler(PingCommand())
    bot.run()


if __name__ == "__main__":
    main()
