$ErrorActionPreference = 'Stop'
$Root = 'C:\Users\taymi\discord-hadith-bot\mizan-web'
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Backup = Join-Path $Root ("_backup-before-ui-patch-" + $Stamp)

New-Item -ItemType Directory -Force -Path $Backup | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Backup 'frontend\src\app\components') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Backup 'frontend\src\app\books') | Out-Null

$Files = @(
  'frontend\src\app\page.tsx',
  'frontend\src\app\books\page.tsx',
  'frontend\src\app\globals.css',
  'frontend\src\app\components\BookShowcase.tsx',
  'frontend\src\app\components\SiteChrome.tsx'
)

foreach ($rel in $Files) {
  $target = Join-Path $Root $rel
  if (Test-Path $target) {
    $backupTarget = Join-Path $Backup $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $backupTarget) | Out-Null
    Copy-Item $target $backupTarget -Force
  }
  $source = Join-Path $PatchRoot $rel
  if (-not (Test-Path $source)) { throw "Patch file missing: $source" }
  Copy-Item $source $target -Force
}

# Backend replacement is intentionally limited to fixing user-facing mojibake.
$backendTarget = Join-Path $Root 'backend\main.py'
$backendBackup = Join-Path $Backup 'backend\main.py'
New-Item -ItemType Directory -Force -Path (Split-Path $backendBackup) | Out-Null
if (Test-Path $backendTarget) { Copy-Item $backendTarget $backendBackup -Force }
Copy-Item (Join-Path $PatchRoot 'backend_main.py') $backendTarget -Force

Write-Host "Patch applied successfully."
Write-Host "Backup: $Backup"
Write-Host "Next: cd $Root\frontend ; npm run build"
