## Setup virtual environment
	conda create -n aidiag python=3.7

## Activate environment before running any experiments
	conda activate aidiag

## and deactivate when finished
	conda deactivate

## Install pyaudio with anaconda
	conda install -c anaconda pyaudio -y

## Install other requirements
	pip install -r requirements.txt

## Install Jupyter Notebook kernel
	python -m ipykernel install --user --name="AI_Diagnostics"

Remember to always use this kernel to work with the project, otherwise your modules will not appear installed. Visit [virtual Environment Jupyter Notebook help](https://stackoverflow.com/questions/42449814/running-jupyter-notebook-in-a-virtualenv-installed-sklearn-module-not-available) to solve similar issues.
