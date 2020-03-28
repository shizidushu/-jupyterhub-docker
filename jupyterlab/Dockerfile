FROM jupyter/datascience-notebook:dc9744740e12

RUN conda install --yes \
    'jupyterhub=0.9.3' \
    && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER