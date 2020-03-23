# Verify Pipelines

Pre condition:
  * Operator should be installed

## Create and run Pipeline using cli (without resources)
Tags: pipelines, e2e

Steps:
  * tkn create task "../../testdata/cli/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/cli/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start "pipeline-test"
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * tkn taskrun list
  * Verify the status of taskrun "running"
  * Wait for the pipelinerun to complete
  * Verify the pipelinerun status "successfull"


## Create and run Pipeline using cli (with resources) (manual)
Tags: pipelines, e2e

Steps:
  * tkn resource create "../../testdata/cli/git-resource.yaml"
  * oc apply "../../testdata/cli/resource-condition.yaml"
  * tkn create task "../../testdata/cli/resource-task.yaml"
  * tkn pipeline create "../../testdata/cli/pipeline-condition.yaml"
  * Start the pipeline manually by selecting the resource manually
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * Wait for pipelinerun to complete 
  * Verify the pipelinerun status "successfull"


## Create and run Pipeline using cli (with resources) (Automated)
Tags: pipelines, e2e

Steps:
  * tkn resource create "../../testdata/cli/git-resource.yaml"
  * oc apply "../../testdata/cli/resource-condition.yaml"
  * tkn create task "../../testdata/cli/resource-task.yaml"
  * tkn pipeline create "../../testdata/cli/pipeline-condition.yaml"
  * tkn pipeline start "pipeline-to-list-files" "pipeline-git=ui-repo"
  * tkn list pipeline
  * Verify the status of pipeline "running"
  * Wait for pipelinerun to complete 
  * Verify the pipelinerun status "successfull"


## Check pipelinerun logs
Tags: Pipelines, e2e

Steps:
  * tkn create task "../../testdata/tasks/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/tasks/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * tkn taskrun list
  * Verify the status of taskrun "running"
  * Wait for the pipelinerun to complete
  * Verify the pipelinerun status "successfull"
  * Verif the pipeline logs


## Chek pipelinerun running logs
Tags: pipelines, e2e

Steps:
  * tkn create task "../../testdata/tasks/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/tasks/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start 
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * tkn taskrun list
  * Verify the status of taskrun "running"
  * Verify the pipeline running logs
  * Wait for the pipelinerun to complete
  * Verify the pipelinerun status "successfull"


## Delete pipelinerun
Tags: pipelines, e2e

Steps:
  * tkn create task "../../testdata/tasks/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/tasks/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * tkn taskrun list
  * Verify the status of taskrun "running"
  * Verify the pipeline running logs
  * Wait for the pipelinerun to complete
  * tkn pipelinerun delete
  * Verify pipelinerun is deleted
  * Verfiy all taskruns of pipelinerun is deleted


## Cancel pipelinerun
Tags: pipelines, e2e

Steps:
  * tkn create task "../../testdata/tasks/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/tasks/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start
  * tkn pipeline list
  * Verify the status of pipeline "running"
  * tkn pipelinerun cancel
  * Verify pipeline run status "Cancelled"
  * Verify the taskrun status "Cancelled"


## Describe pipeline
Tags: Pipelines, e2e

Steps:
  * tkn create task "../../testdata/tasks/shell-script-task.yaml"
  * Verify taks creation status "successfull"
  * tkn create task "../../testdata/tasks/python-script-task.yaml"
  * Verify task creation status "successfull"
  * tkn pipeline create "../../testdata/cli/pipeline-script.yaml"
  * tkn pipeline start
  * tkn pipeline describe 
  * Verify the taskrun description


