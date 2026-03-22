"""Test voice conversion functionality."""

from app.services.eigen_chat import convert_to_voice_friendly_text


def test_markdown_formatting_removal():
    """Test that markdown formatting is properly removed."""
    text = "**Hi there!** This is *emphasized* text."
    result = convert_to_voice_friendly_text(text)
    assert "**" not in result
    assert "*" not in result
    assert "Hi there!" in result


def test_emoji_removal():
    """Test that emojis are removed for natural speech."""
    text = "📋 Summary of the March 1 2026 Consultation 🩺"
    result = convert_to_voice_friendly_text(text)
    assert "📋" not in result
    assert "🩺" not in result
    assert "Summary of the March 1 2026 Consultation" in result


def test_table_conversion():
    """Test that markdown tables are converted to readable text."""
    text = """| Category | Details |
|----------|---------|
| **Reason for visit** | You were experiencing chills at night |
| **Diagnosis** | Food-borne gastroenteritis |"""
    
    result = convert_to_voice_friendly_text(text)
    assert "|" not in result
    assert "Category" in result
    assert "Reason for visit" in result
    assert "You were experiencing chills at night" in result
    assert "Food-borne gastroenteritis" in result


def test_section_headers():
    """Test that markdown headers are converted to plain text."""
    text = """## 📋 Summary of the March 1 2026 Consultation
### What's next?
Here is some content."""
    
    result = convert_to_voice_friendly_text(text)
    assert "#" not in result
    assert "Summary of the March 1 2026 Consultation" in result
    assert "What's next?" in result
    assert "Here is some content" in result


def test_bullet_points():
    """Test that bullet points are converted to readable format."""
    text = """Medications prescribed:
• Paracetamol – for fever and pain
• Antidiarrheal agents or antibiotic"""
    
    result = convert_to_voice_friendly_text(text)
    assert "•" not in result
    assert "Paracetamol" in result
    assert "fever and pain" in result


def test_real_world_example():
    """Test with the actual example from the user."""
    text = """**Hi there!**  
I'm happy to give you a quick recap of the most recent consultation we have on file for you. The only record we have in the system is from **March 1 2026**, which is a little earlier than "last week," but I'll summarize what was discussed and the plan that was set.

---

## 📋 Summary of the March 1 2026 Consultation

| Category | Details |
|----------|---------|
| **Reason for visit** | You were experiencing chills at night, loose motions, loss of appetite, headaches, body pains, and general weakness. |
| **Probable diagnosis** | **Food‑borne gastroenteritis (food poisoning)** – likely related to a recent meal (you mentioned eating dosa). |
| **Medications prescribed** | • **Paracetamol** – for fever and pain (dosage was not specified in the notes).<br>• "A few medicines" to be obtained from the pharmacy (the clinician likely meant antidiarrheal agents or possibly an antibiotic, depending on the severity). |

---

### How can I help you further?

- **Clarify the timeline**: If you had a visit "last week" (mid‑March) and you have a copy of the notes, you can upload or type the details and I'll summarize them for you.  
- **Medication guidance**: If you're unsure about the dosage of paracetamol or any other meds you received, let me know the prescription details and I'll explain the usual dosing.  

**Take care of yourself, and let me know how you'd like to proceed!**"""
    
    result = convert_to_voice_friendly_text(text)
    
    # Check that formatting is removed
    assert "**" not in result
    assert "##" not in result
    assert "📋" not in result
    assert "|" not in result
    assert "•" not in result
    
    # Check that content is preserved
    assert "Hi there" in result
    assert "March 1 2026" in result
    assert "chills at night" in result
    assert "Food-borne gastroenteritis" in result
    assert "Paracetamol" in result
    assert "Take care of yourself" in result
    
    print("✓ Real-world example conversion successful")
    print("\nOriginal length:", len(text), "characters")
    print("Converted length:", len(result), "characters")
    print("\nConverted text (first 500 chars):")
    print(result[:500])


if __name__ == "__main__":
    test_markdown_formatting_removal()
    print("✓ Markdown formatting removal test passed")
    
    test_emoji_removal()
    print("✓ Emoji removal test passed")
    
    test_table_conversion()
    print("✓ Table conversion test passed")
    
    test_section_headers()
    print("✓ Section headers test passed")
    
    test_bullet_points()
    print("✓ Bullet points test passed")
    
    test_real_world_example()
    
    print("\n✅ All voice conversion tests passed!")
