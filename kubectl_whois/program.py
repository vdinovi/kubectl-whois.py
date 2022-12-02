import click

from kubectl_whois.output import OUTPUT_FORMATS, OUTPUT_FORMAT_DEFAULT
from kubectl_whois.client import Context, Namespace, Client


@click.command()
@click.option(
    "--context",
    default=Context.ACTIVE,
    type=str,
    help="k8s context to search within",
    show_default=True,
)
@click.option(
    "--namespace",
    default=Namespace.ALL,
    type=str,
    help="k8s namespace to search within",
    show_default=True,
)
@click.option(
    "--output",
    type=click.Choice(OUTPUT_FORMATS),
    default=OUTPUT_FORMAT_DEFAULT,
    help="output format",
    show_default=True,
)
@click.option(
    "--cidr",
    type=str,
    default="0.0.0.0/0",
    help="cidr block to filter by",
    show_default=True,
)
def execute(context: str, namespace: str, output: str, cidr: str):
    k8_context = Context(context)
    client = Client(k8_context)
    k8_namespace = Namespace(namespace, client)
    pods = client.pods(k8_namespace)
    for pod in pods.items:
        print(f"[Pod] {pod.metadata.name}: {pod.status.pod_ip}")
