# MaiDEN

A command-line utility to generate Markdown files from templates populated with data from YAML or JSON files.

## Installation

\`\`\`bash
pip install maiden
\`\`\`

## Usage

\`\`\`bash
maiden templates/my_template.md output.md -d data.yaml
\`\`\`

```bash
Usage: maiden [OPTIONS] TEMPLATE_FILE OUTPUT_FILE

  CLI command to generate markdown from template

Options:
  -d, --data-file TEXT     Data files in YAML format
  --process-data-template  Process data file as a template
  --help
```

--process-data-template Option will process the data file as a template, so you can use Jinja2 syntax in your template file by using the updated data file.

So the idea will be using the template options in the data file so that it can collect information from files and then use this information in the template file with jinja2 syntax.

## Template Examples

### Read information from a file

Reading a field from a YAML or JSON file:
<% FROM additional_info.yml GET 'requirements' %>

Reading Python File Content
<% FROM src/exceptions.py GET 'content' %>

### Getting current time

<% DATE YYYY-MM-DD %>

### Getting information from OpenAI API
<% OPENAI
    Say something meaningful.
END %>

### Nested Usage
<% OPENAI
Read the following python codes and give me information about what STDOUT and STDERR are in a table.

just give me the information I asked, don't give information about what are you doing.

Action.py is like this
<% FROM src/actions/actions.py GET 'content' %>

Exceptions.py is like this
<% FROM src/exceptions.py GET 'content' %>

Extension.py is like this
<% FROM src/extension.py GET 'content' %>
END %>

### Jinja2 Template Engine
This tool also supports Jinja2 template engine, you can use it to generate more complex templates.