import markdown
import pdfkit

def generate_html_and_pdf_from_md(md_path, output_html_path=None, output_pdf_path=None):
    # Read Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

    # Define output paths
    output_html_path = output_html_path or md_path.replace('.md', '.html')
    output_pdf_path = output_pdf_path or md_path.replace('.md', '.pdf')

    # Write HTML
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_template(html_content))

    # Provide path to wkhtmltopdf manually
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Convert HTML to PDF
    pdfkit.from_file(output_html_path, output_pdf_path, configuration=config)

    print(f"✅ HTML and PDF generated:\n- {output_html_path}\n- {output_pdf_path}")

def html_template(body_html):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Dashboard Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
            code {{ font-family: monospace; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        {body_html}
    </body>
    </html>
    """
