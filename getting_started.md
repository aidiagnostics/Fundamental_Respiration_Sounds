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
	ipython kernel install --user --name="AI_Diagnostics"
	
## 
