rule custom_signatures
{
    meta:
        description = "Detects files containing custom signatures"
        author = "ARMAAN"
    strings:
        $custom1 = "custom_string1" nocase
        $custom2 = "custom_string2" nocase
        $custom3 = "custom_pattern" nocase
    condition:
        any of ($custom1, $custom2, $custom3)
}

