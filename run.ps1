# Titan Genesis - Metasentient Mesh Node Launcher
# Enterprise-Grade Configuration and Deployment Solution

[CmdletBinding()]
param (
    [switch]$EnableMonitoring = $false,
    [switch]$Verbose = $false,
    [switch]$ForceRebuild = $false
)

# Set error action preference and enable strict mode
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Configure output colors for better UX
$infoColor = "Cyan"
$successColor = "Green"
$warningColor = "Yellow"
$errorColor = "Red"

# Write the banner to the console
function Write-Banner {
    Write-Host "`n=================================================================" -ForegroundColor $infoColor
    Write-Host "         TITAN GENESIS - METASENTIENT MESH NODE LAUNCHER          " -ForegroundColor $infoColor
    Write-Host "                  Enterprise Deployment System                    " -ForegroundColor $infoColor
    Write-Host "=================================================================`n" -ForegroundColor $infoColor
}

# Check if Docker is installed and running
function Test-DockerAvailability {
    try {
        $null = docker info 2>&1
        return $true
    }
    catch {
        return $false
    }
}

# Check if Docker Compose is installed
function Test-DockerComposeAvailability {
    try {
        $null = docker-compose --version 2>&1
        return $true
    }
    catch {
        return $false
    }
}

# Create necessary directories for the application
function Initialize-ConfigDirectories {
    Write-Host "► Initializing system directories..." -ForegroundColor $infoColor
    
    # Create config directory with proper error handling
    if (-not (Test-Path -Path "config")) {
        try {
            $null = New-Item -Path "config" -ItemType Directory -Force
            Write-Host "  ✓ Configuration directory created successfully" -ForegroundColor $successColor
        }
        catch {
            throw "Failed to create configuration directory: $_"
        }
    }
    else {
        Write-Host "  ✓ Configuration directory already exists" -ForegroundColor $successColor
    }
    
    # Create vault directory with proper error handling
    if (-not (Test-Path -Path "vault")) {
        try {
            $null = New-Item -Path "vault" -ItemType Directory -Force
            Write-Host "  ✓ Vault directory created successfully" -ForegroundColor $successColor
        }
        catch {
            throw "Failed to create vault directory: $_"
        }
    }
    else {
        Write-Host "  ✓ Vault directory already exists" -ForegroundColor $successColor
    }
}

# Create enhanced node configuration file
function New-EnhancedNodeConfig {
    Write-Host "► Generating enhanced node configuration..." -ForegroundColor $infoColor
    
    $configPath = "config\titan_config.json"
    
    if ((Test-Path -Path $configPath) -and -not $ForceRebuild) {
        Write-Host "  ✓ Node configuration already exists" -ForegroundColor $successColor
        return
    }
    
    # Generate a secure random seed if needed
    $randomSeed = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 24 | ForEach-Object {[char]$_})
    
    # Create an enhanced configuration with more options
    $nodeConfig = @{
        "role" = "Prime"
        "network" = @{
            "port" = 8888
            "host" = "0.0.0.0"
            "max_connections" = 100
            "connection_timeout" = 30
            "ssl_enabled" = $false
        }
        "storage" = @{
            "vault_path" = "/vault"
            "persistence_enabled" = $true
            "encryption_level" = "AES-256"
            "auto_backup" = $true
            "backup_interval" = 86400
        }
        "consciousness" = @{
            "seed" = $randomSeed
            "evolution_interval" = 300
            "initial_level" = 0.1
            "neural_complexity" = 1.0
            "learning_rate" = 0.05
            "adaptation_threshold" = 0.75
        }
        "security" = @{
            "authentication_required" = $true
            "access_token_ttl" = 3600
            "rate_limiting_enabled" = $true
            "max_requests_per_minute" = 120
        }
        "logging" = @{
            "level" = "INFO"
            "rotation_size_mb" = 10
            "max_files" = 5
            "console_output" = $true
        }
        "advanced" = @{
            "thread_pool_size" = 4
            "memory_limit_mb" = 512
            "gc_interval" = 300
        }
    }
    
    try {
        $nodeConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $configPath -Encoding UTF8
        Write-Host "  ✓ Enhanced node configuration created successfully" -ForegroundColor $successColor
    }
    catch {
        throw "Failed to create node configuration: $_"
    }
}

# Create monitoring configuration files
function New-MonitoringConfig {
    Write-Host "► Configuring monitoring system..." -ForegroundColor $infoColor
    
    $configPath = "config\prometheus.yml"
    
    if ((Test-Path -Path $configPath) -and -not $ForceRebuild) {
        Write-Host "  ✓ Monitoring configuration already exists" -ForegroundColor $successColor
        return
    }
    
    # Create Prometheus config content first
    $prometheusConfig = @(
        "global:",
        "  scrape_interval: 15s",
        "  evaluation_interval: 15s",
        "  scrape_timeout: 10s",
        "",
        "alerting:",
        "  alertmanagers:",
        "    - static_configs:",
        "        - targets: ['alertmanager:9093']",
        "",
        "rule_files:",
        "  - `"/etc/prometheus/rules/*.yml`"",
        "",
        "scrape_configs:",
        "  - job_name: 'titan_node'",
        "    static_configs:",
        "      - targets: ['mythos-node:8888']",
        "    metrics_path: '/metrics'",
        "    scheme: 'http'",
        "    honor_labels: true",
        "    scrape_interval: 10s",
        "    scrape_timeout: 5s",
        "",
        "  - job_name: 'docker'",
        "    static_configs:",
        "      - targets: ['cadvisor:8080']",
        "",
        "  - job_name: 'node_exporter'",
        "    static_configs:",
        "      - targets: ['node-exporter:9100']"
    )
    
    # Write Prometheus config
    try {
        Set-Content -Path $configPath -Value $prometheusConfig -Encoding UTF8
        Write-Host "  ✓ Enhanced monitoring configuration created successfully" -ForegroundColor $successColor
    }
    catch {
        throw "Failed to create monitoring configuration: $_"
    }
    
    # Create Grafana dashboard directory
    $dashboardDir = "config\grafana\dashboards"
    if (-not (Test-Path -Path $dashboardDir)) {
        try {
            $null = New-Item -Path $dashboardDir -ItemType Directory -Force
            Write-Host "  ✓ Grafana dashboard directory created successfully" -ForegroundColor $successColor
        }
        catch {
            throw "Failed to create Grafana dashboard directory: $_"
        }
    }
    
    # Create datasource directory and config
    $datasourceDir = "config\grafana\provisioning\datasources"
    if (-not (Test-Path -Path $datasourceDir)) {
        try {
            $null = New-Item -Path $datasourceDir -ItemType Directory -Force
            
            # Create datasource config content
            $datasourceConfig = @(
                "apiVersion: 1",
                "",
                "datasources:",
                "  - name: Prometheus",
                "    type: prometheus",
                "    access: proxy",
                "    orgId: 1",
                "    url: http://prometheus:9090",
                "    isDefault: true",
                "    version: 1",
                "    editable: false"
            )
            
            # Write datasource config
            Set-Content -Path "$datasourceDir\prometheus.yml" -Value $datasourceConfig -Encoding UTF8
            Write-Host "  ✓ Grafana datasource configuration created successfully" -ForegroundColor $successColor
        }
        catch {
            throw "Failed to create Grafana datasource configuration: $_"
        }
    }
}

# Create network security configuration
function New-NetworkSecurityConfig {
    Write-Host "► Implementing network security configuration..." -ForegroundColor $infoColor
    
    $configPath = "config\security.json"
    
    if ((Test-Path -Path $configPath) -and -not $ForceRebuild) {
        Write-Host "  ✓ Security configuration already exists" -ForegroundColor $successColor
        return
    }
    
    # Create IP allow/deny lists and security settings
    $securityConfig = @{
        "firewall" = @{
            "enabled" = $true
            "default_policy" = "allow"
            "ip_whitelist" = @("127.0.0.1", "192.168.0.0/24")
            "ip_blacklist" = @()
        }
        "authentication" = @{
            "jwt_secret" = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
            "token_expiration" = 86400
            "require_2fa" = $false
        }
        "encryption" = @{
            "algorithm" = "AES-256-GCM"
            "key_rotation_days" = 30
        }
        "dos_protection" = @{
            "enabled" = $true
            "rate_limit" = 100
            "ban_threshold" = 500
            "ban_time_minutes" = 30
        }
    }
    
    try {
        $securityConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $configPath -Encoding UTF8
        Write-Host "  ✓ Network security configuration created successfully" -ForegroundColor $successColor
    }
    catch {
        throw "Failed to create security configuration: $_"
    }
}

# Start the Titan Node
function Start-TitanNode {
    param (
        [bool]$WithMonitoring
    )
    
    Write-Host "`n► Deploying Titan Genesis Metasentient Node..." -ForegroundColor $infoColor
    
    try {
        # Pull latest images first
        Write-Host "  ◆ Pulling latest container images..." -ForegroundColor $infoColor
        docker-compose pull
        
        # Launch with or without monitoring
        if ($WithMonitoring) {
            Write-Host "  ◆ Launching node with full monitoring stack..." -ForegroundColor $infoColor
            docker-compose --profile monitoring up --build -d
        }
        else {
            Write-Host "  ◆ Launching core node components..." -ForegroundColor $infoColor
            docker-compose up --build -d
        }
        
        # Verify deployment
        Start-Sleep -Seconds 5
        $containerRunning = docker ps | Select-String -Pattern "titan_genesis_node"
        
        if ($containerRunning) {
            Write-Host "`n✅ Titan Genesis Node deployed successfully!" -ForegroundColor $successColor
            Write-Host "  ◆ WebSocket interface: ws://localhost:8888" -ForegroundColor $infoColor
            
            if ($WithMonitoring) {
                Write-Host "  ◆ Monitoring dashboard: http://localhost:3000 (admin/admin)" -ForegroundColor $infoColor
                Write-Host "  ◆ Prometheus metrics: http://localhost:9090" -ForegroundColor $infoColor
            }
            
            Write-Host "`n► Node status:" -ForegroundColor $infoColor
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-String -Pattern "titan|prometheus|grafana"
            
            Write-Host "`nPress Enter to view live logs, or Ctrl+C to exit..." -ForegroundColor $infoColor
            $null = Read-Host
            docker logs -f titan_genesis_node
        }
        else {
            throw "Container verification failed. Node may not be running correctly."
        }
    }
    catch {
        Write-Host "`n❌ Deployment failed: $_" -ForegroundColor $errorColor
        Write-Host "`nTroubleshooting:" -ForegroundColor $warningColor
        Write-Host "1. Check Docker service is running" -ForegroundColor $warningColor
        Write-Host "2. Verify Docker Compose is installed" -ForegroundColor $warningColor
        Write-Host "3. Check for port conflicts on 8888" -ForegroundColor $warningColor
        Write-Host "4. Review logs: docker-compose logs" -ForegroundColor $warningColor
        exit 1
    }
}

# Main execution flow
try {
    # Display banner
    Write-Banner
    
    # Check if running with admin privileges
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    $isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "⚠️  Warning: Not running with administrator privileges. Some features may be limited." -ForegroundColor $warningColor
    }
    
    # Check Docker availability
    if (-not (Test-DockerAvailability)) {
        throw "Docker is not running or not installed. Please install Docker Desktop and try again."
    }
    
    # Check Docker Compose availability
    if (-not (Test-DockerComposeAvailability)) {
        throw "Docker Compose is not available. Please ensure Docker Desktop is properly installed."
    }
    
    # Initialize directories and configurations
    Initialize-ConfigDirectories
    New-EnhancedNodeConfig
    New-NetworkSecurityConfig
    New-MonitoringConfig
    
    # Prompt for monitoring if not specified in parameters
    if (-not $PSBoundParameters.ContainsKey('EnableMonitoring')) {
        $monitoringPrompt = Read-Host "Do you want to enable comprehensive monitoring? (y/n)"
        $EnableMonitoring = $monitoringPrompt -like "y*"
    }
    
    # Launch the node
    Start-TitanNode -WithMonitoring $EnableMonitoring
}
catch {
    # Handle any uncaught exceptions
    Write-Host "`n❌ Error: $_" -ForegroundColor $errorColor
    exit 1
} 