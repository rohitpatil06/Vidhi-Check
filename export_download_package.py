import os
import sys
import re
import shutil
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
sys.path.insert(0, backend_dir)

import database
from services.report_service import generate_pdf_report

def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    return cleaned.replace(" ", "_")[:35]

def main():
    root_dir = Path(__file__).resolve().parent
    reports_dir = root_dir / "generated_reports"
    reports_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("VIDHICHECK EXPORT & DOWNLOAD PACKAGING TOOL")
    print("=" * 60)

    # 1. Generate PDF Reports for the core demo showcase cases
    database.init_db()
    
    target_ids = ["VC-001", "VC-002", "sample_rice", "sample_biscuit", "sample_oil"]
    all_inspections = database.get_all_inspections()
    
    selected_items = []
    # Find VC-001, VC-002 and recent
    for i in all_inspections:
        if i["id"] in ["VC-001", "VC-002"] or len(selected_items) < 3:
            if i not in selected_items:
                selected_items.append(i)

    generated_pdfs = []
    print(f"\n[1/3] Generating statutory compliance PDF reports for {len(selected_items)} audit cases...")
    for item in selected_items:
        safe_name = sanitize_filename(item.get("product", "Product"))
        pdf_filename = f"VidhiCheck_Report_{item['id']}_{safe_name}.pdf"
        out_path = reports_dir / pdf_filename

        try:
            pdf_stream = generate_pdf_report(item)
            with open(out_path, "wb") as f:
                f.write(pdf_stream.getvalue())
            generated_pdfs.append(out_path)
            print(f"  [OK] Created: {pdf_filename} ({os.path.getsize(out_path):,} bytes)")
        except Exception as e:
            print(f"  [FAIL] Error generating PDF for {item['id']}: {e}")

    # 2. Create clean project ZIP archive
    zip_name = "VidhiCheck-Compliance-Checker-SIH2026.zip"
    zip_path = root_dir / zip_name
    print(f"\n[2/3] Creating complete project ZIP archive: {zip_name}...")

    exclude_dirs = {
        "node_modules", ".git", "__pycache__", ".venv", "venv", 
        ".system_generated", "dist"
    }
    exclude_exts = {".pyc", ".pyo", ".log", ".tmp"}

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                if file == zip_name:
                    continue

                full_file_path = Path(root) / file
                rel_path = full_file_path.relative_to(root_dir)
                zf.write(full_file_path, rel_path)
                file_count += 1

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  [OK] Successfully bundled {file_count} files into {zip_name} ({zip_size_mb:.2f} MB)")

    # 3. Copy to User's Downloads folder
    user_home = Path(os.environ.get("USERPROFILE", str(Path.home())))
    downloads_dir = user_home / "Downloads" / "VidhiCheck-SIH-2026"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[3/3] Copying package and reports to Windows Downloads folder:")
    print(f"  Destination: {downloads_dir}")

    # Copy ZIP
    shutil.copy2(zip_path, downloads_dir / zip_name)
    print(f"  [OK] Copied ZIP archive to: {downloads_dir / zip_name}")

    # Copy PDFs
    for pdf in generated_pdfs:
        dest_pdf = downloads_dir / pdf.name
        shutil.copy2(pdf, dest_pdf)
        print(f"  [OK] Copied Report: {pdf.name}")

    print("\n" + "=" * 60)
    print("ALL DOWNLOAD ASSETS PREPARED SUCCESSFULLY!")
    print(f"1. Project ZIP: {downloads_dir / zip_name}")
    print(f"2. PDF Reports: {downloads_dir}")
    print("=" * 60)

    # Open Downloads folder in Windows Explorer
    os.system(f'explorer "{downloads_dir}"')

if __name__ == "__main__":
    main()
