import os
import click
import yaml

from factories.search_engine_factory import SearchEngineFactory

BANNER = """
=====================================================================



		ooooo      oooooooooo.        oooooooooo.  
		`888'      `888'   `Y8b       `888'   `Y8b 
		 888        888      888       888     888 
		 888        888      888       888oooo888' 
		 888        888      888       888    `88b 
		 888        888     d88'       888    .88P 
		o888o      o888bood8P'        o888bood8P'  
                                           
          		IMAGE DATASET BUILDER V0.0.1                                                                                    
                                                                                                                                 
=====================================================================                                                                                                                                

\n\n\n
		"""

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
	click.echo(BANNER)
	dataset_name = click.prompt("Insert a name to your dataset: ")
	samples = click.prompt("\nHow many samples per seach will be necessary?  ",type=int)
	click.echo("""\nChoose images resolution:

[1] 512 pixels / 512 pixels (recommended)
[2] 1024 pixels / 1024 pixels
[3] 256 pixels / 256 pixels
[4] 128 pixels / 128 pixels
[5] Keep original image size

ps: note that the aspect ratio of the image will not be changed, so possibly the images received will have slightly different size

		""")
	image_size_ratio = click.prompt("\n\nWhat is the desired image size ratio", type=int)
	while image_size_ratio < 1 or image_size_ratio > 5:
		click.echo("Invalid option, please choose between 1 and 5.")
		image_size_ratio= click.prompt("\nOption: ",type=int)

	if image_size_ratio == 1:
		image_size_ratio= 512
	elif image_size_ratio == 2:
		image_size_ratio = 1024
	elif image_size_ratio == 3:
		image_size_ratio = 256
	elif image_size_ratio == 4:
		image_size_ratio= 128
	elif image_size_ratio == 5:
		image_size_ratio = 0

	click.echo("""\nChoose images resolution:

[1] Duck GO (recommended)
[2] Bing
[3] DeviantART (NOT READY TO USE YET)
[4] Pinterest (NOT READY TO USE YET)
[5] Google Images (NOT READY TO USE YET)


		""")
	search_engine= click.prompt("Select option:", type=int)
	while search_engine < 0 or search_engine > 5:
		click.echo("Invalid option, please choose between 1 and 5.")
		search_engine= click.prompt("\nOption: ",type=int)

	search_options = ['none','duckgo', 'bing', 'deviantart', 'pinterest', 'google_images']

	search_engine = search_options[search_engine]

	verbose = click.prompt("\nActivate verbose mode? [Y/n]: ")
	while verbose.lower() != "y" and verbose.lower() != "n":
		click.echo(verbose.lower())
		click.echo("Invalid option")
		verbose = click.prompt("[Y/n]: ")

	number_of_classes = click.prompt("How many image classes are required? ",type=int)

	document_dict = {
  
    "DATASET_NAME": dataset_name,
  
    "SAMPLES_PER_SEARCH": samples,
 
    "IMAGE_SIZE": image_size_ratio,
  
    "ENGINE": search_engine,
  
    "VERBOSE": verbose,
  
    "CLASSES": []
  
}

	for x in range(number_of_classes):
		class_name = click.prompt("\n\nClass {x} name: ".format(x=x+1))
		click.echo("""\n\n\nIn order to achieve better results, choose several keywords that will be provided to the search engine to find your class in different settings.

	Example: 
		Class Name: Pineapple
		keywords: pineapple, pineapple fruit, ananas, abacaxi, pineapple drawing


			""")

		keywords = click.prompt("Type in all keywords used to find your desired class, separated by commas: ")
		document_dict['CLASSES'].append({'CLASS_NAME': class_name, 'SEARCH_KEYWORDS': keywords})


    
	if not os.path.exists("dataset.yaml"):
		click.echo("Creating a dataset configuration file...")
		try:
			f = open("dataset.yaml", "w")
			f.write(yaml.dump(document_dict))
			if f:
				click.echo("Dataset YAML file has been created sucessfully. Now run idb build to mount your dataset!")
		except:
			click.echo("Unable to create file. Please check permission")
		
	else:
		click.echo("A dataset.yaml is already created. To use another one, delete the current dataset.yaml file")

@main.command()
def build():
	click.clear()
	click.echo(BANNER)
	if not os.path.exists("dataset.yaml"):
		click.echo("Dataset config file not found\nRun - idb init\n")
		exit(0)

	with open('dataset.yaml') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)
	
	click.echo("Building {dataset_name} dataset...\n".format(dataset_name=data['DATASET_NAME']))
	for classes in data['CLASSES']:
		click.echo('Creating {name} class'.format(name=classes['CLASS_NAME']))
		search_list = classes['SEARCH_KEYWORDS'].split(",")
		for keywords in search_list:
			factory = SearchEngineFactory(keywords,data['SAMPLES_PER_SEARCH'],classes['CLASS_NAME'],data['VERBOSE'], data['DATASET_NAME'],data['IMAGE_SIZE'], data['ENGINE'])
	click.echo("Dataset READY!")

if __name__ == "__main__":
	main()
