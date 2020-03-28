FROM jupyter/datascience-notebook:dc9744740e12

RUN conda install --yes \
    'jupyterhub=1.0.0' \
    && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER