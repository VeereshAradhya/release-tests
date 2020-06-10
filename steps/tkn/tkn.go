package tkn

import (
	"fmt"
	"github.com/getgauge-contrib/gauge-go/gauge"
	"github.com/getgauge-contrib/gauge-go/testsuit"
	"github.com/openshift-pipelines/release-tests/pkg/tkn"
	"gotest.tools/v3/icmd"
	"log"
	"os"
	"regexp"
	"strings"
)

var tknPath = os.Getenv("TKN_PATH")
var tknCli = tkn.New(tknPath)
var tknVersion = os.Getenv("TKN_VERSION")

var _ = gauge.Step("tkn should be installed", func() {

	if tknPath == "" {
		testsuit.T.Errorf(fmt.Sprintf("\"TKN_PATH\" is not specified in the \"test.properties\" file"))
	} else if tknVersion == "" {
		testsuit.T.Errorf(fmt.Sprintf("\"TKN_VERSION\" is not specified in the \"test.properties\" file"))

	}
	output := tknCli.MustSucceed("version")
	expression := "Client version: " + tknVersion
	matched, _ := regexp.MatchString(expression, output)

	if !matched {
		testsuit.T.Errorf(fmt.Sprintf("\"TKN_VERSION\" specified in the \"test.properties\" file is not matching with the installed tkn version"))
	}

})

var _ = gauge.Step("tkn delete resource type <resourceType> resource name <resourceName> with extra params <param> and expect <expected>", func(resourceType string, resourceName string, param string, expected string) {
	log.Printf("Deleting the resource type #{resourceType}")
	exp := icmd.Expected{}
	switch expected {
	case "Success":
		exp.ExitCode = 0
	case "Failure":
		exp.ExitCode = 1

	}
	if resourceName == ""{
		tknCli.Assert(exp, resourceType, "delete", param, "-f")
	} else {
		tknCli.Assert(exp, resourceType, resourceName, "delete", param, "-f")
	}
})

var _ = gauge.Step("tkn start <resource> <resourceName> and expect <expected>", func(resource string, resourceName string, expected string) {
	log.Printf("Starting %v resource %v", resource, resourceName)
	exp := icmd.Expected{}
	switch expected {
	case "Success":
		exp.ExitCode = 0
	case "Failure":
		exp.ExitCode = 1

	}
	tknCli.Assert(exp, resource, "start", resourceName)
})

var _ = gauge.Step("tkn verify logs for resource <resourceType> with <resourceName> with string <givenString>", func(resourceType string, resourceName string, givenString string) {
	output := tknCli.MustSucceed(resourceType, resourceType, "logs", resourceName, "-L")
	if strings.Contains(output, givenString) {
		log.Printf("Given string %v prsenet in %v %v logs", givenString, resourceType, resourceName)
	} else {
		testsuit.T.Errorf(fmt.Sprintf("Given string %v is not prsenet in %v %v logs", givenString, resourceType, resourceName))
	}
})
