# Use a minimal base image
FROM alpine:3.15 AS builder

# Install necessary packages
RUN apk add --no-cache \
    sudo \
    openssl \
    python3 \
    py3-pip \
    clamav \
    fail2ban \
    wget \
    tar \
    bash \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# Copy custom Python scripts to /usr/local/bin
COPY encrypt.py /usr/local/bin/encrypt.py
COPY decrypt.py /usr/local/bin/decrypt.py
COPY hash_program.py /usr/local/bin/hash_program.py

# Install any necessary Python packages
COPY requirements.txt /usr/local/bin/requirements.txt
RUN pip3 install --no-cache-dir -r /usr/local/bin/requirements.txt

# Make the scripts executable
RUN chmod +x /usr/local/bin/encrypt.py \
    && chmod +x /usr/local/bin/decrypt.py \
    && chmod +x /usr/local/bin/hash_program.py


# Use multi-stage build to copy necessary files to a minimal image
FROM alpine:3.15
COPY --from=builder /usr/local/bin/encrypt.py /usr/local/bin/encrypt.py
COPY --from=builder /usr/local/bin/decrypt.py /usr/local/bin/decrypt.py
COPY --from=builder /usr/local/bin/hash_program.py /usr/local/bin/hash_program.py

# Copy necessary packages and configurations
COPY --from=builder /usr/lib/python3.9/site-packages /usr/lib/python3.9/site-packages

# Make the scripts executable
RUN chmod +x /usr/local/bin/encrypt.py \
    && chmod +x /usr/local/bin/decrypt.py \
    && chmod +x /usr/local/bin/hash_program.py


# Create users and set passwords
RUN adduser -D -s /bin/ash user1 && echo "user1:user1password" | chpasswd && addgroup user1 wheel
RUN adduser -D -s /bin/ash user2 && echo "user2:user2password" | chpasswd
RUN adduser -D -s /bin/ash user3 && echo "user3:user3password" | chpasswd
RUN adduser -D -s /bin/ash user4 && echo "user4:user4password" | chpasswd
RUN adduser -D -s /bin/ash user5 && echo "user5:user5password" | chpasswd
RUN adduser -D -s /bin/ash user6 && echo "user6:user6password" | chpasswd
RUN adduser -D -s /bin/ash user7 && echo "user7:user7password" | chpasswd
RUN adduser -D -s /bin/ash user8 && echo "user8:user8password" | chpasswd
RUN adduser -D -s /bin/ash user9 && echo "user9:user9password" | chpasswd
RUN adduser -D -s /bin/ash user10 && echo "user10:user10password" | chpasswd

# Create a superuser with root privileges (if needed)
RUN adduser -D -s /bin/ash superuser && echo "superuser:superpassword" | chpasswd && addgroup superuser wheel

# Create directory structure and various files for each user
RUN for i in $(seq 1 10); do \
    mkdir -p /home/user${i}/profile/level1/level2; \
    echo "This is a password protected file for user${i}" > /home/user${i}/profile/level1/level2/file.txt; \
    python3 /usr/local/bin/encrypt.py -i /home/user${i}/profile/level1/level2/file.txt -o /home/user${i}/profile/level1/level2/file.txt.enc -p "password${i}"; \
    rm /home/user${i}/profile/level1/level2/file.txt; \
    \
    # Create a file with a random string
    head /dev/urandom | tr -dc A-Za-z0-9 | head -c 30 > /home/user${i}/profile/level1/random_string.txt; \
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

# Run as non-root user by default
USER user1

# Expose port if needed (optional)
EXPOSE 8080

# Set the default command to run when starting the container
CMD ["ash"]
