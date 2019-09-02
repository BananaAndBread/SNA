import subprocess
import sys
path_to_database_mount= sys.argv[1]
path_to_config_mount = sys.argv[2]
docker_compose = f"""
version: '2'
services:
  database:
    image: postgres:9.6-alpine
    environment:
      - POSTGRES_USER=hackmd
      - POSTGRES_PASSWORD=hackmdpass
      - POSTGRES_DB=hackmd
    volumes:
      - database:/var/lib/postgresql/data
    networks:
            no-internet:
    restart: always


  app:
    image: hackmdio/hackmd:1.2.0
    environment:
      - HMD_DB_URL=postgres://hackmd:hackmdpass@database:5432/hackmd
    networks:
      no-internet:
    restart: always
    depends_on:
      - database
  ssh:
    image: rastasheep/ubuntu-sshd
    ports:
      - "1234:22"
    volumes:
      - ssh_config:/etc/ssh
    networks:
      internet:  
      no-internet:
networks:
  internet:
    driver: bridge
    ipam:
        driver: default
        config:
            - subnet: 172.24.1.0/27
  no-internet:
        driver: bridge
        internal: true
        ipam:
            driver: default
            config:
                - subnet: 172.24.0.0/27
   

volumes:
    database:
        driver: local
        driver_opts:
            type: none
            o: bind
            device: {path_to_database_mount}

    ssh_config:
        driver: local
        driver_opts:
            type: none
            o: bind
            device: {path_to_config_mount}
"""

subprocess.call(f'mkdir {path_to_database_mount}', shell=True)
subprocess.call(f'mkdir {path_to_config_mount}', shell=True)
file = open("docker-compose.yml", "w")
file.write(docker_compose)
file.close()
subprocess.call('docker-compose up', shell=True)





