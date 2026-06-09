"""Protocols for dependencies required by application use cases."""

from sherlock_holmes.application.ports.cnpj_enrichment_gateway import (
    CnpjEnrichmentGateway,
    CnpjEnrichmentRecord,
)
from sherlock_holmes.application.ports.document_gateway import DocumentGateway, DocumentListResult
from sherlock_holmes.application.ports.pncp_contract_gateway import (
    PncpContractGateway,
    PncpContractSearchResult,
)
from sherlock_holmes.application.ports.report_writer import ReportWriter
from sherlock_holmes.application.ports.review_status_store import ReviewStatusStore

__all__ = [
    "CnpjEnrichmentGateway",
    "CnpjEnrichmentRecord",
    "DocumentGateway",
    "DocumentListResult",
    "PncpContractGateway",
    "PncpContractSearchResult",
    "ReportWriter",
    "ReviewStatusStore",
]
