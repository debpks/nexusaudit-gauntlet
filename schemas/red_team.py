from pydantic import BaseModel, Field

class RedTeamScenarioSchema(BaseModel):
    scenario_description: str = Field(
        ...,
        description="A concrete, detailed description of an adversarial test case, input data, or scenario designed to test the threat hypothesis. Must specify exact inputs, settings, or conditions to be simulated."
    )
    expected_violation: str = Field(
        ...,
        description="A description of the specific compliance violation, bias, or deviation from the EU AI Act that this test case is expected to trigger."
    )
