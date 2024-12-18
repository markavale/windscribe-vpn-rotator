from windscribe import Windscribe
from utils.logger import Logger
from typing import List
import subprocess
import time
import random
from decouple import config
import os
import re
import asyncio

logger = Logger().get_logger()

class WindscribeSingleton:
    _instance = None
    connected_states = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WindscribeSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.vpn = Windscribe(user=config("WINDSCRIBE_USERNAME"), password=config("WINDSCRIBE_PASSWORD"))
        self.logger = Logger().get_logger()

    def _get_random_servers(self) -> str:
        # Use an absolute path to ensure the file is found
        file_path = os.path.join(os.path.dirname(__file__), "servers.txt")
        try:
            with open(file_path) as f:
                return random.choice([line.strip() for line in f])
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            raise

    def reboot(self):
        self.logger.info("Rebooting Windscribe connection...")
        subprocess.run(['windscribe-cli', 'disconnect'], check=True)
        self.connect()
        self.logger.info("Windscribe has been rebooted successfully")

    def parse_status(self, output: bytes):
        output_str = output.decode('utf-8').strip()
        lines: List[str] = output_str.split('\n')
        status_dict: dict = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                status_dict[key.strip()] = value.strip()
        return status_dict

    def get_status(self):
        response = subprocess.run(['windscribe-cli', 'status'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = self.parse_status(response.stdout)
        logger.info(f"Connection status: {status}")
        return status

    def connect(self):
        self.logger.info("Attempting to connect to Windscribe VPN...")
        status = self.get_status()
        state = status.get('Connect state', status.get('*Connect state'))
        
        # Wait if the status is "Connecting"
        while state in ["Connecting", "Disconnecting"]:
            self.logger.info("Currently connecting, waiting for connection to complete...")
            time.sleep(1)  # Wait for 1 second before checking again
            status = self.get_status()
            state = status.get('Connect state', status.get('*Connect state'))
        
        while state in ["Disconnected", "Disconnecting"] and state in self.connected_states:

            self.logger.info("Connecting to random server...")
            self.vpn.connect(server=self._get_random_servers())
            time.sleep(random.uniform(0.5, 1.5))
            status = self.get_status()
            state = status.get('Connect state', status.get('*Connect state'))
            self.logger.info(f"Connection status: {status}")
        
        self.connected_states.append(state)
        self.logger.info("Successfully connected to Windscribe VPN")

    async def aconnect(self, max_retries=15):
        retries = 0
        while retries < max_retries:
            status = self.get_status()
            state = status.get('Connect state', status.get('*Connect state'))
            if state == "Connected":
                print("VPN is connected.")
                return
            elif re.search(r"\bConnecting\b", state):
                print("VPN is connecting. Waiting for it to complete...")
                await asyncio.sleep(5)  # Wait for a few seconds before checking again
            elif state in ["Disconnected", "Disconnecting"]:
                print(f"VPN is {state}. Attempting to connect...")
                self.vpn.connect(rand=True)
                # subprocess.run(['windscribe-cli', 'connect'], check=True)
                await asyncio.sleep(random.uniform(1, 3))
            else:
                print(f"Unexpected VPN state: {state}. Retrying...")
                return
            retries += 1
        raise Exception("Failed to establish a VPN connection after multiple attempts.")