import os
import string
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display
import arabic_reshaper
from core import word_checker

file_directory = os.path.dirname(__file__)


class InfographicGenerator:
    def __init__(
        self,
        lang = "hebrew",
        highlight_color="#E89024",
        default_font_path= file_directory + r"\fonts\almoni-dl-aaa-900.ttf",
    ):
        """
        Initialize the InfographicGenerator with paths and default settings.
        
        :param template_path: Path to the infographic template image.
        :param highlight_color: Hex color code for highlighting text.
        :param default_font_path: Default font path to use for Hebrew/English.
        """
        self.lang = lang
        self.template_path = f"{file_directory}\\templates\\{lang}.png"
        self.highlight_color = highlight_color
        self.font_path = default_font_path
        if self.lang == "arabic":
            self.font_path = file_directory + r"\fonts\Amiri-Bold.ttf"
        if self.lang == "russian":
            self.font_path = file_directory + r"\fonts\noto-sans.bold.ttf"
            
    def remove_punctuation(self, s: str) -> str:
        """Remove common punctuation from a string for matching purposes."""
        return s.translate(str.maketrans('', '', string.punctuation))
        
    def draw_text(self, draw, position, text, font, fill="white"):
        """Draw text with an optional stroke."""
        draw.text(position, text, font=font, fill=fill)


    def letter_reversal(self, text: str) -> str:
        """
        Correctly reshapes and displays Hebrew/Arabic text in RTL.
        Returns the text as-is for other languages.
        """
        if self.lang in ("hebrew", "arabic"):
            return get_display(arabic_reshaper.reshape(text))
        return text

    def wrap_text(self, draw, text, font, max_width, word_spacing=10):
        """Split text into lines that fit into max_width.
        Returns a list of lines (each line is a list of words)."""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        for word in words:
            # Get word width from bounding box (getbbox returns (x0, y0, x1, y1))
            word_width = font.getbbox(word)[2] - font.getbbox(word)[0]
            # If there are already words in the line, add spacing
            additional_width = word_width if not current_line else word_spacing + word_width
            if current_width + additional_width <= max_width:
                current_line.append(word)
                current_width += additional_width
            else:
                lines.append(current_line)
                current_line = [word]
                current_width = word_width
        if current_line:
            lines.append(current_line)
        return lines

    def draw_wrapped_text(self, draw, lines, font, start_y, total_width, line_spacing=10, word_spacing=10, marked_words=None):
        """Draw the wrapped lines (each as a list of words) centered horizontally.
        Each word is drawn separately so that we can apply a different fill if it’s marked."""
        y = start_y
        # Use a sample text to get approximate line height
        sample_bbox = font.getbbox("Ay")
        line_height = sample_bbox[3] - sample_bbox[1]
        
        for line in lines:
            # Calculate the total width of the line
            line_width = sum((font.getbbox(word)[2] - font.getbbox(word)[0]) for word in line) + word_spacing * (len(line) - 1)
            # Center the line horizontally
            x = (total_width - line_width) // 2
            for word in line:
                # Here we use your existing highlighting logic.
                # (If word_checker isn’t defined, you could simply use: 
                # fill_color = self.highlight_color if word in marked_words else "white")
                fill_color = self.highlight_color if any(
                    word_checker.word_exists(mw, self.letter_reversal(word)) for mw in marked_words
                ) else "white"
                self.draw_text(draw, (x, y), word, font, fill=fill_color)
                word_width = font.getbbox(word)[2] - font.getbbox(word)[0]
                x += word_width + word_spacing
            y += line_height + line_spacing

    def create_infographic(self, output_path, text_data):
        """
        Updated version that dynamically wraps text.
        Expects text_data to have keys "title", "subtitle", "body", "words_to_mark".
        """
        img = Image.open(self.template_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Set font scale based on language (adjust as needed)
        if self.lang == "arabic":
            font_scale = 0.75
        elif self.lang == "russian":
            font_scale = 0.70
        else:
            font_scale = 1.0

        margin = 50
        max_text_width = width - 2 * margin
        line_spacing = 20

        # Prepare fonts
        title_font = ImageFont.truetype(self.font_path, int(95 * font_scale))
        subtitle_font = ImageFont.truetype(self.font_path, int(80 * font_scale))
        body_font = ImageFont.truetype(self.font_path, int(70 * font_scale))

        # Process and reshape texts as needed
        title_text = self.letter_reversal(text_data["title"]["text"])
        subtitle_text = self.letter_reversal(text_data["subtitle"]["text"])
        body_lines_text = [self.letter_reversal(line["text"]) for line in text_data["body"]]
        marked_words = text_data["words_to_mark"]

        # --- Draw Title ---
        title_lines = self.wrap_text(draw, title_text, title_font, max_text_width, word_spacing=10)
        title_start_y = int(height * 0.35)
        self.draw_wrapped_text(draw, title_lines, title_font, title_start_y, width,
                                line_spacing=line_spacing, word_spacing=10, marked_words=marked_words)

        # --- Draw Subtitle ---
        # Calculate the total height of the title block
        sample_bbox = title_font.getbbox("Ay")
        title_line_height = sample_bbox[3] - sample_bbox[1]
        title_total_height = len(title_lines) * (title_line_height + line_spacing)
        subtitle_start_y = title_start_y + title_total_height + 50
        subtitle_lines = self.wrap_text(draw, subtitle_text, subtitle_font, max_text_width, word_spacing=10)
        self.draw_wrapped_text(draw, subtitle_lines, subtitle_font, subtitle_start_y, width,
                                line_spacing=line_spacing, word_spacing=10, marked_words=marked_words)

        # --- Draw Body ---
        # For body text, you might want left-alignment; here we still center each line.
        body_start_y = subtitle_start_y + (len(subtitle_lines) * (subtitle_font.getbbox("Ay")[3] - subtitle_font.getbbox("Ay")[1] + line_spacing)) + 50
        for body_text in body_lines_text:
            wrapped_body_lines = self.wrap_text(draw, body_text, body_font, max_text_width, word_spacing=10)
            self.draw_wrapped_text(draw, wrapped_body_lines, body_font, body_start_y, width,
                                    line_spacing=line_spacing, word_spacing=10, marked_words=marked_words)
            # Increase y for next body text block
            sample_body_bbox = body_font.getbbox("Ay")
            body_line_height = sample_body_bbox[3] - sample_body_bbox[1]
            body_start_y += len(wrapped_body_lines) * (body_line_height + line_spacing) + 10

        img.save(output_path)
        print(f"Infographic saved to {output_path}")



