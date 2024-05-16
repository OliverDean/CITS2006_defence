rule Complex_Code_Obfuscation {
    meta:
        description = "Detects multiple obfuscation techniques combined in executables, indicating sophisticated evasion attempts."
        author = "OLIVER"
        reference = "Developed from common obfuscation patterns observed in modern malware"

    strings:
        // XOR Encoding Patterns
        $xor = /\bxor\b[\s\S]{1,100}\bxor\b/ wide ascii
        
        // Base64 Encoding Usage
        $base64 = /[a-zA-Z0-9\/\+]{50,}={0,2}/ wide ascii
        
        // API Hashing Patterns
        $api_hash = /\bLoadLibrary\b[\s\S]{1,100}\bGetProcAddress\b/ wide ascii
        
        // Dead Code Patterns
        $dead_code = /NOP[\s\S]{1,30}JMP[\s\S]{1,30}NOP/ wide ascii
        
        // Packer Signatures
        $packer = "UPX0" wide ascii

    condition:
        filesize < 2MB and 3 of ($xor, $base64, $api_hash, $dead_code, $packer)
}
