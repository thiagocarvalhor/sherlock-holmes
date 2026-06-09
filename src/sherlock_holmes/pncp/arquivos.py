"""Compatibility wrapper for outbound PNCP document-reference helpers."""

from sherlock_holmes.adapters.outbound.pncp.arquivos import (
    USER_AGENT,
    PncpDocumentReference,
    PncpDownloadedDocument,
    contract_file_references,
    document_reference_from_pncp_file,
    document_references_from_pncp_files,
    download_document_reference,
    procurement_file_references,
    safe_document_filename,
)

__all__ = [
    "USER_AGENT",
    "PncpDocumentReference",
    "PncpDownloadedDocument",
    "contract_file_references",
    "document_reference_from_pncp_file",
    "document_references_from_pncp_files",
    "download_document_reference",
    "procurement_file_references",
    "safe_document_filename",
]
