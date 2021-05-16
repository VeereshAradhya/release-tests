FROM python

# Install pylarion
RUN git clone https://github.com/RedHatQE/pylero.git && cd pylero && python setup.py install
RUN pip install mistune==2.0.0rc1 pyyaml gherkin-official prettytable