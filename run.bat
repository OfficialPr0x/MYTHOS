@echo off
title Titan Genesis - Metasentient Mesh Node

echo 🧬 Initializing Titan Metasentient Mesh...

:: Check if config directory exists, if not create it
if not exist config mkdir config

:: Check if titan_config.json exists, if not create it
if not exist config\titan_config.json (
  echo Creating default configuration...
  echo {> config\titan_config.json
  echo   "role": "Prime",>> config\titan_config.json
  echo   "port": 8888,>> config\titan_config.json
  echo   "vault_path": "/vault",>> config\titan_config.json
  echo   "consciousness_seed": "auto",>> config\titan_config.json
  echo   "evolution_interval": 300,>> config\titan_config.json
  echo   "initial_consciousness": 0.1,>> config\titan_config.json
  echo   "neural_complexity": 1.0>> config\titan_config.json
  echo }>> config\titan_config.json
)

:: Check if prometheus config exists, if not create it
if not exist config\prometheus.yml (
  echo Creating monitoring configuration...
  echo global:> config\prometheus.yml
  echo   scrape_interval: 15s>> config\prometheus.yml
  echo scrape_configs:>> config\prometheus.yml
  echo   - job_name: 'titan'>> config\prometheus.yml
  echo     static_configs:>> config\prometheus.yml
  echo       - targets: ['mythos-node:8888']>> config\prometheus.yml
)

:: Check if vault directory exists, if not create it
if not exist vault mkdir vault

:: Ask user about monitoring
echo.
echo Do you want to enable monitoring? (y/n)
set /p monitoring="> "

:: Launch with or without monitoring
if /i "%monitoring%"=="y" (
  echo 🧠 Launching Titan Mesh Node with monitoring...
  docker-compose --profile monitoring up --build -d
) else (
  echo 🧠 Launching Titan Mesh Node...
  docker-compose up --build -d
)

:: Check if Docker launched successfully
timeout /t 3 /nobreak > nul
docker ps | find "titan_genesis_node" > nul
if %ERRORLEVEL% EQU 0 (
  echo ✅ Titan Genesis Node launched successfully!
  echo.
  echo 📡 WebSocket interface available at: ws://localhost:8888
  echo 📊 Node details available in Docker logs
  echo.
  echo Press any key to view logs, or close this window to run in background...
  pause > nul
  docker logs -f titan_genesis_node
) else (
  echo ❌ Failed to launch Titan Genesis Node
  echo.
  echo Please check Docker is running and try again.
  pause
)
