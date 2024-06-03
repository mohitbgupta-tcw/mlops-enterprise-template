
# Import required modules
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
import os, json

# Set Azure ML workspace information
subscription_id = '9e6414f9-fa32-459d-87f7-26856c9ebc31' 
resource_group  = 'AZ-RG-ML-SHARED-DEV-002'
workspace_name  = 'demoAzMLWorkspace'
workspace_region = 'westus2'

# Create Azure ML workspace if it does not exist
ws = Workspace.create(name = workspace_name,
             subscription_id = subscription_id,
             resource_group = resource_group, 
             location = workspace_region,
             exist_ok = True
             )

# Load specific run configuration file
run_config = RunConfiguration.load("run_config.yml")



# Get the default datastore
data_store = ws.get_default_datastore()

# Define input and output data paths
input_data = data_store.path("path_to_input_data").as_mount()
output_data = data_store.path("path_to_output_data").as_mount()

# Define PythonScriptStep
'''
step = PythonScriptStep(script_name = "script_name.py",
                        arguments =["--input_data", input_data,
                                    "--output_data", output_data],
                        inputs=[input_data],
                        outputs=[output_data],
                        source_directory = "source_directory_path",
                        compute_target = "compute-target-name",
                        runconfig = run_config                        
                        )

'''
source_directory = './train'
step = PythonScriptStep(name="train_step",
                         script_name="train.py", 
                         compute_target="igniteCluster", 
                         source_directory=source_directory,
                         runconfig = run_config,
                         allow_reuse=True)

# Create Azure ML pipeline
pipeline = Pipeline(workspace=ws, steps=[step])

# Submit the pipeline
pipeline_run = pipeline.submit("pipeline_name")

# Set tags for the pipeline run
pipeline_run.set_tags({"Key": "Value"})

# Wait for the pipeline run to complete
pipeline_run.wait_for_completion()
