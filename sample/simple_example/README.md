# Maiden Readme File

A tool to generate Markdown files from templates populated with data from YAML or JSON files.

## Functions

### load_data

The `load_data` function loads data from a file, which can be in YAML or JSON format. It reads the file content and returns it as a dictionary; if the file is neither YAML nor JSON, it returns the raw content.

### openai_prompt

The `openai_prompt` function generates text using OpenAI's API based on a given prompt. It constructs a message for the OpenAI model and retrieves the generated response, which is then returned as a string.

### postprocess_template

The `postprocess_template` function preprocesses a template string to replace custom syntax with actual data. It handles directives for loading data from files, formatting dates, and generating text using OpenAI prompts.

### process_template

The `process_template` function renders a final markdown document using Jinja2 templates. It takes processed template strings and data dictionaries to produce the rendered output.

### process_data_template_file

The `process_data_template_file` function processes a data template file by first loading its content and then preprocessing it. The preprocessed template string is converted back into structured data using YAML parsing.

### generate_md

The `generate_md` function is a CLI command that generates markdown documents from templates. It supports options for specifying data files in YAML format and whether to preprocess these files as templates before rendering the final output.

## Change Log

2024-08-12 - Initial Version