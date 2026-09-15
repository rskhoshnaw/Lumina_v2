# ✨ Lumina Studio

AI-powered educational and motivational video generation studio.

Lumina Studio converts a natural-language scenario into an
animated educational video using:

- Google Gemini
- Manim Community
- Lumina animation engine
- Streamlit

The project is designed to support multiple educational categories,
languages, visual styles, and animation types.

---

## 🎯 Project Goal

Lumina Studio is being developed as a general-purpose educational
video generation platform.

It can be used for:

- Mathematics
- Physics
- Chemistry
- Biology
- History
- Geography
- Languages
- Computer Science
- Motivational content
- Educational explanations
- Conceptual animations

The generated video is currently produced as an MP4 animation.
Voice-over and audio can be added in a later stage.

---

## 🧠 Architecture

The application separates the generation process into several stages:

```text
User Scenario
      ↓
Content Planner
      ↓
Video Blueprint
      ↓
Code Generator
      ↓
Python / Manim Code
      ↓
Validator
      ↓
Manim Renderer
      ↓
MP4 Video
