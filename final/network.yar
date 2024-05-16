rule Reconnaissance_Command_Execution {
    meta:
        description = "Detects execution of multiple command-line tools commonly used for system reconnaissance by attackers"
        author = "Oliver"
        reference = "Best practices in detecting reconnaissance activities"

    strings:
        $str1 = "tasklist" wide ascii
        $str2 = "net time" wide ascii
        $str3 = "systeminfo" wide ascii
        $str4 = "whoami" wide ascii
        $str5 = "nbtstat" wide ascii
        $str6 = "net start" wide ascii
        $str7 = "qprocess" wide ascii
        $str8 = "nslookup" wide ascii
        $str9 = "net user" wide ascii
        $str10 = "net localgroup administrators" wide ascii
        $str11 = "arp -a" wide ascii
        $str12 = "netstat -an" wide ascii
        $str13 = "ipconfig /all" wide ascii
        $str14 = "route print" wide ascii
        $str15 = "netsh interface show interface" wide ascii

    condition:
        filesize < 5KB and 6 of them
}
