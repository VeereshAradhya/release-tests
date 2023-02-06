package utility

import (
	"log"
	"strconv"
	"time"

	"github.com/getgauge-contrib/gauge-go/gauge"
	"github.com/getgauge-contrib/gauge-go/testsuit"
	"github.com/openshift-pipelines/release-tests/pkg/store"
)

var _ = gauge.Step("Sleep for <numberOfSeconds> seconds", func(numberOfSeconds string) {
	log.Printf("Sleeping for %v seconds", numberOfSeconds)
	numberOfSecondsInt, _ := strconv.Atoi(numberOfSeconds)
	time.Sleep(time.Duration(numberOfSecondsInt) * time.Second)
})

var _ = gauge.Step("Assert if values stored in variable <variable1> and variable <variable2> are <equality>", func(variable1, variable2, equality string) {
	log.Printf("Verifying if values stored in %v and %v are %v", variable1, variable2, equality)
	if equality == "equal" {
		if store.GetScenarioData(variable1) == store.GetScenarioData(variable2) {
			log.Printf("The variable %v and %v contains the value %v", variable1, variable2, store.GetScenarioData(variable1))
		} else {
			testsuit.T.Errorf("The variable %v contains %v and the variable %v contains %v", variable1, store.GetScenarioData(variable1), variable2, store.GetScenarioData(variable2))
		}
	} else {
		if store.GetScenarioData(variable1) != store.GetScenarioData(variable2) {
			log.Printf("The variable %v contains %v and the variable %v contains %v", variable1, store.GetScenarioData(variable1), variable2, store.GetScenarioData(variable2))
		} else {
			testsuit.T.Errorf("The variable %v and %v contains the value %v", variable1, variable2, store.GetScenarioData(variable1))
		}
	}
})

var _ = gauge.Step("Switch to project <projectName>", func(projectName string) {
	store.Clients().NewClients(projectName)
	gauge.GetScenarioStore()["namespace"] = projectName
})
