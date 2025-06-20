import json
from openai import OpenAI
from doc_assist_generate_output import generate_html_and_pdf_from_md


# Set your OpenAI API key (or use environment variable)
client = OpenAI(api_key="")

def parse_datasources(ds_section):
    rows = ds_section.get("rows", [])
    parsed = []
    for row in rows:
        props = {p["name"]: p["value"] for p in row.get("properties", [])}
        parsed.append({
            "id": row.get("id"),
            "type": row.get("typeDesc"),
            "name": props.get("name", row.get("rowName")),
            "query": props.get("query", ""),
            "jndi": props.get("jndi", ""),
        })
    return parsed

def parse_components(comp_section):
    rows = comp_section.get("rows", [])
    parsed = []
    for row in rows:
        props = {p["name"]: p["value"] for p in row.get("properties", [])}
        parsed.append({
            "id": row.get("id"),
            "type": row.get("typeDesc"),
            "name": props.get("name", row.get("rowName")),
            "label": props.get("label", ""),
            "expression": props.get("expression", ""),
            "postExecution": props.get("postExecution", ""),
            "htmlObject": props.get("htmlObject", ""),
        })
    return parsed

def parse_parameters(comp_section):
    rows = comp_section.get("rows", [])
    parsed = []
    for row in rows:
        if "parameter" in row.get("type", "").lower():
            props = {p["name"]: p["value"] for p in row.get("properties", [])}
            parsed.append({
                "id": row.get("id"),
                "name": props.get("name", ""),
                "bookmarkable": props.get("bookmarkable", "false"),
                "public": props.get("public", "false"),
                "default": props.get("default", "")
            })
    return parsed

def extract_summary(json_data, max_entries=3, included_names=None):
    # ✅ Define names to exclude
    if included_names is None:
        included_names = set()  # Empty set includes nothing by default

    # Parse and filter data
    datasources = parse_datasources(json_data.get("datasources", {}))
    datasources = [ds for ds in datasources if ds['name'] in included_names]
    datasources = datasources[:max_entries]

    components = parse_components(json_data.get("components", {}))[:max_entries]
    parameters = parse_parameters(json_data.get("parameters", {}))[:max_entries]

    summary = "### Datasources:\n"
    for ds in datasources:
        summary += (
            f"- **{ds['name']}** (Type: {ds['type']})\n"
            f"  - JNDI: `{ds['jndi']}`\n"
            f"  - Query: ```sql\n{ds['query']}\n```\n"
        )

    summary += "\n### Components:\n"
    for comp in components:
        summary += (
            f"- **{comp['name']}** (Type: {comp['type']})\n"
            f"  - Label: {comp['label']}\n"
            f"  - Expression: ```js\n{comp['expression']}\n```\n"
        )

    summary += "\n### Parameters:\n"
    for param in parameters:
        summary += f"- **{param['name']}** (Bookmarkable: {param['bookmarkable']}, Public: {param['public']})\n"

    return summary

def ask_openai(summary):
    prompt = f"""
You are an expert BI technical writer. Based on the following metadata of a Pentaho CDE dashboard, generate a clean, human-readable documentation in Markdown. Include:

1. Overview of what the dashboard does
2. List of KPIs/Charts and their purpose
3. Description of filters and their usage
4. Description of data source and logic

Here is the dashboard metadata:
{summary}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

def generate_documentation(json_file_path, output_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    included_queries = {"InfoQueries", "AssignedKPI", "trendChartLotsAssigned","trendChartLotsAssigned"}
    summary = extract_summary(data, max_entries=5, included_names=included_queries)
    # summary = extract_summary(data, max_entries=3)
    documentation = ask_openai(summary)

    if output_file_path is None:
        output_file_path = json_file_path.replace('.cdfde', '_documentation.md')

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(documentation)

    print(f"✅ Documentation saved to: {output_file_path}")

    generate_html_and_pdf_from_md(output_file_path)
# Example usage:
# generate_documentation("path/to/dashboard.json")

if __name__ == "__main__":
    # 🔁 Change this path to your actual Pentaho .cdfde JSON file
    json_file_path = "opsmetricdashboard.cdfde"
    output_md_path = "output/opsmetricdashboard_documentation.md"
    
    # 🚀 This will parse and generate Markdown documentation
    generate_documentation(json_file_path,output_md_path)