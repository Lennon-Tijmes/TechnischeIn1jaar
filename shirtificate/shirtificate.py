from fpdf import FPDF

class Shirtificate:
    def __init__(self, name):
        self.name = name
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=False)

    def add_header(self):
        self.pdf.set_font("Courier", "B", 28)
        self.pdf.set_text_color(0, 102, 204)
        self.pdf.cell(0, 20, "T!CS Shirtificate", ln=True, align="C")

        self.pdf.set_draw_color(0, 102, 204)
        self.pdf.set_line_width(1)
        self.pdf.line(10, 40, 200, 40)
        self.pdf.ln(10)

    def add_shirt_image(self):
        self.pdf.image("shirtificate.png", x=35, y=60, w=140)

    def add_name(self):
        self.pdf.set_font("Courier", "B", 20)
        self.pdf.set_text_color(255, 255, 255)  # White text
        self.pdf.set_xy(50, 130)
        self.pdf.cell(110, 10, f"{self.name} survived T!CS", align="C")

    def make_pdf(self):
        self.pdf.add_page()
        self.add_header()
        self.add_shirt_image()
        self.add_name()
        self.pdf.output("shirtificate.pdf")
        print("It has been successfull")


if __name__ == "__main__":
    user_name = input("Enter your name: ").strip().capitalize()
    shirtificate= Shirtificate(user_name)
    shirtificate.make_pdf()
