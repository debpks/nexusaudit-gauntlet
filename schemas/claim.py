from typing import Optional, Literal
from pydantic import BaseModel, Field

class ClaimSchema(BaseModel):
    annex_iii_category: Optional[str] = Field(
        None,
        description="The matching Annex III high-risk category name (e.g., '4. Employment, Workers Management and Access to Self-Employment') if applicable, or null if the system is completely outside Annex III scope."
    )
    claimed_status: Literal["high_risk", "exempt", "ambiguous"] = Field(
        ...,
        description="The classification status: 'high_risk' if it falls under Annex III and has no valid Article 6(3) exemption; 'exempt' if it either falls under Annex III but meets an Article 6(3) exemption, or if it is outside the scope of Annex III high-risk categories entirely; 'ambiguous' if the status is not clearly high_risk or exempt."
    )
    exemption_basis: Optional[str] = Field(
        None,
        description="Detailed explanation of the classification decision. If exempt, explain which Article 6(3) condition (a, b, c, d) applies and why. If high-risk, explain the lack of exemption or if the overriding exception of profiling of natural persons applies."
    )
    confidence: float = Field(
        ...,
        description="Confidence score for this classification, a float value between 0.0 and 1.0."
    )
