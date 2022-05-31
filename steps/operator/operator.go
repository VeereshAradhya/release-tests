package olm

import (
	"fmt"
	"log"

	"github.com/getgauge-contrib/gauge-go/gauge"
	"github.com/openshift-pipelines/release-tests/pkg/cmd"
	"github.com/openshift-pipelines/release-tests/pkg/operator"
	"github.com/openshift-pipelines/release-tests/pkg/store"
	"github.com/openshift-pipelines/release-tests/pkg/oc"
)

var _ = gauge.Step("Update TektonConfig CR to use param with name createRbacResource and value <value> to <action> auto creation of RBAC resources", func(value, action string) {
	patchData := fmt.Sprintf("{\"spec\":{\"params\":[{\"name\":\"createRbacResource\",\"value\":\"%s\"}]}}", value)
	fmt.Println(action, "auto creation of RBAC resources")
	log.Printf("output: %s\n", cmd.MustSucceed("oc", "patch", "TektonConfig", "config", "--type=merge", "-p", patchData).Stdout())
})

var _ = gauge.Step("Verify RBAC resources disabled successfully", func() {
	operator.ValidateRBACAfterDisable(store.Clients(), store.GetCRNames())
})

var _ = gauge.Step("Verify RBAC resources are auto created successfully", func() {
	operator.ValidateRBAC(store.Clients(), store.GetCRNames())
})

var _ = gauge.Step("Update addon config param <paramName> with value <paramValue> and expect message <expectedMessage>", func(paramName, paramValue, expectedMessage string){
	patchData := fmt.Sprintf("{\"spec\":{\"addon\":{\"params\":[{\"name\":\"%s\",\"value\":\"%s\"}]}}}", paramName, paramValue)
	if expectedMessage == "" {
		oc.UpdateTektonConfig(patchData)
	} else {
		oc.UpdateTektonConfigwithInvalidData(patchData, expectedMessage)
	}
})
