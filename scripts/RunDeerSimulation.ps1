# RunDeerSimulation.ps1

param(
    [string]$RunId,
    [string]$Repository,
    [string]$CommitSha,
    [string]$MeasurePath,
    [string]$S3Bucket
)

$Workspace = "E:\githubactions\$RunId"
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$LogDir = "$Workspace\logs"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$LogFile = "$LogDir\RunDeerSimulation.log"

# Capture everything written to the console
Start-Transcript -Path $LogFile -Force

$RunStatus = "Success"
$FailureMessage = ""
$StartDate = Get-Date

try {
    Write-Host "RunId: $RunId"
    Write-Host "CommitSha: $CommitSha"
    Write-Host "MeasurePath: $MeasurePath"

    New-Item -ItemType Directory -Force -Path $Workspace

    git clone "https://github.com/$Repository.git" "$Workspace\repo"
    
    Set-Location "$Workspace\repo"
    
    git fetch --all

    git checkout $CommitSha

    Set-Location "$Workspace\repo\$MeasurePath"

    modelkit rake compose *>> "$LogDir\compose.log"

    C:\Program Files\Amazon\AWSCLIV2\aws.exe s3 cp `
        "$LogDir\compose.log" `
        "s3://$S3Bucket/githubactions/$RunId/logs/compose.log"

    # modelkit rake run

    C:\Program Files\Amazon\AWSCLIV2\aws.exe s3 sync `
        "$Workspace\repo\$MeasurePath\runs" `
        "s3://$S3Bucket/githubactions/$RunId/runs"

    # If everything was successful and there is no chance we need to re-run the job,
    # we can clean up the workspace to save space on the instance. Uncomment the following line to enable this behavior.

    # Remove-Item $Workspace -Recurse -Force
}
catch {
    Write-Host "ERROR:"
    Write-Host $_

    $RunStatus = "Failed"
    $FailureMessage = $_.Exception.Message

    throw
}
finally {

    $EndDate = Get-Date
    Stop-Transcript

    $status = @{
        RunId = $RunId
        CommitSha = $CommitSha
        MeasurePath = $MeasurePath
        Status = $RunStatus
        FailureMessage = $FailureMessage
        StartDate = $StartDate
        EndDate = $EndDate
        RunTimeSeconds = ($EndDate - $StartDate).TotalSeconds
    } | ConvertTo-Json

    $status | Set-Content "$Workspace\status.json"

    & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" s3 cp `
    "$Workspace\status.json" `
    "s3://$S3Bucket/githubactions/$RunId/status.json"

    & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" s3 cp `
    $LogFile `
    "s3://$S3Bucket/githubactions/$RunId/logs/RunDeerSimulation.log"
}

