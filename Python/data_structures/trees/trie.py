"""Trie (Prefix Tree) Implementation

A Trie is a tree-like data structure used to efficiently store and retrieve keys
in a dataset of strings. It's particularly useful for prefix-based search operations.

Time Complexity:
    - Insert: O(m) where m is the length of the word
    - Search: O(m) where m is the length of the word
    - StartsWith (prefix search): O(m) where m is the length of the prefix
    - Delete: O(m) where m is the length of the word

Space Complexity:
    - O(ALPHABET_SIZE * N * M) where N is number of words and M is average length
    - In worst case with no common prefixes: O(26 * N * M) for lowercase English

Author: Comet Assistant
Date: October 2025
"""


class TrieNode:
    """Node class for Trie data structure.
    
    Each node contains:
        - children: dictionary mapping characters to child nodes
        - is_end_of_word: boolean flag indicating if node marks end of a word
    """
    
    def __init__(self):
        """Initialize a TrieNode with empty children and is_end_of_word as False."""
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """Trie (Prefix Tree) data structure implementation.
    
    A Trie is a tree where each node represents a character, and paths from root
    to nodes represent prefixes or complete words.
    
    Attributes:
        root (TrieNode): The root node of the Trie
    """
    
    def __init__(self):
        """Initialize the Trie with an empty root node."""
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert a word into the Trie.
        
        Args:
            word (str): The word to insert into the Trie
            
        Time Complexity: O(m) where m is the length of the word
        Space Complexity: O(m) in worst case when no prefix exists
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.search("apple")
            True
        """
        node = self.root
        
        for char in word:
            # If character doesn't exist, create new node
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move to the next node
            node = node.children[char]
        
        # Mark the end of the word
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        """Search for a complete word in the Trie.
        
        Args:
            word (str): The word to search for
            
        Returns:
            bool: True if the word exists in the Trie, False otherwise
            
        Time Complexity: O(m) where m is the length of the word
        Space Complexity: O(1)
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.search("apple")
            True
            >>> trie.search("app")
            False
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        # Return True only if it's a complete word
        return node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the Trie starts with the given prefix.
        
        Args:
            prefix (str): The prefix to search for
            
        Returns:
            bool: True if any word starts with the prefix, False otherwise
            
        Time Complexity: O(m) where m is the length of the prefix
        Space Complexity: O(1)
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.starts_with("app")
            True
            >>> trie.starts_with("ban")
            False
        """
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def delete(self, word: str) -> bool:
        """Delete a word from the Trie.
        
        Args:
            word (str): The word to delete
            
        Returns:
            bool: True if word was deleted, False if word doesn't exist
            
        Time Complexity: O(m) where m is the length of the word
        Space Complexity: O(m) due to recursion stack
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.delete("apple")
            True
            >>> trie.search("apple")
            False
        """
        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            """Recursive helper function to delete a word.
            
            Args:
                node: Current node in the Trie
                word: Word to delete
                index: Current index in the word
                
            Returns:
                bool: True if current node should be deleted, False otherwise
            """
            # Base case: reached end of word
            if index == len(word):
                # Word doesn't exist
                if not node.is_end_of_word:
                    return False
                
                # Unmark the end of word
                node.is_end_of_word = False
                
                # Delete node if it has no children
                return len(node.children) == 0
            
            char = word[index]
            child_node = node.children.get(char)
            
            # Character doesn't exist
            if child_node is None:
                return False
            
            # Recursively delete in child
            should_delete_child = _delete_helper(child_node, word, index + 1)
            
            # Delete child node if needed
            if should_delete_child:
                del node.children[char]
                # Return True if current node has no children and is not end of another word
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        return not _delete_helper(self.root, word, 0) or self.search(word) is False
    
    def get_all_words_with_prefix(self, prefix: str) -> list:
        """Get all words in the Trie that start with the given prefix.
        
        Args:
            prefix (str): The prefix to search for
            
        Returns:
            list: List of all words with the given prefix
            
        Time Complexity: O(p + n) where p is prefix length and n is number of nodes in subtree
        Space Complexity: O(n) for storing results and recursion
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.insert("app")
            >>> trie.insert("application")
            >>> trie.get_all_words_with_prefix("app")
            ['app', 'apple', 'application']
        """
        def _get_all_words(node: TrieNode, current_word: str, words: list) -> None:
            """Recursive helper to collect all words from a node.
            
            Args:
                node: Current node in the Trie
                current_word: Word built so far
                words: List to store found words
            """
            if node.is_end_of_word:
                words.append(current_word)
            
            for char, child_node in node.children.items():
                _get_all_words(child_node, current_word + char, words)
        
        # Navigate to the prefix node
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this prefix
        words = []
        _get_all_words(node, prefix, words)
        return words
    
    def count_words(self) -> int:
        """Count the total number of words in the Trie.
        
        Returns:
            int: Total number of words stored
            
        Time Complexity: O(n) where n is total number of nodes
        Space Complexity: O(h) where h is height of trie (recursion stack)
        
        Example:
            >>> trie = Trie()
            >>> trie.insert("apple")
            >>> trie.insert("app")
            >>> trie.count_words()
            2
        """
        def _count_helper(node: TrieNode) -> int:
            count = 1 if node.is_end_of_word else 0
            for child in node.children.values():
                count += _count_helper(child)
            return count
        
        return _count_helper(self.root)


def main():
    """Example usage and demonstration of Trie operations."""
    print("=" * 60)
    print("Trie (Prefix Tree) Implementation Demo")
    print("=" * 60)
    
    # Create a new Trie
    trie = Trie()
    
    # Example 1: Basic Insert and Search
    print("\n1. Basic Insert and Search Operations:")
    print("-" * 40)
    words = ["apple", "app", "application", "apply", "banana", "band", "bandana"]
    print(f"Inserting words: {words}")
    for word in words:
        trie.insert(word)
    
    print(f"\nSearch 'apple': {trie.search('apple')}")
    print(f"Search 'app': {trie.search('app')}")
    print(f"Search 'appl': {trie.search('appl')}")
    print(f"Search 'orange': {trie.search('orange')}")
    
    # Example 2: Prefix Search
    print("\n2. Prefix Search (starts_with):")
    print("-" * 40)
    print(f"Starts with 'app': {trie.starts_with('app')}")
    print(f"Starts with 'ban': {trie.starts_with('ban')}")
    print(f"Starts with 'cat': {trie.starts_with('cat')}")
    
    # Example 3: Get all words with prefix
    print("\n3. Get All Words with Prefix:")
    print("-" * 40)
    print(f"Words with prefix 'app': {trie.get_all_words_with_prefix('app')}")
    print(f"Words with prefix 'ban': {trie.get_all_words_with_prefix('ban')}")
    print(f"Words with prefix 'a': {trie.get_all_words_with_prefix('a')}")
    
    # Example 4: Count words
    print("\n4. Count Total Words:")
    print("-" * 40)
    print(f"Total words in Trie: {trie.count_words()}")
    
    # Example 5: Delete operations
    print("\n5. Delete Operations:")
    print("-" * 40)
    print(f"Delete 'app': {trie.delete('app')}")
    print(f"Search 'app' after deletion: {trie.search('app')}")
    print(f"Search 'apple' after deleting 'app': {trie.search('apple')}")
    print(f"Total words after deletion: {trie.count_words()}")
    
    # Example 6: Autocomplete use case
    print("\n6. Autocomplete Use Case:")
    print("-" * 40)
    autocomplete_trie = Trie()
    search_history = ["python", "programming", "program", "programmer", 
                      "project", "proxy", "process"]
    for term in search_history:
        autocomplete_trie.insert(term)
    
    prefix = "pro"
    suggestions = autocomplete_trie.get_all_words_with_prefix(prefix)
    print(f"Autocomplete suggestions for '{prefix}': {suggestions}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
