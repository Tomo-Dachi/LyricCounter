import click
import musicranx


@click.command()
@click.option('--apikey', prompt="Your musicranx api key", help="A valid musicranx api key associated with a developer account")
@click.option('--artist', prompt="Your favourite artist ", help="The artist whose average word count you want to know")
def cli(apikey, artist):
    click.echo(f"Determining the average word count in all \"{artist}\" songs")
    api = MusicranxApi(apikey)
    click.echo("Please wait...")
    average_word_count = api.get_artist_average_wordcount(artist)
    click.echo(f"Thanks for waiting! The average number of words in each \"{artist}\" song is {average_word_count}")