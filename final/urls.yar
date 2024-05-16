rule urls
{
    meta:
        description = "Detects executables accessing malicious URLs"
        author = "ARMAAN"
    strings:
        $url = /http[s]?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}\/[a-zA-Z0-9\/%&=\?_\-\.]+/ nocase
    condition:
        uint32(0) == 0x7F454C46 and $url
}

