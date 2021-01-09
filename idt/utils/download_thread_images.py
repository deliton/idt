from idt.utils.download_images import download

__name__ = "download_thread_images"
def downloadThread(link, self):
    try:
        if(self.downloaded_images <= self.n_images):
            download(link, self.size, self.root_folder, self.folder, self.resize_method)
            self.downloaded_images += 1
        else:
            raise Exception("Exceed")
    except Exception as e:
        pass