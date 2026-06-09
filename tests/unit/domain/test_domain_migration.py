"""Regression tests for the incremental domain migration."""

from sherlock_holmes.domain.entities import EvidenceRecord as DomainEvidenceRecord
from sherlock_holmes.domain.entities import FieldComparison as DomainFieldComparison
from sherlock_holmes.domain.entities import RecordComparison as DomainRecordComparison
from sherlock_holmes.domain.entities import compare_records as domain_compare_records
from sherlock_holmes.domain.entities import evidence_from_official_api as domain_evidence_from_official_api
from sherlock_holmes.validation import EvidenceRecord as LegacyEvidenceRecord
from sherlock_holmes.validation import FieldComparison as LegacyFieldComparison
from sherlock_holmes.validation import RecordComparison as LegacyRecordComparison
from sherlock_holmes.validation import compare_records as legacy_compare_records
from sherlock_holmes.validation import evidence_from_official_api as legacy_evidence_from_official_api


def test_validation_exports_domain_models():
    assert LegacyEvidenceRecord is DomainEvidenceRecord
    assert LegacyFieldComparison is DomainFieldComparison
    assert LegacyRecordComparison is DomainRecordComparison
    assert legacy_compare_records is domain_compare_records
    assert legacy_evidence_from_official_api is domain_evidence_from_official_api
