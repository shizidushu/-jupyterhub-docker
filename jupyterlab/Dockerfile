FROM jupyter/datascience-notebook:dc9744740e12

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata \
    scilab \
    pari-gp \
    libpari-dev \
    sagemath \
    sagemath-jupyter \
    libgmp-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Conda packages
RUN conda install --quiet --yes \
    'jupyterhub' \
    && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

ENV CPATH=$CONDA_DIR/include

RUN pip install \
    pari_jupyter \
#    PySingular jupyter_kernel_singular \
    scilab-kernel && \
    fix-permissions $CONDA_DIR

# Fix SageMath kernel
USER root
RUN sed -i 's/"\/usr\/bin\/sage"/"env", "PATH=\/usr\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin", "\/usr\/bin\/sage"/' /usr/share/jupyter/kernels/sagemath/kernel.json
USER $NB_UID

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/