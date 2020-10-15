import os
import click
import yaml
import rich
from rich.console import Console

from idt.factories import SearchEngineFactory
from idt.utils.remove_corrupt import remove_corrupt
from idt.utils.create_dataset_csv import create_dataset_csv
from idt.utils.split_dataset import split_dataset

BANNER = """
[bold blue]=====================================================================


                             
                8888888 8888888b. 88888888888 
                  888   888  "Y88b    888     
                  888   888    888    888     
                  888   888    888    888     
                  888   888    888    888     
                  888   888    888    888     
                  888   888  .d88P    888     
                8888888 8888888P"     888  
                                           
          		[italic]IMAGE DATASET TOOL V0.4[/italic]                                                                                    
                                                                                                                                 
=====================================================================[/bold blue]                                                                                                                                
		"""

#@click.command()
@click.group()
def main():
    
    """
    Image Dataset Builder CLI to create amazing datasets
    """
    pass

@main.command()
def version():
	"""
	Shows what version idt is currently on
	"""
	click.clear()
	rich.print("[bold magenta]Image Dataset Tool (IDT)[/bold magenta] version 0.0.3 alpha")

@main.command()
def authors():
	"""
	Shows who are the creators of IDT
	"""
	click.clear()
	rich.print("[bold]IDT[/bold] was initially made by [bold magenta]Deliton Junior[/bold magenta] and [bold red]Misael Kelviny[/bold red]")

@main.command()
@click.option('--input', '-i','--i', help="The name of the thing you want to download")
@click.option('--size', '-s','--s', default=50, help="The number of images you want to download.")
@click.option('--engine', '-e','--e', default="duckgo", help="What search engine will be used to find your images")
@click.option('--verbose', '-v','--v', is_flag=False, help="Display additional logs")
@click.option('--imagesize', '-is','--is', default=512, help="What image size ratio should be applied to your dataset")
@click.option('--api-key', '-ak','--ak', default=None, help="Provide an api-key for the engines that require one")
def run(input, size, engine, verbose, imagesize, api_key):
	"""
	This command executes a single search and downloads it
	"""
	engine_list = ['duckgo', 'bing', 'bing_api', 'flickr_api']
	click.clear()

	if input and engine in engine_list:
		factory = SearchEngineFactory(input,size,input,verbose,"dataset",imagesize, engine, api_key)
		# Remove corrupt files
		remove_corrupt("dataset")

	else:
		rich.print("Please provide a valid name")

@main.command()
@click.option('--default', '-d','--d', is_flag=True,default=False, help="Generate a default config file")
def init(default):
	"""
	This command initialyzes idt and creates a dataset config file
	"""
	console = Console()
	console.clear()

	if default:
		document_dict = {
			"DATASET_NAME": "dataset",
			"SAMPLES_PER_SEARCH": "50",
			"IMAGE_SIZE": 512,
			"ENGINE": "duckgo",
			"VERBOSE": "n",
			"CLASSES": [{"CLASS_NAME": "Test", "SEARCH_KEYWORDS": "images of cats"}]}

		if not os.path.exists("dataset.yaml"):
			console.print("[bold]Creating a dataset configuration file...[/bold]")
			
			f = open("dataset.yaml", "w")
			f.write(yaml.dump(document_dict))
			if f:
				console.clear()
				console.print("Dataset YAML file has been created sucessfully. Now run [bold blue]idt build[/bold blue] to mount your dataset!")
				exit(0)
			
		
		else:
			console.print("[red]A dataset.yaml is already created. To use another one, delete the current dataset.yaml file[/red]")
			exit(0)

	console.print(BANNER)
	dataset_name = click.prompt("Insert a name to your dataset: ")

	console.clear()
	samples = click.prompt("How many samples per seach will be necessary?  ",type=int)

	console.clear()
	console.print("[bold]Choose image resolution[/bold]", justify="center")
	console.print("""

[1] 512 pixels / 512 pixels [bold blue](recommended)[/bold blue]
[2] 1024 pixels / 1024 pixels
[3] 256 pixels / 256 pixels
[4] 128 pixels / 128 pixels
[5] Keep original image size

[italic]ps: note that the aspect ratio of the image will [bold]not[/bold] be changed, so possibly the images received will have slightly different size[/italic]
		
		""")


	image_size_ratio = click.prompt("What is the desired image size ratio", type=int)
	while image_size_ratio < 1 or image_size_ratio > 5:
		console.print("[italic red]Invalid option, please choose between 1 and 5. [/italic red]")
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

	console.clear()
	verbose = click.prompt("Activate verbose mode? [Y/n]: ")
	while verbose.lower() != "y" and verbose.lower() != "n":
		console.print("[red]Invalid option[/red]")
		verbose = click.prompt("[Y/n]: ")

	console.clear()
	number_of_classes = click.prompt("How many image classes are required? ",type=int)

	document_dict = {
  
    "DATASET_NAME": dataset_name,
  
    "SAMPLES_PER_SEARCH": samples,
 
    "IMAGE_SIZE": image_size_ratio,
  
    "VERBOSE": verbose,
  
    "CLASSES": []
  
}

	console.clear()
	console.print("[bold]Choose a search engine[/bold]", justify="center")
	console.print("""

[1] Duck GO [bold blue](recommended)[/bold blue]
[2] Bing
[3] Bing API [italic yellow](Requires API key)[/italic yellow]
[4] Flickr API [italic yellow](Requires API key)[/italic yellow]

		""")
	search_engine= click.prompt("Select option:", type=int)
	while search_engine < 0 or search_engine > 4:
		console.print("[italic red]Invalid option, please choose between 1 and 4.[/italic red]")
		search_engine = click.prompt("\nOption: ", type=int)

	search_options = ['none', 'duckgo', 'bing', 'bing_api', 'flickr_api']
	document_dict['ENGINE'] = search_options[search_engine]

	if search_engine > 2:
		console.clear()
		console.print(f'Insert your [bold blue]{search_options[search_engine]}[/bold blue] API key')
		engine_api_key = click.prompt("API key: ", type=str)
		document_dict['API_KEY'] = engine_api_key
	else:
		document_dict['API_KEY'] = "NONE"

	search_engine = search_options[search_engine]

	for x in range(number_of_classes):
		console.clear()
		class_name = click.prompt("Class {x} name: ".format(x=x+1))
		console.clear()

		console.print("""In order to achieve better results, choose several keywords that will be provided to the search engine to find your class in different settings.
	
[bold blue]Example: [/bold blue]

Class Name: [bold yellow]Pineapple[/bold yellow]
[italic]keywords[/italic]: [underline]pineapple, pineapple fruit, ananas, abacaxi, pineapple drawing[/underline]

			""")
		keywords = click.prompt("Type in all keywords used to find your desired class, separated by commas: ")
		document_dict['CLASSES'].append({'CLASS_NAME': class_name, 'SEARCH_KEYWORDS': keywords})
    
	if not os.path.exists("dataset.yaml"):
		console.print("[bold]Creating a dataset configuration file...[/bold]")
		try:
			f = open("dataset.yaml", "w")
			f.write(yaml.dump(document_dict))
			if f:
				console.clear()
				console.print("Dataset YAML file has been created sucessfully. Now run [bold blue]idt build[/bold blue] to mount your dataset!")
		except:
			console.print("[red]Unable to create file. Please check permission[/red]")
		
	else:
		console.print("[red]A dataset.yaml is already created. To use another one, delete the current dataset.yaml file[/red]")

@main.command()
def build():
	"""
	This command mounts the dataset
	"""
	console = Console()
	console.clear()
	console.print(BANNER)
	if not os.path.exists("dataset.yaml"):
		click.clear()
		console.print("Dataset config file not found\nRun - idt init\n")
		exit(0)

	with open('dataset.yaml') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)
	
	click.clear()
	console.print("Building [bold blue]{dataset_name}[/bold blue] dataset...\n".format(dataset_name=data['DATASET_NAME']))
	for classes in data['CLASSES']:
		click.clear()
		console.print('Creating [bold blue]{name} class[/bold blue] \n'.format(name=classes['CLASS_NAME']))
		search_list = classes['SEARCH_KEYWORDS'].split(",")
		for keywords in search_list:
			factory = SearchEngineFactory(keywords,data['SAMPLES_PER_SEARCH'],classes['CLASS_NAME'],data['VERBOSE'], data['DATASET_NAME'],data['IMAGE_SIZE'], data['ENGINE'],data['API_KEY'])
	# Remove corrupt files
	remove_corrupt(data['DATASET_NAME'])

	# Create a CSV with dataset info
	create_dataset_csv(data['DATASET_NAME'])
	click.clear()
	console.print("Dataset READY!")

@main.command()
def split():
	"""
	Split dataset into train/valid folders
	"""
	console = Console()
	while True:
		click.clear()
		console.print(BANNER)
		console.print("Choose the desired proportion of images of each class to be distributed in train/valid folders. [bold]What percentage of images should be distributed towards training?[/bold] ")
		train_proportion = click.prompt("(0-100)", type=int)
		validation_proportion = 100 - train_proportion
		if train_proportion < 0 or train_proportion > 100:
			click.clear()
			console.print("[red]Please provide a valid amount. Choose a number between 0 and 100 to be assigned to training.[/red]")
			continue
		else:
			click.clear()
			console.print("[bold blue]{train} percent[/bold blue] of the images will be moved to a [bold yellow]train[/bold yellow] folder, while [bold blue]{valid} percent [/bold blue] of the remaining images will be stored in a [bold yellow]validation[/bold yellow] folder.".format(train=train_proportion, valid=validation_proportion))
			c= click.prompt("Is that ok? [Y/n]")
			if c.lower() == 'y':
				if not os.path.exists("dataset.yaml"):
					click.clear()
					console.print("Dataset config file not found\nRun - [bold blue]idt init[/bold blue]")
					exit(0)

				with open('dataset.yaml') as f:
					click.clear()
					console.print("[italic]Copying files to the train/valid folders. Please wait...[/italic]")
					data = yaml.load(f, Loader=yaml.FullLoader)
					split_dataset(data['DATASET_NAME'], train_proportion)
				console.clear()
				console.print("[bold blue]Done[/bold blue]")
				break
			else:
				continue
		
	

if __name__ == "__main__":
	main()
