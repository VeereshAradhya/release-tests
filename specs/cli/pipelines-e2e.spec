# Verify Pipeline cli e2e

Pre condition:
  * tkn should be installed
  * Operator should be installed

## Run sample pipeline cli
Tags: e2e, integration, pipelines, cli

Steps:
    * tkn delete resource type "pr" resource name "" with extra params "--all" and expect "Success"
    * tkn delete resource type "tr" resource name "" with extra params "--all" and expect "Success"