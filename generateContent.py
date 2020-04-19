#!/usr/bin/env python

"""
Generate the contents (documents, code)
"""

import os
import json

from jinja2 import Template

#
# Constants
#

_TEMPLATES_DIR = "template"
_MAIN_TEMPLATE_FILE = "main.html"
_INDEX_FILE = "index.html"
_EXPERIMENTS_TEMPLATE_FILE = "experiment.html"
_EXPERIMENTS_DIR = "experiments"
_EXPERIMENT_CONTEXT_FILE = "context.json"
_EXPERIMENT_CONTENT_FILE = "content.html"


def MergeDict(srcDict, dstDict):
    """
    Merge key values from ``srcDict`` into ``dstDict``.
    """
    for key, value in srcDict.items():
        assert(key not in dstDict)
        dstDict[key] = value


def WriteFile(filePath, content):
    """
    Write a file to disk.

    Args:
        filePath (str): path to write to.
        content (str): content to write.
    """
    print("Generated {!r}".format(filePath))
    with open(filePath, 'w') as f:
        f.write(content)


def GenerateDocument(templatePath, context):
    """
    Generate a dcoument with a template and context.

    Args:
        templatePath (str): path to the template file to perform substitution.
        context (obj): context object with attributes which are consumed in the template rendering.

    Returns:
        str: file name of generated document.
    """
    with open(templatePath, 'r') as f:
        templateStr = f.read()
        template = Template(templateStr)
        code = template.render(context=context)
        return code


def GenerateMainPage(experiments):
    """
    Generate the main page document.

    Args:
        experiments (list): experiment context dicts.
    """
    templatesDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), _TEMPLATES_DIR)
    mainTemplatePath = os.path.join(templatesDir, _MAIN_TEMPLATE_FILE)

    context = {
        "experiments": experiments
    }

    document = GenerateDocument(mainTemplatePath, context)
    indexPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), _INDEX_FILE)
    WriteFile(indexPath, document)


def GenerateExperiments():
    """
    Generate all the experiment documents.

    Returns:
        list: list of experiment context dict(s).
    """
    templatesDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), _TEMPLATES_DIR)
    experimentTemplatePath = os.path.join(templatesDir, _EXPERIMENTS_TEMPLATE_FILE)
    experimentsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), _EXPERIMENTS_DIR)
    experiments = []

    # Generate an index.html document for each experiment.
    for experimentName in os.listdir(experimentsDir):
        context = {
            "name": experimentName
        }

        experimentDir = os.path.join(experimentsDir, experimentName)
        contextPath = os.path.join(experimentDir, _EXPERIMENT_CONTEXT_FILE)
        with open(contextPath, 'r') as contextFile:
            MergeDict(json.load(contextFile), context)

        contentPath = os.path.join(experimentDir, _EXPERIMENT_CONTENT_FILE)
        with open(contentPath, 'r') as contentFile:
            context["content"] = contentFile.read().strip()

        # Write out index document.
        document = GenerateDocument(experimentTemplatePath, context)
        indexPath = os.path.join(experimentDir, _INDEX_FILE)
        WriteFile(indexPath, document)

        # Collect all the experiment contexts, used to generate the main page.
        experiments.append(context)

    return experiments


if __name__ == "__main__":
    experiments = GenerateExperiments()
    GenerateMainPage(experiments)
