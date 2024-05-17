# Navigate to the Git repository
Set-Location -Path "C:\Users\olive\OneDrive\Desktop\CompSci\2024_semester_1\CITS2006_defensive_cybersecurity\CITS2006_defence"

# Path to output file
$outputFilePath = "C:\Users\olive\OneDrive\Desktop\CompSci\2024_semester_1\CITS2006_defensive_cybersecurity\CITS2006_defence\git_contributions_combined.txt"

# Get the list of authors
$authors = git log --pretty=format:"%an" | Sort-Object -Unique

# Initialize the hashtable to store the data
$contributions = @{}

# Function to count unique lines of code for each author
function Get-UniqueLinesByAuthor {
    param ($author)
    $commits = git log --author="$author" --pretty=format:"%H"
    $uniqueLines = @()
    foreach ($commit in $commits) {
        $diffLines = git show $commit --pretty="" --unified=0 --word-diff=porcelain | Select-String "^\+[^+]" | ForEach-Object { $_.Line.TrimStart('+') }
        $uniqueLines += $diffLines
    }
    return ($uniqueLines | Sort-Object -Unique).Count
}

# Gather contributions data
foreach ($author in $authors) {
    $uniqueLines = Get-UniqueLinesByAuthor $author
    $commitCount = (git log --author="$author" --pretty=format:"%H" | Measure-Object).Count
    $contributions[$author] = [PSCustomObject]@{
        Name        = $author
        UniqueLines = $uniqueLines
        Commits     = $commitCount
    }
}

# Convert hashtable to array and sort by UniqueLines descending
$contributionsArray = $contributions.GetEnumerator() | Sort-Object -Property Value.UniqueLines -Descending | ForEach-Object { $_.Value }

# Output the results to a file
$contributionsArray | Format-Table -Property Name, UniqueLines, Commits -AutoSize | Out-File $outputFilePath

Write-Output "File 'git_contributions_combined.txt' has been created at the specified location."
