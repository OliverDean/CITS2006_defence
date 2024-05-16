rule network_executables
{
    meta:
        description = "Detects ELF executables accessing network resources"
        author = "ARMAAN"
    strings:
        $network1 = "socket" nocase
        $network2 = "connect" nocase
        $network3 = "http" nocase
    condition:
        uint32(0) == 0x7F454C46 and any of ($network1, $network2, $network3)
}

rule network_executables_pe
{
    meta:
        description = "Detects PE executables accessing network resources"
        author = "AATRO"
    strings:
        $network1 = "socket" nocase
        $network2 = "connect" nocase
        $network3 = "http" nocase
    condition:
        uint16(0) == 0x5A4D and any of ($network1, $network2, $network3) // PE files start with 'MZ' header
}

