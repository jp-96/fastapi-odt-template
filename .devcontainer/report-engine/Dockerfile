## See here for image contents: https://github.com/microsoft/vscode-dev-containers/blob/v0.163.0/containers/python-3/.devcontainer/base.Dockerfile
## Available image variants: https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Optional] Allow the vscode user to pip install globally w/o sudo
ENV PIP_TARGET=/usr/local/pip-global
ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN if ! cat /etc/group | grep -e "^pip-global:" > /dev/null 2>&1; then groupadd -r pip-global; fi \
    && usermod -a -G pip-global vscode \
    && umask 0002 && mkdir -p ${PIP_TARGET} \
    && chown :pip-global ${PIP_TARGET} \
    && ( [ ! -f "/etc/profile.d/00-restore-env.sh" ] || sed -i -e "s/export PATH=/export PATH=\/usr\/local\/pip-global:/" /etc/profile.d/00-restore-env.sh )

# [Option] Install Node.js
# ARG INSTALL_NODE="true"
# ARG NODE_VERSION="lts/*"
# RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# Create directory and set permission
RUN mkdir /opt/report-engine \ 
    && chown -R vscode:vscode /opt/report-engine
RUN mkdir /opt/report-engine/.vscode \
    && chown vscode:vscode /opt/report-engine/.vscode
RUN mkdir /home/vscode/.vscode-server \
    && chown vscode:vscode /home/vscode/.vscode-server

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends unzip poppler-utils

# Install several additional components and Python libs:
#  - a Java Runtime Environment (JRE), which can be OpenJDK,
#  - Libreoffice started in the background in headless mode,
#  - the Java driver for Libreoffice (Juno).
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
		# Installation of Libreoffice, JRE and required Java libs on Debian/Ubuntu:
		# default-jre \
        default-jdk \
		libreoffice-java-common \
		libreoffice-writer \
		# Init system
		supervisor \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# replace default setup with a one disabling logos by default
ADD .devcontainer/report-engine/overlay /

# Install fonts
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
		# Google Fonts - https://fonts.google.com/noto
		fonts-noto-cjk \
		# To have the special unicode symbols for phone/fax/email
		fonts-symbola \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Japanese fonts
# ###################################
#   IPA FONT LICENSE AGREEMENT V1.0
# https://moji.or.jp/ipafont/license/
# ###################################
ADD archiveipa /usr/local/archiveipa
USER vscode
RUN mkdir -p ~/.local/share/fonts
RUN cd /usr/local/archiveipa \
	# IPAmj Mincho Font
    && unzip ipamjm00601.zip -d ~/.local/share/fonts/ipamjm00601 \
    # IPAex Font（2 fonts）
    && unzip IPAexfont00401.zip -d ~/.local/share/fonts/IPAexfont00401 \
    # IPA Font（4 fonts）
    && unzip IPAfont00303.zip -d ~/.local/share/fonts/IPAfont00303 \
    # Build font information cache files
    && fc-cache -vf
USER root

# # [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#     && rm -rf /tmp/pip-tmp

# ENTRYPOINT ["/usr/bin/supervisord"]
