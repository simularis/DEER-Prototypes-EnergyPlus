# RunDeerSimulation.ps1

param(
    [string]$RunId,
    [string]$Repository,
    [string]$CommitSha,
    [string]$MeasurePath,
    [string]$S3Bucket,
    [int]$RunAttempt
)

$Workspace = "E:\githubactions\$RunId"
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$LogDir = "$Workspace\attempt-$RunAttempt"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$LogFile = "$LogDir\RunDeerSimulation.log"

# Capture everything written to the console
Start-Transcript -Path $LogFile -Force

$RunStatus = "Success"
$FailureMessage = ""
$StartDate = Get-Date
$AwsCli = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"

try {
    Write-Host "RunId: $RunId"
    Write-Host "CommitSha: $CommitSha"
    Write-Host "MeasurePath: $MeasurePath"

    Write-Host "Cloning repository into $Workspace\repo"

    New-Item -ItemType Directory -Force -Path $Workspace

    $RepoDir = "$Workspace\repo"

    if (-not (Test-Path "$RepoDir\.git")) {
        Write-Host "Repository not found. Cloning..."
        git clone "https://github.com/$Repository.git" $RepoDir
    }
    else {
        Write-Host "Repository already exists. Reusing existing checkout."
    }

    Set-Location $RepoDir
    git remote get-url origin

    # In case the user re-runs the same job with a different commit, we need to fetch all commits to ensure the specified commit is available.
    git fetch --all
    git checkout $CommitSha

    Set-Location "$Workspace\repo\$MeasurePath"

    modelkit rake compose *>> "$LogDir\compose.log"

    & $AwsCli s3 cp `
        "$LogDir\compose.log" `
        "s3://$S3Bucket/githubactions/$RunId/logs/compose.log"

    # modelkit rake run

    & $AwsCli s3 sync `
        "$Workspace\repo\$MeasurePath\runs" `
        "s3://$S3Bucket/githubactions/$RunId/runs"

    # Run the "QC incomplete simulations notebook" and publish its outputs.
    $QcDir = Join-Path $Workspace "qc"
    $QcNotebook = Join-Path $QcDir "QC incomplete simulations.ipynb"
    $QcExecutedNotebook = Join-Path $QcDir "QC incomplete simulations.executed.ipynb"
    $QcHtml = Join-Path $QcDir "QC incomplete simulations.html"
    $SimulationStats = Join-Path $QcDir "simulation_stats.csv"

    New-Item -ItemType Directory -Force -Path $QcDir | Out-Null

    Write-Host "Downloading QC notebook from S3..."

    & $AwsCli s3 cp `
        "s3://$S3Bucket/githubactions/$RunId/QC incomplete simulations.ipynb" `
        $QcNotebook

    Write-Host "Executing QC notebook..."

    $CondaExe = "C:\ProgramData\Anaconda3\Scripts\conda.exe"

    if (-not (Test-Path $CondaExe)) {
        throw "Conda executable not found at $CondaExe"
    }

    & $CondaExe run --no-capture-output -n py314 `
        python --version

    # Use conda run instead of conda activate because this script executes
    # non-interactively through SSM.
    $PapermillLog = Join-Path $LogDir "papermill.log"

    try {
        & $CondaExe run --no-capture-output -n py314 `
            papermill `
            $QcNotebook `
            $QcExecutedNotebook `
            -p simfolder "$Workspace\repo\$MeasurePath" `
            -p output_file $SimulationStats `
            *>&1 | Tee-Object -FilePath $PapermillLog

        if ($LASTEXITCODE -ne 0) {
            throw "Papermill failed with exit code $LASTEXITCODE. See $PapermillLog"
        }
    }
    finally {
        if (Test-Path -LiteralPath $PapermillLog) {
            & $AwsCli s3 cp `
                $PapermillLog `
                "s3://$S3Bucket/githubactions/$RunId/attempt-$RunAttempt/papermill.log"
        }
    }

    Write-Host "Converting executed notebook to HTML..."

    & $CondaExe run --no-capture-output -n py314 `
        jupyter nbconvert `
        --to html `
        $QcExecutedNotebook `
        --output "QC incomplete simulations.html" `
        --output-dir $QcDir

    if (-not (Test-Path -LiteralPath $QcHtml)) {
        throw "QC HTML report was not generated: $QcHtml"
    }

    if (-not (Test-Path -LiteralPath $SimulationStats)) {
        throw "QC simulation statistics file was not generated: $SimulationStats"
    }

    Write-Host "Uploading QC outputs to S3..."

    & $AwsCli s3 cp `
        $QcHtml `
        "s3://$S3Bucket/githubactions/$RunId/qc/QC incomplete simulations.html"

    & $AwsCli s3 cp `
        $SimulationStats `
        "s3://$S3Bucket/githubactions/$RunId/qc/simulation_stats.csv"

    & $AwsCli s3 cp `
        $QcExecutedNotebook `
        "s3://$S3Bucket/githubactions/$RunId/qc/QC incomplete simulations.executed.ipynb"

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
        Repository = $Repository
        CommitSha = $CommitSha
        MeasurePath = $MeasurePath
        Status = $RunStatus
        FailureMessage = $FailureMessage
        StartDate = $StartDate
        EndDate = $EndDate
        RunTimeSeconds = ($EndDate - $StartDate).TotalSeconds
    } | ConvertTo-Json

    $status | Set-Content "$Workspace\status.json"

    & $AwsCli s3 cp `
        "$Workspace\status.json" `
        "s3://$S3Bucket/githubactions/$RunId/status.json"

    & $AwsCli s3 cp `
        $LogFile `
        "s3://$S3Bucket/githubactions/$RunId/attempt-$RunAttempt/RunDeerSimulation.log"

}

