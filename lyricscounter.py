import click
from musixmatch import *

@click.command()
@click.option(
    "--apikey",
    prompt="Your musicranx api key",
    help="A valid musicranx api key associated with a developer account",
)
@click.option(
    "--artist",
    prompt="Your favourite artist ",
    help="The artist whose average word count you want to know",
)
def cli(apikey, artist):
    click.echo(f'Determining the average word count in all "{artist}" songs')
    click.echo("Please wait...")
    average_word_count = get_artist_average_wordcount(apikey, artist)
    click.echo(
        f'Thanks for waiting! The average number of words in each "{artist}" song is {average_word_count}'
    )
