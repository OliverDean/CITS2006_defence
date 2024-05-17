# Use a minimal base image
FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    openssl \
    python3 \
    python3-pip \
    clamav \
    fail2ban \
    wget \
    tar \
    bash \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify installation of Python and sudo
RUN python3 --version \
    && pip3 --version \
    && sudo --version

# Create a secure_coding directory and copy all files from the current directory to /root/secure_coding
RUN mkdir -p /root/secure_coding
COPY . /root/secure_coding/

# Install any necessary Python packages
RUN pip3 install --no-cache-dir -r /root/secure_coding/requirements.txt

# Make the scripts executable and set permissions
RUN chmod -R 700 /root/secure_coding

# Create users and set passwords
RUN adduser --disabled-password --gecos "" user1 && echo "user1:user1password" | chpasswd && usermod -aG sudo user1
RUN adduser --disabled-password --gecos "" user2 && echo "user2:user2password" | chpasswd
RUN adduser --disabled-password --gecos "" user3 && echo "user3:user3password" | chpasswd
RUN adduser --disabled-password --gecos "" user4 && echo "user4:user4password" | chpasswd
RUN adduser --disabled-password --gecos "" user5 && echo "user5:user5password" | chpasswd
RUN adduser --disabled-password --gecos "" user6 && echo "user6:user6password" | chpasswd
RUN adduser --disabled-password --gecos "" user7 && echo "user7:user7password" | chpasswd
RUN adduser --disabled-password --gecos "" user8 && echo "user8:user8password" | chpasswd
RUN adduser --disabled-password --gecos "" user9 && echo "user9:user9password" | chpasswd
RUN adduser --disabled-password --gecos "" user10 && echo "user10:user10password" | chpasswd

# Create a superuser with root privileges
RUN adduser --disabled-password --gecos "" superuser && echo "superuser:superpassword" | chpasswd && usermod -aG sudo superuser

# Configure superuser to have UID 0 (root user)
RUN usermod -u 0 -o superuser && groupmod -g 0 -o superuser

# Create directory structure and various files for each user
RUN for i in $(seq 1 10); do \
    mkdir -p /home/user${i}/profile/level1/level2; \
    echo "This is a password protected file for user${i}" > /home/user${i}/profile/level1/level2/file.txt; \
    python3 /root/secure_coding/encrypt.py -i /home/user${i}/profile/level1/level2/file.txt -o /home/user${i}/profile/level1/level2/file.txt.enc -p "password${i}"; \
    rm /home/user${i}/profile/level1/level2/file.txt; \
    \
    # Create a file with a random string
    head /dev/urandom | tr -dc A-Za-z0-9 | head -c 300 > /home/user${i}/profile/level1/random_string.txt; \
    \
    # Create files with Star Trek quotes
    echo "Live long and prosper. - Spock" > /home/user${i}/profile/level1/level2/quote1.txt; \
    echo "The needs of the many outweigh the needs of the few. - Spock" > /home/user${i}/profile/level1/level2/quote2.txt; \
    echo "Resistance is futile. - Borg" > /home/user${i}/profile/level1/level2/quote3.txt; \
    done

# Set permissions for the directory structure
RUN for i in $(seq 1 10); do \
    chown -R user${i}:user${i} /home/user${i}/profile; \
    chmod -R 700 /home/user${i}/profile; \
    done

# Ensure that only root can access the secure_coding directory
RUN chmod -R 700 /root/secure_coding

# Expose port if needed (optional)
EXPOSE 8080

# Set the default command to run when starting the container
CMD ["bash"]
