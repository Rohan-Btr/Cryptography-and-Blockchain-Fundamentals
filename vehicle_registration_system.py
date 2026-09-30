import hashlib
import time

# BLOCK CLASS
class Block:
    def __init__(self, index, voter_id, vote, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.voter_id = voter_id
        self.vote = vote
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        value = (
            str(self.index)
            + str(self.timestamp)
            + str(self.voter_id)
            + str(self.vote)
            + str(self.previous_hash)
        )

        return hashlib.sha256(value.encode()).hexdigest()
# VOTER CLASS
class Voter:
    def __init__(self, voter_id, name):
        self.voter_id = voter_id
        self.name = name
        self.has_voted = False


# CANDIDATE CLASS
class Candidate:
    def __init__(self, candidate_id, name):
        self.candidate_id = candidate_id
        self.name = name


# BLOCKCHAIN CLASS

class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.voters = {}
        self.candidates = {}


    # Create Genesis Block
    

    def create_genesis_block(self):
        return Block(0, "GENESIS", "GENESIS", "0")

  
    # Get Latest Block
   

    def get_latest_block(self):
        return self.chain[-1]

    
    # Add Candidate
    

    def add_candidate(self, candidate_id, name):

        if candidate_id in self.candidates:
            print("\n❌ Candidate ID already exists.")
            return

        candidate = Candidate(candidate_id, name)
        self.candidates[candidate_id] = candidate

        print(f"\n✅ Candidate '{name}' added successfully.")

   
    # Add Voter
  

    def add_voter(self, voter_id, name):

        if voter_id in self.voters:
            print("\n❌ Voter ID already exists.")
            return

        voter = Voter(voter_id, name)
        self.voters[voter_id] = voter

        print(f"\n✅ Voter '{name}' added successfully.")

   
    # Cast Vote
    

    def cast_vote(self, voter_id, candidate_id):

        # Check voter
        if voter_id not in self.voters:
            print("\n❌ Voter not found.")
            return

        # Check candidate
        if candidate_id not in self.candidates:
            print("\n❌ Candidate not found.")
            return

        voter = self.voters[voter_id]

        # Prevent double voting
        if voter.has_voted:
            print("\n❌ This voter has already voted.")
            return

        # Get latest block
        latest_block = self.get_latest_block()

        # Create new block
        new_block = Block(
            len(self.chain),
            voter_id,
            candidate_id,
            latest_block.hash
        )

        # Add block to blockchain
        self.chain.append(new_block)

        # Mark voter as voted
        voter.has_voted = True

        candidate_name = self.candidates[candidate_id].name

        print(
            f"\n✅ Vote cast successfully!"
            f"\nVoter: {voter.name}"
            f"\nCandidate: {candidate_name}"
        )

    
    # Validate Blockchain
    

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check whether current block hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check whether previous hash is correctly linked
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

   
    # Count Votes
   

    def count_votes(self):

        results = {}

        # Initialize all candidates with 0 votes
        for candidate_id, candidate in self.candidates.items():
            results[candidate_id] = 0

        # Count votes from blockchain
        for block in self.chain[1:]:
            if block.vote in results:
                results[block.vote] += 1

        return results

   
    # Print Blockchain
    

    def print_blockchain(self):

        print("\n" + "=" * 60)
        print("                 BLOCKCHAIN")
        print("=" * 60)

        for block in self.chain:

            print(f"\nBlock #{block.index}")
            print("-" * 40)

            print(f"Timestamp     : {block.timestamp}")
            print(f"Voter ID      : {block.voter_id}")
            print(f"Vote          : {block.vote}")
            print(f"Previous Hash : {block.previous_hash}")
            print(f"Hash          : {block.hash}")

        print("\n" + "=" * 60)

   
    # Display Candidates
    

    def show_candidates(self):

        if not self.candidates:
            print("\n❌ No candidates available.")
            return

        print("\nCandidates:")
        print("-" * 30)

        for candidate_id, candidate in self.candidates.items():
            print(
                f"ID: {candidate_id} | "
                f"Name: {candidate.name}"
            )

   
    # Display Voters
    

    def show_voters(self):

        if not self.voters:
            print("\n❌ No voters registered.")
            return

        print("\nVoters:")
        print("-" * 30)

        for voter_id, voter in self.voters.items():

            status = "Voted" if voter.has_voted else "Not Voted"

            print(
                f"ID: {voter_id} | "
                f"Name: {voter.name} | "
                f"Status: {status}"
            )

  
    # Display Vote Results
    

    def show_results(self):

        results = self.count_votes()

        print("\n" + "=" * 40)
        print("             VOTE RESULTS")
        print("=" * 40)

        for candidate_id, count in results.items():

            candidate = self.candidates[candidate_id]

            print(
                f"{candidate.name} "
                f"(ID: {candidate_id}) : {count} vote(s)"
            )



# MENU


def main():

    blockchain = Blockchain()

    while True:

        print("\n")
        print("=" * 50)
        print("       VOTING MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Add Candidate")
        print("2. Add Voter")
        print("3. Cast Vote")
        print("4. Print Blockchain")
        print("5. Validate Chain")
        print("6. Show Vote Results")
        print("7. Show Candidates")
        print("8. Show Voters")
        print("9. Exit")

        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        
        # Add Candidate
      

        if choice == "1":

            candidate_id = input("Enter Candidate ID: ").strip()
            name = input("Enter Candidate Name: ").strip()

            if not candidate_id or not name:
                print("\n❌ Candidate ID and name cannot be empty.")
                continue

            blockchain.add_candidate(candidate_id, name)

        
        # Add Voter
       

        elif choice == "2":

            voter_id = input("Enter Voter ID: ").strip()
            name = input("Enter Voter Name: ").strip()

            if not voter_id or not name:
                print("\n❌ Voter ID and name cannot be empty.")
                continue

            blockchain.add_voter(voter_id, name)

       
        # Cast Vote
       

        elif choice == "3":

            if not blockchain.voters:
                print("\n❌ No voters registered.")
                continue

            if not blockchain.candidates:
                print("\n❌ No candidates registered.")
                continue

            blockchain.show_candidates()

            voter_id = input("\nEnter Voter ID: ").strip()
            candidate_id = input("Enter Candidate ID: ").strip()

            blockchain.cast_vote(voter_id, candidate_id)

        
        # Print Blockchain
        

        elif choice == "4":

            blockchain.print_blockchain()

        
        # Validate Chain
        

        elif choice == "5":

            if blockchain.is_chain_valid():
                print("\n✅ Blockchain is valid.")
            else:
                print("\n❌ Blockchain has been tampered with!")

        
        # Show Results
        

        elif choice == "6":

            blockchain.show_results()

        
        # Show Candidates
       

        elif choice == "7":

            blockchain.show_candidates()

       
        # Show Voters
        

        elif choice == "8":

            blockchain.show_voters()

        
        # Exit
        

        elif choice == "9":

            print("\nThank you for using the Voting Management System.")
            print("Goodbye! 👋")
            break

        
        # Invalid Choice
        

        else:

            print("\n❌ Invalid choice. Please select a valid option.")



# PROGRAM START


if __name__ == "__main__":
    main()
