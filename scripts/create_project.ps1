#==========================================================
# Reusable Data Quality Framework
# Bootstrap Script
# Version : v0
#==========================================================

Clear-Host

$ProjectRoot = Split-Path $PSScriptRoot -Parent

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Reusable Data Quality Framework" -ForegroundColor Green
Write-Host "Bootstrap Script" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

#----------------------------------------------------------
# Project Structure Verification
#----------------------------------------------------------

$RequiredFolders = @(
".github",
"assets",
"config",
"deployment",
"docs",
"examples",
"logs",
"notebooks",
"sample_data",
"scripts",
"sql",
"src",
"src\dqframework",
"tests"
)

Write-Host "[1/5] Verifying Project Structure..."

foreach($Folder in $RequiredFolders)
{
    $Path = Join-Path $ProjectRoot $Folder

    if(!(Test-Path $Path))
    {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
        Write-Host "Created : $Folder"
    }
}

#----------------------------------------------------------
# Git Verification
#----------------------------------------------------------

Write-Host ""
Write-Host "[2/5] Verifying Git..."

try
{
    git --version | Out-Null
    Write-Host "Git Installed"
}
catch
{
    Write-Host "Git NOT Installed" -ForegroundColor Red
}

#----------------------------------------------------------
# Python Verification
#----------------------------------------------------------

Write-Host ""
Write-Host "[3/5] Verifying Python..."

try
{
    python --version
}
catch
{
    Write-Host "Python NOT Installed" -ForegroundColor Red
}

#----------------------------------------------------------
# Databricks CLI Verification
#----------------------------------------------------------

Write-Host ""
Write-Host "[4/5] Verifying Databricks CLI..."

try
{
    databricks version
}
catch
{
    Write-Host "Databricks CLI NOT Installed"
}

#----------------------------------------------------------
# Configuration Verification
#----------------------------------------------------------

Write-Host ""
Write-Host "[5/5] Verifying Configuration..."

if(Test-Path "$ProjectRoot\config\framework.yml")
{
    Write-Host "framework.yml Found"
}
else
{
    Write-Host "framework.yml Missing" -ForegroundColor Red
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Bootstrap Completed Successfully" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan