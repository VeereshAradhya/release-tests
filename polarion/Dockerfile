FROM registry.access.redhat.com/ubi8/ubi:8.1

# install prerequisites
RUN dnf install cpio python3 git -y

# Install pylarion
RUN GIT_SSL_NO_VERIFY=true git clone https://code.engineering.redhat.com/gerrit/pylarion && cd pylarion/dist && mv pylarion-0.0.1-1.noarch.rpm / && cd / && rpm2cpio pylarion-0.0.1-1.noarch.rpm | cpio -idmv
RUN pip3 install mistune==2.0.0rc1 pyyaml gherkin-official prettytable requests suds-py3 click