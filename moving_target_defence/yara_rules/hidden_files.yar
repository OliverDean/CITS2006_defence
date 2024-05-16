rule hidden_files
{
    meta:
        description = "Detect hidden files containing sensitive information"
        author = "Your Name"
    strings:
        $hidden = /\.(hidden|secret|private|confidential)\.[a-z]{2,4}$/ nocase
    condition:
        $hidden
}
