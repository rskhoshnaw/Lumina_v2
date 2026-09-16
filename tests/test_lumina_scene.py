from manim import BLACK, Scene

from lumina import LuminaScene


def test_lumina_scene_is_manim_scene():
    scene = LuminaScene()

    assert isinstance(scene, Scene)


def test_lumina_scene_background_color():
    scene = LuminaScene()
    scene.setup()

    assert scene.camera.background_color == BLACK
