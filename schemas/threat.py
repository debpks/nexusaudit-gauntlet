from pydantic import BaseModel, Field

class ThreatHypothesisSchema(BaseModel):
    hypothesis: str = Field(
        ...,
        description="A specific hypothesis explaining how the system's compliance claim could be false or bypassed in practice (e.g. how an exempt system might perform profiling or ranking, or how a high-risk system might violate safety/fundamental rights guidelines)."
    )
    target_clause: str = Field(
        ...,
        description="The specific Annex III category or Article 6(3) exemption condition targeted by this hypothesis."
    )
    test_strategy: str = Field(
        ...,
        description="Detailed description of the concrete scenario or inputs that a red-team simulator should use to test and prove/disprove this hypothesis."
    )
