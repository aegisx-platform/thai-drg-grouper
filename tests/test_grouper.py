"""
Tests for Thai DRG Grouper
"""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thai_drg_grouper import GrouperResult, ThaiDRGGrouper, ThaiDRGGrouperManager

# Path to test data
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "versions")


class TestGrouper:
    """Test single version grouper"""

    @pytest.fixture
    def grouper(self):
        version_path = os.path.join(DATA_PATH, "6.3", "data")
        if os.path.exists(version_path):
            return ThaiDRGGrouper(version_path, "6.3")
        pytest.skip("Test data not available")

    def test_group_fracture(self, grouper):
        """Test fracture case"""
        result = grouper.group(
            pdx="S82201D", sdx=["E119", "I10"], procedures=["7936"], age=25, sex="M", los=5
        )

        assert isinstance(result, GrouperResult)
        assert result.is_valid
        assert result.mdc == "08"
        assert result.drg.startswith("08")
        assert result.rw > 0

    def test_group_pneumonia(self, grouper):
        """Test pneumonia case"""
        result = grouper.group(pdx="J189", sdx=["E119"], los=7)

        assert result.is_valid
        assert result.mdc == "04"
        assert not result.is_surgical

    def test_invalid_pdx(self, grouper):
        """Test invalid PDx"""
        result = grouper.group(pdx="INVALID123")

        assert not result.is_valid
        assert result.drg == "26509"
        assert "Invalid PDx" in result.errors[0]

    def test_daycase(self, grouper):
        """Test day case (LOS=0)"""
        result = grouper.group(pdx="J189", los=0)

        assert result.los_status == "daycase"
        assert result.adjrw == result.rw0d

    def test_get_stats(self, grouper):
        """Test statistics"""
        stats = grouper.get_stats()

        assert "version" in stats
        assert stats["icd10_count"] > 0
        assert stats["drg_count"] > 0


class TestManager:
    """Test multi-version manager"""

    @pytest.fixture
    def manager(self):
        if os.path.exists(DATA_PATH):
            return ThaiDRGGrouperManager(DATA_PATH)
        pytest.skip("Test data not available")

    def test_list_versions(self, manager):
        """Test listing versions"""
        versions = manager.list_versions()
        assert len(versions) > 0

    def test_group_latest(self, manager):
        """Test grouping with latest version"""
        result = manager.group_latest(pdx="J189", los=5)
        assert result.is_valid

    def test_group_specific_version(self, manager):
        """Test grouping with specific version"""
        versions = manager.list_versions()
        if versions:
            result = manager.group(versions[0].version, pdx="J189", los=5)
            assert result.is_valid

    def test_invalid_version(self, manager):
        """Test invalid version"""
        with pytest.raises(ValueError):
            manager.group("99.99", pdx="J189")


class TestTypes:
    """Test type classes"""

    def test_grouper_result_to_dict(self):
        """Test GrouperResult.to_dict()"""
        result = GrouperResult(
            version="6.3",
            pdx="J189",
            sdx=[],
            procedures=[],
            age=30,
            sex="M",
            los=5,
            mdc="04",
            mdc_name="Test",
            dc="0450",
            drg="04509",
            drg_name="Test DRG",
            rw=1.0,
            rw0d=0.5,
            adjrw=1.0,
            wtlos=5.0,
            ot=10,
            pcl=0,
            cc_list=[],
            mcc_list=[],
            has_or_procedure=False,
            is_surgical=False,
            los_status="normal",
            is_valid=True,
            errors=[],
            warnings=[],
        )

        d = result.to_dict()
        assert d["drg"] == "04509"
        assert d["rw"] == 1.0

    def test_grouper_result_to_json(self):
        """Test GrouperResult.to_json()"""
        result = GrouperResult(
            version="6.3",
            pdx="J189",
            sdx=[],
            procedures=[],
            age=30,
            sex="M",
            los=5,
            mdc="04",
            mdc_name="Test",
            dc="0450",
            drg="04509",
            drg_name="Test DRG",
            rw=1.0,
            rw0d=0.5,
            adjrw=1.0,
            wtlos=5.0,
            ot=10,
            pcl=0,
            cc_list=[],
            mcc_list=[],
            has_or_procedure=False,
            is_surgical=False,
            los_status="normal",
            is_valid=True,
            errors=[],
            warnings=[],
        )

        json_str = result.to_json()
        assert '"drg": "04509"' in json_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
