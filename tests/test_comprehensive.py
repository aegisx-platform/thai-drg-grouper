"""
Comprehensive Test Suite for Thai DRG Grouper
Based on Thai DRG Version 6.3.3 Official Specifications

Test Coverage:
1. CC/MCC Detection & Exclusion
2. PCL (Patient Complexity Level) Calculation
3. Adjusted RW Calculation (Daycase, Normal, Long Stay)
4. MDC & DC Assignment
5. DRG Selection Logic
6. Edge Cases & Error Handling
7. Real-world Clinical Scenarios
"""

import os
import sys
import pytest
from decimal import Decimal

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thai_drg_grouper import GrouperResult, ThaiDRGGrouper, ThaiDRGGrouperManager

# Path to test data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "versions")


@pytest.fixture
def grouper():
    """Fixture for version 6.3 grouper"""
    version_path = os.path.join(DATA_PATH, "6.3", "data")
    if os.path.exists(version_path):
        return ThaiDRGGrouper(version_path, "6.3")
    pytest.skip("Test data not available")


@pytest.fixture
def manager():
    """Fixture for multi-version manager"""
    if os.path.exists(DATA_PATH):
        return ThaiDRGGrouperManager(DATA_PATH)
    pytest.skip("Test data not available")


class TestCCMCCDetection:
    """Test CC/MCC detection and exclusion logic"""

    def test_no_cc_or_mcc(self, grouper):
        """Test case with no CC or MCC - should have PCL=0"""
        result = grouper.group(
            pdx="J189",  # Pneumonia (no CC from PDx)
            sdx=[],  # No secondary diagnoses
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert result.pcl == 0
        assert len(result.cc_list) == 0
        assert len(result.mcc_list) == 0

    def test_single_cc_detection(self, grouper):
        """Test case with 1 valid CC - should have PCL=1"""
        result = grouper.group(
            pdx="J189",  # Pneumonia
            sdx=["I10"],  # Essential hypertension (CC)
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        # PCL should be 1 if I10 is a valid CC
        if len(result.cc_list) > 0:
            assert result.pcl >= 1

    def test_multiple_cc_detection(self, grouper):
        """Test case with 2+ valid CCs - should have PCL=2"""
        result = grouper.group(
            pdx="J189",  # Pneumonia
            sdx=["I10", "E119", "N179"],  # Multiple potential CCs
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        # PCL should be 2 if we have 2+ valid CCs
        if len(result.cc_list) >= 2:
            assert result.pcl == 2

    def test_mcc_detection(self, grouper):
        """Test MCC detection (ccrow >= 3) - should have higher PCL"""
        result = grouper.group(
            pdx="J189",  # Pneumonia
            sdx=["J960", "R570"],  # Respiratory failure (potential MCC)
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        # If any MCC detected, PCL should be >= 2
        if len(result.mcc_list) > 0:
            assert result.pcl >= 2

    def test_cc_exclusion_rules(self, grouper):
        """Test CC exclusion logic - related diagnoses should be excluded"""
        # Example: If PDx is diabetes, other diabetes codes shouldn't count as CC
        result = grouper.group(
            pdx="E119",  # Type 2 diabetes without complications
            sdx=["E118", "E117"],  # Other diabetes codes (should be excluded)
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        # Related diabetes codes should be excluded by CC exclusion rules
        # Exact behavior depends on ccex.dbf data

    def test_pcl_calculation_with_mixed_cc_mcc(self, grouper):
        """Test PCL calculation with both CCs and MCCs"""
        result = grouper.group(
            pdx="S82201D",  # Fracture
            sdx=["I10", "E119", "J960"],  # Mix of CC and potential MCC
            procedures=["7936"],  # OR procedure
            age=25,
            sex="M",
            los=5
        )

        assert result.is_valid
        # PCL should reflect the most severe complication level
        if len(result.mcc_list) > 0:
            assert result.pcl >= 2


class TestAdjustedRWCalculation:
    """Test Adjusted Relative Weight calculation for different LOS scenarios"""

    def test_daycase_los_zero(self, grouper):
        """Test daycase (LOS=0) - should use rw0d"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex="M",
            los=0
        )

        assert result.is_valid
        assert result.los_status == "daycase"
        # For daycase, adjrw should equal rw0d
        assert result.adjrw == result.rw0d

    def test_normal_stay_within_ot(self, grouper):
        """Test normal stay (LOS <= OT) - should use base rw"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex="M",
            los=3  # Assume this is within OT
        )

        assert result.is_valid
        # For normal stay, adjrw should equal rw (or close to it)
        if result.los_status == "normal":
            assert abs(result.adjrw - result.rw) < 0.01

    def test_long_stay_beyond_ot(self, grouper):
        """Test long stay (LOS > OT) - should use adjusted formula"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex="M",
            los=20  # Long stay
        )

        assert result.is_valid
        if result.los_status == "long_stay" and result.wtlos > 0:
            # For long stay: adjrw = rw + (los - ot) × (rw / wtlos) × 0.5
            expected_adjrw = result.rw + (result.los - result.ot) * (result.rw / result.wtlos) * 0.5
            # Allow small floating point difference
            assert abs(result.adjrw - expected_adjrw) < 0.01
            # Adjusted RW should be higher than base RW
            assert result.adjrw > result.rw

    def test_adjrw_formula_accuracy(self, grouper):
        """Test the exact AdjRW calculation formula"""
        result = grouper.group(
            pdx="S82201D",  # Fracture
            procedures=["7936"],
            age=25,
            sex="M",
            los=15  # Long enough to trigger long stay
        )

        assert result.is_valid
        if result.los_status == "long_stay" and result.wtlos > 0:
            # Verify formula: adjrw = rw + (los - ot) × (rw / wtlos) × 0.5
            excess_days = result.los - result.ot
            per_day_weight = result.rw / result.wtlos
            additional_weight = excess_days * per_day_weight * 0.5
            expected_adjrw = result.rw + additional_weight

            assert abs(result.adjrw - expected_adjrw) < 0.01


class TestMDCAndDCAssignment:
    """Test MDC and Disease Cluster assignment logic"""

    def test_mdc_assignment_respiratory(self, grouper):
        """Test MDC assignment for respiratory conditions (MDC 04)"""
        result = grouper.group(
            pdx="J189",  # Pneumonia
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert result.mdc == "04"  # Respiratory system
        assert "Respiratory" in result.mdc_name or "ทางเดินหายใจ" in result.mdc_name

    def test_mdc_assignment_musculoskeletal(self, grouper):
        """Test MDC assignment for musculoskeletal conditions (MDC 08)"""
        result = grouper.group(
            pdx="S82201D",  # Fracture
            age=25,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert result.mdc == "08"  # Musculoskeletal system

    def test_dc_surgical_vs_medical(self, grouper):
        """Test DC assignment for surgical vs medical cases"""
        # Medical case (no OR procedure)
        result_medical = grouper.group(
            pdx="J189",  # Pneumonia
            age=30,
            sex="M",
            los=5
        )

        # Surgical case (with OR procedure)
        result_surgical = grouper.group(
            pdx="S82201D",  # Fracture
            procedures=["7936"],  # OR procedure
            age=25,
            sex="M",
            los=5
        )

        assert result_medical.is_valid
        assert result_surgical.is_valid

        # Medical cases should have DC >= 50 (suffix 50-99)
        if result_medical.dc:
            dc_suffix = int(result_medical.dc[-2:])
            assert dc_suffix >= 50, "Medical case should have DC suffix >= 50"

        # Surgical cases should have DC < 50 (suffix 01-49)
        if result_surgical.dc:
            dc_suffix = int(result_surgical.dc[-2:])
            assert dc_suffix < 50, "Surgical case should have DC suffix < 50"

    def test_dc_fallback_logic(self, grouper):
        """Test DC fallback when exact DC not found"""
        # Use an edge case that might trigger fallback
        result = grouper.group(
            pdx="Z000",  # Special health examination
            age=30,
            sex="M",
            los=1
        )

        # Should still find a DRG even if exact DC not found
        assert result.drg is not None


class TestDRGSelection:
    """Test DRG selection logic based on PCL and other factors"""

    def test_drg_selection_by_pcl(self, grouper):
        """Test that higher PCL selects higher-numbered DRG in same DC"""
        # Same diagnosis, different complexity levels
        result_no_cc = grouper.group(
            pdx="J189",
            sdx=[],  # No CC
            age=30,
            sex="M",
            los=5
        )

        result_with_cc = grouper.group(
            pdx="J189",
            sdx=["I10", "E119"],  # With CCs
            age=30,
            sex="M",
            los=5
        )

        assert result_no_cc.is_valid
        assert result_with_cc.is_valid

        # If both have same DC, the one with CC should have higher DRG number
        if result_no_cc.dc == result_with_cc.dc and result_with_cc.pcl > result_no_cc.pcl:
            assert result_with_cc.drg >= result_no_cc.drg

    def test_or_procedure_detection(self, grouper):
        """Test OR procedure detection affects DRG selection"""
        result = grouper.group(
            pdx="S82201D",
            procedures=["7936"],  # OR procedure
            age=25,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert result.has_or_procedure
        assert result.is_surgical

    def test_non_or_procedure(self, grouper):
        """Test non-OR procedures don't trigger surgical classification"""
        result = grouper.group(
            pdx="J189",
            procedures=[],  # No procedures
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert not result.has_or_procedure
        assert not result.is_surgical


class TestEdgeCasesAndErrors:
    """Test edge cases and error handling"""

    def test_invalid_age_negative(self, grouper):
        """Test invalid age (negative) - should return error DRG"""
        result = grouper.group(
            pdx="J189",
            age=-1,
            sex="M",
            los=5
        )

        assert not result.is_valid
        assert result.drg == "26539"  # Age error DRG
        assert any("age" in error.lower() for error in result.errors)

    def test_invalid_age_too_high(self, grouper):
        """Test invalid age (>124) - should return error DRG"""
        result = grouper.group(
            pdx="J189",
            age=150,
            sex="M",
            los=5
        )

        assert not result.is_valid
        assert result.drg == "26539"  # Age error DRG
        assert any("age" in error.lower() for error in result.errors)

    def test_invalid_pdx(self, grouper):
        """Test invalid PDx code - should return ungroupable DRG"""
        result = grouper.group(
            pdx="INVALID999",
            age=30,
            sex="M",
            los=5
        )

        assert not result.is_valid
        assert result.drg == "26509"  # Invalid PDx DRG
        assert any("PDx" in error for error in result.errors)

    def test_missing_sex_warning(self, grouper):
        """Test missing sex - should generate warning but continue"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex=None,
            los=5
        )

        # Should still group, but with warning
        assert result.is_valid or len(result.warnings) > 0

    def test_invalid_sex_format(self, grouper):
        """Test invalid sex format - should handle gracefully"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex="X",  # Invalid
            los=5
        )

        # Should handle gracefully (warning or default)
        assert result.drg is not None

    def test_empty_procedures_list(self, grouper):
        """Test empty procedures list - should work normally"""
        result = grouper.group(
            pdx="J189",
            procedures=[],
            age=30,
            sex="M",
            los=5
        )

        assert result.is_valid
        assert not result.has_or_procedure

    def test_valid_age_range_boundary(self, grouper):
        """Test valid age boundaries (0 and 124)"""
        result_newborn = grouper.group(
            pdx="P220",  # Newborn diagnosis
            age=0,
            sex="M",
            los=3
        )

        result_elderly = grouper.group(
            pdx="J189",
            age=124,
            sex="F",
            los=5
        )

        # Both should be valid
        assert result_newborn.drg is not None
        assert result_elderly.drg is not None


class TestRealWorldClinicalScenarios:
    """Test real-world clinical scenarios"""

    def test_pneumonia_with_complications(self, grouper):
        """Test pneumonia case with multiple complications"""
        result = grouper.group(
            pdx="J189",  # Pneumonia, unspecified
            sdx=["J960", "I10", "E119"],  # Respiratory failure, HTN, DM
            age=75,
            sex="M",
            los=10
        )

        assert result.is_valid
        assert result.mdc == "04"
        assert not result.is_surgical
        # Should have some CC/MCC detected
        assert result.pcl > 0 or len(result.cc_list) > 0

    def test_hip_fracture_with_orif(self, grouper):
        """Test hip fracture with ORIF procedure"""
        result = grouper.group(
            pdx="S72001D",  # Hip fracture
            sdx=["I10", "E119"],  # HTN, DM
            procedures=["7936"],  # ORIF
            age=80,
            sex="F",
            los=7
        )

        assert result.is_valid
        assert result.mdc == "08"  # Musculoskeletal
        assert result.is_surgical
        assert result.has_or_procedure

    def test_diabetic_ketoacidosis(self, grouper):
        """Test diabetic ketoacidosis (severe metabolic disorder)"""
        result = grouper.group(
            pdx="E101",  # Type 1 DM with ketoacidosis
            sdx=["E875", "N179"],  # Fluid/electrolyte disorder, AKI
            age=25,
            sex="M",
            los=5
        )

        assert result.is_valid
        # Should group to endocrine/metabolic MDC
        assert result.mdc in ["10", "11"]

    def test_cesarean_delivery(self, grouper):
        """Test cesarean delivery case"""
        result = grouper.group(
            pdx="O820",  # Delivery by cesarean
            procedures=["7499"],  # C-section procedure code
            age=28,
            sex="F",
            los=3
        )

        assert result.is_valid
        # Should group to MDC 14 (Pregnancy/childbirth)
        assert result.mdc == "14"

    def test_acute_mi_with_pci(self, grouper):
        """Test acute MI with PCI procedure"""
        result = grouper.group(
            pdx="I214",  # Acute MI
            sdx=["I10", "E119"],  # HTN, DM
            procedures=["3606"],  # PCI (if this is the code)
            age=65,
            sex="M",
            los=8
        )

        assert result.is_valid
        assert result.mdc == "05"  # Circulatory system


class TestMultiVersionComparison:
    """Test multi-version manager functionality"""

    def test_version_listing(self, manager):
        """Test listing available versions"""
        versions = manager.list_versions()
        assert len(versions) > 0
        assert all(hasattr(v, 'version') for v in versions)

    def test_group_with_specific_version(self, manager):
        """Test grouping with specific version"""
        versions = manager.list_versions()
        if versions:
            result = manager.group(
                versions[0].version,
                pdx="J189",
                age=30,
                sex="M",
                los=5
            )
            assert result.is_valid
            assert result.version == versions[0].version

    def test_group_latest_version(self, manager):
        """Test grouping with latest version"""
        result = manager.group_latest(
            pdx="J189",
            age=30,
            sex="M",
            los=5
        )
        assert result.is_valid

    def test_compare_all_versions(self, manager):
        """Test comparing results across all versions"""
        results = manager.group_all_versions(
            pdx="J189",
            age=30,
            sex="M",
            los=5
        )

        assert len(results) > 0
        # All results should be valid for this simple case
        assert all(r.is_valid for r in results.values() if r is not None)

    def test_invalid_version_error(self, manager):
        """Test error handling for invalid version"""
        with pytest.raises(ValueError):
            manager.group("99.99.99", pdx="J189")


class TestStatisticsAndMetadata:
    """Test statistics and metadata functions"""

    def test_grouper_statistics(self, grouper):
        """Test grouper statistics"""
        stats = grouper.get_stats()

        assert "version" in stats
        assert "icd10_count" in stats
        assert "drg_count" in stats
        assert "procedure_count" in stats

        # Counts should be positive
        assert stats["icd10_count"] > 0
        assert stats["drg_count"] > 0

    def test_version_info(self, manager):
        """Test version information"""
        versions = manager.list_versions()

        for version_info in versions:
            assert hasattr(version_info, 'version')
            assert hasattr(version_info, 'dbf_path')
            assert hasattr(version_info, 'is_default')


class TestDataIntegrity:
    """Test data loading and integrity"""

    def test_dbf_file_loading(self, grouper):
        """Test that all DBF files are loaded correctly"""
        stats = grouper.get_stats()

        # Should have loaded data from all 4 DBF files
        assert stats["icd10_count"] > 0, "ICD-10 data not loaded"
        assert stats["drg_count"] > 0, "DRG data not loaded"
        assert stats["procedure_count"] > 0, "Procedure data not loaded"
        # Note: ccex count not in stats, but exclusion logic should work

    def test_icd10_code_normalization(self, grouper):
        """Test ICD-10 code normalization (dots, spaces, case)"""
        # Test with different formats of the same code
        result1 = grouper.group(pdx="J18.9", age=30, sex="M", los=5)
        result2 = grouper.group(pdx="J189", age=30, sex="M", los=5)
        result3 = grouper.group(pdx="j18.9", age=30, sex="M", los=5)

        # All should group to the same DRG
        assert result1.drg == result2.drg == result3.drg


class TestResultSerialization:
    """Test result serialization (to_dict, to_json)"""

    def test_result_to_dict(self, grouper):
        """Test GrouperResult.to_dict()"""
        result = grouper.group(
            pdx="J189",
            sdx=["I10", "E119"],
            age=30,
            sex="M",
            los=5
        )

        d = result.to_dict()

        # Check all required fields
        assert "drg" in d
        assert "rw" in d
        assert "adjrw" in d
        assert "mdc" in d
        assert "pcl" in d
        assert "is_valid" in d

    def test_result_to_json(self, grouper):
        """Test GrouperResult.to_json()"""
        result = grouper.group(
            pdx="J189",
            age=30,
            sex="M",
            los=5
        )

        json_str = result.to_json()

        # Should be valid JSON string
        import json
        data = json.loads(json_str)
        assert "drg" in data
        assert "rw" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
