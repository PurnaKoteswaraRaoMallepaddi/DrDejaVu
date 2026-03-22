# DrDejaVu Database Cleanup Script
# Removes all database records and starts fresh

param(
    [switch]$Full = $false,
    [switch]$KeepUploads = $false
)

Write-Host "🗑️  DrDejaVu Database Cleanup" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

$dataPath = Join-Path $PSScriptRoot "data"

# Delete ChromaDB
if (Test-Path "$dataPath/chroma_db/chroma.sqlite3") {
    Remove-Item -Path "$dataPath/chroma_db/chroma.sqlite3" -Force
    Write-Host "✓ Deleted ChromaDB vector store" -ForegroundColor Green
}

# Delete ChromaDB collections
Get-ChildItem -Path "$dataPath/chroma_db" -Directory | ForEach-Object {
    Remove-Item -Path $_.FullName -Recurse -Force
    Write-Host "✓ Deleted ChromaDB collection: $($_.Name)" -ForegroundColor Green
}

# Delete consultation database
if (Test-Path "$dataPath/drdejacu.db") {
    Remove-Item -Path "$dataPath/drdejacu.db" -Force
    Write-Host "✓ Deleted consultation database" -ForegroundColor Green
}

# Delete uploaded files (unless -KeepUploads specified)
if (-not $KeepUploads) {
    $uploadsPath = "$dataPath/uploads"
    if (Test-Path $uploadsPath) {
        Get-ChildItem -Path $uploadsPath | Remove-Item -Recurse -Force
        Write-Host "✓ Deleted all uploaded files" -ForegroundColor Green
    }
}

# Full reset: recreate directories
if ($Full) {
    @("chroma_db", "uploads") | ForEach-Object {
        $dir = Join-Path $dataPath $_
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "✓ Created fresh: $dir" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "✅ Cleanup complete! Database is fresh and ready." -ForegroundColor Green
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  .\cleanup.ps1                    # Delete databases, keep uploads"
Write-Host "  .\cleanup.ps1 -KeepUploads       # Delete databases, keep uploads"
Write-Host "  .\cleanup.ps1 -Full              # Delete everything and recreate dirs"
