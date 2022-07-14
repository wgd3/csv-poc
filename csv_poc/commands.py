"""Custom Flask CLI commands"""
import os
import click
import pprint
from flask import current_app, json
from flask.cli import with_appcontext

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option("-c", "--coverage", is_flag=True, default=False)
def test(coverage):
    """Run the tests."""
    import pytest

    if coverage is True:
        import coverage

        cov = coverage.Coverage()
        cov.start()

    rv = pytest.main(
        [
            TEST_PATH,
            "--no-header",
            # "--no-summary",
            # "-q",
            # "--verbose",
            # "--log-level=DEBUG",
            # "-s"
        ]
    )

    if coverage:
        cov.stop()
        cov.save()
        click.echo("\n\nCoverage Report:\n")
        cov.report()
        click.echo(
            "\nHTML version: "
            + os.path.join(PROJECT_ROOT, "htmlcov/index.html")
        )
        cov.html_report(directory="htmlcov")
        cov.erase()

    exit(rv)


@click.command()
@click.option("--urlvars", is_flag=True, default=False)
@click.option("--swagger", is_flag=True, default=True)
@click.option("-f", "--file", help="Output file for import into Postman")
@with_appcontext
def postman(urlvars, swagger, file):
    """Outputs a Postman collection for the API

    Args:
        urlvars:
        swagger:
        file: Filename used for output instead of stdout
    """
    from csv_poc.api.v1 import api

    click.echo("Collection API information and creating a Postman collection..")
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    click.echo(
        "WARNING: The output from this command is in a V1 format, and is not compatible with the latest versions of Postman!",
    )
    if file is not None:
        with open(file, "w") as f:
            f.write(json.dumps(data))
            click.echo(
                f"Postman collection is now available in the file: {file}"
            )

    else:
        click.echo("Printing Postman collection...\n")
        pprint.pprint(json.dumps(data), indent=2)
