# Windscribe VPN Manager

A Python-based management tool for Windscribe VPN that provides automated connection handling and logging capabilities.

## Features

- Singleton pattern implementation for VPN connection management
- Automatic random server selection
- Connection status monitoring
- Comprehensive logging system
- Automatic reconnection handling
- Command-line interface for VPN operations

## Requirements

- Python 3.6+
- Windscribe CLI (v2.12.7)
- Linux/Unix operating system

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/markavale/windscribe-vpn-rotator.git
   cd windscribe-vpn-rotator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your Windscribe credentials:
   ```
   WINDSCRIBE_USERNAME=your_username
   WINDSCRIBE_PASSWORD=your_password
   ```

## Usage

### Basic Usage

1. Run the main script to start VPN rotation:
   ```bash
   python src/main.py
   ```
   This will connect to random Windscribe servers and rotate between them.

### Using the WindscribeSingleton Class

</file>