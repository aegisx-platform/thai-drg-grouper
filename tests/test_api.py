"""
API Tests for Thai DRG Grouper
Tests all FastAPI endpoints and functionality
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from thai_drg_grouper.api import create_api
from thai_drg_grouper.manager import ThaiDRGGrouperManager

# Test data path
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "versions")


@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    if not os.path.exists(DATA_PATH):
        pytest.skip("Test data not available")

    # Create manager and API app
    manager = ThaiDRGGrouperManager(DATA_PATH)
    app = create_api(manager)
    return TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints"""

    def test_read_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "Thai DRG Grouper" in data["name"]

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "versions_loaded" in data

    def test_list_versions(self, client):
        """Test GET /versions endpoint"""
        response = client.get("/versions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Check version structure
        version = data[0]
        assert "version" in version
        assert "name" in version
        assert "is_default" in version


class TestGroupEndpoints:
    """Test grouping endpoints"""

    def test_group_latest_simple(self, client):
        """Test POST /group with simple case"""
        response = client.post(
            "/group",
            json={
                "pdx": "J189",
                "age": 30,
                "sex": "M",
                "los": 5
            }
        )

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "drg" in data
        assert "rw" in data
        assert "adjrw" in data
        assert "mdc" in data
        assert "is_valid" in data
        assert data["is_valid"] is True
        assert data["mdc"] == "04"  # Respiratory

    def test_group_latest_with_complications(self, client):
        """Test POST /group with CC/MCC"""
        response = client.post(
            "/group",
            json={
                "pdx": "J189",
                "sdx": ["I10", "E119"],
                "age": 75,
                "sex": "M",
                "los": 10
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["pcl"] > 0  # Should have complexity level

    def test_group_latest_with_procedure(self, client):
        """Test POST /group with OR procedure"""
        response = client.post(
            "/group",
            json={
                "pdx": "S82201D",
                "sdx": ["I10"],
                "procedures": ["7936"],
                "age": 25,
                "sex": "M",
                "los": 7
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["is_surgical"] is True
        assert data["has_or_procedure"] is True

    def test_group_specific_version(self, client):
        """Test POST /group/{version}"""
        # First get available versions
        versions_response = client.get("/versions")
        versions = versions_response.json()

        if versions:
            version = versions[0]["version"]
            response = client.post(
                f"/group/{version}",
                json={
                    "pdx": "J189",
                    "age": 30,
                    "sex": "M",
                    "los": 5
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["is_valid"] is True
            assert data["version"] == version

    def test_group_invalid_version(self, client):
        """Test POST /group/{version} with invalid version"""
        response = client.post(
            "/group/99.99",
            json={
                "pdx": "J189",
                "age": 30,
                "sex": "M",
                "los": 5
            }
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_group_invalid_age(self, client):
        """Test POST /group with invalid age"""
        response = client.post(
            "/group",
            json={
                "pdx": "J189",
                "age": -1,
                "sex": "M",
                "los": 5
            }
        )

        # Should still return 200 but with invalid result
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["drg"] == "26539"  # Age error DRG

    def test_group_invalid_pdx(self, client):
        """Test POST /group with invalid PDx"""
        response = client.post(
            "/group",
            json={
                "pdx": "INVALID999",
                "age": 30,
                "sex": "M",
                "los": 5
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["drg"] == "26509"  # Invalid PDx DRG

    def test_group_missing_required_field(self, client):
        """Test POST /group with missing required field (pdx)"""
        response = client.post(
            "/group",
            json={
                "age": 30,
                "sex": "M",
                "los": 5
            }
        )

        # FastAPI should return 422 for validation error
        assert response.status_code == 422


class TestCompareEndpoint:
    """Test comparison endpoint"""

    def test_compare_versions(self, client):
        """Test POST /group/compare"""
        response = client.post(
            "/group/compare",
            json={
                "pdx": "J189",
                "age": 30,
                "sex": "M",
                "los": 5
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

        # Should have at least one version result
        assert len(data) > 0

        # Check structure of results
        for version, result in data.items():
            if result:  # May be None if grouping failed
                assert "drg" in result
                assert "rw" in result
                assert "is_valid" in result

    def test_compare_versions_complex(self, client):
        """Test POST /group/compare with complex case"""
        response = client.post(
            "/group/compare",
            json={
                "pdx": "S82201D",
                "sdx": ["I10", "E119"],
                "procedures": ["7936"],
                "age": 65,
                "sex": "M",
                "los": 10
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0


class TestBatchEndpoint:
    """Test batch processing endpoint"""

    def test_batch_group_simple(self, client):
        """Test POST /group/batch with simple cases"""
        response = client.post(
            "/group/batch",
            json={
                "cases": [
                    {
                        "pdx": "J189",
                        "age": 30,
                        "sex": "M",
                        "los": 5
                    },
                    {
                        "pdx": "S82201D",
                        "procedures": ["7936"],
                        "age": 25,
                        "sex": "M",
                        "los": 7
                    }
                ]
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 2

        # Check each result
        for result in data["results"]:
            assert "drg" in result
            assert "rw" in result
            assert "is_valid" in result

    def test_batch_group_with_version(self, client):
        """Test POST /group/batch with specific version"""
        # Get first available version
        versions_response = client.get("/versions")
        versions = versions_response.json()

        if versions:
            version = versions[0]["version"]
            response = client.post(
                "/group/batch",
                json={
                    "version": version,
                    "cases": [
                        {
                            "pdx": "J189",
                            "age": 30,
                            "sex": "M",
                            "los": 5
                        }
                    ]
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["results"]) == 1
            assert data["results"][0]["version"] == version

    def test_batch_group_empty(self, client):
        """Test POST /group/batch with empty cases"""
        response = client.post(
            "/group/batch",
            json={"cases": []}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 0

    def test_batch_group_mixed_valid_invalid(self, client):
        """Test POST /group/batch with mix of valid and invalid cases"""
        response = client.post(
            "/group/batch",
            json={
                "cases": [
                    {
                        "pdx": "J189",
                        "age": 30,
                        "sex": "M",
                        "los": 5
                    },
                    {
                        "pdx": "INVALID999",
                        "age": 30,
                        "sex": "M",
                        "los": 5
                    },
                    {
                        "pdx": "J189",
                        "age": -1,
                        "sex": "M",
                        "los": 5
                    }
                ]
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 3

        # First should be valid
        assert data["results"][0]["is_valid"] is True

        # Second and third should be invalid
        assert data["results"][1]["is_valid"] is False
        assert data["results"][2]["is_valid"] is False


class TestAPIValidation:
    """Test API input validation"""

    def test_group_invalid_json(self, client):
        """Test POST /group with invalid JSON"""
        response = client.post(
            "/group",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422

    def test_group_invalid_data_types(self, client):
        """Test POST /group with wrong data types"""
        response = client.post(
            "/group",
            json={
                "pdx": "J189",
                "age": "not a number",  # Should be int
                "sex": "M",
                "los": 5
            }
        )

        assert response.status_code == 422

    def test_group_extra_fields_ignored(self, client):
        """Test POST /group with extra fields (should be ignored)"""
        response = client.post(
            "/group",
            json={
                "pdx": "J189",
                "age": 30,
                "sex": "M",
                "los": 5,
                "extra_field": "should be ignored"
            }
        )

        # Should succeed, extra fields are typically ignored
        assert response.status_code == 200


class TestAPICORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options(
            "/group",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )

        # CORS should allow requests
        assert response.status_code in [200, 204]


class TestAPIDocumentation:
    """Test API documentation endpoints"""

    def test_openapi_schema(self, client):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()

        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

        # Check that our endpoints are documented
        assert "/group" in schema["paths"]
        assert "/versions" in schema["paths"]

    def test_docs_endpoint(self, client):
        """Test Swagger UI endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_redoc_endpoint(self, client):
        """Test ReDoc endpoint"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "redoc" in response.text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
