# MPU Discord Bot
MPU is a modular Discord bot designed to enable users to add movies and shows to a personal home media server. It integrates with Plex for the user interface and Radarr/Sonarr for automatic content management.

## Features
- **Media Management**: Easily add movies and shows to your Plex server.
- **User Management**: Manage access to your media server.
- **Integration**: Seamless integration with Plex, Radarr, and Sonarr.

## Quickstart
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/PapyMonkey/mpu.git
    cd mpu
    ```
2. **Setup Environment Variables**:
    Copy the .env.template file to .env and fill in the required values:
    ```bash
    cp .env.template .env
    ```
3. **Install Requirements**:
    Ensure you have Python 3.11 installed and then:
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Bot**:
    ```bash
    python main.py
    ```

## Requirements
- Python 3.11
- A running Plex server
- Radarr and Sonarr (for automatic content management)

## Configuration
All configuration values are stored in the .env file. Use the .env.template as a reference to set up your environment variables.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.
