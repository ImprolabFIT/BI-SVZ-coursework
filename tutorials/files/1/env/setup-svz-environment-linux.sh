#!/bin/sh
ENV_NAME="mySvz" && 
SPEC_FILE="SVZ-spec-file-linux.txt"
PYPYLON_FILE="pypylon-1.4.0-cp37-cp37m-linux_x86_64.whl" && 
echo "Creating enviroment '$ENV_NAME' with packages specified in $SPEC_FILE" && 
echo "========================================================================"
conda create --name $ENV_NAME --file "$SPEC_FILE" && 
CONDA_PREFIX_FAKE=$(conda info --envs | grep "^$ENV_NAME" | grep -o '/.*') && 
echo "Packages specified in spec-file-linux.txt were successfully installed." && 
echo "Now downloading pypylon wheel from github and installing using pip" && 
echo "========================================================================"
wget "https://github.com/basler/pypylon/releases/download/1.4.0/$PYPYLON_FILE" && 
"$CONDA_PREFIX_FAKE"/bin/pip install "$PYPYLON_FILE" && 
rm -f "$PYPYLON_FILE" && 
echo "Pypylon was installed, now setting enviroment variables according manual https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#macos-and-linux" && 
echo "========================================================================" && 
cd $CONDA_PREFIX_FAKE && 
mkdir -p ./etc/conda/activate.d && 
mkdir -p ./etc/conda/deactivate.d && 
touch ./etc/conda/activate.d/env_vars.sh && 
touch ./etc/conda/deactivate.d/env_vars.sh && 
echo '
#!/bin/sh

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH":"$CONDA_PREFIX"/lib
' > ./etc/conda/activate.d/env_vars.sh && 
cd - &&  
echo "Environment was successfully installed. Type 'conda activate $ENV_NAME' to activate it" 
