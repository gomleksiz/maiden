from datetime import datetime
import re
import os
import json

import click
import yaml

from jinja2 import Template
from openai import OpenAI
import logging
from maiden import __version__

logging.basicConfig(level=logging.INFO)

def load_data(file_path):
    """Load data from a YAML or JSON file"""
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        with open(file_path, 'r') as f:
            return { "content" : f.read() }

def openai_prompt(prompt):
    """Generate text from OpenAI based on the prompt"""
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": "You are a helpful assistant for writing techinal documents"},
        {"role": "user", "content": f"Input: {prompt}"},
        {"role": "user", "content": "Please provide the requested information below:"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        # max_tokens=2048,
        stop=None,
        temperature=0.1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )

    corrected_text = response.choices[0].message.content.strip()
    return corrected_text.strip()

def postprocess_template(template_str):
    """Preprocess the template to replace custom syntax with actual data"""
    pattern = r"<% FROM (.+?) GET '(.+?)' %>"
    matches = re.findall(pattern, template_str)

    for match in matches:
        source_file, key = match
        data = load_data(source_file)
        
        # Split the key by dots to traverse nested dictionaries
        keys = key.split('.')
        value = data
        for key_ in keys:
            if isinstance(value, list):
                filtered_list = [item for item in value if isinstance(item, dict) and key_ in item]
                logging.info(f"List value = {filtered_list}")
                if filtered_list:
                    value = filtered_list[0]
                else:
                    value = '[Missing Data]'
                    break
            elif isinstance(value, dict):
                value = value.get(key_, '[Missing Data]')
                if value == '[Missing Data]':
                    break
        
        # Handle cases where the key path is invalid
        if not value:
            value = "[Missing Data]"

        # Replace the custom directive with the actual value
        template_str = template_str.replace(f"<% FROM {source_file} GET '{key}' %>", f"{value}")
    
    date_pattern = r"<% DATE (.+?) %>"

    def date_replacement_func(match):
        date_format = match.groups()[0]
        return datetime.now().strftime(date_format)

    template_str = re.sub(date_pattern, date_replacement_func, template_str)

    # Handle OpenAI prompts
    openai_pattern = r"<% OPENAI(.+?)END %>"
    matches = re.findall(openai_pattern, template_str, re.DOTALL)

    for match in matches:
        prompt_template = match.strip()
        logging.info(f"OPENAI PART {prompt_template}")
        value = openai_prompt(prompt_template)
        logging.info(f"VALUE = {value}")
        template_str = template_str.replace(f"<% OPENAI{match}END %>", value)

    return template_str

def process_template(data, processed_template_str):
    # Render the final markdown using Jinja2
    template = Template(processed_template_str)

    # Render template with data
    result = template.render(data)

    return result

def process_data_template_file(data_file):
    logging.info("Processing Data Template File")
    # Load the template from the file
    with open(data_file) as f:
        template_str = f.read()
    
    processed_template_str = postprocess_template(template_str)
    return yaml.safe_load(processed_template_str)

@click.command()
@click.argument('template_file')
@click.argument('output_file')
@click.option('--data-file', '-d', help='Data files in YAML format')
@click.option('--process-data-template', is_flag=True, default=True, help="Process data file as a template")
@click.version_option(__version__)
def generate_md(template_file, output_file, data_file, process_data_template):
    """CLI command to generate markdown from template"""
    if process_data_template:
        data = process_data_template_file(data_file)
    else:
        data = load_data(data_file)
    
    logging.info(f"Data = {data}")

    with open(template_file, 'r') as f:
        template_str = f.read()

    # Preprocess template to replace custom syntax
    processed_template_str = process_template(data, template_str)
    processed_template_str = postprocess_template(processed_template_str)
    
    # Write output to file
    with open(output_file, 'w') as f:
        f.write(processed_template_str)

if __name__ == '__main__':
    generate_md()
