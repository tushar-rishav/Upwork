import csv  # Python module to parse csv files

def main():
    
    # 'data' stores file name and keyword that user enters as menu options. 
    data = {
    'file': None,
    'keyword': set()
    }
    # Store 1 or 0 depending on if user wants to try again or not
    tryAgain = 1
    
    # Keep iterating until user asks to stop.

    while True:
        # Print menu options
        print "1. Input file"
        print "2. Input keyword file"
        

        try:
            # Read menu options
            option = int(raw_input("Provide required option from the above options: "))
        except Exception as e:
            print e
            continue; # Restart from menu
            # Whenever user enters something wrong, we print the error and reprint the menu.
            # `contiinue` basically continues with the next iteration.
            # For example see http://stackoverflow.com/a/23470680/3673031

        if option == 2:
            # Search for keyword only if the file has been provided by user before.
            # If the file hasn't been provided by user, then it makes no sense to search for keyword
            if data['file'] is not None:
                keywordFile = raw_input("You've chosen 2nd option. Provide keyword file: ")
                with open(keywordFile, 'r') as fp:
                    for key in fp:
                        data['keyword'].add(key) # Store the keys extracted from keyword file
                results = []
                
                try:
                    with open(data['file'], 'r') as fp:
                        # Open file and parse for csv
                        lines = csv.reader(fp)
                        for line in lines:
                            # Create a sentence to be able to search for a keyword in line.
                            line_string = ''.join(line)
                            for key in data['keyword']: # For each keyword search in line
                                if key in line_string:
                                    # If the keyword is found in a line then store the line.
                                    results.append(line[:10])

                    # Print table heading
                    print '+{:<50}| {:<50}  | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50}+'.format("Date received",
                                                          "Product",
                                                          "Sub-product",
                                                          "Issue",
                                                          "Sub-issue",
                                                          "Consumer complaint narrative",
                                                          "Company public response",
                                                          "Company",
                                                          "State",
                                                          "ZIP code")
                    print '{:=^150}'.format("")

                    # Print results iff at least one match for keywords is found
                    if results is not None:
                        for result in results:
                            print '+{:<50}| {:<50}  | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50} | {:<50}+'.format(result[0],
                                                                    result[1],
                                                                    result[2],
                                                                    result[3],
                                                                    result[4],
                                                                    result[5],
                                                                    result[6],
                                                                    result[7],
                                                                    result[8],
                                                                    result[9])
                    else:
                        print 'No match found for the given keyword'

                except Exception as e:
                    print(e)



            else:
                print "You must provide an Input file at least once prior selecting option 2."

        elif option == 1:
            # For option one read the file name from user.
            # Store the given filename to data['file']
            try:
                data['file'] = raw_input("You've chosen 1st option. Provide input file: ")
            except Exception as e:
                print(e)
        else:
            print "Invalid choice"
            continue; # Restart with listing menu


        try:
            # Ask user if it wants to try again.
            # 0 for No and 1 for Yes
            tryAgain = int(raw_input("Want to try again? 0 for No and 1 for Yes: "))
            if not tryAgain:
                break
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()