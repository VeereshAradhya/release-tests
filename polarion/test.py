s = 'aaaabbbcccccccccdddddaaaaaaaaaaaaaaaa'

element = s[0]
length = 1
maxLength = 1
maxElement = element
for i in range(1, len(s)):
    if s[i] == element:
        length = length + 1
    else:
        element = s[i]
        length = 1
    if length > maxLength:
        maxLength = length
        maxElement = s[i]
print(maxElement * maxLength)
