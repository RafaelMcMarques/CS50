import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Incorrect usage")
        exit(1)

    # Read database file into a variable
    with open(sys.argv[1]) as csvFile:
        dataBase = csv.DictReader(csvFile)

        # Read DNA sequence file into a variable'
        with open(sys.argv[2]) as dnaSeqFile:
            dnaSeq = dnaSeqFile.read()

            # Find longest match of each STR in DNA sequence
            dnaSubSeqs = {}
            for subSeq in dataBase.fieldnames:
                if subSeq != "name":
                    dnaSubSeqs[subSeq] = longest_match(dnaSeq, subSeq)

            # Check database for matching profiles
            found = False
            for person in dataBase:
                if found:
                    break
                found = True
                answer = person['name']
                for key in person.keys():
                    if (key != "name") and (int(person[key]) != int(dnaSubSeqs[key])):
                        found = False
    if found:
        print(answer)
    else:
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
