from google.cloud import documentai 

project_id = "astute-purpose-321514"
location = "us"
client = documentai.DocumentProcessorServiceClient()
parent = f"projects/{project_id}/locations/{location}"
response = client.list_processors(parent=parent)

for processor in response:
    print(f"Processor name: {processor.name}")
    print(f"Processor ID: {processor.name.split('/')[-1]}")
