"""Outbound PNCP adapter package."""

from sherlock_holmes.adapters.outbound.pncp.contract_gateway import PncpContractSearchGateway
from sherlock_holmes.adapters.outbound.pncp.document_gateway import PncpDocumentGateway

__all__ = ["PncpContractSearchGateway", "PncpDocumentGateway"]
