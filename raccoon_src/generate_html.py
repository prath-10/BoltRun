# raccoon_src/generate_html.py

from jinja2 import Template

def generate(scan_results):
    # Generate HTML content using Jinja2 template
    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scan Results</title>
    </head>
    <body>
        <h1>Scan Results</h1>
        <ul>
        {% for result in scan_results %}
            <li>{{ result }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """)

    html_output = template.render(scan_results=scan_results)

    # Write HTML output to file
    with open("scan_results.html", "w") as f:
        f.write(html_output)

if __name__ == "__main__":
    # Example usage for testing
    scan_results = ["Result 1", "Result 2", "Result 3"]
    generate(scan_results)
