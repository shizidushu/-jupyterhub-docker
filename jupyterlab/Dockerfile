FROM jupyter/datascience-notebook:dc9744740e12

RUN pip3 install jupyterhub==0.9.3

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/