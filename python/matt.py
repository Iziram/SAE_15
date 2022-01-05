def transformationCsvDicoMetrique2(path:str):
    dico = {}
    
    with open(path, newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            interface : str = row[0]
            temps : int = int(row[3])
            
            port_proto : dict = {
                    row[1] : converter(row[2])
                }
            
            if interface in dico:
                if temps in dico[interface]:
                    dico[interface][temps][row[1]] = converter(row[2])
                else:
                    dico[interface][temps] = port_proto
            else:
                dico[interface] = {
                    temps:port_proto}
                
    return dico