# RunDeerSimulation.ps1

param(
    [string]$RunId,
    [string]$Repository,
    [string]$CommitSha,
    [string]$MeasurePath,
    [string]$S3Bucket
)

$Workspace = "E:\githubactions\$RunId"

New-Item -ItemType Directory -Force -Path $Workspace

git clone "$Repository" "$Workspace\repo"

Set-Location "$Workspace\repo"

git checkout $CommitSha

modelkit rake compose

# modelkit rake run

aws s3 sync `
    "$Workspace\repo\$MeasurePath\runs" `
    "s3://$S3Bucket/githubactions/$RunId"
