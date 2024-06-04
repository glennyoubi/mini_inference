import json
import time

from fontTools.ttLib.tables.TupleVariation import INTERMEDIATE_REGION

import json_converter
import my_utils
import relation_links_id_name
import reqs



def type_of_inference_by_relation(relation):
    # This function give which type of inference we should do due to the relation enter by the user

    pass

def deduction(json_data_term_one, json_data_term_two,target_type_one, target_type_two,term_1, term_2, relation1):
    filtered_data = {}
    find = False
    i = 0
    f = 100
    #while not find:
    if len(json_data_term_one)==0 or len(json_data_term_two)==0:
        return find
    for key1 in json_data_term_one:
        #print(f"Key: {key}")
        #print(json_data_term_one[key])  # Printing the value associated with the key

        # Get elements of the node
        for item1 in json_data_term_one[key1]:
            
            itm_term_one = item1
            rid_term_one = item1.get('rid')
            node1_term_one = item1.get('node1')
            node2_term_one = item1.get('node2')
            type_term_one = item1.get('type')
            w_term_one = item1.get('w')
        time.sleep(1)
        mid_node_name = reqs.get_node_name_by_eid(node2_term_one, term_1, relation_links_id_name.rels_use.index(relation1))
        #print(f"Mid  node : {mid_node_name}")
        #print("First loop")
        i+=1
        #print(i)
        # Check if the node extract have the good relation and the weight above or equals to 0
        if (type_term_one) == str(target_type_one) and '-' not in w_term_one and mid_node_name != term_1 and mid_node_name != term_2:
            for key2 in json_data_term_two:
                #print("Second loop")
                #print(f"Key: {key}")
                #print(json_data_term_two[key])  # Printing the value associated with the key
                f+=1
                #print(f)
                    # Get elements of the node
                for item2 in json_data_term_two[key2]:
                        itm_term_two = item2
                        rid_term_two = item2.get('rid')
                        node1_term_two = item2.get('node1')
                        node2_term_two = item2.get('node2')
                        type_term_two = item2.get('type')
                        w_term_two = item2.get('w')

                if node2_term_one == node1_term_two and type_term_two == str(target_type_two):
                    #find = True
                    return (term_1, target_type_one, mid_node_name, target_type_two, term_2, w_term_one, w_term_two, node2_term_one)
                    #mid_node_name = reqs.get_node_name_by_eid(json_data_term_one[key]['node2'])
        # If you want to access the values within the list, you can do this         
    return find



if __name__ == '__main__':
    print()
    print('----------------Les noms des relations et des termes doivent écris en miniscule----------------')
    
    term_one = input("Enter the first term : ")
    term_two = input("Enter the second term : ")
    relation = input("Enter the relation : ")

    # We took the id of the relation
    relation_id = relation_links_id_name.rels_use.index(relation)

    # We take what type of inference we should do 
    inferences_to_do = relation_links_id_name.relations[relation]
    # We start the timer
    full_process_start = time.time()


    # Transitivity
    if "Transitive" in inferences_to_do:
        reqs.get_jdm_page(term_one, relation_id)
        reqs.get_jdm_page(term_two, relation_id)
        #reqs.get_jdm_page(term_one)
        #reqs.get_jdm_page(term_two)

        ## Loading relations files 
        with open(f'./words/relations/{term_one}_relations_sortantes_{relation_id}.json', 'r') as f:
            data_term_one = json.load(f)
        
        with open(f'./words/relations/{term_two}_relations_entrantes_{relation_id}.json', 'r') as f:
            data_term_two = json.load(f)
        
        ## Types d'inférences

        ## Déduction
        print('-----------------------------------------START----------------------------------------------')
        res_deduction = deduction(data_term_one, data_term_two, relation_id, relation_id, term_one, term_two, relation)
        if res_deduction !=  False:
            term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
            w_final = (int(w1r1) + int(w2r2))/2
            print(f"Oui car {term_1} {relation} {mid_node_name} et {mid_node_name} {relation} {term2}")
            print(f"Avec un poids de {w_final}")
        else:
            print("Aucune inférence n'a été trouvée !")
        print('-----------------------------------------END-------------------------------------------------')
    

    # Transitivity
    if "r_has_part" in inferences_to_do:
        r_one = relation_links_id_name.rels_use.index('r_isa')
        reqs.get_jdm_page(term_one, relation_id)
        reqs.get_jdm_page(term_two, r_one)
        #reqs.get_jdm_page(term_one)
        #reqs.get_jdm_page(term_two)

        ## Loading relations files 
        with open(f'./words/relations/{term_one}_relations_sortantes_{relation_id}.json', 'r') as f:
            data_term_one = json.load(f)
        
        with open(f'./words/relations/{term_two}_relations_entrantes_{r_one}.json', 'r') as f:
            data_term_two = json.load(f)
        
        ## Types d'inférences

        ## Déduction
        print('-----------------------------------------START----------------------------------------------')
        res_deduction = deduction(data_term_two, data_term_one, r_one, relation_id, term_one, term_two, 'r_isa')
        if res_deduction !=  False:
            term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
            w_final = (int(w1r1) + int(w2r2))/2
            print(f"Oui car {term_1} r_isa {mid_node_name} et {mid_node_name} {relation} {term2}")
            print(f"Avec un poids de {w_final}")
        else:
            print('---------------------------------------PHASE 2----------------------------------------------')
            reqs.get_jdm_page(term_two, relation_id)
            with open(f'./words/relations/{term_one}_relations_sortantes_{relation_id}.json', 'r') as f:
                data_term_one = json.load(f)
            res_deduction_2 = deduction( data_term_one, data_term_two,relation_id, relation_id, term_one, term_two, relation)
            if res_deduction_2 !=  False:
                term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
                w_final = (int(w1r1) + int(w2r2))/2
                print(f"Oui car {term_1} r_isa {mid_node_name} et {mid_node_name} {relation} {term2}")
                print(f"Avec un poids de {w_final}")
            else:
                print("Aucune inférence n'a été trouvée !")
        print('-----------------------------------------END-------------------------------------------------')



    ## r-agent-1
    if relation == 'r_agent-1' or relation=='r_patient':
        r_one = relation_links_id_name.rels_use.index('r_isa')
        reqs.get_jdm_page(term_one, r_one)
        reqs.get_jdm_page(term_two, relation_id)
        #reqs.get_jdm_page(term_one)
        #reqs.get_jdm_page(term_two)

        ## Loading relations files 
        with open(f'./words/relations/{term_one}_relations_sortantes_{r_one}.json', 'r') as f:
            data_term_one = json.load(f)
        
        with open(f'./words/relations/{term_two}_relations_entrantes_{relation_id}.json', 'r') as f:
            data_term_two = json.load(f)
        
        ## Types d'inférences

        ## Déduction
        print('-----------------------------------------START----------------------------------------------')
        res_deduction = deduction(data_term_one, data_term_two, r_one, relation_id, term_one, term_two, 'r_isa')
        if res_deduction !=  False:
            term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
            w_final = (int(w1r1) + int(w2r2))/2
            print(f"Oui car {term_1} r_isa {mid_node_name} et {mid_node_name} {relation} {term2}")
            print(f"{w1r1} et {w2r2}")
            print(f"Avec un poids de {w_final}")
        else:
            print("Aucune inférence n'a été trouvée !")
        print('-----------------------------------------END-------------------------------------------------')



        ## r-isa
    if relation == 'r_isa':
        reqs.get_jdm_page(term_one, relation_id)
        reqs.get_jdm_page(term_two, relation_id)
        #reqs.get_jdm_page(term_one)
        #reqs.get_jdm_page(term_two)

        ## Loading relations files 
        with open(f'./words/relations/{term_one}_relations_sortantes_{relation_id}.json', 'r') as f:
            data_term_one = json.load(f)
        
        with open(f'./words/relations/{term_two}_relations_entrantes_{relation_id}.json', 'r') as f:
            data_term_two = json.load(f)
        
        ## Types d'inférences

        ## Déduction
        print('-----------------------------------------START----------------------------------------------')
        res_deduction = deduction(data_term_one, data_term_two, relation_id, relation_id, term_one, term_two, relation)
        if res_deduction !=  False:
            term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
            w_final = (int(w1r1) + int(w2r2))/2
            print(f"Oui car {term_1} {relation} {mid_node_name} et {mid_node_name} {relation} {term2}")
            print(f"Avec un poids de {w_final} sachant que {term_1} {relation} {mid_node_name} a pour poids {w1r1} et {mid_node_name} {relation} {term2} a pour poids {w2r2}")
        else:
            print("Aucune inférence n'a été trouvée !")
        print('-----------------------------------------END-------------------------------------------------')
    
    ## r_carac
    if relation == 'r_carac':
        r_one = relation_links_id_name.rels_use.index('r_isa')
        reqs.get_jdm_page(term_one, r_one)
        reqs.get_jdm_page(term_two, relation_id)
        #reqs.get_jdm_page(term_one)
        #reqs.get_jdm_page(term_two)

        ## Loading relations files 
        with open(f'./words/relations/{term_one}_relations_sortantes_{r_one}.json', 'r') as f:
            data_term_one = json.load(f)
        
        with open(f'./words/relations/{term_two}_relations_entrantes_{relation_id}.json', 'r') as f:
            data_term_two = json.load(f)
        
        ## Types d'inférences

        ## Déduction
        print('-----------------------------------------START----------------------------------------------')
        res_deduction = deduction(data_term_one, data_term_two, r_one, relation_id, term_one, term_two, 'r_isa')
        if res_deduction !=  False:
            term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
            w_final = (int(w1r1) + int(w2r2))/2
            print(f"Oui car {term_1} r_isa {mid_node_name} et {mid_node_name} {relation} {term2}")
            print(f"Avec un poids de {w_final}")
        else:
            print('---------------------------------------PHASE 2----------------------------------------------')
            reqs.get_jdm_page(term_one, relation_id)
            with open(f'./words/relations/{term_one}_relations_sortantes_{relation_id}.json', 'r') as f:
                data_term_one = json.load(f)
            res_deduction_2 = deduction(data_term_one, data_term_two, relation_id, relation_id, term_one, term_two, relation)
            if res_deduction_2 !=  False:
                term_1, r1, mid_node_name, r2, term2, w1r1, w2r2, mid_node_eid = res_deduction
                w_final = (int(w1r1) + int(w2r2))/2
                print(f"Oui car {term_1} r_isa {mid_node_name} et {mid_node_name} {relation} {term2}")
                print(f"Avec un poids de {w_final}")
            else:
                print("Aucune inférence n'a été trouvée !")
        print('-----------------------------------------END-------------------------------------------------')








    full_process_end   = time.time()
    process_time = full_process_end - full_process_start
    print(f'EXECUTION TIME IS : {process_time}')
    print('-----------------------------------------------------------------------------------------------')

