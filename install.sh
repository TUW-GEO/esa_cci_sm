#!/bin/bash

###
### How to use the installation script
#
# - Install miniconda, then install this package
# $ bash install.sh miniconda $HOME/miniconda
# OR ###
# - Only install this package, needs conda installed.
# $ bash install.sh --python 3.6 --name my_env_name
###

function install_conda()
  {
  local __conda_root=$1

  wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh;
  bash  /tmp/miniconda.sh -b -p $__conda_root/miniconda;
  export PATH="$__conda_root/miniconda/bin:$PATH";
  conda config --set always_yes yes
  conda update -q conda;
  conda info;
  source $conda_root/miniconda/etc/profile.d/conda.sh
  }

function setup()
 {
  local __py_vers=$1
  local __name=$2
  local __develop=$3


  conda create -n $__name python=$__py_vers
  conda activate $__name
  conda env update -f environment.yml -n $__name

  if [[ $__develop -eq 0 ]]; then
    echo "Installing package..."
    python setup.py install
  else
    echo "Installing package in development mode..."
    python setup.py develop
  fi;

 conda config --set always_yes no

 }

function install()
  {
  local __name=$NAME
  local __py=$PYTHON
  local __develop=$DEVELOP
  local __croot=$CONDA_ROOT

  if [[ $__croot -eq 0 ]]; then
    echo "Skip conda installation."
    conda_base=$(conda info --base)
    source $conda_base/etc/profile.d/conda.sh
  else
    echo "Download and install conda..."
    install_conda $__croot;
  fi;

  echo "Setup environment $__name ..."
  setup $__py $__name $__develop
  }

#===============================================================================

# default
DEVELOP=1
NAME="esa_cci_sm"
PYTHON="3.6"
CONDA_ROOT=0
_help=0

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -d|--develop) #switch
        DEVELOP=1
        shift # Remove --develop from processing
        ;;
        -n|--name) # kwarg
        NAME="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        -p|--python) # kwarg
        PYTHON="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        -r|--conda_root) # kwarg
        CONDA_ROOT="$2"
        shift # Remove argument name from processing
        shift # Remove argument value from processing
        ;;
        -h|--help)
        _help=1
        shift
        echo "Usage: bash install.sh [OPTION] "
        echo "Setup environment for developing this package. "
        echo "Optional arguments/flags to pass to >> $ bash install.sh "
        echo "-d, --develop      Install package in development mode (default: True) "
        echo "-n, --name         Name of the environment to install, (default: $NAME)"
        echo "-p, --python       Python version to install together with other dependencies (default: $PYTHON) "
        echo "-r, --conda_root   Also download and install conda. This is the root directly where conda will be installed. "
        echo "                   Skip this to not install conda. (default: False = Do not download/install)."
        echo "-h, --help         Show this help message."
    esac
done

if [[ $_help -eq 0 ]]; then
  install $NAME $PYTHON $DEVELOP $CONDA_ROOT;
  if [[ $CONDA_ROOT -ne 0 ]]; then
    echo " "
    echo "Installed conda in $CONDA_ROOT"
    echo " "
    echo "!!Don't forget to add conda to your .bashrc file!!"
    echo "=================================================="
  fi
  echo " "
  echo "Installation complete."
  echo " "
  echo "#"
  echo "# To activate this environment, use"
  echo "#"
  echo "#   $ conda activate $NAME"
  echo "#"
  echo "# To deactivate an active environment, use"
  echo "#"
  echo "#   $ conda deactivate $NAME"
  echo " "
fi

