rule port_ssh {
    meta:
        author = "OLIVER"
        description = "Detects binaries and scripts involved in SSH and port sniffing activities"
    strings:

        $ssh_config = "/etc/ssh/sshd_config" ascii
        $ssh_command = "ssh " ascii

        $nmap = "nmap" ascii
        $masscan = "masscan" ascii

        $netcat = "nc " ascii
        $socat = "socat" ascii
        
        $iptables = "iptables" ascii
        $ufw = "ufw" ascii

    condition:
        any of them and filesize < 1MB  // Keeping the file size check to limit false positives in larger benign files
}
