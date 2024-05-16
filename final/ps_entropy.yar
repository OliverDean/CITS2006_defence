import "hash"
import "math"

rule High_Entropy_Scripts {
    meta:
        description = "Detects Bash and PowerShell scripts with unusually high entropy, which may indicate obfuscation or encryption to conceal malicious intent."
        author = "OLIVER"
    
    strings:
        $bash_shebang = "#!/bin/bash" ascii
        $ps_shebang = "#!/usr/bin/env pwsh" ascii
        $ps_tag = "powershell" ascii

    condition:
        (
            $bash_shebang or 
            $ps_shebang or 
            $ps_tag
        ) and (
            math.entropy(0, filesize) > 7.0
        )
}
