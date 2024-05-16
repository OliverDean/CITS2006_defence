how to build the docker image and run it

need the files decrypt.py encrypt.py hash_program.py and requirements.txt

to change them alter this section 

# Use multi-stage build to copy necessary files to a minimal image
FROM ubuntu:20.04
COPY --from=builder /usr/local/bin/encrypt.py /usr/local/bin/encrypt.py
COPY --from=builder /usr/local/bin/decrypt.py /usr/local/bin/decrypt.py
COPY --from=builder /usr/local/bin/hash_program.py /usr/local/bin/hash_program.py


# Make the scripts executable
RUN chmod +x /usr/local/bin/encrypt.py \
    && chmod +x /usr/local/bin/decrypt.py \
    && chmod +x /usr/local/bin/hash_program.py




docker build -t custom-linux-image .

can alter --name to our group or something

docker run -it --rm --cap-drop=ALL --read-only --security-opt=no-new-privileges=true --name secure-container custom-linux-image

Start a new container from the custom-linux-image.
Allocate a terminal session and keep it interactive (-it).
Automatically remove the container once it stops (--rm).
Drop all capabilities to minimize potential security vulnerabilities (--cap-drop=ALL).
Mount the filesystem as read-only to prevent unauthorized modifications (--read-only).
Ensure that no new privileges can be gained by processes in the container (--security-opt=no-new-privileges=true).
Assign the name secure-container to this running container instance for easy reference

inside the container

encrypt a file
ls /home/user1/profile/level1/level2/file.txt.enc

cat /home/user1/profile/level1/random_string.txt

cat /home/user1/profile/level1/level2/quote1.txt
cat /home/user1/profile/level1/level2/quote2.txt
cat /home/user2/profile/level1/level2/quote3.txt

user credentials are

user1 user1password

if needed
RUN useradd -m -s /bin/bash superuser && echo "superuser:superpassword" | chpasswd && adduser superuser sudo
