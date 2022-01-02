from csv import reader
def converter(port:int) -> str or None:
  return _getDico().get(port, None)  
    

def _getDico():
  with open('portsList.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    dico = {}
    for row in csv_reader:
        try:
          dico[int(row[1])] = row[0]
        except:
          pass
  return dico  


if __name__ == "__main__":
    print(converter(8080))