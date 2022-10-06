from colorama import Fore

NO_OF_CHARS = 256

class BoyerMooreAlgorithm():
    def __init__(self, pattern):
        self.pattern = pattern
        self.shift_table = [-1] * NO_OF_CHARS
 
    # Fill the actual value of last occurrence
        for char in range(len(pattern)):
            self.shift_table[ord(pattern[char])] = char;

    def find_pattern(self, source, file = False, line_number = 0):
        source = " ".join(source)
        pattern_length = len(self.pattern)
        result = []
        source_index = 0
        while(source_index <= len(source) - pattern_length):
            j = pattern_length - 1
    
            '''
                Keep reducing index j of pattern while
                characters of pattern and text are matching
                at this shift source_index
            '''
            while j >= 0 and self.pattern[j] == source[source_index+j]:
                j -= 1
    
            '''
                If the pattern is present at current shift,
                then index j will become -1 after the above loop
            '''
            if j < 0:
                result.append(source_index)
                '''   
                    Shift the pattern so that the next character in text
                    aligns with the last occurrence of it in pattern.
                    The condition source_index + pattern_length < len(source) is necessary for the case when
                    pattern occurs at the end of text
                '''
                source_index += (pattern_length - self.shift_table[ord(source[source_index + pattern_length])] 
                                    if source_index + pattern_length < len(source) else 1)
            else:
                '''
                Shift the pattern so that the bad character in source text
                aligns with the last occurrence of it in pattern. The
                max function is used to make sure that we get a positive
                shift. We may get a negative shift if the last occurrence
                of bad character in pattern is on the right side of the
                current character.
                '''
                source_index += max(1, j - self.shift_table[ord(source[source_index+j])])

        if file and result != []:
            print(f"Line {line_number}: ", end = '')

        previos_index = 0
        for index in result:
            print(source[previos_index:index], end="")
            print(Fore.CYAN + source[index:index + len(self.pattern)] + Fore.RESET, end = "")
            previos_index = index + len(self.pattern)

        if result != []:
            print('\n')
