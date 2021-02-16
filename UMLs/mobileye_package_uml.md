
## Package Diagram
```plantuml

package Model{
    package Frames{
    }
}
package View{
    class ViewObserver{}
}

package TechsCodes{
    package RunAttention{}
     package TflSelection{}
   package SFM{}
}

package IntegrationEntities{
    package Management{
    class Controller{}
    class TflManager{}
    }
    package Flow{
        class CandidatesDetector{}
        class CandidatesFilter{}
        class DistanceEstimator{}
    }
}
IntegrationEntities -.-left-> View
IntegrationEntities -.-left-> Model
Flow -.-up--> TechsCodes
TflManager -.-left->Flow
```