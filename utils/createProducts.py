from pyairtable import Table
from mdutils.mdutils import MdUtils
from datetime import date
import markdown

## fetch airtable
airtable_api_key = 'keyiwDP2050hwqBso'
table = Table(airtable_api_key, 'appBIo9dduk5tP7gE', 'tblbweRinfoFzeKjS')

## create markdown file
def createMD(record): 
  date = record['Scheduled for']
  name = record['Name']
  external_url = record['External_Url']
  description = record['Description']
  tags= record['Tags']
  image_url= record["Logo"][0]['url']
  github= record['Github']
  
  mdFile = MdUtils(file_name=date+"_"+name,title="---")
  mdFile.new_line(f'date: {date}')
  mdFile.new_line("---")
  mdFile.create_md_file()

  output = markdown.markdown(f"""
          ---
          date: {date}
          layout: product
          name: {name}
          description: {description}
          image: {image_url}
          external_url: {external_url}
          github: {github}
          tags: {tags}
          ---
          """)
  return(output)


for records in table.iterate(page_size=100, max_records=1000):
    for record in records:
      if record['fields']['Status'] == "Ready":
        today = str(date.today())
        if record['fields']['Scheduled for'] == today:
          print(createMD(record['fields']))