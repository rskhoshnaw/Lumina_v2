import pytest
from unittest.mock import MagicMock, patch
from core.pipeline import LuminaPipeline

@patch("core.pipeline.GeminiProvider")
@patch("core.pipeline.ContentPlanner")
@patch("core.pipeline.CodeGenerator")
@patch("core.pipeline.ManimRenderer")
@patch("core.pipeline.validate_code")
def test_pipeline_success_flow(mock_validate, MockRenderer, MockGen, MockPlanner, MockProvider, tmp_path):
    """Test that the pipeline correctly calls all components in sequence."""
    # Mocking validation to pass
    mock_validate.return_value = (True, [])
    
    # Setup pipeline with mocked components
    pipeline = LuminaPipeline(api_key="TEST_KEY")
    
    # Setup mock returns
    pipeline.planner.create_blueprint.return_value = {"title": "Test Video"}
    pipeline.generator.generate.return_value = "from manim import *"
    pipeline.renderer.find_video.return_value = "/mock/media/video.mp4"
    
    # Execute pipeline
    result = pipeline.run(
        prompt="Explain Newton",
        category="physics",
        language="ckb",
        audience="teenagers",
        style="educational",
        duration_seconds=60,
        output_dir=str(tmp_path)
    )
    
    # Assertions to ensure architecture is respected
    assert result["blueprint"] == {"title": "Test Video"}
    assert "auto_scene.py" in result["code_file"]
    assert result["video_file"] == "/mock/media/video.mp4"
    pipeline.renderer.render.assert_called_once()
    mock_validate.assert_called_once()

@patch("core.pipeline.GeminiProvider")
@patch("core.pipeline.ContentPlanner")
@patch("core.pipeline.CodeGenerator")
@patch("core.pipeline.ManimRenderer")
@patch("core.pipeline.validate_code")
def test_pipeline_fails_on_validation(mock_validate, MockRenderer, MockGen, MockPlanner, MockProvider, tmp_path):
    """Test that the pipeline stops and raises an error if validation fails."""
    # Mocking validation to fail
    mock_validate.return_value = (False, ["Missing mandatory class"])
    
    pipeline = LuminaPipeline(api_key="TEST_KEY")
    
    with pytest.raises(ValueError, match="Code validation failed"):
        pipeline.run(
            prompt="Explain Newton",
            category="physics",
            language="ckb",
            audience="teenagers",
            style="educational",
            duration_seconds=60,
            output_dir=str(tmp_path)
        )
    
    # Ensure render is never called if validation fails
    pipeline.renderer.render.assert_not_called()
