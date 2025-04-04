from fpdf import FPDF

class StyledPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 51, 102)  # Dark blue header
        self.cell(0, 10, "Astrology & Ayurveda: A Holistic Approach to Your Child's Well-Being", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 102, 204)  # Blue title color
        self.cell(0, 8, title, ln=True, align="L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.set_text_color(50, 50, 50)  # Dark gray text
        self.multi_cell(0, 7, body)
        self.ln(5)

# Create PDF
pdf = StyledPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Introduction
pdf.chapter_title("Understanding Your Child Through Ancient Wisdom")
pdf.chapter_body(
    "Parenting is a journey filled with joy, challenges, and the desire to nurture a child's physical, emotional, and mental well-being. "
    "Ancient sciences like Astrology and Ayurveda provide a deeper understanding of a child's nature, helping parents align their upbringing with cosmic and biological rhythms.\n\n"
    "This guide explores the connection between astrological influences (planets, signs, and houses) and Ayurvedic body constitutions (Vata, Pitta, Kapha), offering practical solutions for common childhood concerns."
)

# Astrology & Ayurveda Connection
pdf.chapter_title("The Link Between Astrology & Ayurveda")
pdf.chapter_body(
    "Astrology and Ayurveda are two interconnected ancient sciences that provide a comprehensive understanding of human nature and well-being. "
    "While Astrology reveals a child's mental tendencies, emotions, personality traits, and life path, Ayurveda explains their body constitution, health predispositions, and natural inclinations. "
    "Together, they offer personalized guidance for nurturing a child's overall well-being."
)

pdf.chapter_title("How They Complement Each Other")
pdf.chapter_body(
    "- Astrology determines planetary influences on a child's temperament, emotions, learning style, and behavior.\n"
    "- Ayurveda classifies a child's body type (Prakriti) as Vata, Pitta, or Kapha, which affects their physical and mental health.\n"
    "- By integrating both sciences, parents can create a nurturing environment, ensuring balance in diet, lifestyle, and daily routines tailored to the child's unique needs."
)

# Save PDF
pdf_filename = "Astrology_Ayurveda_Child_Wellbeing.pdf"
pdf.output(pdf_filename)
