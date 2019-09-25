FROM jupyter/base-notebook

USER root
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        lxde \
        net-tools \
        novnc \
        tigervnc-standalone-server


EXPOSE 8080
ENTRYPOINT ["bash"]
# https://serverfault.com/questions/376302/tigervnc-ssh-without-a-vnc-password/580859#580859
# vncserver -verbose -xstartup startlxde -SecurityTypes None -geometry 1024x768
# /usr/share/novnc/utils/launch.sh --listen 5902 --vnc localhost:5901

# In browser go to http://localhost:8080/vnc.html?autoconnect=true

