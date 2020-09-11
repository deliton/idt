import os
import click
import yaml

from factories.search_engine_factory import SearchEngineFactory
from analyzers.dataset_status import analyze_dataset, remove_corrupt
from analyzers.split_dataset_into_valid_and_train import split_dataset

BANNER = """
=====================================================================



		ooooo      oooooooooo.        oooooooooo.  
		`888'      `888'   `Y8b       `888'   `Y8b 
		 888        888      888       888     888 
		 888        888      888       888oooo888' 
		 888        888      888       888    `88b 
		 888        888     d88'       888    .88P 
		o888o      o888bood8P'        o888bood8P'  
                                           
          		IMAGE DATASET BUILDER V0.0.2                                                                                    
                                                                                                                                 
=====================================================================                                                                                                                                
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
	click.clear()
	click.echo("Image Dataset Builder (IDB) version 0.0.2 alpha")

@main.command()
def authors():
	click.echo("IDB was initially made by Deliton Junior and Misael Kelviny")
	click.echo("\n\nCoontributors: ")

@main.command()
@click.option('--input', '-i','--i')
@click.option('--size', '-s','--s', default=50)
@click.option('--engine', '-e','--e', default="duckgo")
@click.option('--verbose', '-v','--v', is_flag=False)
@click.option('--imagesize', '-is','--is', default=512)
def run(input, size, engine, verbose, imagesize):
	engine_list = ['duckgo','deviantart', 'bing']
	click.clear()

	if input and engine in engine_list:
		factory = SearchEngineFactory(input,size,input,verbose,"dataset",imagesize, engine)
		# Remove corrupt files
		remove_corrupt("dataset")
	else:
		click.echo("Please provide a valid name")

@main.command()
def init():
	click.clear()
	click.echo(BANNER)
	dataset_name = click.prompt("Insert a name to your dataset: ")

	click.clear()
	click.echo(BANNER)
	samples = click.prompt("\nHow many samples per seach will be necessary?  ",type=int)

	click.clear()
	click.echo(BANNER)
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

	click.clear()
	click.echo(BANNER)
	click.echo("""\nChoose a search engine:

[1] Duck GO (recommended)
[2] Bing
[3] Flickr

		""")
	search_engine= click.prompt("Select option:", type=int)
	while search_engine < 0 or search_engine > 3:
		click.echo("Invalid option, please choose between 1 and 2.")
		search_engine = click.prompt("\nOption: ", type=int)

	search_options = ['none', 'duckgo', 'bing', 'flickr', 'deviantart', 'pinterest', 'google_images']

	search_engine = search_options[search_engine]

	click.clear()
	click.echo(BANNER)
	verbose = click.prompt("\nActivate verbose mode? [Y/n]: ")
	while verbose.lower() != "y" and verbose.lower() != "n":
		click.clear()
		click.echo(BANNER)
		click.echo("Invalid option")
		verbose = click.prompt("[Y/n]: ")

	click.clear()
	click.echo(BANNER)
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
		click.clear()
		click.echo(BANNER)
		class_name = click.prompt("Class {x} name: ".format(x=x+1))

		click.clear()
		click.echo("""In order to achieve better results, choose several keywords that will be provided to the search engine to find your class in different settings.
	
Example: 

Class Name: Pineapple
keywords: pineapple, pineapple fruit, ananas, abacaxi, pineapple drawing

			""")
		keywords = click.prompt("Type in all keywords used to find your desired class, separated by commas: ")
		document_dict['CLASSES'].append({'CLASS_NAME': class_name, 'SEARCH_KEYWORDS': keywords})
    
	if not os.path.exists("dataset.yaml"):
		click.clear()
		click.echo(BANNER)
		click.echo("Creating a dataset configuration file...")
		try:
			f = open("dataset.yaml", "w")
			f.write(yaml.dump(document_dict))
			if f:
				click.clear()
				click.echo("Dataset YAML file has been created sucessfully. Now run idb build to mount your dataset!")
		except:
			click.clear()
			click.echo("Unable to create file. Please check permission")
		
	else:
		click.clear()
		click.echo("A dataset.yaml is already created. To use another one, delete the current dataset.yaml file")

@main.command()
def build():
	click.clear()
	click.echo(BANNER)
	if not os.path.exists("dataset.yaml"):
		click.clear()
		click.echo("Dataset config file not found\nRun - idb init\n")
		exit(0)

	with open('dataset.yaml') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)
	
	click.clear()
	click.echo("Building {dataset_name} dataset...\n".format(dataset_name=data['DATASET_NAME']))
	for classes in data['CLASSES']:
		click.clear()
		click.echo('Creating {name} class'.format(name=classes['CLASS_NAME']))
		search_list = classes['SEARCH_KEYWORDS'].split(",")
		for keywords in search_list:
			factory = SearchEngineFactory(keywords,data['SAMPLES_PER_SEARCH'],classes['CLASS_NAME'],data['VERBOSE'], data['DATASET_NAME'],data['IMAGE_SIZE'], data['ENGINE'])
	
	# Remove corrupt files
	remove_corrupt(data['DATASET_NAME'])

	# Create a CSV with dataset info
	analyze_dataset(data['DATASET_NAME'])
	click.clear()
	click.echo("Dataset READY!")

@main.command()
def split():
	while True:
		click.clear()
		click.echo(BANNER)
		train_proportion = click.prompt("Choose the desired proportion of images of each class to be distributed in train/valid folders. What percentage of images should be distributed towards training? (0-100)", type=int)
		validation_proportion = 100 - train_proportion
		if train_proportion < 0 or train_proportion > 100:
			click.clear()
			click.echo("Please provide a valid amount. Choose a number between 0 and 100 to be assigned to training.")
			continue
		else:
			click.clear()
			c = click.prompt("{train} percent of the images will be moved to a train folder, while {valid} percent of the remaining images will be stored in a validation folder. Is that ok? [Y/n]".format(train=train_proportion, valid=validation_proportion))
			if c.lower() == 'y':
				# TODO: Implement a method that distributes de dataset among train/valid
				if not os.path.exists("dataset.yaml"):
					click.clear()
					click.echo("Dataset config file not found\nRun - idb init\n")
					exit(0)

				with open('dataset.yaml') as f:
					click.clear()
					click.echo(BANNER)
					data = yaml.load(f, Loader=yaml.FullLoader)
					split_dataset(data['DATASET_NAME'], train_proportion)
				click.echo("Done")
				break
			else:
				continue
		
	

if __name__ == "__main__":
	main()
