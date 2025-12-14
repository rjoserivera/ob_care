# Script PowerShell para gestionar usuarios y roles
# Uso: .\gestionar_usuarios.ps1

# Colores
$SuccessColor = "Green"
$ErrorColor = "Red"
$WarningColor = "Yellow"
$InfoColor = "Cyan"

function Show-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $InfoColor
    Write-Host "║                                                           ║" -ForegroundColor $InfoColor
    Write-Host "║      🏥  GESTOR DE USUARIOS Y ROLES - OB CARE  🏥       ║" -ForegroundColor $InfoColor
    Write-Host "║                                                           ║" -ForegroundColor $InfoColor
    Write-Host "║          Sistema de Gestión Hospitalaria                 ║" -ForegroundColor $InfoColor
    Write-Host "║                                                           ║" -ForegroundColor $InfoColor
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor $InfoColor
    Write-Host ""
}

function Show-Menu {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $InfoColor
    Write-Host "║                    MENÚ PRINCIPAL                         ║" -ForegroundColor $InfoColor
    Write-Host "╠═══════════════════════════════════════════════════════════╣" -ForegroundColor $InfoColor
    Write-Host "║                                                           ║" -ForegroundColor $InfoColor
    Write-Host "║  1️⃣  Modo interactivo (RECOMENDADO)                      ║" -ForegroundColor $InfoColor
    Write-Host "║  2️⃣  Crear grupos del sistema                             ║" -ForegroundColor $InfoColor
    Write-Host "║  3️⃣  Crear usuarios iniciales                             ║" -ForegroundColor $InfoColor
    Write-Host "║  4️⃣  Crear usuarios demo (10 usuarios)                    ║" -ForegroundColor $InfoColor
    Write-Host "║  5️⃣  Listar todos los usuarios                            ║" -ForegroundColor $InfoColor
    Write-Host "║  6️⃣  Listar Médicos                                       ║" -ForegroundColor $InfoColor
    Write-Host "║  7️⃣  Listar Matronas                                      ║" -ForegroundColor $InfoColor
    Write-Host "║  8️⃣  Listar TENS                                          ║" -ForegroundColor $InfoColor
    Write-Host "║  9️⃣  Listar Administradores                               ║" -ForegroundColor $InfoColor
    Write-Host "║  0️⃣  Salir                                                 ║" -ForegroundColor $InfoColor
    Write-Host "║                                                           ║" -ForegroundColor $InfoColor
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor $InfoColor
    Write-Host ""
}

function Activate-VirtualEnv {
    Write-Host "🔧 Activando entorno virtual..." -ForegroundColor $WarningColor
    
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & .\.venv\Scripts\Activate.ps1
        Write-Host "✅ Entorno virtual activado" -ForegroundColor $SuccessColor
        return $true
    } else {
        Write-Host "❌ No se encontró el entorno virtual en .\.venv" -ForegroundColor $ErrorColor
        Write-Host "   Asegúrate de estar en el directorio raíz del proyecto" -ForegroundColor $WarningColor
        return $false
    }
}

function Run-DjangoCommand {
    param (
        [string]$Command
    )
    
    Write-Host ""
    Write-Host "🚀 Ejecutando: $Command" -ForegroundColor $InfoColor
    Write-Host ("═" * 60) -ForegroundColor $InfoColor
    Write-Host ""
    
    Invoke-Expression "python manage.py $Command"
    
    Write-Host ""
    Write-Host ("═" * 60) -ForegroundColor $InfoColor
    Write-Host "✅ Comando completado" -ForegroundColor $SuccessColor
    Write-Host ""
}

# Main
Clear-Host
Show-Banner

# Verificar si estamos en el directorio correcto
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: No se encontró manage.py" -ForegroundColor $ErrorColor
    Write-Host "   Por favor, ejecuta este script desde el directorio raíz del proyecto" -ForegroundColor $WarningColor
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit
}

# Activar entorno virtual
if (-not (Activate-VirtualEnv)) {
    Read-Host "Presiona Enter para salir"
    exit
}

$continuar = $true

while ($continuar) {
    Show-Menu
    $opcion = Read-Host "👉 Selecciona una opción"
    
    switch ($opcion) {
        "1" {
            Run-DjangoCommand "gestionar_usuarios_roles"
        }
        "2" {
            Run-DjangoCommand "crear_grupos_sistema"
        }
        "3" {
            Run-DjangoCommand "crear_usuarios_iniciales"
        }
        "4" {
            Write-Host ""
            Write-Host "🚀 Iniciando modo interactivo para crear usuarios demo..." -ForegroundColor $InfoColor
            Write-Host "   Selecciona la opción 7 en el menú siguiente" -ForegroundColor $WarningColor
            Write-Host ""
            Start-Sleep -Seconds 2
            Run-DjangoCommand "gestionar_usuarios_roles"
        }
        "5" {
            Run-DjangoCommand "gestionar_usuarios_roles --listar todos"
        }
        "6" {
            Run-DjangoCommand "gestionar_usuarios_roles --listar medico"
        }
        "7" {
            Run-DjangoCommand "gestionar_usuarios_roles --listar matrona"
        }
        "8" {
            Run-DjangoCommand "gestionar_usuarios_roles --listar tens"
        }
        "9" {
            Run-DjangoCommand "gestionar_usuarios_roles --listar administrador"
        }
        "0" {
            Write-Host ""
            Write-Host "👋 ¡Hasta luego!" -ForegroundColor $SuccessColor
            Write-Host ""
            $continuar = $false
        }
        default {
            Write-Host ""
            Write-Host "❌ Opción inválida. Por favor, intenta de nuevo." -ForegroundColor $ErrorColor
            Write-Host ""
            Start-Sleep -Seconds 2
        }
    }
    
    if ($continuar) {
        Write-Host ""
        Read-Host "Presiona Enter para continuar"
        Clear-Host
        Show-Banner
    }
}
