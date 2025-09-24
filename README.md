# Invoice Generator API

A FastAPI-based microservice that generates professional PDF invoices using **ReportLab**.

## 🚀 Features
- Generate PDF invoices with custom metadata
- RESTful API built with FastAPI
- Interactive API docs at `/docs`
- Organized output folder for generated invoices

## 📦 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/invoice-generator-api.git
cd invoice-generator-api
pip install -r requirements.txt
▶️ Run the app
Start the server with Uvicorn:

Bash


Copy
uvicorn main:app --reload
The app will be available at:

API root: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

📂 Project Structure
Code


Copy
Invoice_Generator/
├── main.py            # FastAPI app
├── output/            # Generated invoices
├── data/              # Input/sample data
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
└── .gitignore         # Ignore venv, cache, PDFs
📝 Example Request
Http


Copy
POST /generate_invoice
Content-Type: application/json

{
  "invoice_id": "INV-001",
  "client": "John Doe",
  "amount": 250.00
}
✅ Step 4: Save and commit
Once you’ve added the content, save the file and commit it:

Powershell


Copy
git add README.md
git commit -m "Add README.md with project details"
git push origin main
