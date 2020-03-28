FROM jupyter/datascience-notebook:dc9744740e12

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/

CMD ["jupyterhub-singleuser"]