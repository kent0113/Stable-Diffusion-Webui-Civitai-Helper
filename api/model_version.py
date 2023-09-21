class ModelVersion:
    def __init__(self, model_path, model_id, model_name, new_version_id, new_version_name, description, download_url,
                 img_url):
        self.model_path = model_path
        self.model_id = model_id
        self.model_name = model_name
        self.new_version_id = new_version_id
        self.new_version_name = new_version_name
        self.description = description
        self.download_url = download_url
        self.img_url = img_url
