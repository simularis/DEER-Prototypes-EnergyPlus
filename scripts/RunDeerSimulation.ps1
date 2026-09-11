# RunDeerSimulation.ps1

param(
    [string]$RunId,
    [string]$Repository,
    [string]$CommitSha,
    [string]$MeasurePath,
    [string]$S3Bucket
)

$Workspace = "E:\gh-worker\$RunId"

New-Item -ItemType Directory -Force -Path $Workspace

git clone https://github.com/simularis/DEER-Prototypes-in-EnergyPlus.git `
    "$Workspace\repo"

Set-Location "$Workspace\repo"

git checkout $CommitSha

modelkit rake compose

modelkit rake run

aws s3 sync `
    "$Workspace\repo\$MeasurePath\runs" `
    "s3://$S3Bucket/runs/$RunId"
