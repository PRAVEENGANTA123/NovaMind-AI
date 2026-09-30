from database.pdf_repository import PDFRepository
from services.pdf.pdf_reader import PDFReaderService


EMAIL = "23se02ml099@ppsu.ac.in"


pdfs = PDFRepository.get_user_pdfs(EMAIL)

if not pdfs:

    print("No PDFs Found")

    exit()


pdf = pdfs[0]

print("=" * 60)

print("Filename :", pdf["filename"])

print("Path     :", pdf["filepath"])

print("=" * 60)


result = PDFReaderService.extract_text(

    pdf["filepath"]

)

print("Success :", result["success"])

print("Pages   :", result["pages"])

print("Error   :", result["error"])

print("Characters :", len(result["text"]))

print("=" * 60)

print(result["text"][:1500])