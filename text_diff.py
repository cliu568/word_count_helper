
# coding: utf-8

# In[59]:

import numpy as np
def is_char(c):
    d = c - 'a'
    if(d >=0 and d<=25):
        return True
    d = c - 'A'
    if(d>=0 and d <=25):
        return True
    return False

def parse(s):
    words = []
    l = len(s)
    curr = 0
    for i in range(l):
        if(s[i] ==' '):
            if(s[curr:i] != ''):
                words.append(s[curr:i])
            curr = i+1
    if(curr < l):
        words.append(s[curr:l])
        
    return words

    



# In[47]:

def diff(s1,s2):
    l1 = len(s1)
    l2 = len(s2)
    dp = np.zeros((l1+5,l2+5))
    operations = [['' for i in range(l2+5)] for j in range(l1+5)]
    for i in range(l1):
        dp[i][l2] = l1 - i 
        operations[i][l2] = '-'+ s1[i]
        
    for j in range(l2):
        dp[l1][j] = l2 - j
        operations[l1][j] = '+' + s2[j]
    
    for i in range(l1):
        for j in range(l2):
            if(s1[l1-i-1] == s2[l2-j-1]):
                case_equal = dp[l1-i][l2-j]
            else:
                case_equal = l1 + l2 + 10
            case_insert = dp[l1-i-1][l2-j] + 1
            case_delete = dp[l1 - i ][l2 - j - 1 ] + 1
            
            
            if(case_equal == min(case_equal, case_insert, case_delete)):
                dp[l1-i-1][l2-j-1] = case_equal
                operations[l1-i-1][l2-j-1] = s1[l1-i-1]
                
            if(case_insert == min(case_equal, case_insert, case_delete)):
                dp[l1-i-1][l2-j-1] = case_insert
                operations[l1-i-1][l2-j-1] = '+' + s2[l2-j-1]
                
            if(case_delete == min(case_equal, case_insert, case_delete)):
                dp[l1-i-1][l2-j-1] = case_delete
                operations[l1-i-1][l2-j-1] = '-'+s1[l1-i-1]
                
                
    i = 0
    j = 0
    output = '%'
    while(i < l1 or j < l2):
        
        output += operations[i][j]
        output += "%"
        
            
        if(operations[i][j][0] =='-'):
            i += 1
            
        elif(operations[i][j][0] == '+'):
            j += 1
        
        else:
            i += 1
            j += 1
            
            
    return (output, dp[0][0],operations)
                
        

def filter_sentences(s1,s2):
    sentences1 = s1.split('.')
    sentences2 = s2.split('.')
    if(s1.endswith('.')):
        sentences1.pop()
    if(s2.endswith('.')):
        sentences2.pop()

    if(len(sentences1) != len(sentences2)):
        count1 = len(s1.split(' '))
        count2 = len(s2.split(' '))
        if(count1 < count2):
            return {'shorter':s1,'longer':s2}
        else:
            return {'shorter':s2,'longer':s1}
    else:
        long_version = ''
        short_version = ''
        l = len(sentences1)
        for i in range(l):
            count1 = len(sentences1[i].split(' '))
            count2 = len(sentences2[i].split(' '))
            if(count1 < count2):
                short_version += (sentences1[i] + '.')
                long_version += (sentences2[i] + '.')
            else:
                short_version += (sentences2[i] + '.')
                long_version += (sentences1[i] + '.')
    return{'shorter':short_version,'longer':long_version}

            


# In[64]:




# In[ ]:



