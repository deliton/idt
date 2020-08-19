import os
import argparse
import click

from crawlers.duckgo import duckgoSearch

#@click.command()
@click.group()
@click.option('--version', '-v', is_flag=True)
@click.option('--authors', is_flag=True)
def main(version, authors):
    
    """
    Image Dataset Builder CLI to create amazing datasets
    """
    pass

@main.command()
def version():
	click.echo("Image Dataset Builder (IDB) version 0.0.1 alpha")

@main.command()
def authors():
	click.echo("IDB was initially made by Deliton Junior and Misael Kelviny")
	click.echo("\n\nCoontributors: ")


@main.command()
@click.option('--input', '-i','--i')
@click.option('--size', '-s','--s', default=50)
@click.option('--engine', '-e','--e', default="duckgo")
@click.option('--verbose', '-v','--v', is_flag=True)
def run(input, size, engine, verbose):

	# TODO: Implement multi class search
	if input:
		duckgoSearch(input, size, verbose)
	else:
		click.echo("Please provide a valid name")

@main.command()
def init():
	click.clear()
	click.echo("""
=========================================================================================================================================

ooooo                                                       oooooooooo.                 .                                    .   
`888'                                                       `888'   `Y8b              .o8                                  .o8   
 888  ooo. .oo.  .oo.    .oooo.    .oooooooo  .ooooo.        888      888  .oooo.   .o888oo  .oooo.    .oooo.o  .ooooo.  .o888oo 
 888  `888P"Y88bP"Y88b  `P  )88b  888' `88b  d88' `88b       888      888 `P  )88b    888   `P  )88b  d88(  "8 d88' `88b   888   
 888   888   888   888   .oP"888  888   888  888ooo888       888      888  .oP"888    888    .oP"888  `"Y88b.  888ooo888   888   
 888   888   888   888  d8(  888  `88bod8P'  888    .o       888     d88' d8(  888    888 . d8(  888  o.  )88b 888    .o   888 . 
o888o o888o o888o o888o `Y888""8o `8oooooo.  `Y8bod8P'      o888bood8P'   `Y888""8o   "888" `Y888""8o 8""888P' `Y8bod8P'   "888" 
                                  d"     YD                                                                                      
oooooooooo.               o8o  ooooY88888P'.o8                            .o  o8o        .o8   .o8       o.                      
`888'   `Y8b              `"'  `888       "888                           .8'  `"'       "888  "888       `8.                     
 888     888 oooo  oooo  oooo   888   .oooo888   .ooooo.  oooo d8b      .8'  oooo   .oooo888   888oooo.   `8.                    
 888oooo888' `888  `888  `888   888  d88' `888  d88' `88b `888""8P      88   `888  d88' `888   d88' `88b   88                    
 888    `88b  888   888   888   888  888   888  888ooo888  888          88    888  888   888   888   888   88                    
 888    .88P  888   888   888   888  888   888  888    .o  888          `8.   888  888   888   888   888  .8'                    
o888bood8P'   `V88V"V8P' o888o o888o `Y8bod88P" `Y8bod8P' d888b          `8. o888o `Y8bod88P"  `Y8bod8P' .8'                     
                                                                          `"                             "'                      
                                                                                                                                 
 ============================================================================================================================================                                                                                                                                

\n\n\n\n\n\n
		""")
	dataset_name = click.prompt("Insert a name to your dataset: ")

	document_upper_part = """
# Dataset Name
- DATASET_NAME: {dataset_name}

# How many images per search is needed
- SAMPLES_PER_SEARCH: {samples}

# Desired image size (recommended: 512x512)
- IMAGE_SIZE: '{image_size_ratio}, {image_size_ratio}'

# Choose which engine will search for the images (options: DUCKGO, GOOGLE, PINTEREST, DEVIANTART, PHOTOBUCKET)
- ENGINE: {search_engine}

# Verbose mode
- VERBOSE: {verbose}

# List here all the classes you need for your dataset. Replace PINEAPPLES and APPLES by the classes you need
- CLASSES:
	"""

	document_classnames = """
	# Name of the CLASS/FOLDER
    - CLASS_NAME: {class_name}
      # Keywords used in the search engine to get the results
      SEARCH_KEYWORDS:
        - {class_name}

	"""

	document_keywords = """
        - {class_name}

	"""

    
	if not os.path.exists("dataset.yaml"):
		click.echo("Creating a dataset configuration file...")
		try:
			f = open("dataset.yaml", "w")
			f.write(document)
			if f:
				click.echo("Dataset YAML file has been created sucessfully")
		except:
			click.echo("Unable to create file. Please check permission")
		
	else:
		click.echo("A dataset.yaml is already created. To use another one, delete the current dataset.yaml file")


if __name__ == "__main__":
	main()


	# idb -i Fusca 