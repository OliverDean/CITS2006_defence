rule Script_Obfuscation {
    meta:
        description = "Targets script files using obfuscation to conceal malicious activity, such as encoded payloads and evasion techniques."
        author = "OLIVER"
        reference = "Analysis of script-based malware"

    strings:
        // Encoded PowerShell Commands
        $ps_encoded = "powershell.exe -EncodedCommand" wide ascii
        
        // ROT13 Usage in Scripts
        $rot13 = "rot13" wide ascii
        
        // Base64 Encoding in JavaScript
        $js_base64 = "atob(" wide ascii
        
        // Obfuscated Python Code
        $py_obfusc = "exec" wide ascii
        
        // Nested PowerShell Invocation
        $nested_ps = /Start-Process.* -Command.*Start-Process/ wide ascii

    condition:
        // Check for scripts larger than typical simple scripts but small enough to be malware
        filesize > 10KB and filesize < 500KB and
        (2 of ($ps_encoded, $nested_ps) or 3 of ($rot13, $js_base64, $py_obfusc))
}
