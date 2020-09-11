# IDB - Image Dataset Builder

## Version 0.0.2 alpha

![idb](https://user-images.githubusercontent.com/47995046/92179763-be275d80-ee1b-11ea-8063-aa2b565616f6.png)


## Description

The image dataset builder is a CLI tool developed to make it easier and faster to create image datasets to be used for deep learning. The tool achieves this by scraping images from several search engines such as duckgo, bing and deviantart. IDB also optimizes the image dataset, although this feature is optional, the user can downscale and compress the images for optimal file size and dimensions. An example dataset created using idb that contains 23.688 files weights only 559,2MBs.

## Getting Started

The quickiest way to get started with IDB is running the simple "run" command. Just write in your facorite console something like:

```console
user@admin:~$ python3 main.py run -i apples 
```
This will quickly download 50 images of apples. By default it uses the duckgo search engne to do so. 
The run command accept the following options:
| Syntax | Description |
| ----------- | ----------- |
| Option | Meaning |
| **-i** or **--input** | the keyword to find the desired images. | 
| **-s** or **--size** | the amount of images to be downloaded. |
| **-e** or **--engine** | the desired search engine (options: duckgo, bing and flickr) |
| **-v** or **--verbose** | flag to activate verbose mode. |
| **-is** or **--image-size** | option to set the desired image size ratio. default=512 |

## Usage

While this project is still in pre-alpha, in order to test it, you need to clone this repository. Later, when it reaches a more mature, stable and advanced state, this project will be available to be downloaded through pip.

First of all, you need to install this project and its dependencies:

```console
user@admin:~$ git clone https://github.com/deliton/idb.git && cd idb
user@admin:~$ pip3 install -r requirements.txt
```

IDB requires a config file that tells it how your dataset should be organized. You can create it using the following command:

```console
user@admin:~$ python3 main.py init
```

This command will trigger the config file creator and will ask for the desired dataset parameters. In this example let's create a dataset containing images of your favorite cars.

```console
Insert a name to your dataset: : My favorite cars
```

The first parameters this command will ask is what name should your dataset have? In this example, let's name our dataset "My favorite cars"

Then the tool will ask how many samples per search are required to mount your dataset. In order to build a good dataset for deep learning, many images are required and since we're using a search engine to scrape images, many searches with different keywords are required to mount a good sized dataset. This value will correspond to how many images should be downloaded at every search. In this example we need a dataset with 250 images in each class, and we'll use 5 keywords to mount each class. So if we type the number 50 here, IDB will download 50 images of every keyword provided. If we provide 5 keywords we should get the required 250 images.

```console
How many samples per seach will be necessary?  : 50
```

The tool will now ask for and image size ratio. Since using large images to train neural networks are not viable, we can optionally choose one of the following image size ratios and scale down our images to that size. In this example, we'll go for 512x512, although 256x256 would be an even better option for this task.

```console
Choose images resolution:

[1] 512 pixels / 512 pixels (recommended)
[2] 1024 pixels / 1024 pixels
[3] 256 pixels / 256 pixels
[4] 128 pixels / 128 pixels
[5] Keep original image size

ps: note that the aspect ratio of the image will not be changed, so possibly the images received will have slightly different size

What is the desired image size ratio: 1
```

Afterwards, you'll be asked to choose between one of the search engines available. In this example, we'll use DuckGO to search images for us.

```console
Choose a search engine:

[1] Duck GO (recommended)
[2] Bing

Select option:: 1
```

And then choose "No" for verbose mode

```console
Activate verbose mode? [Y/n]: : n
```

Now you must choose how many classes/folders your dataset should have. In this example, this part can be very personal, but my favorite cars are: Chevrolet Impala, Range Rover Evoque, Tesla Model X and (why not) AvtoVAZ Lada. So in this case we have 4 classes, one for each favorite.

```console
How many image classes are required? : 4
```

Now we have to do some repetitive form filling. We must name each class and all the keywords that will be used to find the images. Note that this part can be later changed by your own code, to generate more classes and keywords.

```console
Class 1 name: : Chevrolet Impala
```

After typing the first class name, we'll be asked to provide all the keywords to find the dataset. Remember that we tld the program to download 50 images of each keyword so we must provide 5 keywords in this case to get all 250 images. Each keyword MUST be separated by commas(,)

```console
In order to achieve better results, choose several keywords that will be provided to the search engine to find your class in different settings.

Example: 

Class Name: Pineapple
keywords: pineapple, pineapple fruit, ananas, abacaxi, pineapple drawing

Type in all keywords used to find your desired class, separated by commas: : Chevrolet Impala 1967 car photos, chevrolet impala on the road, chevrolet impala vintage car, chevrolet impala convertible 1961, chevrolet impala 1964 lowrider

```

Then repeat the process of filling class name and its keywords until you fill all the 4 classes required.

```console
Dataset YAML file has been created sucessfully. Now run idb build to mount your dataset!
```

Your dataset configuration file has been created. Now just rust the following command and see the magic happen:

```console
user@admin:~$ python3 main.py build
```

And wait while the dataset is being mounted:

```console
Creating Chevrolet Impala class
Downloading Chevrolet Impala 1967 car photos  [#########################-----------]   72%  00:00:12

```

At the end, all your images will be available in a folder with the dataset name. Also, a csv file with the dataset stats are also included in the dataset's root folder.

## Split image dataset for Deep Learning

Since deep learning often requires you to split your dataset into a subset of training/validation folders, this project can also do this for you! Just run:

```console
user@admin:~$ python3 main.py split
```

Now you must choose a train/valid proportion. In this example I've choosen that 70% of the images will be reserved for training, while the rest will be reserved to validation: 

```console
Choose the desired proportion of images of each class to be distributed in train/valid folders. What percentage of images should be distributed towards training? (0-100): 70

70 percent of the images will be moved to a train folder, while 30 percent of the remaining images will be stored in a validation folder. Is that ok? [Y/n]: y
```

And that's it! The dataset-split should now be found with the corresponding train/valid subdirectories.

## Issues

This project is being developed in my spare time and it still needs a lot of effort to be free of bugs. Pull requests and contributors are really apreciated, feel free to contribute in any way you can!

