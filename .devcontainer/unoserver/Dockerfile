FROM ghcr.io/unoconv/unoserver-docker

# Install Japanese fonts
# ###################################
#   IPA FONT LICENSE AGREEMENT V1.0
# https://moji.or.jp/ipafont/license/
# ###################################
ADD archiveipa /usr/local/archiveipa
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
