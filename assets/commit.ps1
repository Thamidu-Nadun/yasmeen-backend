# This script is used to commit changes to a Git repository with a specified commit message and date.

param(
    [string]$message,
    [string]$date
)

if (-not $message) {
    Write-Host "Error: Commit message is required."
    exit 1
}

if (-not $date) {
    Write-Host "Error: Commit date is required."
    Write-Host "Usage: .\commit.ps1 `"message`" `"YYYY-MM-DDTHH:MM:SS`""
    Write-Host "Example: .\commit.ps1 `"Initial commit`" `"2024-06-01T12:00:00`""
    exit 1
}

$env:GIT_AUTHOR_DATE = $date
$env:GIT_COMMITTER_DATE = $date

git add -A
git commit -m $message

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Commit created with message: '$message' and date: '$date'"
} else {
    Write-Host "[-] Commit failed."
    exit 1
}

# Clean up environment variables
Remove-Item Env:\GIT_AUTHOR_DATE -ErrorAction SilentlyContinue
Remove-Item Env:\GIT_COMMITTER_DATE -ErrorAction SilentlyContinue
